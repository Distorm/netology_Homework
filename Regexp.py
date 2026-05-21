import csv
import re
from pprint import pprint


def format_phone(match_obj):
    phone = (
        f"+7({match_obj.group(2)}){match_obj.group(3)}-"
        f"{match_obj.group(4)}-{match_obj.group(5)}"
    )
    if match_obj.group(7):
        phone += f" доб.{match_obj.group(7)}"

    return phone


def process_contacts(contacts_list):
    phone_pattern = re.compile(
        r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
        r"(?:\s*\(?(доб\.?)\s*(\d+)\)?)?"
    )

    merged_contacts = {}

    for row in contacts_list[1:]:
        full_name = " ".join(row[:3]).split()

        while len(full_name) < 3:
            full_name.append("")

        lastname = full_name[0]
        firstname = full_name[1]
        surname = full_name[2]
        phone = row[5]
        if phone:
            phone = phone_pattern.sub(format_phone, phone)

        unique_id = (lastname, firstname)

        if unique_id not in merged_contacts:
            merged_contacts[unique_id] = [
                lastname, firstname, surname, row[3], row[4], phone, row[6]
            ]
        else:
            existing = merged_contacts[unique_id]
            existing[2] = existing[2] or surname
            existing[3] = existing[3] or row[3]
            existing[4] = existing[4] or row[4]
            existing[5] = existing[5] or phone
            existing[6] = existing[6] or row[6]

    return [contacts_list[0]] + list(merged_contacts.values())


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as file:
        rows = csv.reader(file, delimiter=",")
        contacts = list(rows)

    processed_contacts = process_contacts(contacts)

    pprint(processed_contacts)

    with open("phonebook.csv", "w", encoding="utf-8", newline="") as file:
        data_writer = csv.writer(file, delimiter=',')
        data_writer.writerows(processed_contacts)