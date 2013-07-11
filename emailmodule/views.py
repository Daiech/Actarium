#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from actions_log.views import saveErrorLog
from django.contrib.auth.models import User


def sendEmailHtml(email_type, ctx, to):
    """
        Este modulo esta en proceso de construccion, por el momento se utilizara este metodo que recibe
        el tipo de correo que se envia y el contexto con las variables que se trasmitiran a cada template.
        La siguiente lista define los valores perimitidos para la variable type y su respectivo significado.
        1- Correo de validacion.
        2- Correo de nueva reunion
        3- Correo de nueva Acta
        4- Correo de asignacion de rol
        5- Correo de confirmacion de asistencia a reunion
        6- Correo de invitacion a un grupo
        7- Correo de invitacion a actarium
        8- Correo de notificacion de aceptacion de grupo
        9- Correo notificacion de feedback al staff de Actarium
    """

    if email_type == 1:
        subject = ctx['username'] + " Bienvenido a Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_activate_account.html')
    elif email_type == 2:  # no necesary
        subject = ctx['firstname'] + " (" + ctx['username'] + u") Te ha invitado a una reunión del grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_reunion.html')
    elif email_type == 3:  # colocar restriccioin
        subject = ctx['firstname'] + " (" + ctx['username'] + u") redactó un acta en el grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_minutes.html')
    elif email_type == 4:  # colocar restriccion
        subject = ctx['firstname'] + " (" + ctx['username'] + u") te asignó como " + ctx['rolename'] + " en el grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_set_role.html')
    elif email_type == 5:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + ctx['response'] + u" a la reunión de " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_confirm_assistance.html')
    elif email_type == 6:  # colocar restriccoin
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u" te invitó a unirte al grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_group_invitation.html')
    elif email_type == 7:
        subject = ctx['username'] + u" te invitó a usar Actarium, La plataforma para la gestión de Actas y Reuniones."
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_actarium_invitation.html')
    elif email_type == 8:
        subject = ctx['username'] + u" " + ctx['response'] + u" ha aceptado la invitación al grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_response_group_invitation.html')
    elif email_type == 9:
        subject = ctx['email'] + " Dejo un comentario tipo: " + ctx['type_feed'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_feedback_notification.html')
    elif email_type == 10:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"está solicitando tu precencia en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_resend_activate_account.html')
    elif email_type == 11:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"quiere que hacerte parte de su grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_group_reinvitation.html')
    elif email_type == 12:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"publicó una anotación en un Acta del grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_annotation.html')
    elif email_type == 13:  # colocar restriccioin
        subject = ctx['firstname'] + " (" + ctx['username'] + u") redactó un acta en el grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_new_minutes_for_approvers.html')
    elif email_type == 14:  # colocar restriccioin
        subject = ctx['firstname'] + " (" + ctx['username'] + u") Solicita acceso a tu DNI para el grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/email_dni_request.html')
    else:
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly = get_template('emailmodule/emailtest.html')
        subject, to = 'Mensaje de prueba', ['emesa@daiech.com']
    from_email = 'Actarium <no-reply@daiech.com>'
    d = Context(ctx)
    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    actives_required_list = [3,4,6,14] # This list contains the number of email_type that requires the user is active in actarium
    if email_type in  actives_required_list:
        to = activeFilter(to)

        #    print 'se enviara un correo a las siguientes direcciones ', to

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        #        print "Error al enviar correo electronico tipo: ", email_type, " con plantilla HTML."
        saveErrorLog('Ha ocurrido un error al intentar enviar un correo de tipo %s a %s' % (email_type, to))


def activeFilter(email_list):
    new_email_list = []
    #    print '----------Active filter----------------------------------------'
    for email in email_list:
        _user = User.objects.get(email=email)
        if _user.is_active == True:
            new_email_list.append(email)
            # print 'Se ha evitado enviar correo a: ', email
    return new_email_list
