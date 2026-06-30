from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NurseDesk API is running"}
