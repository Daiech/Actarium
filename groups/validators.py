from django.core.exceptions import ValidationError
import datetime
from django.utils.timezone import make_aware, get_default_timezone, make_naive

def validate_date(value):
    td = make_naive(value,get_default_timezone()) - datetime.datetime.now()
    if not(td.days >=0 and td.seconds >= 0 and td.microseconds >=0):
        raise ValidationError("La fecha ingresada es anterior a este momento")