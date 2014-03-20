from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login')
def saveOrganization(request, form, org_obj=False):
    org = form.save()
    # org.admin = request.user
    # org.save()
    ref = request.POST.get('ref')
    if ref:
        ref = request.POST.get('ref') + "?org=" + str(org.id)
    return org.get_absolute_url()