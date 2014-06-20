from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from social.exceptions import AuthAlreadyAssociated
from django.http import HttpResponseRedirect


def send_validation(strategy, code):
    url = reverse('social:complete', args=(strategy.backend_name,)) + \
            '?verification_code=' + code.code
    send_mail('Validate your account',
              'Validate your account {0}'.format(url),
              settings.EMAIL_FROM,
              [code.email],
              fail_silently=False)

from social.exceptions import InvalidEmail
from social.pipeline.partial import partial


@partial
def mail_unique(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user is None or is_new and details.get('email'):
        data = strategy.request_data()
        from .validators import is_email_unique
        if not is_email_unique(details['email']):
            details['email'] = ""


def social_user(strategy, uid, user=None, *args, **kwargs):
    provider = strategy.backend.name
    social = strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            """the account has in use. Other user have it"""
            return HttpResponseRedirect(reverse("personal_data") + "?backend=" + format(provider) + "&msg=account-in-use")
            # msg = 'This {0} account is already in use.'.format(provider)
            # raise AuthAlreadyAssociated(strategy.backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}
