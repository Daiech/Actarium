def gloval_vars_url(request):
    from website.views import getGlobalVar
    return {"URL_PRIVACY": getGlobalVar("URL_PRIVACY"), "URL_TERMS": getGlobalVar("URL_TERMS")}
