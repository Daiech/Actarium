from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    print "EL USUARIO EXISTE?"
    print exists
    if exists:
        raise ValidationError("%s ya existe, intente con otra cuenta de correo." % value)
