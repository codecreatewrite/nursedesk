import sqlite3
#import json
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

print("Creating tables...")
create_table()

patients = load_patients("ward_data.json")
#with open("ward_data.json", "r") as file:
#    patients = json.load(file)
print("Data loaded from json sucessfully...")
for patient in patients:
    name = patient["name"]
    age = patient["age"]
    ward = patient["ward"]
    diagnosis = patient["diagnosis"]
    medication = patient["medication"]
    is_critical = patient["is_critical"]

    insert_patient(name, age, ward, diagnosis, medication, is_critical)
print("Added patient records to database.")

print("\n=== ALL PATIENT DATA ===")
rows = get_all_patients()
for row in rows:
    print(row)

print("\n=== CRITICAL PATIENTS ===")
rows = get_critical_patients()
for row in rows:
    print(row)
