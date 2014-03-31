from actarium_apps.organizations.models import rel_user_group
def get_groups(request):
	if request.user.is_authenticated():
		g = rel_user_group.objects.filter(id_user=request.user, is_active=True, is_member=True)
	else:
		g = None
	return {"THE_GROUPS": g}