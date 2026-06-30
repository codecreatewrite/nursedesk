import database

database.create_table()
database.seed_if_empty()

while True:
    print("\n=== NURSEDESK MENU ===")
    print("1. View all patients")
    print("2. Add patient")
    print("3. View critical alerts")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        rows = database.get_all_patients()
        for row in rows:
            id, name, age, ward, diagnosis, medication, is_critical = row
            print("=== PATIENT CARD ===")
            print("Name:", name)
            print("Age:", age)
            print("Ward:", ward)
            print("Diagnosis:", diagnosis)
            print("Medication:", medication)
            print("Status:", "Critical" if is_critical else "Stable")
            print("")
        print("=== SUMMARY ===")
        print("Total Patients:", len(rows))
        print("Critical:", database.count_patients_by_status(True))
        print("Stable:", database.count_patients_by_status(False))

    elif choice == "2":
        name = input("Name: ")
        age = int(input("Age: "))
        ward = input("Ward: ")
        diagnosis = input("Diagnosis: ")
        medication = input("Medication: ")
        critical_input = input("Critical? (yes/no): ")
        is_critical = critical_input.lower() == "yes"
        database.insert_patient(name, age, ward, diagnosis, medication, is_critical)
        print("Patient added successfully.")

    elif choice == "3":
        rows = database.get_critical_patients()
        print("=== CRITICAL ALERTS ===")
        if not rows:
            print("No critical patients on ward.")
        for row in rows:
            print(row[1], "— Immediate attention required.")

    elif choice == "4":
        print("Goodbye.")
        break

    else:
        print("Invalid choice. Try again.")
