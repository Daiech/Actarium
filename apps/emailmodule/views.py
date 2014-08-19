#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context,  RequestContext
from apps.actions_log.views import saveErrorLog
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from actarium_apps.organizations.models import rel_user_group
from apps.emailmodule.models import *
from apps.actions_log.views import saveActionLog, saveViewsLog
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.header import Header
import json
import smtplib

END_SUBJECT = u" en %s" % settings.PROJECT_NAME

def sendEmailHtml(email_type, ctx, to, _group=None):
    """Este modulo esta en proceso de construccion, por el momento se utilizara este metodo que recibe
        el tipo de correo que se envia y el contexto con las variables que se trasmitiran a cada template.
        La siguiente lista define los valores perimitidos para la variable type y su respectivo significado.
        1- Correo de validacion.                                   (Siempre es necesario)
        2- Correo de nueva reunion                                 (Depende del grupo)
        3- Correo de nueva Acta                                    (Depende del grupo)
        4- Correo de asignacion de rol                             (Depende del grupo)
        5- Correo de confirmacion de asistencia a reunion          (Depende del grupo)
        6- Correo de invitacion a un grupo                         (Por definir)
        7- Correo de invitacion a actarium                         (Siempre es necesario)
        8- Correo de notificacion de aceptacion de grupo           (Depende del grupo)
        9- Correo notificacion de feedback al staff de Actarium    (Siempre es necesario)
        10- email_resend_activate_account  (Por definir)
        11- email_group_reinvitation   (Depende del grupo)
        12- email_new_annotation   (Depende del grupo)
        13- email_new_minutes_for_approvers   (Depende del grupo)
        14- Correo de solicitud de acceso a DNI para un grupo      (Depende del grupo)
        15- Recordar aprobar un acta. (va a toda la comisión)
        16- Correo de invitacion a organizacion"""
    htmly = ""
    if email_type == 1:
        subject = ctx['username'] + " Bienvenido a %s" % settings.PROJECT_NAME
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_activate_account.html')
    elif email_type == 2:  # no necesary
        subject = ctx['firstname'] + " (" + ctx['username'] + u") Te ha invitado a una reunión del grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_reunion.html')
    elif email_type == 3:  # colocar restriccioin
        subject = u"El acta " + ctx["code"] + u" ya está disponible en el grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_minutes.html')
    elif email_type == 4:  # colocar restriccion
        subject = ctx['firstname'] + " (" + ctx['username'] + u") te asignó como " + ctx['rolename'] + " en el grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_set_role.html')
    elif email_type == 5:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + ctx['response'] + u" a la reunión de " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_confirm_assistance.html')
    elif email_type == 6:  # colocar restriccoin
        subject = ctx['full_name'] + " (" + ctx['username'] + ") " + u" te invitó a unirte al grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_group_invitation.html')
    elif email_type == 7:
        subject = ctx['username'] + u" te invitó a usar %s, El espacio más cómodo para registrar el resultado de tus reuniones." % settings.PROJECT_NAME
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_actarium_invitation.html')
    elif email_type == 8:
        subject = ctx['username'] + u" " + ctx['response'] + u" ha aceptado la invitación al grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_response_group_invitation.html')
    elif email_type == 9:
        subject = ctx['email'] + " Dejo un comentario tipo: " + ctx['type_feed'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_feedback_notification.html')
    elif email_type == 10:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"está solicitando tu precencia" + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_resend_activate_account.html')
    elif email_type == 11:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"quiere que hacerte de su grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_group_reinvitation.html')
    elif email_type == 12:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"publicó una anotación en un Acta del grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_annotation.html')
    elif email_type == 13:  # colocar restriccioin
        subject = ctx['firstname'] + " (" + ctx['username'] + u") redactó el acta "+ctx['code']+" en el grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_minutes_for_approvers.html')
    elif email_type == 14:  # colocar restriccion
        subject = ctx['firstname'] + " (" + ctx['username'] + u") Solicita acceso a tu DNI para el grupo " + ctx['groupname'] + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_dni_request.html')
    elif email_type == 15:
        subject = u"El acta "+ctx['code']+" del grupo " + ctx['groupname'] + u" espera tu aprobación" + END_SUBJECT
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_remember_approve.html')
    elif email_type == 16:
        subject = ctx['from_first_name'] + u" te invitó a usar %s, El espacio más cómodo para registrar el resultado de tus reuniones." % settings.PROJECT_NAME
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_actarium_invitation.html')
    else:
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/emailtest.html')
        subject, to = 'Mensaje de prueba', ['emesa@daiech.com']
    
    from_email = '%s <no-reply@daiech.com>' % settings.PROJECT_NAME
    ctx["URL_BASE"] = settings.URL_BASE # <- está en el Context proccessor y no funciona con get_template
    d = Context(ctx)
    text_content = plaintext.render(d)
    if htmly:
        html_content = htmly.render(d)
    else:
        return

    actives_required_list = [3, 4, 6, 14]  # This list contains the number of email_type that requires the user is active in actarium
    if email_type in actives_required_list:
        to = activeFilter(to)

    to = groupAdminFilter(to, email_type, _group)

    try:
        smtp = settings.EMAIL_HOST_PASSWORD and settings.EMAIL_HOST_USER
    except NameError:
        smtp = None
    if smtp:
        if len(to) > 0 and not settings.DEBUG:
            sendGmailEmail(to, subject, html_content)
    else:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception, e:
            print e
            print "Error al enviar correo electronico tipo: ", email_type, " con plantilla HTML."
            saveErrorLog('Ha ocurrido un error al intentar enviar un correo de tipo %s a %s' % (email_type, to))


def groupAdminFilter(email_list, email_type, _group):
    new_email_list = []
    _email_admin_type = email_admin_type.objects.get(name='grupo')
    print "email type", email_type
    _email = email.objects.get(email_type=email_type)
    if _email.admin_type == _email_admin_type:
        for e in email_list:
            _user = User.objects.get(email=e)
            try:
                egp = email_group_permissions.objects.get(id_user=_user, id_email_type=_email, id_group=_group)
                if egp.is_active:
                    new_email_list.append(e)
                else:
                    print ".....si esta, no activo"
            except email_group_permissions.DoesNotExist:
                new_email_list.append(e)
            except Exception, e:
                print "groupAdminFilter:", e
        print new_email_list

        return new_email_list
    else:
        return email_list


def activeFilter(email_list):
    new_email_list = []
    #    print '----------Active filter----------------------------------------'
    for email in email_list:
        _user = User.objects.get(email=email)
        if _user.is_active == True:
            new_email_list.append(email)
            # print 'Se ha evitado enviar correo a: ', email
    return new_email_list


@login_required(login_url='/account/login')
def emailNotifications(request, slug_group):
    from apps.groups_app.views import getGroupBySlug
    _group = getGroupBySlug(slug=slug_group)
    try:
        _user_rel = rel_user_group.objects.get(id_user=request.user, id_group=_group)
        _email_admin_type = email_admin_type.objects.get(name='grupo')
        _emails = email.objects.filter(admin_type=_email_admin_type)
        email_list = []
        for e in _emails:
            try:
                egp = email_group_permissions.objects.get(id_user=request.user, id_email_type=e.id, id_group=_group)
                checked = egp.is_active
            except email_group_permissions.DoesNotExist:
                checked = True
            except:
                return HttpResponseRedirect('/groups/#error-email-permissions')
            email_list.append({"id": e.id, "name": e.name, "description": e.description, "checked": checked})
        ctx = {"group": _group, "is_admin": _user_rel.is_admin, "email_list": email_list}
        return render_to_response('groups/adminEmail.html', ctx, context_instance=RequestContext(request))
    except rel_user_group.DoesNotExist:
        return HttpResponseRedirect('/groups/#error-user-rel-group')


@login_required(login_url='/account/login')
def emailAjax(request, slug_group):
    saveViewsLog(request, "apps.groups_app.views.emailAjax")
    # if request.is_ajax():
    _email_admin_type = email_admin_type.objects.get(name='grupo')
    from apps.groups_app.views import getGroupBySlug
    _group = getGroupBySlug(slug=slug_group)

    if request.method == "GET":
        try:
            id_email_type = str(request.GET['id_email_type'])
            input_status = str(request.GET['input_status'])
            if input_status == "false":
                input_status = False
            elif input_status == "true":
                input_status = True
            try:
                _email = email.objects.get(admin_type=_email_admin_type, email_type=id_email_type)
                try:
                    _email_group_permission = email_group_permissions.objects.get(id_user=request.user, id_group=_group, id_email_type=_email)
                    _email_group_permission.is_active = input_status
                    _email_group_permission.save()
                    message = {"saved": True}
                    return HttpResponse(json.dumps(message), mimetype="application/json")
                except email_group_permissions.DoesNotExist:
                    email_group_permissions(id_user=request.user, id_group=_group, id_email_type=_email, is_active=input_status).save()
                    message = {"saved": True}
                    return HttpResponse(json.dumps(message), mimetype="application/json")
                except:
                    message = False
                    return HttpResponse(message)
            except:
                message = False
                return HttpResponse(message)
        except:
            message = False
            return HttpResponse(message)
    else:
        message = False
        return HttpResponse(message)



def sendGmailEmail(to, subject, text, attach=False):
    gmail_user = settings.EMAIL_HOST_USER
    gmail_pwd = settings.EMAIL_HOST_PASSWORD
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = ",".join(to)
    msg['Subject'] = Header("[%s] %s" % (settings.PROJECT_NAME, subject), 'utf-8')

    # msg.attach(MIMEText(text, "html"))
    msg.attach(MIMEText(text, "html", 'utf-8'))

    if attach:
        from email import Encoders
        from email.MIMEBase import MIMEBase
        import os
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    print "Mail Sent"


def show_template(request):
    if request.user.is_staff:

        # variables for testing
        agenda = "Socialización del proyecto a Oscar Granada"
        groupslug = "Grupo-1-1"
        username = "Enriqueto"
        firstname = "Luis"
        titlereunion = u"La reunion del año"
        datereunion = "23 de marzo de 2015"
        locale = "Pereira"
        id_reunion = 4
        datereunionshort="2014-06-11"
        link = "actarium.com/acta"

        return render(request, "emailmodule/" + request.GET.get("p"), locals())
    else:
        raise Http404
