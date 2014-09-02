from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def greater_than_or_equal_to_five(value):
	try:
		value = int(value)
	except:
		raise ValidationError(_(u"Ingrese un número entero."))
	if value < 1:
		raise ValidationError(_(u"El número debe ser mayor o igual a 5"))
	else:
		print "Correcto"



