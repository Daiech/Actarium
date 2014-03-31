from django import template
from django.template import Variable, VariableDoesNotExist
from actarium_apps.organizations.models import rel_user_group
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

@register.assignment_tag(takes_context=True)
def is_member_of_group(context, user, g):
    try:
        group = Variable(g).resolve(context)
    except VariableDoesNotExist:
        print "Errorcito"
        group = None
    try:
        user = Variable(user).resolve(context)
    except VariableDoesNotExist:
        user = None
    if user and group:
        rel = rel_user_group.objects.get_rel(user, group)
        if rel.count() > 0:
            return True
        else:
            return False
    else:
        return False
