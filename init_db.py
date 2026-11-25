from pathlib import Path
import pymysql
import yaml


def parse_sql_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    delimiter = ";"
    buffer: list[str] = []

    for raw_line in sql_text.splitlines():
        stripped = raw_line.strip()

        if stripped.upper().startswith("DELIMITER "):
            delimiter = stripped.split(None, 1)[1].strip()
            continue

        if not buffer and (not stripped or stripped.startswith("--")):
            continue

        buffer.append(raw_line)
        joined = "\n".join(buffer).rstrip()
        if joined.endswith(delimiter):
            stmt = joined[: -len(delimiter)].strip()
            if stmt:
                statements.append(stmt)
            buffer = []

    leftover = "\n".join(buffer).strip()
    if leftover:
        statements.append(leftover)

    return statements


def execute_sql_file(cursor, path: Path) -> int:
    sql_text = path.read_text(encoding="utf-8")
    statements = parse_sql_statements(sql_text)
    for stmt in statements:
        cursor.execute(stmt)
    return len(statements)


def init_database(config_path: str = "config/app.yml") -> None:
    root = Path(__file__).resolve().parent
    with open(root / config_path, "r", encoding="utf-8") as f:
        db_cfg = yaml.safe_load(f)["db"]

    conn = pymysql.connect(
        host=db_cfg["host"],
        user=db_cfg["user"],
        password=db_cfg["password"],
        charset="utf8mb4",
        autocommit=True,
        connect_timeout=5,
    )
    try:
        with conn.cursor() as cursor:
            n_data = execute_sql_file(cursor, root / "data.sql")
            print(f"[OK] Executed data.sql ({n_data} statements)")
            n_sp = execute_sql_file(cursor, root / "stored_programs.sql")
            print(f"[OK] Executed stored_programs.sql ({n_sp} statements)")
    finally:
        conn.close()


if __name__ == "__main__":
    init_database()
