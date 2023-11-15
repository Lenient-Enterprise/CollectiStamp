import re


def validate_email(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return email.match(patron)