import argparse

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="ehr", description="Manages electronic health records")
        parser.add_argument("-t", "--type", type=str, help="Identify user type (patient/doctor)")
        # parser.add_argument("-")
        args = parser.parse_args()
        self.blockchain = None
        self.user_type = args.type.lower()
        self.patient_id = None
        self.patient_name = None
        self.doctor_id = None
        self.doctor_name = None
        self.patient_address = None
        self.patient_phone = None

    def run(self):

        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                if self.user_type == "patient":
                    print("Error: Insufficient permission")
                    continue
                self.create_record()
            elif choice == "2":
                self.view_records()
            elif choice == "3":
                if self.user_type == "patient":
                    print("Error: Insufficient permission")
                    continue
                self.update_record()
            elif choice == "4":
                if self.user_type == "patient":
                    print("Error: Insufficient permission")
                    continue
                self.delete_record()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def fill_details(self):
        if self.user_type == "patient":
            self.patient_id = int(input("Enter id: "))
            self.patient_name = input("Enter name: ")
        else:
            self.doctor_id = int(input("Enter id: "))
            self.doctor_name = input("Enter name: ")
            self.patient_id = int(input("Enter patient id: "))
            self.patient_name = input("Enter patient name: ")
            self.patient_phone = input("Enter patient's phone number: ")
            self.patient_address = input("Enter patient's address: ")

    def display_menu(self):
        print("\n==== Electronic Health Records CLI ====")
        print("1. Create New Record")
        print("2. View My Records")
        print("3. Update Existing Record")
        print("4. Delete Record")
        print("5. Logout")
        print("=======================================")

    def create_record(self):
        print("\n--- Create New Record ---")
        data = input("Enter medical record details: ")
        self.blockchain.add_record(self.user_id, data)
        print("Record successfully added.")

    def view_records(self):
        print("\n--- View My Records ---")
        records = self.blockchain.get_records_by_user(self.user_id)
        if not records:
            print("No records found.")
            return
        for idx, record in enumerate(records, 1):
            print(f"{idx}. {record}")

    def update_record(self):
        print("\n--- Update Record ---")
        records = self.blockchain.get_records_by_user(self.user_id)
        if not records:
            print("No records found.")
            return
        self.view_records()
        record_num = int(input("Enter record number to update: ")) - 1
        if 0 <= record_num < len(records):
            new_data = input("Enter new medical details: ")
            self.blockchain.update_record(self.user_id, record_num, new_data)
            print("Record updated successfully.")
        else:
            print("Invalid record number.")

    def delete_record(self):
        print("\n--- Delete Record ---")
        records = self.blockchain.get_records_by_user(self.user_id)
        if not records:
            print("No records found.")
            return
        self.view_records()
        record_num = int(input("Enter record number to delete: ")) - 1
        if 0 <= record_num < len(records):
            self.blockchain.delete_record(self.user_id, record_num)
            print("Record deleted successfully.")
        else:
            print("Invalid record number.")

cli_obj = CLI()
cli_obj.run()