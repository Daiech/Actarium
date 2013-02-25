#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def sendEmailHtml(email_type,ctx, to):
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
    """
    if email_type == 1:
        subject = ctx['username']+" Bienvenido a Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_activate_account.html')
    elif email_type == 2:
        subject = ctx['firstname']+" (" + ctx['username'] + u") Te ha invitado a una reunión del grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_new_reunion.html')
    elif email_type == 3:
        subject = ctx['firstname']+" (" + ctx['username'] + u") redactó un acta en el grupo " + ctx['groupname'] + " en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_new_minutes.html')
    elif email_type == 4:
        subject = ctx['firstname']+" (" + ctx['username'] + u") te asignó como " + ctx['rolename'] + " en el grupo "+ ctx['groupname']+" en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_set_role.html')
    elif email_type == 5:
        subject = ctx['firstname']+" (" + ctx['username'] + ") " + ctx['response'] + u" a la reunión de "+ ctx['groupname']+" en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_confirm_assistance.html')
    elif email_type == 6:
        subject = ctx['firstname']+" (" + ctx['username'] + ") " + u" te invitó a unirte al grupo "+ ctx['groupname']+" en Actarium"
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_group_invitation.html')
    elif email_type == 7:
        subject =  ctx['username'] + u" te invitó a usar Actarium, La plataforma para la gestión de Actas y Reuniones."
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_group_invitation.html')
    else:
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/emailtest.html')
        subject, to = 'Mensaje de prueba', ['emesa@daiech.com']
    from_email =  'Actarium <no-reply@daiech.com>'
    d = Context(ctx)
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        print "Error al enviar correo electronico."


# 4 title str(request.user.first_name.encode('utf8', 'replace')) + " (" + str(request.user.username.encode('utf8', 'replace')) + ") te " + agrego + " como " + role_name + " en el grupo " + str(g.name)
# contenido = "<br>" + str(request.user.first_name.encode('utf8', 'replace')) + " (" + str(request.user.username.encode('utf8', 'replace')) + ") te ha agregado como <strong>" + role_name + "</strong> en el grupo <a href='" + link + "'>" + str(g.name.encode('utf8', 'replace')) + "</a>. Ahora tienes permisos especiales sobre este grupo.<br><br><br>Ingresa a Actarium en <a href='http://actarium.com' >Actarium.com</a> y ent&eacute;rate de lo que est&aacute; pasando."
# ctx_email = {
#     'firstname':request.user.first_name,
#     'username':request.user.username, 
#     'rolename': role_name, 
#     'groupname': g.name, 
#     'grouplink':link, 
#     'urlgravatar': showgravatar(request.user.email, 50)
# }

# 5 title = str(request.user.first_name.encode('utf8', 'replace')) + " (" + str(request.user.username.encode('utf8', 'replace')) + ") " + resp + " a la reunion de " + str(id_reunion.id_group.name.encode('utf8', 'replace')) + " en Actarium"
# contenido = "Reuni&oacute;n: <strong>" + id_reunion.title + "</strong><br><br>Grupo: <strong>" + str(id_reunion.id_group.name.encode('utf8', 'replace')) + "</strong><br><br>Respuesta: <strong>" + resp + "</strong>"
# ctx_email = {
#     'firstname':request.user.firstname,
#     'username':request.user.username, 
#     'response':resp,
#     'groupname': id_reunion.id_group.name,
#     'titlereunion':  id_reunion.title,
#     'urlgravatar': showgravatar(request.user.email, 50)
# }

# 6 title = str(user_invite.first_name.encode('utf8', 'replace')) + " (" + str(user_invite.username.encode('utf8', 'replace')) + ") te agrego a un grupo en Actarium"
# contenido = str(user_invite.first_name.encode('utf8', 'replace')) + " (" + str(user_invite.username.encode('utf8', 'replace')) + ") te ha invitado al grupo <strong>" + str(group.name.encode('utf8', 'replace')) + "</strong><br><br>" + "Ingresa a Actarium en: <a href='http://actarium.com' >Actarium.com</a> y acepta o rechaza &eacute;sta invitaci&oacute;n."

# ctx_email={
#     'firstname':user_invite.first_name,
#     'username':user_invite.username,
#     'groupname':group.name,
#     'urlgravatar': showgravatar(user_invite.email,50)
# }

title = username_invited + u" te invitó a Actarium, La plataforma de gestión de Actas y reuniones."
contenido = "Bienvenido a Actarium!<br><br><strong>" + username_invited + "</strong> te invit&oacute; a registrarte en Actarium.<br><br><br>Debes ingresar al siguiente link para activar tu cuenta: <a href='http://actarium.daiech.com/account/activate/" + activation_key + "/invited" + id_inv + "' >http://actarium.daiech.com/account/activate/" + activation_key + "</a>, si no lo haces, no se activar&aacute; tu cuenta<br><br>Datos Temporales:<br><ul><li>Nombre de usuario: <strong>" + _username + "</strong></li><li>Contrase&ntilde;a: <strong>" + activation_key[:8] + "</strong></li></ul><br><br><br>Qu&eacute; es Actarium? <br>Actarium es la plataforma para la gesti&oacute;n de cualquier tipo de actas y reuniones.<br><br>Ent&eacute;rate de Actarium en <a href='http://actarium.com/about'>http://actarium.com/about</a>"

ctx_email = {
    'username':username_invited,
    'activation_key':activation_key,
    'id_inv':id_inv,
    'newuser_username':_username,
    'pass': activation_key[:8],
    'urlgravatar': showgravatar(???email,50)
}