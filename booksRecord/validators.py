from re import compile

from django.core.exceptions import ValidationError
import barcodenumber

import django.core.validators as dv

def ean13_validator(value):
    if not barcodenumber.check_code(
        'ean13',
        str(value)
    ):
        raise ValidationError(
            'контрольная сумма штрихкода "%(value)s" неверна, проверьте введённые данные',
            params={'value':value}
        )
        
_grade_regex = compile(r"(?:^1[01]|^\d)(?:(?:-)1[01]$|\d$)?")

# the regular expression above may be too difficult,
# in the case of much overhead replace it with the following string
# (just copy-paste it into quotation marks):
# ^[01]?\d(?:-[01]?\d)?$


def grade_validator(value):
    # check if the given value matches
    # a number of grade (1, 2, 3, etc.) or an range
    # of grades (1-11, 4-5, etc.)
    return dv.RegexValidator(
        regex=_grade_regex,
        message='''Введите номер класса или диапазон номеров, \
например: "5", "4-5", и т. п.'''
    )