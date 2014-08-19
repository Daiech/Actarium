#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from apps.account.templatetags.gravatartag import showgravatar
from apps.emailmodule.views import sendEmailHtml
from django.conf import settings


@login_required(login_url='/account/login')
def saveOrganization(request, form, org_obj=False):
    org = form.save()
    # org.admin = request.user
    # org.save()
    ref = request.POST.get('ref')
    if ref:
        ref = request.POST.get('ref') + "?org=" + str(org.id)
    return org.get_absolute_url()


def send_email_invitation_to_org(user_from, user_to, org):
    try:
        link = settings.URL_BASE + reverse("show_org", args=(org.slug, ))
        email_ctx = {
            'org': minutes.id_group.name,
            'link': link,
            'url_base': settings.URL_BASE,
            'from_first_name': user_from.first_name,
            'from_full_name': user_from.get_full_name()
        }
        sendEmailHtml(16, email_ctx, [user_to.email])
    except Exception, e:
        pass



def set_invitation_to_org(org, u):
    message = {"error": _(u"Ocurrió un error y no se agregó al usuario. por favor recargue pa página e intente de nuevo")}
    if org and u:
        if org.has_user_role(u, "is_member"):
            message = {"error": _(u"%s ya es miembro de la organización" % u.get_full_name())}
        else:
            if org.can_add_members():
                org.set_role(u, is_member=True)
                user = {
                    "id": u.id,
                    "email": u.email,
                    "username": u.username,
                    "image": showgravatar(u.email, 28),
                    "full_name": u.get_full_name(),
                    "is_member": True
                }
                message = {"invited": _(u"%s ahora es miembro de la organización %s" % (u.get_full_name(), org.name)), "user": user}
            else:
                message = {"error": _(u"La organización ya no tiene cupos para agregar usuarios. Comuniquese con el administrador de la organización para actualizar el cupo de miembros.")}
    return message