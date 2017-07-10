# -*- coding:utf-8 -*-  
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import logging
import zlib
import base64

from django.conf import settings
from django import shortcuts
import django.views.decorators.vary

import horizon
from horizon import base
from horizon import exceptions
from horizon import notifications

from utils.sendmail import send_email_on_user_register_request
from utils.sendmail import send_email_on_user_register_result

LOG = logging.getLogger(__name__)

MESSAGES_PATH = getattr(settings, 'MESSAGES_PATH', None)

AUTHORIZATION_EMAIL_DOMAIN = getattr(settings, 'AUTHORIZATION_EMAIL_DOMAIN', None)


def get_user_home(user):
    try:
        token = user.token
    except AttributeError:
        raise exceptions.NotAuthenticated()
    # Domain Admin, Project Admin will default to identity
    if token.project.get('id') is None or user.is_superuser:
        try:
            dashboard = horizon.get_dashboard('identity')
        except base.NotRegistered:
            pass
    else:
        dashboard = horizon.get_default_dashboard()

    return dashboard.get_absolute_url()

def index(request):
    return shortcuts.render(request, 'index.html')

def register(request):
    if request.method == 'POST':
       register_email = request.POST.get('register-email')
       register_name = register_email.split('@')[0]
       register_domain = register_email.split('@')[1]

       LOG.info("Register: %s, %s, %s" % (register_email, register_name, register_domain))

       if register_domain in AUTHORIZATION_EMAIL_DOMAIN.keys():
           send_email_on_user_register_request(register_email)
           return shortcuts.redirect('/register/notification/')
       else:
           return shortcuts.render(request, 'user/register/register.html', {'error_message': 'invalid-email-address'})
    else:
       return shortcuts.render(request, 'user/register/register.html')

def register_notification(request):
    return shortcuts.render(request, 'user/register/register_msg.html')

def register_verification(request, code='0'):
    if request.method == 'GET':
        LOG.info("register_verification: GET")
        register_email = None
        try:
            register_email = zlib.decompress(base64.b16decode(code.upper()))
            LOG.info("Email: %s", register_email)
        except:
            LOG.info("Email: decompress/decode failure")
            return shortcuts.render(request, 'user/register/register_verify.html', {'error_message': 'invalid-verification-code'})

        if (register_email):
            register_name = register_email.split('@')[0]
            register_domain = register_email.split('@')[1]
            register_projectprefix = AUTHORIZATION_EMAIL_DOMAIN[register_domain]

            return shortcuts.render(request, 'user/register/register_verify.html', {'register_name':register_name, 'register_email':register_email})
        else:
            return shortcuts.render(request, 'user/register/register_verify.html', {'error_message': 'invalid-verification-code'})
        pass

    if request.method == 'POST':
        LOG.info("register_verification: POST")
        register_email = request.POST.get("register-email")
        register_name = request.POST.get("register-name")
        register_password = request.POST.get("register-password")

        register_domain = register_email.split('@')[1]
        register_projectprefix = AUTHORIZATION_EMAIL_DOMAIN[register_domain]
        
        LOG.info("Register: %s, %s, %s, %s, %s" % (register_email, register_name, register_password, register_domain, register_projectprefix))

        nret = os.system("/opt/user_create.sh %s %s %s %s" % (register_name, register_password, register_projectprefix, register_domain))
        LOG.info("Result: %d" % (nret))
        # TODO: CALL API

        send_email_on_user_register_result(register_email)

        return shortcuts.render(request, 'user/register/register_result.html', {'register_name':register_name})
        pass

    return shortcuts.redirect('/register/')

@django.views.decorators.vary.vary_on_cookie
def splash(request):
    if not request.user.is_authenticated():
        # raise exceptions.NotAuthenticated()
        LOG.info("User Not Authenticated: %s", request.user)
        return index(request)
    else:
        LOG.info("User Has Authenticated: %s", request.user)

    response = shortcuts.redirect(horizon.get_user_home(request.user))
    if 'logout_reason' in request.COOKIES:
        response.delete_cookie('logout_reason')
    # Display Message of the Day message from the message files
    # located in MESSAGES_PATH
    if MESSAGES_PATH:
        notifications.process_message_notification(request, MESSAGES_PATH)
    return response
