import json
from copy import deepcopy
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import rest_framework.authtoken.models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
import re

# from home.Notify.Basic import PushNotification
from CustomAuth.Manager import UserManager
from django.core.mail import send_mail
from CustomAuth.permission import UserPermission
from .device import Device
from django.conf import settings

TOKEN_REFRESH_PERIOD=settings.TOKEN_REFRESH_PERIOD

@python_2_unicode_compatible
class Token(rest_framework.authtoken.models.Token):

    # key is no longer primary key, but still indexed and unique
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True, primary_key=True)
    # relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    notification_id = models.CharField(max_length=300, default=None, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, default=None)
    expires_on = models.DateTimeField(null=True, default=timezone.now()+timedelta(days=TOKEN_REFRESH_PERIOD), blank=True)
    permissions = models.CharField(max_length=800,default="{}")


    @property
    def permission(self):
        return json.loads(self.permissions)

    @staticmethod
    def refreshToken(old_token, notification_id=None, additional_days=TOKEN_REFRESH_PERIOD):
        new_token = deepcopy(old_token)
        new_token.key = None
        old_token.delete()
        if notification_id:
            print("storing refreshed notification tokeen",notification_id)
            new_token.notification_id = notification_id
        new_token.expires_on = timezone.now() + timedelta(days=additional_days)
        return new_token

    @staticmethod
    def repermitAllTokens(user):
        permissions=UserPermission(user)
        Token.objects.filter(user=user).update(permissions=str(permissions))

    @staticmethod
    def authenticateForToken(username, password,device_id=None, device_name=None,notification_id=None):
        '''
            THIS FUNCTION GENERATES TOKEN FOR BUSINESS AND NORMAL USERS
            IT CANNOT BE USED TO GENERATE PARTIAL TOKENS AS EMPTY PASSWORDS WILL BE RETURNED AS INVALID
        '''
        device = None
        user=User.objects.get(username=username)
        if not user.check_password(password):
            return (False, "Credentials do not match")
        user.last_login = timezone.now()
        user.save()
        if device_id and device_name:
            device,created = Device.objects.get_or_create(name=device_name,device_id=device_id)
        else:
            device=None

        token, created = Token.objects.get_or_create(user=user, device=device, type=type)
        """
            if token exists:
                delete the token, create a new token with expirity date post 4 days
            if token does not exist and got created freshly:
                add expirity date post 4 days to the token  and save it
        """
        if not created:  # if old token recieved
            token= Token.refreshToken(token, notification_id=notification_id)
        else:
            token.expires_on=timezone.now()+timedelta(days=TOKEN_REFRESH_PERIOD)
        from .permission import UserPermission
        permissions=UserPermission(user)
        token.permissions=str(permissions)

        if notification_id:
            print("manually adding token", notification_id)
            token.notification_id = notification_id
        token.save()
        return (token,"success")
