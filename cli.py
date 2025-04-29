import argparse
import sys
from datetime import datetime
from blockChain import Blockchain
from auth import authenticate_user, register_user

class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="ehr", description="Manages electronic health records")
        parser.add_argument("-t", "--type", type=str, required=False,
                            help="Identify user type (patient/doctor)")
        args = parser.parse_args()
        if args.type:
            self.user_type = args.type.lower()
        else:
            self.user_type = input("Please enter your user type (patient/doctor): ").strip().lower()
        self.blockchain = Blockchain()
        # Common user details
        self.patient_id = None
        self.patient_name = None
        self.patient_address = None
        self.patient_phone = None
        # Doctor details
        self.doctor_id = None
        self.doctor_name = None

    def run(self):
        print("1- Register\n2- Login\n")
        choice = int(input("Enter choice: ").strip())
        if choice == 1:
            if not self.register():
                sys.exit("User could not be registered. Exiting program...")
        else:
            if not self.authenticate():
                print("Authentication failed. Exiting.")
                return

        self.fill_details()

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

    def register(self):
        username = input("Enter username: ").strip()
        while True:
            password = input("Enter password: ").strip()
            try:
                if not register_user(username, password, role=self.user_type):
                    sys.exit("User could not be registered. Exiting program...")

                # Fill name of current user before running fill_details function
                if self.user_type == "patient":
                    self.patient_name = username
                else:
                    self.doctor_name = username

                print("User registered successfully.")
                return True
            except ValueError as ve:
                print(ve.args)
                continue
        return False

    def authenticate(self):
        # Prompt for username/password and authenticate
        username = input("Username: ")
        pwd = input("Password: ")
        if authenticate_user(username, pwd, self.user_type):
            if self.user_type == "patient":
                self.patient_name = username
            else:
                self.doctor_name = username
            print(f"Welcome, {username}!")
            return True
        return False

    def fill_details(self):
        if self.user_type == "patient":
            self.patient_id = input("Enter your patient ID: ")
            # self.patient_name = input("Enter your name: ")
        else:
            self.doctor_id = input("Enter your doctor ID: ")
            # self.doctor_name = input("Enter your name: ")
            self.patient_id = input("Enter patient ID to manage: ")
            self.patient_name = input("Enter patient name: ")
            self.patient_phone = input("Enter patient's phone number: ")
            self.patient_address = input("Enter patient's address: ")

    def display_menu(self):
        print("\n==== Electronic Health Records CLI ====\n"
              "1. Create New Record\n"
              "2. View My Records\n"
              "3. Update Existing Record\n"
              "4. Delete Record\n"
              "5. Logout\n"
              "=======================================")

    def create_record(self):
        print("\n--- Create New Record ---")
        record_id = input("Enter record ID: ")
        details = input("Enter medical record details: ")
        # Build record payload
        record = {
            "record_id": record_id,
            "patient_id": self.patient_id,
            "pname": self.patient_name,
            "address": self.patient_address,
            "phone": self.patient_phone,
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "data": details
        }
        self.blockchain.add_block(record)
        print("Record successfully added to blockchain.")

    def view_records(self):
        print("\n--- View Records ---")
        records = self.blockchain.list_blocks()

        # Ignore genesis block
        records = [b for b in records if b['index'] != 0]

        # Filter records based on user type
        if self.user_type == 'patient':
            records = [b for b in records if b['data'].get('patient_id') == self.patient_id]
        elif self.user_type == 'doctor':
            records = [b for b in records if b['data'].get('doctor_id') == self.doctor_id]

        if not records:
            print("No records found.")
            return

        for idx, blk in enumerate(records, 1):
            data = blk['data']
            print(f"\n--- Record {idx} ---")
            print(f"Record ID: {data.get('record_id', 'N/A')}")
            print(f"Date: {data.get('date', 'N/A')}")
            print(f"Patient Name: {data.get('pname', 'N/A')}")
            print(f"Patient Address: {data.get('address', 'N/A')}")
            print(f"Patient Phone: {data.get('phone', 'N/A')}")
            print(f"Doctor Name: {data.get('doctor_name', 'N/A')}")
            print(f"Medical Details: {data.get('data', 'N/A')}")

    def update_record(self):
        print("\n--- Update Record ---")
        records = self.blockchain.list_blocks()
        records = [b for b in records if b['data']['patient_id'] == self.patient_id]
        if not records:
            print("No records found.")
            return
        for idx, blk in enumerate(records, 1):
            print(f"{idx}. ID={blk['data']['record_id']} Date={blk['data']['date']}")
        choice = int(input("Select record number to update: ")) - 1
        if not (0 <= choice < len(records)):
            print("Invalid record number.")
            return
        record = records[choice]['data']
        new_details = input("Enter new medical details: ")
        record['data'] = encrypt_data(new_details).decode()
        record['date'] = datetime.now().strftime("%Y-%m-%d")
        record['status'] = 'updated'
        self.blockchain.add_block(record)
        print("Record updated successfully.")

    def delete_record(self):
        print("\n--- Delete Record ---")
        records = self.blockchain.list_blocks()
        records = [b for b in records if b['data']['patient_id'] == self.patient_id]
        if not records:
            print("No records found.")
            return
        for idx, blk in enumerate(records, 1):
            print(f"{idx}. ID={blk['data']['record_id']} Date={blk['data']['date']}")
        choice = int(input("Select record number to delete: ")) - 1
        if not (0 <= choice < len(records)):
            print("Invalid record number.")
            return
        record = records[choice]['data']
        record['status'] = 'deleted'
        self.blockchain.add_block(record)
        print("Record deleted successfully.")

if __name__ == '__main__':
    CLI().run()
