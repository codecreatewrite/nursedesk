from fastapi import FastAPI
import database

app = FastAPI()

database.create_table()
database.seed_if_empty()

@app.get("/")
def home():
    return {"message": "NurseDesk API is running"}

@app.get("/patients")
def view_patients():
    rows = database.get_all_patients()
    patients = []
    for row in rows:
        id, name, age, ward, diagnosis, medication, is_critical = row
        patients.append({
            "id": id,
            "name": name,
            "age": age,
            "ward": ward,
            "diagnosis": diagnosis,
            "medication": medication,
            "is_critical": bool(is_critical)
        })
    return patients

@app.get("/patients/critical")
def view_critical_patients():
    rows = database.get_critical_patients()
    patients = []
    for row in rows:
        id, name, age, ward, diagnosis, medication, is_critical = row
        patients.append({
            "id": id,
            "name": name,
            "ward": ward,
            "diagnosis": diagnosis
        })
    return patients
