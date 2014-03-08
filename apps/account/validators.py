from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError("%s ya existe, intente con otra cuenta de correo." % value)


def is_email_unique(value):
	if User.objects.filter(email=value).count() == 0:
		return True
	else:
		return False