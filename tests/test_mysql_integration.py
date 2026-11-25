import unittest
from sqlalchemy import text

from app import create_app
from init_db import init_database
from my_project import db


class MySQLStoredProgramsIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_database()
        cls.app = create_app({"TESTING": True})
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        init_database()

    def test_01_task1_no_physical_fk_and_trigger_integrity(self):
        with self.app.app_context():
            fk_count = db.session.execute(
                text(
                    """
                    SELECT COUNT(*) FROM information_schema.KEY_COLUMN_USAGE
                    WHERE TABLE_SCHEMA = 'fablab_db'
                      AND TABLE_NAME = 'equipment_notes'
                      AND REFERENCED_TABLE_NAME IS NOT NULL
                    """
                )
            ).scalar()
            self.assertEqual(fk_count, 0, "equipment_notes must NOT have a physical FK!")

        res = self.client.post(
            "/api/equipment-notes",
            json={"equipment_id": 9999, "note_text": "Неіснуюче обладнання"},
        )
        self.assertEqual(res.status_code, 422, res.get_data(as_text=True))
        self.assertEqual(res.get_json()["error"]["code"], "TRIGGER_OR_PROCEDURE_ERROR")
        self.assertIn("equipment_id does not exist", res.get_json()["error"]["message"])

        eq_res = self.client.post(
            "/api/equipment",
            json={
                "inventory_number": "INV-8801",
                "name": "Тестовий стенд",
                "status_id": 1,
                "category_id": 1,
                "equipment_info_id": 1,
            },
        )
        self.assertEqual(eq_res.status_code, 201, eq_res.get_data(as_text=True))
        eq_id = eq_res.get_json()["id"]

        note_res = self.client.post(
            "/api/equipment-notes",
            json={"equipment_id": eq_id, "note_text": "Примітка для тесту цілісності"},
        )
        self.assertEqual(note_res.status_code, 201, note_res.get_data(as_text=True))
        note_id = note_res.get_json()["id"]

        upd_bad = self.client.put(f"/api/equipment-notes/{note_id}", json={"equipment_id": 9999})
        self.assertEqual(upd_bad.status_code, 422)

        del_eq_bad = self.client.delete(f"/api/equipment/{eq_id}")
        self.assertEqual(del_eq_bad.status_code, 422)
        self.assertIn("equipment_notes", del_eq_bad.get_json()["error"]["message"])

        self.assertEqual(self.client.delete(f"/api/equipment-notes/{note_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment/{eq_id}").status_code, 204)

    def test_02_task2a_sp_insert_project(self):
        res = self.client.post(
            "/api/procedures/projects",
            json={"title": "Лаб 5 Проєкт", "description": "Вставлено через процедуру"},
        )
        self.assertEqual(res.status_code, 201, res.get_data(as_text=True))
        body = res.get_json()
        self.assertEqual(body["title"], "Лаб 5 Проєкт")
        self.assertIn("id", body)

    def test_03_task2b_sp_add_equipment_to_kit(self):
        res = self.client.post(
            "/api/procedures/kit-items/by-name",
            json={"equipment_name": "Prusa i3 MK3", "kit_name": "Набір для пайки"},
        )
        self.assertEqual(res.status_code, 201, res.get_data(as_text=True))
        body = res.get_json()
        self.assertEqual(body["equipment_name"], "Prusa i3 MK3")
        self.assertEqual(body["kit_name"], "Набір для пайки")

        dup = self.client.post(
            "/api/procedures/kit-items/by-name",
            json={"equipment_name": "Prusa i3 MK3", "kit_name": "Набір для пайки"},
        )
        self.assertEqual(dup.status_code, 422)

        missing = self.client.post(
            "/api/procedures/kit-items/by-name",
            json={"equipment_name": "Неіснуючий прилад", "kit_name": "Набір для пайки"},
        )
        self.assertEqual(missing.status_code, 422)

    def test_04_task2c_sp_insert_10_noname_categories(self):
        res = self.client.post(
            "/api/procedures/categories/noname-batch",
            json={"start_num": 5},
        )
        self.assertEqual(res.status_code, 201, res.get_data(as_text=True))
        body = res.get_json()
        self.assertEqual(body["inserted_count"], 10)
        names = [item["name"] for item in body["items"]]
        self.assertEqual(names, [f"Noname{i}" for i in range(5, 15)])

    def test_05_task2d_function_and_procedure_stats(self):
        res_all = self.client.get("/api/procedures/machine-sessions/stats?operation=ALL")
        self.assertEqual(res_all.status_code, 200, res_all.get_data(as_text=True))
        data = res_all.get_json()
        self.assertEqual(data["min_duration"], 45.0)
        self.assertEqual(data["max_duration"], 300.0)
        self.assertEqual(data["sum_duration"], 1455.0)
        self.assertEqual(data["avg_duration"], 145.5)

        res_avg = self.client.get("/api/procedures/machine-sessions/stats?operation=AVG")
        self.assertEqual(res_avg.status_code, 200)
        self.assertEqual(res_avg.get_json()["value"], 145.5)

    def test_06_task2e_cursor_split_projects_random(self):
        total_projects = len(self.client.get("/api/projects").get_json())

        run1 = self.client.post("/api/procedures/projects/split-random")
        self.assertEqual(run1.status_code, 201, run1.get_data(as_text=True))
        d1 = run1.get_json()
        self.assertEqual(d1["table_1_rows"] + d1["table_2_rows"], total_projects)
        self.assertEqual(len(d1["table_1_data"]), d1["table_1_rows"])
        self.assertEqual(len(d1["table_2_data"]), d1["table_2_rows"])

        run2 = self.client.post("/api/procedures/projects/split-random")
        self.assertEqual(run2.status_code, 201, run2.get_data(as_text=True))
        d2 = run2.get_json()
        self.assertNotEqual(d1["table_1"], d2["table_1"])
        self.assertEqual(d2["table_1_rows"] + d2["table_2_rows"], total_projects)

        with self.app.app_context():
            for tbl in (d1["table_1"], d1["table_2"], d2["table_1"], d2["table_2"]):
                db.session.execute(text(f"DROP TABLE IF EXISTS `{tbl}`"))
            db.session.commit()

    def test_07_task3a_trigger_inventory_not_ending_00(self):
        res = self.client.post(
            "/api/equipment",
            json={
                "inventory_number": "INV-9900",
                "name": "Bad Inventory",
                "status_id": 1,
                "category_id": 1,
            },
        )
        self.assertEqual(res.status_code, 422, res.get_data(as_text=True))
        self.assertIn("two zeros", res.get_json()["error"]["message"])

        upd = self.client.put("/api/equipment/1", json={"inventory_number": "INV-5500"})
        self.assertEqual(upd.status_code, 422)

    def test_08_task3d_trigger_min_cardinality_6(self):
        for status_id in (10, 9, 8, 7):
            r = self.client.delete(f"/api/equipment-statuses/{status_id}")
            self.assertEqual(r.status_code, 204, r.get_data(as_text=True))

        blocked = self.client.delete("/api/equipment-statuses/6")
        self.assertEqual(blocked.status_code, 422, blocked.get_data(as_text=True))
        self.assertIn("minimum cardinality of 6", blocked.get_json()["error"]["message"])

    def test_09_task3f_trigger_rentals_delete_audit_log(self):
        created = self.client.post(
            "/api/rentals",
            json={
                "checkout_time": "2026-11-25T10:00:00",
                "return_time": "2026-11-25T12:00:00",
                "user_id": 1,
                "equipment_id": 1,
                "project_id": 1,
                "lab_id": 1,
            },
        )
        self.assertEqual(created.status_code, 201, created.get_data(as_text=True))
        rental_id = created.get_json()["id"]

        self.assertEqual(self.client.delete(f"/api/rentals/{rental_id}").status_code, 204)

        logs = self.client.get("/api/rentals-delete-log").get_json()
        matching = [row for row in logs if row["rental_id"] == rental_id]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["user_id"], 1)
        self.assertEqual(matching[0]["equipment_id"], 1)
        self.assertIsNotNone(matching[0]["deleted_at"])

    def test_10_custom_sql_errors_in_data_sql(self):
        res_phone = self.client.post(
            "/api/users",
            json={
                "first_name": "Тест",
                "last_name": "Юзер",
                "email": "phone.test@fablab.ua",
                "phone": "not_a_phone!!!",
            },
        )
        self.assertEqual(res_phone.status_code, 422, res_phone.get_data(as_text=True))
        self.assertEqual(res_phone.get_json()["error"]["code"], "SQL_CUSTOM_ERROR_20003")

        res_dur = self.client.post(
            "/api/machine-sessions",
            json={
                "session_start": "2026-11-25T10:00:00",
                "duration_minutes": 2000,
                "equipment_id": 1,
                "user_id": 1,
            },
        )
        self.assertEqual(res_dur.status_code, 422, res_dur.get_data(as_text=True))
        self.assertEqual(res_dur.get_json()["error"]["code"], "SQL_CUSTOM_ERROR_20008")

        res_inv = self.client.post(
            "/api/equipment",
            json={
                "inventory_number": "INV 123!",
                "name": "Bad Chars",
                "status_id": 1,
                "category_id": 1,
            },
        )
        self.assertEqual(res_inv.status_code, 422, res_inv.get_data(as_text=True))
        self.assertEqual(res_inv.get_json()["error"]["code"], "SQL_CUSTOM_ERROR_20010")

        with self.app.app_context():
            for sql, expected_errno in [
                (
                    "INSERT INTO users (first_name, last_name, email) VALUES ('A', 'B', 'bad-email')",
                    20001,
                ),
                (
                    "INSERT INTO rentals (checkout_time, return_time, user_id, equipment_id) VALUES ('2026-11-25 15:00:00', '2026-11-25 10:00:00', 1, 1)",
                    20004,
                ),
                (
                    "INSERT INTO repairs (issue_description, start_date, end_date, equipment_id) VALUES ('Bug', '2026-11-25', '2026-11-20', 1)",
                    20005,
                ),
                (
                    "INSERT INTO projects (title) VALUES ('   ')",
                    20011,
                ),
            ]:
                with self.assertRaises(Exception) as ctx:
                    db.session.execute(text(sql))
                    db.session.commit()
                db.session.rollback()
                self.assertIn(str(expected_errno), str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
