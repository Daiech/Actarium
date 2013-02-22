#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def sendEmailHtml(email_type,ctx, to):
    """
        Este modulo esta en proceso de construccion, por el momento se utilizara este metodo que recibe 
        el tipo de correo que se envia y el contexto con las variables que se trasmitiran a cada template.
        La siguiente lista define los valores perimitidos para la variable type y su respectivo significado.
        1- correo de validacion.
    """
    if email_type == 1:
        plaintext = get_template('emailmodule/emailtest.txt')
        htmly     = get_template('emailmodule/email_activate_account.html')
        subject = ctx['username']+" Bienvenido a Actarium"
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
