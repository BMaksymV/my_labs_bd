from datetime import date, datetime
from decimal import Decimal
import re
from typing import Any
import pymysql.cursors
from my_project import db

_SPLIT_TABLE_RE = re.compile(r"^projects_split_[12]_\d{8}_\d{6}_\d{6}$")


def _serialize_value(val: Any) -> Any:
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    return val


def _serialize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{k: _serialize_value(v) for k, v in row.items()} for row in rows]


class StoredProceduresDAO:
    def _call_proc(self, proc_name: str, args: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        raw_conn = db.engine.raw_connection()
        cursor = None
        try:
            cursor = raw_conn.cursor(pymysql.cursors.DictCursor)
            cursor.callproc(proc_name, args)
            rows = list(cursor.fetchall() or [])
            while cursor.nextset():
                pass
            raw_conn.commit()
            return _serialize_rows(rows)
        except Exception:
            raw_conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()
            raw_conn.close()

    def insert_project(self, title: str, description: str | None) -> dict[str, Any]:
        rows = self._call_proc("sp_insert_project", (title, description))
        return rows[0] if rows else {}

    def add_equipment_to_kit(self, equipment_name: str, kit_name: str) -> dict[str, Any]:
        rows = self._call_proc("sp_add_equipment_to_kit", (equipment_name, kit_name))
        return rows[0] if rows else {}

    def insert_10_noname_categories(self, start_num: int) -> list[dict[str, Any]]:
        return self._call_proc("sp_insert_10_noname_categories", (start_num,))

    def get_session_duration_stats(self, operation: str) -> dict[str, Any]:
        rows = self._call_proc("sp_get_session_duration_stats", (operation,))
        return rows[0] if rows else {}

    def split_projects_random(self) -> dict[str, Any]:
        rows = self._call_proc("sp_split_projects_random", ())
        meta = rows[0] if rows else {}
        table_1 = meta.get("table_1", "")
        table_2 = meta.get("table_2", "")

        raw_conn = db.engine.raw_connection()
        cursor = None
        try:
            cursor = raw_conn.cursor(pymysql.cursors.DictCursor)
            table_1_data: list[dict[str, Any]] = []
            table_2_data: list[dict[str, Any]] = []
            if _SPLIT_TABLE_RE.match(table_1):
                cursor.execute(f"SELECT id, title, description FROM `{table_1}` ORDER BY id")
                table_1_data = _serialize_rows(list(cursor.fetchall() or []))
            if _SPLIT_TABLE_RE.match(table_2):
                cursor.execute(f"SELECT id, title, description FROM `{table_2}` ORDER BY id")
                table_2_data = _serialize_rows(list(cursor.fetchall() or []))
            meta["table_1_data"] = table_1_data
            meta["table_2_data"] = table_2_data
            return meta
        finally:
            if cursor is not None:
                cursor.close()
            raw_conn.close()
