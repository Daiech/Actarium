#encoding:utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson as json

from groups.views import getGroupBySlug


def showGroup(request, slug_group):
    '''
        Carga el menú de un grupo 
    '''
    g = getGroupBySlug(slug_group)
    ctx = {
        "group": g
    }
    return render_to_response("groups/menu.html", ctx, context_instance=RequestContext(request))