import csv
from connect import connect, create_table


def insert_from_csv():
    filename = "contacts.csv"

    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cur.execute("""
                    INSERT INTO contacts (first_name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING;
                """, (row["first_name"], row["phone"]))

        conn.commit()
        print("Contacts imported successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

def insert_contact():
    name = input("Enter first name: ")
    phone = input("Enter phone number: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO contacts (first_name, phone)
            VALUES (%s, %s);
        """, (name, phone))

        conn.commit()
        print("Contact added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

def update_contact():
    old_phone = input("Enter current phone number: ")

    print("1. Update first name")
    print("2. Update phone number")

    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_name = input("Enter new first name: ")

            cur.execute("""
                UPDATE contacts
                SET first_name = %s
                WHERE phone = %s;
            """, (new_name, old_phone))

        elif choice == "2":
            new_phone = input("Enter new phone number: ")

            cur.execute("""
                UPDATE contacts
                SET phone = %s
                WHERE phone = %s;
            """, (new_phone, old_phone))

        else:
            print("Invalid choice!")
            return

        if cur.rowcount > 0:
            print("Contact updated successfully!")
        else:
            print("Contact not found!")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

def search_contacts():
    print("1. Search by name")
    print("2. Search by phone prefix")

    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("Enter name: ")

            cur.execute("""
                SELECT * FROM contacts
                WHERE first_name ILIKE %s;
            """, ("%" + name + "%",))

        elif choice == "2":
            prefix = input("Enter phone prefix: ")

            cur.execute("""
                SELECT * FROM contacts
                WHERE phone LIKE %s;
            """, (prefix + "%",))

        else:
            print("Invalid choice!")
            return

        results = cur.fetchall()

        if results:
            for contact in results:
                print(contact)
        else:
            print("No contacts found!")

    finally:
        cur.close()
        conn.close()
if __name__ == "__main__":
    create_table()
    search_contacts()
def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone number")

    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            name = input("Enter first name: ")

            cur.execute("""
                DELETE FROM contacts
                WHERE first_name ILIKE %s;
            """, (name,))

        elif choice == "2":
            phone = input("Enter phone number: ")

            cur.execute("""
                DELETE FROM contacts
                WHERE phone = %s;
            """, (phone,))

        else:
            print("Invalid choice!")
            return

        deleted = cur.rowcount
        conn.commit()

        print(deleted, "contact(s) deleted!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()
def main():
    create_table()

    while True:
        print("\n===== PHONE BOOK =====")
        print("1. Import contacts from CSV")
        print("2. Add contact")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            insert_from_csv()

        elif choice == "2":
            insert_contact()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            search_contacts()

        elif choice == "5":
            delete_contact()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()