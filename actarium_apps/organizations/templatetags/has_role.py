from django import template
from django.template import Variable, VariableDoesNotExist
register = template.Library()

@register.assignment_tag(takes_context=True)
def has_role(context, user, obj, role):
    l = role.split(",")
    try:
        org = Variable(obj).resolve(context)
    except VariableDoesNotExist:
        print "Errorcito"
        org = None
    try:
        user = Variable(user).resolve(context)
    except VariableDoesNotExist:
        user = None
    if user and org:
        return org.has_user_role(user, l[0])
    else:
        return False
