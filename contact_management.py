import json
import os
import csv
from datetime import datetime

def load_from_file(filename="contacts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}

def save_to_file(contacts, filename="contacts.json"):
    with open(filename, "w") as file:
        json.dump(contacts, file, indent=4)
    print("Contacts saved successfully")

def backup_contacts(contacts, backup_dir="backups"):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/contacts_backup_{timestamp}.json"

    with open(backup_file, "w") as file:
        json.dump(contacts, file, indent=4)

    print("Backup created successfully")

def add_contact(contacts):
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    address = input("Enter address: ").strip()

    if not phone.isdigit():
        print("Invalid phone number")
        return

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address
    }
    print("Contact added successfully")

def search_contact_by_name(contacts):
    name = input("Enter name to search: ").strip()
    if name in contacts:
        display_single_contact(name, contacts[name])
    else:
        print("Contact not found")

def search_contact_by_mobile(contacts):
    phone = input("Enter phone number to search: ").strip()
    for name, info in contacts.items():
        if info["phone"] == phone:
            display_single_contact(name, info)
            return
    print("Contact not found")

def update_contact(contacts):
    name = input("Enter name to update: ").strip()
    if name not in contacts:
        print("Contact not found")
        return

    contacts[name]["phone"] = input("New phone: ").strip()
    contacts[name]["email"] = input("New email: ").strip()
    contacts[name]["address"] = input("New address: ").strip()

    print("Contact updated successfully")

def delete_contact(contacts):
    name = input("Enter name to delete: ").strip()
    if name in contacts:
        del contacts[name]
        print("Contact deleted successfully")
    else:
        print("Contact not found")



def display_single_contact(name, info):
    print("\n----------------------------")
    print("Name    :", name)
    print("Phone   :", info["phone"])
    print("Email   :", info["email"])
    print("Address :", info["address"])
    print("----------------------------")

def display_all_contacts(contacts):
    if not contacts:
        print("No contacts available")
        return

    print("\n{:<15} {:<15} {:<25}".format("Name", "Phone", "Email"))
    print("-" * 55)

    for name, info in contacts.items():
        print("{:<15} {:<15} {:<25}".format(
            name, info["phone"], info["email"]
        ))


def export_to_csv(contacts, filename="contacts.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address"])

        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["address"]])

    print("Contacts exported to CSV")


def main_menu():
    contacts = load_from_file()

    while True:
        print("""
------ CONTACT MANAGEMENT SYSTEM ------
1. Add Contact
2. Search Contact by Name
3. Search Contact by Phone
4. Update Contact
5. Delete Contact
6. Display All Contacts
7. Export to CSV
8. Save & Backup
9. Exit
""")

        choice = input("Enter your choice (1-9): ").strip()

        if not choice.isdigit():
            print("Invalid input")
            continue

        choice = int(choice)

        if choice == 1:
            add_contact(contacts)
        elif choice == 2:
            search_contact_by_name(contacts)
        elif choice == 3:
            search_contact_by_mobile(contacts)
        elif choice == 4:
            update_contact(contacts)
        elif choice == 5:
            delete_contact(contacts)
        elif choice == 6:
            display_all_contacts(contacts)
        elif choice == 7:
            export_to_csv(contacts)
        elif choice == 8:
            save_to_file(contacts)
            backup_contacts(contacts)
        elif choice == 9:
            save_to_file(contacts)
            print("Program exited successfully")
            break
        else:
            print("Invalid choice")


main_menu()
