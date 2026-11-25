import unittest
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app import create_app
from my_project import db
from init_db import parse_sql_statements
from pathlib import Path


@event.listens_for(Engine, "connect")
def _enable_sqlite_fks(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class FabLabCrudAndErrorsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_api_index(self):
        res = self.client.get("/api")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data["crud_resources"]), 14)
        self.assertEqual(len(data["stored_procedures"]), 5)

    def test_full_crud_all_14_tables(self):
        r = self.client.post(
            "/api/users",
            json={
                "first_name": "Олександр",
                "last_name": "Іванов",
                "email": "alex@fablab.ua",
                "phone": "+380501112233",
            },
        )
        self.assertEqual(r.status_code, 201, r.get_data(as_text=True))
        user_id = r.get_json()["id"]
        self.assertEqual(self.client.get(f"/api/users/{user_id}").status_code, 200)
        r = self.client.put(f"/api/users/{user_id}", json={"phone": "+380991112233"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["phone"], "+380991112233")

        r = self.client.post(
            "/api/projects",
            json={"title": "Робот", "description": "Опис проєкту"},
        )
        self.assertEqual(r.status_code, 201)
        project_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/projects/{project_id}", json={"title": "Робот v2"}).status_code,
            200,
        )

        r = self.client.post(
            "/api/labs",
            json={"lab_name": "Електроніка", "course_name": "IoT"},
        )
        self.assertEqual(r.status_code, 201)
        lab_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/labs/{lab_id}", json={"course_name": "IoT 2.0"}).status_code,
            200,
        )

        r = self.client.post("/api/equipment-categories", json={"name": "3D Принтери"})
        self.assertEqual(r.status_code, 201)
        cat_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/equipment-categories/{cat_id}", json={"name": "3D Друк"}).status_code,
            200,
        )

        r = self.client.post("/api/equipment-statuses", json={"status_name": "Доступно"})
        self.assertEqual(r.status_code, 201)
        status_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/equipment-statuses/{status_id}", json={"status_name": "Вільне"}).status_code,
            200,
        )

        r = self.client.post("/api/equipment-info", json={"instruction": "Прогріти до 200C"})
        self.assertEqual(r.status_code, 201)
        info_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/equipment-info/{info_id}", json={"instruction": "Прогріти до 210C"}).status_code,
            200,
        )

        r = self.client.post(
            "/api/equipment-kits",
            json={"kit_name": "Набір 3D", "description": "Шпатель і клей"},
        )
        self.assertEqual(r.status_code, 201)
        kit_id = r.get_json()["id"]
        r2 = self.client.post(
            "/api/equipment-kits",
            json={"kit_name": "Набір IoT", "description": "Датчики"},
        )
        kit2_id = r2.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/equipment-kits/{kit_id}", json={"kit_name": "Набір 3D Pro"}).status_code,
            200,
        )

        r = self.client.post(
            "/api/equipment",
            json={
                "inventory_number": "INV-2001",
                "name": "Prusa MK4",
                "status_id": status_id,
                "category_id": cat_id,
                "equipment_info_id": info_id,
            },
        )
        self.assertEqual(r.status_code, 201)
        eq_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/equipment/{eq_id}", json={"name": "Prusa MK4S"}).status_code,
            200,
        )

        r = self.client.post("/api/kit-items", json={"equipment_id": eq_id, "kit_id": kit_id})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.client.get(f"/api/kit-items/{eq_id}/{kit_id}").status_code, 200)
        r = self.client.put(f"/api/kit-items/{eq_id}/{kit_id}", json={"kit_id": kit2_id})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["kit_id"], kit2_id)
        self.assertEqual(len(self.client.get(f"/api/equipment-kits/{kit2_id}/equipment").get_json()), 1)
        self.assertEqual(len(self.client.get(f"/api/equipment/{eq_id}/kits").get_json()), 1)

        r = self.client.post(
            "/api/rentals",
            json={
                "checkout_time": "2026-11-20T10:00:00",
                "return_time": "2026-11-20T14:00:00",
                "user_id": user_id,
                "equipment_id": eq_id,
                "project_id": project_id,
                "lab_id": lab_id,
            },
        )
        self.assertEqual(r.status_code, 201)
        rental_id = r.get_json()["id"]
        self.assertEqual(self.client.get(f"/api/rentals/{rental_id}/equipment").get_json()["id"], eq_id)
        self.assertEqual(len(self.client.get(f"/api/users/{user_id}/rentals").get_json()), 1)
        self.assertEqual(
            self.client.put(f"/api/rentals/{rental_id}", json={"return_time": "2026-11-20T16:00:00"}).status_code,
            200,
        )

        r = self.client.post(
            "/api/repairs",
            json={
                "issue_description": "Заміна сопла",
                "start_date": "2026-11-21",
                "end_date": "2026-11-22",
                "equipment_id": eq_id,
            },
        )
        self.assertEqual(r.status_code, 201)
        repair_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/repairs/{repair_id}", json={"issue_description": "Заміна екструдера"}).status_code,
            200,
        )

        r = self.client.post(
            "/api/machine-sessions",
            json={
                "session_start": "2026-11-21T09:00:00",
                "duration_minutes": 120,
                "equipment_id": eq_id,
                "user_id": user_id,
            },
        )
        self.assertEqual(r.status_code, 201)
        session_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/machine-sessions/{session_id}", json={"duration_minutes": 150}).status_code,
            200,
        )

        r = self.client.post(
            "/api/equipment-notes",
            json={"equipment_id": eq_id, "note_text": "Перевірено калібрування"},
        )
        self.assertEqual(r.status_code, 201)
        note_id = r.get_json()["id"]
        self.assertEqual(len(self.client.get(f"/api/equipment/{eq_id}/notes").get_json()), 1)
        self.assertEqual(
            self.client.put(f"/api/equipment-notes/{note_id}", json={"note_text": "Оновлена нотатка"}).status_code,
            200,
        )

        r = self.client.post(
            "/api/rentals-delete-log",
            json={
                "rental_id": rental_id,
                "user_id": user_id,
                "equipment_id": eq_id,
                "checkout_time": "2026-11-20T10:00:00",
                "return_time": "2026-11-20T16:00:00",
            },
        )
        self.assertEqual(r.status_code, 201)
        log_id = r.get_json()["id"]
        self.assertEqual(
            self.client.put(f"/api/rentals-delete-log/{log_id}", json={"return_time": None}).status_code,
            200,
        )

        self.assertEqual(self.client.delete(f"/api/rentals-delete-log/{log_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment-notes/{note_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/machine-sessions/{session_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/repairs/{repair_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/rentals/{rental_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/kit-items/{eq_id}/{kit2_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment/{eq_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment-kits/{kit_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment-kits/{kit2_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment-info/{info_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment-statuses/{status_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/equipment-categories/{cat_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/labs/{lab_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/projects/{project_id}").status_code, 204)
        self.assertEqual(self.client.delete(f"/api/users/{user_id}").status_code, 204)

    def test_custom_errors(self):
        res = self.client.get("/api/users/99999")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()["error"]["code"], "NOT_FOUND")

        res = self.client.post("/api/users", data="{bad json", content_type="application/json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error"]["code"], "BAD_REQUEST")

        res = self.client.post("/api/users", json={"first_name": "Іван", "email": "not-an-email"})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error"]["code"], "VALIDATION_ERROR")
        self.assertIn("last_name", res.get_json()["error"]["details"])
        self.assertIn("email", res.get_json()["error"]["details"])

        res = self.client.post(
            "/api/projects",
            json={"title": "Test", "unknown_col": 123},
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error"]["code"], "VALIDATION_ERROR")

        user_payload = {
            "first_name": "А",
            "last_name": "Б",
            "email": "dup@fablab.ua",
        }
        self.assertEqual(self.client.post("/api/users", json=user_payload).status_code, 201)
        res = self.client.post("/api/users", json=user_payload)
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.get_json()["error"]["code"], "DUPLICATE_ENTRY")

        res = self.client.post(
            "/api/rentals",
            json={
                "checkout_time": "2026-11-20T15:00:00",
                "return_time": "2026-11-20T10:00:00",
                "user_id": 1,
                "equipment_id": 1,
            },
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("return_time", res.get_json()["error"]["message"])

        res = self.client.get("/api/procedures/machine-sessions/stats?operation=MEDIAN")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["error"]["code"], "VALIDATION_ERROR")

        res = self.client.get("/api/nonexistent-endpoint")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json()["error"]["code"], "NOT_FOUND")

        res = self.client.patch("/api/users")
        self.assertEqual(res.status_code, 405)
        self.assertEqual(res.get_json()["error"]["code"], "METHOD_NOT_ALLOWED")

    def test_sql_scripts_parse_cleanly(self):
        root = Path(__file__).resolve().parent.parent
        data_stmts = parse_sql_statements((root / "data.sql").read_text(encoding="utf-8"))
        sp_stmts = parse_sql_statements((root / "stored_programs.sql").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data_stmts), 40)
        joined_sp = "\n".join(sp_stmts)
        for name in [
            "trg_equipment_notes_before_insert",
            "trg_equipment_notes_before_update",
            "trg_equipment_before_delete_notes_integrity",
            "trg_equipment_before_update_notes_integrity",
            "sp_insert_project",
            "sp_add_equipment_to_kit",
            "sp_insert_10_noname_categories",
            "fn_session_duration_stat",
            "sp_get_session_duration_stats",
            "sp_split_projects_random",
            "trg_equipment_no_double_zero_insert",
            "trg_equipment_no_double_zero_update",
            "trg_equipment_statuses_min_cardinality",
            "trg_rentals_after_delete_log",
        ]:
            self.assertIn(name, joined_sp, f"Missing stored program: {name}")


if __name__ == "__main__":
    unittest.main()
