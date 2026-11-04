import os
import sqlite3

try:
    import pymysql
    import pymysql.cursors
except ImportError:
    pymysql = None

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes.db")


def is_mysql():
    return pymysql is not None and bool(os.getenv("DB_HOST", "").strip())


def get_connection(database=None):
    if is_mysql():
        db_name = database if database is not None else os.getenv("DB_NAME", "cloud_notes").strip()
        kwargs = {
            "host": os.getenv("DB_HOST", "localhost").strip(),
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER", "root").strip(),
            "password": os.getenv("DB_PASSWORD", ""),
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": True
        }
        if db_name:
            kwargs["database"] = db_name
        return pymysql.connect(**kwargs)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    if is_mysql():
        db_name = os.getenv("DB_NAME", "cloud_notes").strip()
        admin_conn = get_connection(database="")
        with admin_conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        admin_conn.close()

        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id VARCHAR(64) PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    body TEXT,
                    file_url VARCHAR(500),
                    added_on VARCHAR(50) NOT NULL,
                    updated_on VARCHAR(50)
                )
            """)
            try:
                cur.execute("ALTER TABLE notes ADD COLUMN updated_on VARCHAR(50)")
            except Exception:
                pass
        conn.close()
    else:
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT,
                file_url TEXT,
                added_on TEXT NOT NULL,
                updated_on TEXT
            )
        """)
        try:
            conn.execute("ALTER TABLE notes ADD COLUMN updated_on TEXT")
            conn.commit()
        except sqlite3.OperationalError:
            pass
        conn.close()


def fetch_all_notes():
    conn = get_connection()
    if is_mysql():
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM notes ORDER BY added_on DESC")
            rows = cur.fetchall()
        conn.close()
        return rows

    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY added_on DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


def insert_note(note_id, title, body, file_url, added_on):
    conn = get_connection()
    if is_mysql():
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (id, title, body, file_url, added_on) VALUES (%s, %s, %s, %s, %s)",
                (note_id, title, body, file_url, added_on)
            )
        conn.close()
    else:
        conn.execute(
            "INSERT INTO notes (id, title, body, file_url, added_on) VALUES (?, ?, ?, ?, ?)",
            (note_id, title, body, file_url, added_on)
        )
        conn.commit()
        conn.close()


def update_note(note_id, title, body, file_url=None, updated_on=None):
    conn = get_connection()
    if file_url:
        query = "UPDATE notes SET title = %s, body = %s, file_url = %s, updated_on = %s WHERE id = %s" if is_mysql() \
            else "UPDATE notes SET title = ?, body = ?, file_url = ?, updated_on = ? WHERE id = ?"
        params = (title, body, file_url, updated_on, note_id)
    else:
        query = "UPDATE notes SET title = %s, body = %s, updated_on = %s WHERE id = %s" if is_mysql() \
            else "UPDATE notes SET title = ?, body = ?, updated_on = ? WHERE id = ?"
        params = (title, body, updated_on, note_id)

    if is_mysql():
        with conn.cursor() as cur:
            cur.execute(query, params)
            updated = cur.rowcount > 0
        conn.close()
        return updated

    cur = conn.cursor()
    cur.execute(query, params)
    updated = cur.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def remove_note(note_id):
    conn = get_connection()
    if is_mysql():
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
            deleted = cur.rowcount > 0
        conn.close()
        return deleted

    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
