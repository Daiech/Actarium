#encoding:utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.http import Http404
from groups.models import billing, packages, organizations, groups_pro, templates, rel_user_private_templates, private_templates, rel_user_group
# group_type, rel_user_group, minutes, invitations, minutes_type_1, minutes_type, reunions, admin_group, assistance, rel_user_minutes_assistance
from groups.forms import newOrganizationForm
#from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
#import re
import datetime
# from dateutil.relativedelta import *
#from django.utils.timezone import make_aware, get_default_timezone, make_naive
from django.utils import simplejson as json
#from account.templatetags.gravatartag import showgravatar
#from django.core.mail import EmailMessage
from actions_log.views import saveActionLog
from Actarium.settings import MEDIA_ROOT, ORGS_IMG_DIR, MEDIA_URL, PROJECT_PATH


#def settings(request):
#    ctx = {'TITLE': "Actarium by Daiech"}
#    return render_to_response('website/settings_menu.html', ctx, context_instance=RequestContext(request))

#def settings_account(request):
#    ctx = {'TITLE': "Actarium by Daiech"}
#    return render_to_response('website/settings_account.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def settingsBilling(request):
    array_billing = []
    try:
        packages_list = packages.objects.filter(is_visible=True)
    except packages.DoesNotExist:
        packages_list = "No hay información disponible."
    try:
        billing_list = billing.objects.filter(id_user=request.user)
    except billing.DoesNotExist:
        billing_list = "No hay información disponible."
        for b in billing:
            array_billing[b.id] = int(b.time) * int(b.id_package.price)
    ctx = {'TITLE': "Facturación - configuración", "packages_list": packages_list, "billing_list": billing_list, 'array_billing': array_billing}
    return render_to_response('asettings/settings_billing.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def settingsOrganizations(request):
    if request.method == "GET":  # envia una variable para seleccionar una organizacion
        try:
            new_group = request.GET['saved']
        except Exception:
            new_group = False
    try:
        orgs = organizations.objects.filter(is_active=True, id_admin=request.user)
    except Exception, e:
        orgs = None
        raise e
    groups = list()
    for org in orgs:
        groups.append({"org": org, "groups_org_list": groups_pro.objects.filter(id_organization=org.id)})
    ctx = {"organizations": groups, "group_saved": new_group}
    return render_to_response('asettings/settings_organization.html', ctx, context_instance=RequestContext(request))


@login_required(login_url='/account/login')
def newOrganization(request):
    ref_get = ""
    if request.method == "GET":
        try:
            ref_get = request.GET['ref']
        except Exception:
            ref_get = "/settings/organizations"
    if request.method == "POST":
        form = newOrganizationForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            url = "/static/img/groups/default.jpg"
            org = organizations(
                id_admin=request.user,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                logo_address=url)
            org.save()
            saveActionLog(request.user, 'NEW_ORG', "name: %s" % (form.cleaned_data['name']), request.META['REMOTE_ADDR'])
            try:
                url_file = request.FILES['logo_address']
            except Exception:
                url_file = None
            if url_file:
                from django.template import defaultfilters
                url = save_file(url_file, defaultfilters.slugify(org.name) + "-" + str(org.id), path=ORGS_IMG_DIR)
                createThumbnail(url)
                org.logo_address = MEDIA_URL + url + "-thumbnail.jpg"
                deleteRealImage(url)
            org.save()
            try:
                ref = request.POST['ref'] + "?org=" + str(org.id)
            except Exception:
                ref = ref_get
            return HttpResponseRedirect(ref)
    else:
        form = newOrganizationForm()
    ctx = {"form_org": form, "ref": ref_get}
    return render_to_response('asettings/settings_new_organization.html', ctx, context_instance=RequestContext(request))


def createThumbnail(buf):
    try:
        try:
            from PIL import Image
        except Exception, e:
            # raise e
            print e
            return False
        import glob
        import os

        size = 128, 128
        for infile in glob.glob(PROJECT_PATH + MEDIA_URL[:-1] + buf):
            file, ext = os.path.splitext(infile)
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(file + "-thumbnail.jpg", "JPEG")
            return file + "-thumbnail.jpg"
    except Exception, e:
        print e
        return False


def resize_uploaded_image(buf):
    print "------ URL ------:", buf
    import Image
    from cStringIO import StringIO
    try:
        image = Image.open(buf)

        (width, height) = image.size
        print "ANCHO ALTO", width, height
        (width, height) = scale_dimensions(width, height, longest_side=240)
        print "NEW ANCHO ALTO", width, height
        resizedImage = image.resize((width, height))
        print "-------------IMAGEN-----------", resizedImage

        # Turn back into file-like object
        resizedImageFile = StringIO.StringIO()
        print "VA BIEN 0", resizedImageFile
        resizedImage.save(resizedImageFile, 'PNG', optimize=True)
        print "VA BIEN 1", resizedImage
        resizedImageFile.seek(0)    # So that the next read starts at the beginning
        print "VA BIEN 2"
        buf = resizedImageFile
        print "VA BIEN 3"
        return resizedImageFile
    except Exception, e:
        print "------ ERROR AL CREAR thumbnail", e
    return buf


def scale_dimensions(width, height, longest_side):
    if width > height:
        if width > longest_side:
            ratio = longest_side*1./width
            return (int(width*ratio), int(height*ratio))
        elif height > longest_side:
            ratio = longest_side*1./height
            return (int(width*ratio), int(height*ratio))
    return (width, height)


def resize_uploaded_image2(buf):
    try:
        import Image
        from cStringIO import StringIO

        image = Image.open(buf)

        maxSize = (240, 240)
        resizedImage = image.thumbnail(maxSize, Image.ANTIALIAS)
        print "-------------IMAGEN-----------", resizedImage
        # Turn back into file-like object
        resizedImageFile = StringIO()
        resizedImage.save(resizedImageFile, 'PNG', optimize=True)
        resizedImageFile.seek(0)    # So that the next read starts at the beginning
        buf = resizedImageFile
    except Exception, e:
        print "ERROR AL CREAR thumbnail", e
    return buf


@login_required(login_url='/account/login')
def editOrganization(request, id_org):
    if request.method == "POST":
        form = newOrganizationForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            org = organizations.objects.get(id=id_org)
            org.name = form.cleaned_data['name']
            org.description = form.cleaned_data['description']
            org.save()
            try:
                url_file = request.FILES['logo_address']
            except Exception:
                url_file = None
            if url_file:
                # if url_file._size > 4*1024*1024:
                #     raise ValidationError("Image file too large ( > 4mb )")
                from django.template import defaultfilters
                url = save_file(url_file, defaultfilters.slugify(org.name) + "-" + str(org.id), path=ORGS_IMG_DIR)
                org.logo_address = url
                org.save()
            return HttpResponseRedirect("/settings/organizations/?org=" + id_org)
    try:
        org = organizations.objects.get(id=id_org)
        initial = {"name": org.name, "logo_address": org.logo_address, "description": org.description}
    except Exception:
        org = None
        initial = {}
    form = newOrganizationForm(initial=initial)
    ctx = {"form_org": form, "org": org}
    return render_to_response('asettings/settings_edit_organization.html', ctx, context_instance=RequestContext(request))


def deleteRealImage(url):
    import os
    os.remove(MEDIA_ROOT + url)


def save_file(file, slug, path=''):
    ''' Little helper to save a file
    '''
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(slug)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()
    return "/" + str(path) + str(slug)


@login_required(login_url='/account/login')
def requestPackage(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_pack = str(request.GET['id_package'])
            id_package = packages.objects.get(pk=id_pack)
            gpa = str(request.GET['gpa'])
            time = str(request.GET['time'])
            billing(id_package=id_package, id_user=request.user, groups_pro_available=gpa, time=time).save()
            is_billing_saved = "True"
        else:
            is_billing_saved = "False"
    else:
        is_billing_saved = "Error de servidor"
    return HttpResponse(json.dumps(is_billing_saved), mimetype="application/json")


@login_required(login_url="/account/login")
def replyRequestPackage(request):
    if request.user.is_staff:
        ctx = {"billing_list": billing.objects.exclude(state=0).order_by("-date_request"),
                "billing_list2": billing.objects.filter(state='0').order_by("-date_request")
        }
        return render_to_response('asettings/settings_replyRequest.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

@login_required(login_url="/account/login")
def setReplyRequestPackage(request):
    if request.is_ajax():
        if request.method == 'GET':
            id_billing = str(request.GET['id_billing'])
            state = str(request.GET['answer'])
            b = billing.objects.get(id=id_billing)
            mtim = b.time
            dtn = datetime.datetime.now()
            b.date_start = dtn
            dtn = dtn + datetime.timedelta(days=(30 * int(mtim)))
            b.date_end = dtn
            b.state = state
            b.save()
            is_billing_saved = "True"
        else:
            is_billing_saved = "False"
    else:
        is_billing_saved = "Error de servidor"
    return HttpResponse(json.dumps(is_billing_saved), mimetype="application/json")

@login_required(login_url="/account/login")
def settingsTemplates(request):
    _templates = rel_user_private_templates.objects.filter(id_user=request.user)
    _groups = rel_user_group.objects.filter(id_user=request.user, is_admin=True)
    _private_templates = private_templates.objects.filter(id_user=request.user)
    ctx = {
            "templates":_templates,
            "groups": _groups,
            "private_templates_assigned": _private_templates
    }
    return render_to_response('asettings/settings_templates.html', ctx, context_instance=RequestContext(request))

@login_required(login_url="/account/login")
def assignTemplateAjax(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                id_template = str(request.GET['id_template'])
                id_group = str(request.GET['id_group'])
                try:
                    from groups.models import groups
                    _rel_user_private_templates = rel_user_private_templates.objects.get(id_user=request.user, id_template = templates.objects.get(pk=id_template))
                    _group = rel_user_group.objects.get(id_user=request.user, id_group = groups.objects.get(pk=id_group), is_admin=True)
                    try:
                        response = "True"
                        private_templates(id_template=_rel_user_private_templates.id_template, id_group = _group.id_group, id_user= request.user).save()
                    except:
                        response = 'Error al guardar los datos, probablemente la plantilla que desea asignar ya se encuentra relacionada con el grupo seleccionado, por favor verifica los datos'
                except:
                    response = "Error: No se ha podido guardar la asignacion."
                print id_template, id_group
            except:
                response = "Problema con los parametros get"
        else:
            response = "No se recibio una peticion get"
    else:
        response = "No ser recibio una consulta Ajax"
    return HttpResponse(json.dumps(response), mimetype="application/json")
    
@login_required(login_url="/account/login")
def unassignTemplateAjax(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                id_template = str(request.GET['id_template'])
                id_group = str(request.GET['id_group'])
                try:
                    from groups.models import groups
                    _rel_user_private_templates = rel_user_private_templates.objects.get(id_user=request.user, id_template = templates.objects.get(pk=id_template))
                    _group = rel_user_group.objects.get(id_user=request.user, id_group = groups.objects.get(pk=id_group), is_admin=True)
                    response = "True"
                    try:
                        response = "True"
                        private_templates.objects.get(id_template=_rel_user_private_templates.id_template, id_group = _group.id_group, id_user= request.user).delete()
                    except:
                        response = 'La plantilla seleccionada no esta asignada al grupo seleccionado'
                except:
                    response = "Error: los datos no coinciden con los datos guardados"
                print id_template, id_group
            except:
                response = "Problema con los parametros get"
        else:
            response = "No se recibio una peticion get"
    else:
        response = "No ser recibio una consulta Ajax"
    return HttpResponse(json.dumps(response), mimetype="application/json")

    