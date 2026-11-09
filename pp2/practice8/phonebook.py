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
        cur.execute(
            "CALL insert_or_update_user(%s, %s);",
            (name, phone)
        )

        conn.commit()
        print("Contact inserted or updated successfully!")

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
    pattern = input("Enter name or phone pattern: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM search_contacts(%s);",
            (pattern,)
        )

        results = cur.fetchall()

        if results:
            for contact in results:
                print(contact)
        else:
            print("No contacts found!")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()
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
def insert_many_contacts():
    names_input = input("Enter names separated by commas: ")
    phones_input = input("Enter phones separated by commas: ")

    names = names_input.split(",")
    phones = phones_input.split(",")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            CALL insert_many_users(%s, %s, NULL);
            """,
            (names, phones)
        )

        result = cur.fetchone()
        conn.commit()

        print("Invalid data:")
        print(result[0] if result else "No invalid data!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()
def show_contacts_page():
    limit = int(input("Enter contacts per page: "))
    page = int(input("Enter page number: "))

    offset = (page - 1) * limit

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT * FROM get_contacts_page(%s, %s);",
            (limit, offset)
        )

        results = cur.fetchall()

        if results:
            for contact in results:
                print(contact)
        else:
            print("No contacts on this page!")

    except Exception as e:
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
        print("6. Insert many contacts")
        print("7. Show contacts by pages")
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

        elif choice == "6":
            insert_many_contacts()
        
        elif choice == "7":
            show_contacts_page()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()