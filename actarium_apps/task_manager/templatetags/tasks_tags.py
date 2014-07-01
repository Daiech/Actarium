#encoding:utf-8
from django.template import Library
from django.utils.translation import ugettext as _

register = Library()


@register.filter
def get_rol_name(rol_code):
    
    if rol_code == "RES":
        return _('Responsable')
    elif rol_code == "CRE":
        return _('Creador')
    else:
        return rol_code
       

@register.filter
def get_status_name(rol_code):
    
    if rol_code == "CAN":
        return _('Cancelada')
    elif rol_code == "TER":
        return _('Terminada')
     elif rol_code == "ASI":
        return _('Asignada')
    else:
        return rol_code