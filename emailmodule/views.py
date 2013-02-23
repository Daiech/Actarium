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
