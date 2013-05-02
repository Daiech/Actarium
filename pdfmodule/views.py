#encoding:utf-8
# from django.contrib.auth.decorators import login_required
from groups.models import minutes
# from django.contrib.auth.models import User
# from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
# from django.template import RequestContext
#from django.core.mail import EmailMessage
import random
from Actarium.settings import MEDIA_ROOT

from reportlab.platypus import Table
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
# from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import inch
from reportlab.platypus import Frame
from xhtml2pdf.pisa import CreatePDF, startViewer
from actions_log.views import saveActionLog, saveViewsLog


def minutesToPdf(request, id_minutes):
    saveViewsLog(request, "pdfmodule.views.minutesToPdf")
    if request.user.is_staff:

        _minutes = minutes.objects.get(pk=id_minutes)

        # Datos del acta
        m_group = _minutes.id_group.name
        m_code = _minutes.code
        m_date_created = _minutes.date_created
        m_date_start = _minutes.id_extra_minutes.date_start
        m_date_end = _minutes.id_extra_minutes.date_end
        m_location = _minutes.id_extra_minutes.location
        m_agenda = _minutes.id_extra_minutes.agenda
        m_agreement = _minutes.id_extra_minutes.agreement

        # --------------------------------------------------------------
        # Creacion del PDF
        pdf_address = "/pdf/reporte%s.pdf" % (int(random.random() * 100000))

        #Generar el objeto canvas (documento PDF)
        from reportlab.pdfgen import canvas
        canvas_obj = canvas.Canvas("%s%s" % (MEDIA_ROOT, pdf_address))

        #Definiendo estilos basicos
        estiloHoja = getSampleStyleSheet()
        estilo1 = estiloHoja['BodyText']
        estilo2 = estiloHoja['Normal']

        # Inicializamos story (Listas de objetos flowables)
        story = []

        # Añadimos algunos flowables.
        p1 = Paragraph(u"Grupo: %s" % (m_group), estilo1)
        p2 = Paragraph(u"Codigo de acta: %s Creada el: %s" % (m_code, m_date_created), estilo1)
        p3 = Paragraph(u"La reunion inicio el: %s Y finalizo el: %s" % (m_date_start, m_date_end), estilo1)
        p4 = Paragraph(u"Lugar de encuentro: %s" % (m_location), estilo1)
        p5 = Paragraph(u"Orden de dia", estilo1)
        p6 = Paragraph(u"%s" % (m_agenda), estilo1)
        p7 = Paragraph(u"Conclusiones", estilo1)
        p8 = Paragraph(u"%s" % (m_agreement), estilo1)

        # Añadimos los flowables a la lista story.

        story.append(p1)
        story.append(p2)
        story.append(p3)
        story.append(p4)
        story.append(p5)
        story.append(p6)
        story.append(p7)
        story.append(p8)

        #creo los frames
        f1 = Frame(50, 600, 500, 200, showBoundary=1)

        # agregando los frames al objeto canvas
        f1.addFromList(story, canvas_obj)

        canvas_obj.save()

        return HttpResponseRedirect('/media%s' % (pdf_address))
    else:
        return HttpResponseRedirect('/')


def minutesToPdfTest(request, id_minutes):
    saveViewsLog(request, "pdfmodule.views.minutesToPdfTest")
    if request.user.is_staff:
        pdf_address = "/pdf/reporte%s.pdf" % (int(random.random()*100000))
    # try:
        # _actions= rel_user_action.objects.all().order_by("-date_done")

        from reportlab.pdfgen import canvas
        canvas_obj = canvas.Canvas("%s%s" % (MEDIA_ROOT, pdf_address))
        # c.drawString(50,700,"700 Primera prueba de reportlab con django")
        # c.showPage()
        # c.save()
        estiloHoja = getSampleStyleSheet()
        estilo1 = estiloHoja['BodyText']
        estilo2 = estiloHoja['Normal']

        # Inicializamos story.

        story = []
        story2 = []

        # Añadimos algunos flowables.

        parrafo1 = Paragraph('Id de Acta: %s' % (id_minutes),estilo1)
        parrafo2 = Paragraph('España, Murcia, Lorca', estilo2)

        # Agregamos una tabla
        list_data = [ ["Esto","Es","Una","Tabla"],
                      ["Esto","Es","Una","Tabla"],
                      ["Esto","Es","Una","Tabla"],
                      ["Esto","Es","Una","Tabla"],]
        t = Table(list_data)

        #agregamos una imagen
        img = Image("static/img/dragon.jpg",width=100,height=100)
        # img = Image("static/img/org.png",width=4,height=3)

        # Añadimos los flowables a la lista story.

        story.append(parrafo1)
        story.append(parrafo2)
        story.append(t)
        story.append(Spacer(0,20))
        story2.append(img)

        # Creamos documento.

        # documento = SimpleDocTemplate("%s%s"%(MEDIA_ROOT,pdf_address), pagesize = A4)

        # Y construimos el documento.

        # documento.build(story)

        #creo los frames
        f1 = Frame(350,350,200,200,showBoundary=1)
        f2 = Frame(50,50,200,200,showBoundary=1)


        # agregando los frames al objeto canvas
        f1.addFromList(story,canvas_obj)
        canvas_obj.showPage()
        
        f2.addFromList(story2,canvas_obj)

        canvas_obj.save()
    # except:
        # print "Ocurrio un error al generar el PDF"
        # ctx = {"actions": rel_user_action.objects.all().order_by("-date_done")}
        return HttpResponseRedirect('/media%s'%(pdf_address))
    else:
        return HttpResponseRedirect('/')


def minutesHtmlToPdf(html_string, name_pdf):
    pdf_address = "/pdf/%s_Actarium%s.pdf" % (name_pdf, int(random.random() * 100000))
    file_dir = "%s%s" % (MEDIA_ROOT, pdf_address)
    file_dir = file(file_dir, "wb")
    pdf = CreatePDF(html_string, file_dir)  #, default_css="#minute{margin:200px}")
    if not pdf.err:
        startViewer(name_pdf)
    file_dir.close()
    return '/media%s' % (pdf_address)
