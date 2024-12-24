import csv
import os
import re
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), 'phonebook_raw.csv'), encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    headers = next(rows)
    pprint(headers)
    contacts_list = list(rows)


def normalize_fullname(contacts: list):
    for contact in contacts:
        user_main_data = " ".join(contact[0:2]).strip().split(" ")
        contact[:2] = user_main_data


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



if __name__ == '__main__':
    normalize_fullname(contacts_list)
    normalize_phone_number(contacts_list)
    pprint(contacts_list)

    # with open(os.path.join(os.path.dirname(__file__), 'phonebook.csv'), 'w', encoding='utf-8') as f:
    #     datawriter = csv.writer(f, delimiter=',')
    #     datawriter.writerow(headers)
    #     datawriter.writerows(contacts_list)