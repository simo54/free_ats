import re
import os
import docx2txt

from xlsx_file import workbook, excel_file
from openpyxl import load_workbook
from key_words import return_keys
from load_and_write import load_and_write


def upload_docx(file):
    doc = docx2txt.process(file)
    text_to_analyze = ''
    results = []
    text_formatted = doc.lower()

    for key_word in return_keys():
        key_word_formatted = key_word.lower()
        match = text_formatted.count(key_word_formatted)
        results.append(match)

    hits = [x for x in results if x != 0]

    try:
        score = str("{:.0%}".format(len(hits) / len(results)))
    except ZeroDivisionError:
        score = 0

    email_user = re.search(r'[\w\.-]+@[\w\.-]+', text_formatted)
    phone_number = re.findall(
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text_formatted)

    value_row = [[str(os.path.basename(
        file)), str(score), str(email_user.group(0)), str(phone_number)]]

    load_and_write(value_row)
