from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def greater_than_or_equal_to_five(value):
	try:
		value = int(value)
	except:
		raise ValidationError(_("Ingrese un numero entero."))
	if value < 5:
		raise ValidationError(_("El numero debe ser mayor o igual a 5"))
	else:
		print "Correcto"



