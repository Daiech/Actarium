from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import datetime
from django.utils.timezone import get_default_timezone, make_naive
import os


def validate_date(value):
    td = make_naive(value, get_default_timezone()) - datetime.datetime.now()
    if not (td.days >= 0 and td.seconds >= 0 and td.microseconds >= 0):
        raise ValidationError("La fecha ingresada es anterior a la fecha actual")


def validateEmail(email):
    '''Using Django validators'''
    try:
        validate_email(email)
        return True
    except:
        return False
    # ''' Using regural expressions '''
    # if len(email) > 4:
    #     import re
    #     if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
    #         return True
    #     else:
    #         return False
    # else:
    #     return False


def validateExtension(value):
    extentions_acepted = ['pdf', 'doc', 'docx']
    if not (os.path.splitext(value)[1][1:].strip().lower() in extentions_acepted):
        return False
    return True
