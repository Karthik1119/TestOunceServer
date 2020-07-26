import rest_framework.authentication
from django.utils.functional import lazy

from .models import Token
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

class TokenAuthentication(rest_framework.authentication.TokenAuthentication):
    model = Token

    # def authenticate_credentials(self, key):
    #     model = self.get_model()
    #     try:
    #         token = model.objects.select_related('user').prefetch_related("user__ounceUser").get(key=key)
    #         print(token.expires_on)
    #     except model.DoesNotExist:
    #         raise exceptions.AuthenticationFailed(_('Invalid token.'))
    #
    #     if not token.user.is_active:
    #         raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
    #
    #     return (token.user, token)