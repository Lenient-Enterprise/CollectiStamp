import re


def validate_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.compile(patron).match(email)