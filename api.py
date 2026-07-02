from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException, Depends
import database
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth

load_dotenv()

API_KEY = os.getenv("NURSEDESK_API_KEY")

app = FastAPI()

database.create_table()
database.seed_if_empty()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = auth.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

def require_admin(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = database.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    id, username, hashed_password, role = user
    if not auth.verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_token({"sub": username, "role": role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def home():
    return {"message": "NurseDesk API is running"}

@app.get("/patients")
def view_patients(current_user=Depends(get_current_user)):
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
def view_critical_patients(current_user=Depends(get_current_user)):
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
def view_discharged_patients(current_user=Depends(get_current_user)):
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
def add_patient(patient: PatientInput, current_user=Depends(require_admin)):
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
def update_patient(patient_id: int, status: StatusUpdate, current_user=Depends(get_current_user)):
    database.update_patient_status(patient_id, status.is_critical)
    return {"message": f"Patient {patient_id} status updated"}

@app.delete("/patients/{patient_id}")
def discharge_patient(patient_id: int, current_user=Depends(require_admin)):
    database.discharge_patient(patient_id)
    return {"message": f"Patient {patient_id} discharged"}
