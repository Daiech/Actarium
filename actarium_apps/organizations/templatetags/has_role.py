from django import template
register = template.Library()


def has_role(user, role_list):
	print "%s TIENE ESTE ROL??????????????????????????? %s" % (user, role_list)
	return True

register.filter('has_role', has_role)
