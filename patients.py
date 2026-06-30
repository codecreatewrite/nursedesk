def get_status(is_critical):
    if is_critical:
        return "Critical"
    else:
        return "Stable"

def get_age_group(age):
    if age < 18:
        return "Pediatric"
    elif 18 <= age <= 59:
        return "Adult"
    else:
        return "Elderly — fall risk note"

def count_critical(patients):
    count = 0
    for patient in patients:
        if patient["is_critical"]:
            count += 1
    return count

def count_stable(patients):
    count = 0
    for patient in patients:
        if not patient["is_critical"]:
            count += 1
    return count

def print_patient_card(patient_data):
    print("=== PATIENT CARD ===")
    print("Name:", patient_data["name"])
    print("Age:", patient_data["age"])
    print("Ward:", patient_data["ward"])
    print("Diagnosis:", patient_data["diagnosis"])
    print("Medication:", patient_data["medication"])
    print("Status:", get_status(patient_data["is_critical"]))
    print("Age Group:", get_age_group(patient_data["age"]))
    print("")

def add_patient(patients):
    print("=== ADD NEW PATIENT ===")
    name = input("Name: ")
    age = int(input("Age: "))
    ward = input("Ward: ")
    diagnosis = input("Diagnosis: ")
    medication = input("Medication: ")
    critical_input = input("Critical? (yes/no): ")
    is_critical = critical_input.lower() == "yes"

    new_patient = {
        "name": name,
        "age": age,
        "ward": ward,
        "diagnosis": diagnosis,
        "medication": medication,
        "is_critical": is_critical
    }

    patients.append(new_patient)
    print("Patient added successfully.")

def print_critical_summary(patients):
    print("=== CRITICAL ALERTS ===")
    for patient in patients:
        if patient['is_critical']:
            print(patient["name"], "— Immediate attention required.")
    if not count_critical(patients):
        print("No critical patients on ward.")

