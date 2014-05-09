from django import template
from django.template import Variable, VariableDoesNotExist
from actarium_apps.organizations.models import rel_user_group
register = template.Library()

@register.assignment_tag(takes_context=True)
def has_role(context, user, org, role):
    l = role.split(",")
    try:
        org = Variable(org).resolve(context)
    except VariableDoesNotExist:
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


def filter_only_groups_of_user(group_list, user):
    """if user is an admin, return the initial group_list var, else the group_list list will be filtered"""
    org = group_list[0].organization if len(group_list) > 0 else None
    if org and not org.has_user_role(user, "is_admin"):
        group_list = [g for g in group_list if rel_user_group.objects.get_rel(user, g)]
    return group_list
register.filter('only_groups_of', filter_only_groups_of_user)