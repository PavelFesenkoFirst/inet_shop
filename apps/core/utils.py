import re


def phone_formatting(value):
    value = re.sub(r'\D', '', value)
    return '380' + value[:9]
