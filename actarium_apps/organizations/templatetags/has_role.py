from django import template
register = template.Library()


def has_role(user, role):
	print "%s TIENE ESTE ROL??????????????????????????? %s" % (user, role)
	return True

register.filter('has_role', has_role)
