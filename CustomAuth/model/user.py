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

TOKEN_REFRESH_PERIOD=settings.TOKEN_REFRESH_PERIOD




class User(AbstractBaseUser, PermissionsMixin):
    BUSINESS_USER = 0;
    NORMAL_USER = 1;
    USER_TYPES = ((BUSINESS_USER, "Business User"), (NORMAL_USER, "Normal User"))
    MALE = 1;
    FEMALE = 0;
    GENDER = ((MALE, "Male"), (FEMALE, "Female"))

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(_('email address'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_email_verified = models.BooleanField(default=False)
    gender = models.BooleanField(choices=GENDER, default=None)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    passcode = models.CharField(max_length=100, default=-1)
    last_fail = models.DateTimeField(default=None, null=True)
    passcode_retries = models.IntegerField(default=0)



    def get_gender_choice(self):
        if self.gender:
            return 1
        else:
            return 0
    @property
    def phone(self):
        if "CMP_" in self.username:
            return self.username[4:]
        else:
            return self.username

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @staticmethod
    def getBusinessUser(username):
        return User.objects.get(username="CMP_" + username)

    @staticmethod
    def getNormalUser(username):
        return User.objects.get(username=username)

    @staticmethod
    def authenticateBusinessUser(username,**kwargs):
        return authenticate(username="CMP_"+username,**kwargs)

    def checkPasscode(self, passcode):
        # if last failure happened before 60 minutes

        if (self.last_fail is not None):
            failed_since = timezone.now() - self.last_fail
            failed_since = failed_since.total_seconds() / 60
        else:
            failed_since = 400

        if failed_since < 60 and self.passcode_retries > 5:
            return False, "You have crossed maximum retries, Try again later!"
        else:
            # user has valid attempts left
            if check_password(passcode, self.passcode):
                # valid passcode found
                print("encoded password found")
                return True, "Valid Passcode"
            elif passcode == self.passcode:
                print("unencoded password found")
                # if user is invoking this method then user has updated the app
                # hence we are explicity migrating the passcode to a hash
                # todo this condition should be removed post some time
                self.setPasscode(self.passcode)

                return True, "Valid Passcode"
            else:
                # invalid passcode found
                if failed_since < 60:
                    if self.passcode_retries == 4:
                        self.passcode_retries = 5
                        self.save()
                        return False, "You have crossed max retry limit. Try again after 1 hour."
                    else:
                        self.passcode_retries = self.passcode_retries + 1
                        self.save()
                        return False, "Invalid Passcode!"
                else:
                    self.last_fail = timezone.now()
                    self.passcode_retries = 1
                    self.save()
                    return False, "Invalid Passcode!"

    def setPasscode(self, passcode):
        if len(passcode) == 4:
            hashed_password = make_password(passcode)
            self.passcode = hashed_password
            self.save()

    @staticmethod
    def isPartialUser(username=None,user=None):
        if user :
            return True if user.check_password("") else False
        if username:
            return True if authenticate(username=username,password="") else False
        return False

    @staticmethod
    def register(username,password,email,first_name,last_name,device_id=None,device_name=None):
        user=authenticate(username=username,password='')# WILL AUTHENTICATE FOR PARTIAL USER
        if user : # PARTIAL USER EXISTS, ADD ADDITIONAL DATA TO USER
            user.set_password(password)
            user.email,user.first_name,user.last_name=email,first_name,last_name
            user.save()
            return user
        else: #PARTIAL USER DOES NOT EXIST
            try:
                user=User(username=username,email=email,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.save()
                return user
            except:
                return None #EXCEPTION CAUSED DUE TO EXISTING USER WHO IS NOT PARTIAL






