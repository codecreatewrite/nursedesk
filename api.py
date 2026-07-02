from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException, Depends
import database
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NURSEDESK_API_KEY")

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

def verify_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/")
def home():
    return {"message": "NurseDesk API is running"}

@app.get("/patients")
def view_patients(auth=Depends(verify_key)):
    rows = database.get_all_patients()
    patients = []
    for row in rows:
        id, name, age, ward, diagnosis, medication, is_critical, status = row
        patients.append({
            "id": id,
            "name": name,
            "age": age,
            "ward": ward,
            "diagnosis": diagnosis,
            "medication": medication,
            "is_critical": bool(is_critical),
            "status": status
        })
    return patients

@app.get("/patients/critical")
def view_critical_patients(auth=Depends(verify_key)):
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

@app.get("/patients/discharged")
def view_discharged_patients(auth=Depends(verify_key)):
    rows = database.get_discharged_patients()
    patients = []
    for row in rows:
        id, name, age, ward, diagnosis, medication, is_critical, status = row
        patients.append({
            "id": id,
            "name": name,
            "age": age,
            "ward": ward,
            "diagnosis": diagnosis,
            "medication": medication,
            "is_critical": bool(is_critical),
            "status": status
        })
    return patients

@app.post("/patients")
def add_patient(patient: PatientInput, auth=Depends(verify_key)):
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
def update_patient(patient_id: int, status: StatusUpdate, auth=Depends(verify_key)):
    database.update_patient_status(patient_id, status.is_critical)
    return {"message": f"Patient {patient_id} status updated"}

@app.delete("/patients/{patient_id}")
def discharge_patient(patient_id: int, auth=Depends(verify_key)):
    database.discharge_patient(patient_id)
    return {"message": f"Patient {patient_id} discharged"}
