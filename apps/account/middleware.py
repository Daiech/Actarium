from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import AuthCanceled, NotAllowedToDisconnect
from django.shortcuts import redirect
from social.exceptions import SocialAuthBaseException

class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        strategy = getattr(request, 'social_strategy', None)
        if strategy is None or self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            backend_name = strategy.backend.name
            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)
            if type(exception) == AuthCanceled:
                return HttpResponseRedirect(reverse("personal_data") + "?msg=%s" % ('AuthCanceled'))
            elif type(exception) == NotAllowedToDisconnect:
                return HttpResponseRedirect(reverse("personal_data") + "?msg=%s" % ('NotAllowedToDisconnect'))
            else:
                pass
            try:
                messages.error(request, message,
                               extra_tags='social-auth ' + backend_name)
            except MessageFailure:
                url += ('?' in url and '&' or '?') + \
                       'message={0}&backend={1}'.format(urlquote(message),
                                                        backend_name)
            return redirect(url)
        else:
        	print "NO ES INSTANCIA DE SOCIAL AUTH EXCEPCION"
