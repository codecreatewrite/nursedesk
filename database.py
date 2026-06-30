import sqlite3
from storage import load_patients

def get_connection():
    return sqlite3.connect("nursedesk.db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            ward TEXT,
            diagnosis TEXT,
            medication TEXT,
            is_critical INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_patient(name, age, ward, diagnosis, medication, is_critical):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, ward, diagnosis, medication, is_critical) VALUES (?, ?, ?, ?, ?, ?)",
        (name, age, ward, diagnosis, medication, int(is_critical))
    )
    conn.commit()
    conn.close()

def get_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_critical_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE is_critical = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def seed_if_empty():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]
    conn.close()
    print(count)

    if count == 0:
        print("Database empty. Seeding from JSON...")
        patients = load_patients()
        for p in patients:
            insert_patient(
                p["name"], p["age"], p["ward"],
                p["diagnosis"], p["medication"], p["is_critical"]
            )
        print("Seeding complete.")
    else:
        print(f"Database already has {count} patients. Skipping seed.")

def count_patients_by_status(is_critical):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients WHERE is_critical = ?", (int(is_critical),))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def update_patient_status(is_critical, patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "UPDATE patients SET is_critical = ? WHERE id = ?", (int(is_critical), patient_id)
    )
    conn.commit()
    conn.close()

def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()
