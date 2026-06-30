import json

def load_patients(filename="ward_data.json"):
    try:
        with open(filename, "r") as file:
            patients = json.load(file)
        print("Patient data loaded from file.")
        return patients
    except FileNotFoundError:
        print("No saved data found. Using default patients.")
        return get_default_patients()

def save_patients(patients, filename="ward_data.json"):
    with open(filename, "w") as file:
        json.dump(patients, file)
    print("Ward data saved.")

def get_default_patients():
    return [
        {
            "name": "Amara Osei",
            "age": 34,
            "ward": "Maternity",
            "diagnosis": "Gestational hypertension",
            "medication": "Methyldopa",
            "is_critical": False
        },
        {
            "name": "Kwame Mensah",
            "age": 67,
            "ward": "Cardiology",
            "diagnosis": "Acute myocardial infarction",
            "medication": "Aspirin",
            "is_critical": True
        },
        {
            "name": "Amina Odak",
            "age": 15,
            "ward": "Female Medical",
            "diagnosis": "Peptic Ulcer Disease",
            "medication": "Omeprazole",
            "is_critical": False
        },
        {
            "name": "Obi Chucks",
            "age": 14,
            "ward": "Theatre",
            "diagnosis": "Appendicitis",
            "medication": "Pentazocine",
            "is_critical": True
        },
        {
            "name": "Amara Fatima",
            "age": 74,
            "ward": "Female Surgical",
            "diagnosis": "Fibroids",
            "medication": "Anesthetics",
            "is_critical": False
        }
    ]
