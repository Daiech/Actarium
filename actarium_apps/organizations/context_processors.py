from .models import OrganizationsUser
def my_orgs(request):
	if request.user.is_authenticated():
		orgs = request.user.organizationsuser_user.get_orgs_by_role_code("is_member")
	else:
		orgs = None
	return {"MY_ORGS": orgs}