import sqlite3

conn = sqlite3.connect("health.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()


def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    c.execute(
        "INSERT INTO patients(name,dob,email,glucose,haemoglobin,cholesterol,remarks) VALUES(?,?,?,?,?,?,?)",
        (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
    )
    conn.commit()


def view_patients():
    c.execute("SELECT * FROM patients")
    return c.fetchall()


def delete_patient(patient_id):
    c.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
