import csv
import os
import re

with open(os.path.join(os.path.dirname(__file__), 'phonebook_raw.csv'), encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    headers = next(rows)
    contacts_list = list(rows)

def normalize_fullname(contacts: list):
    for contact in contacts:
        user_main_data = ' '.join(contact[:3]).strip().split(' ')
        if len(user_main_data) > 3:
            for i in user_main_data:
                if not i.isalpha():
                    user_main_data.remove(i)
        elif len(user_main_data) < 3:
            contact[:2] = user_main_data
        else:
            contact[:3] = user_main_data


def normalize_phone_number(contacts: list):
    for contact in contacts:
        phone_number = contact[5]
        pattern = r'(?:\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
        if phone_number and 'доб' not in phone_number:
            contact[5] = (re.sub(pattern, r"+7(\1)\2\3\4", phone_number))
        elif phone_number and 'доб' in phone_number:
            extra_pattern = r'доб.?\s*(\d+)'
            extra = re.search(extra_pattern, phone_number)
            if extra:
                match = re.search(pattern, phone_number)
                contact[5] = f'+7({match.group(1)}){match.group(2)}{match.group(3)}{match.group(4)} доб.{extra.group(1)}'
    return contacts


def group_contacts(contacts: list):
    result = {}
    for contact in contacts:
        key = tuple(contact[0:2])
        if key not in result:
            result[key] = contact
        else:
            result[key] = [
                result[key][i] or contact[i] for i in range(len(contact))
            ]
    return list(result.values())

normalize_fullname(contacts_list)
normalize_phone_number(contacts_list)

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), 'phonebook.csv'), 'w', encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(headers)
        normalize_fullname(contacts_list)
        normalize_phone_number(contacts_list)
        datawriter.writerows(group_contacts(contacts_list))
        print('Done!')