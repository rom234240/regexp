from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

for contact in contacts_list[1:]:
    parts = []
    for i in range(3):
        if contact[i].strip():
            parts.append(contact[i].strip())

    full_name = " ".join(parts).split()
    contact[0] = full_name[0] if len(full_name) >= 1 else ""
    contact[1] = full_name[1] if len(full_name) >= 2 else ""
    contact[2] = full_name[2] if len(full_name) >= 3 else ""


pattern = re.compile(
    r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
    r"(\s*\(?доб\.?\s*(\d+)\)?)?"
)
      
for contact in contacts_list[1:]:
    phone = contact[5]
    if not phone:
        continue
    
    match = pattern.search(phone)
    if match:
        main_number = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        extension = f" доб.{match.group(7)}" if match.group(7) else ""
        contact[5] = main_number + extension
    else:
        contact[5] = phone

merged = {}
for contact in contacts_list[1:]:
    key = (contact[0], contact[1])
    if key in merged:
        for i in range(len(contact)):
            if merged[key][i] == "" and contact[i] != "":
                merged[key][i] = contact[i]
    else:
        merged[key] = contact.copy()

processed_contacts = [contacts_list[0]] + list(merged.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(processed_contacts)

pprint(f"Данные обработаны и сохранены")