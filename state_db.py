import sqlite3

DB = "state.db"

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS outreach (
                row_number          TEXT PRIMARY KEY,
                notion_page_id      TEXT,
                company_name        TEXT,
                website             TEXT,
                brief_description   TEXT,
                career_page_link    TEXT,
                sector              TEXT,
                ind_a_name          TEXT,
                ind_a_role          TEXT,
                ind_a_email         TEXT,
                ind_a_linkedin      TEXT,
                ind_b_name          TEXT,
                ind_b_role          TEXT,
                ind_b_email         TEXT,
                ind_b_linkedin      TEXT,
                cover_letter        TEXT,
                email_subject       TEXT,
                email_body          TEXT,
                email_sent_date     TEXT,
                state               TEXT DEFAULT 'NEW'
            )
        """)

def upsert(row_number, **kwargs):
    fields = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [row_number]
    with sqlite3.connect(DB) as con:
        con.execute(f"UPDATE outreach SET {fields} WHERE row_number = ?", values)
        if con.execute("SELECT changes()").fetchone()[0] == 0:
            cols = "row_number, " + ", ".join(kwargs.keys())
            placeholders = ", ".join(["?"] * (len(kwargs) + 1))
            con.execute(f"INSERT INTO outreach ({cols}) VALUES ({placeholders})",
                        [row_number] + list(kwargs.values()))

def get_active():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        return con.execute(
            "SELECT * FROM outreach WHERE state != 'SENT' ORDER BY row_number LIMIT 1"
        ).fetchone()

def get_by_email(email):
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        return con.execute(
            "SELECT * FROM outreach WHERE ind_a_email = ? OR ind_b_email = ?",
            (email, email)
        ).fetchone()