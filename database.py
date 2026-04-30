import sqlite3

def create_database():
    conn = sqlite3.connect("data_v4.db")
    c = conn.cursor()

    c.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enumerator_name TEXT,
    enumerator_phone TEXT,
    district TEXT,
    block TEXT,
    clf_name TEXT,
    survey_date TEXT,
    pre_support_business TEXT,
    pre_revenue REAL,
    reap_support TEXT,
    govt_support TEXT,
    revenue_table TEXT,
    cost_table TEXT,
    staff_salary REAL,
    latest_revenue REAL,
    section_j TEXT,
    section_k TEXT,
    total_revenue REAL,
    total_cost REAL,
    sustainability TEXT
)
""")

    conn.commit()
    conn.close()

create_database()
