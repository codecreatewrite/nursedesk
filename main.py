from pydantic import BaseModel
from fastapi import FastAPI
import database

app = FastAPI()

database.create_table()
database.seed_if_empty()

class PatientInput(BaseModel):
    name: str
    age: int
    ward: str
    diagnosis: str
    medication: str
    is_critical: bool

class StatusUpdate(BaseModel):
    is_critical: bool

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

@app.post("/patients")
def add_patient(patient: PatientInput):
    database.insert_patient(
        patient.name,
        patient.age,
        patient.ward,
        patient.diagnosis,
        patient.medication,
        patient.is_critical
    )
    return {"message": "Patient added successfully"}

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, status: StatusUpdate):
    database.update_patient_status(patient_id, status.is_critical)
    return {"message": f"Patient {patient_id} status updated"}

@app.delete("/patients/{patient_id}")
def discharge_patient(patient_id: int):
    database.delete_patient(patient_id)
    return {"message": f"Patient {patient_id} discharged"}
