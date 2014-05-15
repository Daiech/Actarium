from django import template
register = template.Library()
from apps.website.views import getGlobalVar


# @register.tag_function
@register.tag(name="global_var") #('get_global_var', get_global_var)
def get_global_var(p, name):
    print "p", p
    print "NOMBRE:", name
    return getGlobalVar(name)

# register.filter('global_var', get_global_var)