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

import logging

from django.core.mail import send_mail
from django.conf import settings
from django import shortcuts
import django.views.decorators.vary

import horizon
from horizon import base
from horizon import exceptions
from horizon import notifications

LOG = logging.getLogger(__name__)

MESSAGES_PATH = getattr(settings, 'MESSAGES_PATH', None)


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
    return shortcuts.render(request, 'horizon/index.html')

def register(request):
    if request.method == 'POST':
       register_email = request.POST.get('register-email')
       register_password = request.POST.get('register-password')
       LOG.info("User Register Info: email=%s, password=%s" % (register_email, register_password))

       if '@capitek.com.cn' in register_email:
           send_mail(
              'Capitek Cloud: Welcome to Cloud Platform',
              'Email: %s\nPassword: %s\n' % (register_email, register_password),
              'cloud@capitek.com.cn',
              [register_email, 'linfeng@capitek.com.cn'],
              fail_silently=False,
           )
           return shortcuts.render(request, 'horizon/register_msg.html')
       else:
           return shortcuts.render(request, 'horizon/register.html')
    else:
       return shortcuts.render(request, 'horizon/register.html')

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
