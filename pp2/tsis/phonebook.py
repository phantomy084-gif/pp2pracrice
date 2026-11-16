import csv
import json
from connect import connect, create_table


def insert_from_csv():
    filename = "contacts.csv"

    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                first_name = row["first_name"]
                phone = row["phone"]
                phone_type = row["phone_type"]
                email = row["email"]
                birthday = row["birthday"]
                group_name = row["group"]

                cur.execute("""
                    INSERT INTO groups (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING;
                """, (group_name,))

                cur.execute(
                    "SELECT id FROM groups WHERE name = %s",
                    (group_name,)
                )
                group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts
                    (first_name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    RETURNING id;
                """, (first_name, phone, email, birthday, group_id))

                result = cur.fetchone()

                if result:
                    contact_id = result[0]

                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s);
                    """, (contact_id, phone, phone_type))

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
import json
import os

def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.first_name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(
                json_agg(
                    json_build_object(
                        'phone', p.phone,
                        'type', p.type
                    )
                ) FILTER (WHERE p.id IS NOT NULL),
                '[]'::json
            )
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
        ORDER BY c.id;
    """)

    rows = cur.fetchall()
    contacts = []

    for row in rows:
        contacts.append({
            "first_name": row[0],
            "email": row[1],
            "birthday": row[2].isoformat() if row[2] else None,
            "group": row[3],
            "phones": row[4]
        })

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.json")

    with open(file_path, "w") as file:
        json.dump(contacts, file, indent=4)

    cur.close()
    conn.close()

    print("Export successful!")
    print("Saved to:", file_path)

def import_json():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "contacts.json"
    )

    with open(file_path, "r") as file:
        contacts = json.load(file)

    conn = connect()
    cur = conn.cursor()

    try:
        for contact in contacts:
            name = contact["first_name"]
            phones = contact["phones"]
            first_phone = phones[0]["phone"] if phones else None

            cur.execute(
                "SELECT id FROM contacts WHERE first_name = %s",
                (name,)
            )

            existing = cur.fetchone()

            if existing:
                answer = input(
                    f"{name} already exists. Skip or overwrite? (s/o): "
                )

                if answer.lower() == "s":
                    continue

                elif answer.lower() == "o":
                    contact_id = existing[0]

                    cur.execute("""
                        UPDATE contacts
                        SET phone = %s,
                            email = %s,
                            birthday = %s
                        WHERE id = %s
                    """, (
                        first_phone,
                        contact["email"],
                        contact["birthday"],
                        contact_id
                    ))

                    cur.execute(
                        "DELETE FROM phones WHERE contact_id = %s",
                        (contact_id,)
                    )

                else:
                    print("Invalid choice. Skipping contact.")
                    continue

            else:
                cur.execute("""
                    INSERT INTO contacts
                    (first_name, phone, email, birthday)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (
                    name,
                    first_phone,
                    contact["email"],
                    contact["birthday"]
                ))

                contact_id = cur.fetchone()[0]

            group_name = contact["group"]

            if group_name:
                cur.execute("""
                    INSERT INTO groups (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (group_name,))

                cur.execute(
                    "SELECT id FROM groups WHERE name = %s",
                    (group_name,)
                )

                group_id = cur.fetchone()[0]

                cur.execute(
                    "UPDATE contacts SET group_id = %s WHERE id = %s",
                    (group_id, contact_id)
                )

            for phone in phones:
                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (
                    contact_id,
                    phone["phone"],
                    phone["type"]
                ))

        conn.commit()
        print("JSON import completed!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

def filter_by_group():
    group_name = input("Enter group name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.first_name, c.email, c.birthday, p.phone
        FROM contacts c
        LEFT JOIN phones p ON c.id = p.contact_id
        JOIN groups g ON c.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY c.first_name;
    """, ('%' + group_name + '%',))

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found!")

    cur.close()
    conn.close()
def search_by_email():
    email = input("Enter email or part of email: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.first_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.first_name;
    """, ('%' + email + '%',))

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found!")

    cur.close()
    conn.close()
def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose sorting option: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        order = "c.first_name"
    elif choice == "2":
        order = "c.birthday"
    elif choice == "3":
        order = "c.date_added"
    else:
        print("Invalid choice!")
        cur.close()
        conn.close()
        return

    cur.execute(f"""
        SELECT c.id, c.first_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {order};
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()
def browse_contacts():
    limit = 3
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        try:
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s);",
                (limit, offset)
            )

            rows = cur.fetchall()

            if not rows:
                print("No more contacts!")
                offset = max(0, offset - limit)
            else:
                print("\n===== CONTACTS =====")

                for row in rows:
                    print(row)

            print("\n1. Next page")
            print("2. Previous page")
            print("0. Quit")

            choice = input("Choose: ")

            if choice == "1":
                offset += limit
            elif choice == "2":
                offset = max(0, offset - limit)
            elif choice == "0":
                break
            else:
                print("Invalid choice!")

        except Exception as e:
            print("Error:", e)
            break

    cur.close()
    conn.close()
def add_phone_menu():
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    phone_type = input("Enter phone type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL add_phone(%s::VARCHAR, %s::VARCHAR, %s::VARCHAR)",
            (name, phone, phone_type)
        )

        conn.commit()
        print("Phone added successfully!")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()
def move_contact_menu():
    name = input("Enter contact name: ")
    group_name = input("Enter group name: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL add_phone(%s::VARCHAR, %s::VARCHAR, %s::VARCHAR)",
            (name, group_name)
        )

        conn.commit()
        print("Contact moved successfully!")

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
        print("6. Insert many contacts")
        print("7. Show contacts by pages")
        print("8. Export contacts to JSON")
        print("9. Import contacts from JSON")
        print("10. Filter contacts by group")
        print("11. Search contacts by email")
        print("12. Sort contacts")
        print("13. Browse contacts")
        print("14. Add phone to existing contact")
        print("15. Move contact to group")
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

        elif choice == "8":
            export_json()

        elif choice == "9":
            import_json()
        elif choice == "10":
            filter_by_group()

        elif choice == "11":
            search_by_email()
        
        elif choice == "12":
            sort_contacts()

        elif choice == "13":
            browse_contacts()

        elif choice == "14":
            add_phone_menu()
        
        elif choice == "15":
            move_contact_menu()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid option!")


if __name__ == "__main__":
    main()