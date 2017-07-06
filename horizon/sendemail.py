from __future__ import absolute_import

import os
import collections
import logging
import string
import random

from django.core.mail import send_mail

# add Codes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.conf import settings
from django.utils.functional import cached_property  # noqa
from django.utils.translation import ugettext_lazy as _
import six

from novaclient import api_versions
from novaclient import client as nova_client
from novaclient import exceptions as nova_exceptions
from novaclient.v2 import instance_action as nova_instance_action
from novaclient.v2 import list_extensions as nova_list_extensions
from novaclient.v2 import security_group_rules as nova_rules
from novaclient.v2 import servers as nova_servers

from horizon import conf
from horizon import exceptions as horizon_exceptions
from horizon.utils import functions as utils
from horizon.utils.memoized import memoized  # noqa
from horizon.utils.memoized import memoized_with_request  # noqa

from openstack_dashboard.api import base
from openstack_dashboard.api import keystone
from openstack_dashboard.api import network_base
from openstack_dashboard.contrib.developer.profiler import api as profiler
import threading

class SendHtmlEmail(threading.Thread):
    def __int__(self, mail_subject, html_content, mail_from, to_list, fail_silently = False):
        self.mail_subject = mail_subject
        self.html_content = html_content
        self.mail_from = mail_from
        self.to_list = to_list
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        #for mail_to in self.mail_to_list:
        html_content = loader.render_to_string(email_template_name_html, context)
        msg = EmailMessage(self.mail_subject, self.html_content, self.mail_from, self.to_list)
        msg.content_subtype = "html"
        msg.send(self.fail_silently)

def send_email_by_template(subject, module, data, mail_from, to_list):
    '''
        subject: string, 主题
        module:  string, 模版名称
        data:    dict,   数据
        to_list: list,   收件人
    '''
    html_content = loader.render_to_string(module, data)
    send_from = mail_from
    send_email = SendHtmlEmail(subject, html_content, send_from, to_list)
    send_email.start()















