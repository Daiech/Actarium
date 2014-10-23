#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
# from django.http import Http404
from apps.groups_app.models import templates, rel_user_private_templates, private_templates, Groups
from apps.actions_log.views import saveActionLog, saveErrorLog, saveViewsLog
from actarium_apps.organizations.models import rel_user_group

import datetime
import json



@login_required(login_url="/account/login")
def settingsTemplates(request):
    saveViewsLog(request, "asettings.views.settingsTemplates")
    _templates = rel_user_private_templates.objects.filter(id_user=request.user)
    _groups = rel_user_group.objects.filter(id_user=request.user, is_admin=True)
    _private_templates = private_templates.objects.filter(id_user=request.user)
    ctx = {
        "templates": _templates,
        "groups": _groups,
        "private_templates_assigned": _private_templates
    }
    return render_to_response('asettings/settings_templates.html', ctx, context_instance=RequestContext(request))


@login_required(login_url="/account/login")
def assignTemplateAjax(request):
    saveViewsLog(request, "asettings.views.assignTemplateAjax")
    if request.is_ajax():
        if request.method == 'GET':
            try:
                id_template = str(request.GET['id_template'])
                id_group = str(request.GET['id_group'])
            except:
                response = _(u"Problema al intentar recibir los parametros para realizar esta operación")
                return HttpResponse(json.dumps(response), mimetype="application/json")
            try:
                _rel_user_private_templates = rel_user_private_templates.objects.get(id_user=request.user, id_template=templates.objects.get(pk=id_template))
                _group = rel_user_group.objects.get(id_user=request.user, id_group=Groups.objects.get(pk=id_group), is_admin=True)
            except:
                response = _(u"Error: No se ha podido guardar la asignacion.")
                return HttpResponse(json.dumps(response), mimetype="application/json")
            try:
                private_templates(id_template=_rel_user_private_templates.id_template, id_group=_group.id_group, id_user=request.user).save()
                response = "True"
            except:
                response = _(u'Error al guardar los datos, probablemente la plantilla que desea asignar ya se encuentra relacionada con el grupo seleccionado, por favor verifica los datos')
                return HttpResponse(json.dumps(response), mimetype="application/json")
            # print id_template, id_group
        else:
            response = "No se recibio una peticion get"
    else:
        response = "No ser recibio una consulta Ajax"
    return HttpResponse(json.dumps(response), mimetype="application/json")


@login_required(login_url="/account/login")
def unassignTemplateAjax(request):
    saveViewsLog(request, "asettings.views.unassignTemplateAjax")
    if request.is_ajax():
        if request.method == 'GET':
            try:
                id_template = str(request.GET['id_template'])
                id_group = str(request.GET['id_group'])
            except:
                response = _(u"Problema con los parametros get")
                return HttpResponse(json.dumps(response), mimetype="application/json")
            try:
                _rel_user_private_templates = rel_user_private_templates.objects.get(id_user=request.user, id_template=templates.objects.get(pk=id_template))
                _group = rel_user_group.objects.get(id_user=request.user, id_group=Groups.objects.get(pk=id_group), is_admin=True)
            except:
                response = _(u"Error: los datos no coinciden con los datos guardados")
                return HttpResponse(json.dumps(response), mimetype="application/json")
            try:
                private_templates.objects.get(id_template=_rel_user_private_templates.id_template, id_group=_group.id_group, id_user=request.user).delete()
                response = "True"
            except:
                response = _(u'La plantilla seleccionada no está asignada al grupo seleccionado')
                return HttpResponse(json.dumps(response), mimetype="application/json")
            # print id_template, id_group
        else:
            response = "No se recibio una peticion get"
    else:
        response = "No ser recibio una consulta Ajax"
    return HttpResponse(json.dumps(response), mimetype="application/json")
