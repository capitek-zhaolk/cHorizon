# -*- coding:utf-8 -*-  

import threading
import logging
import time
import zlib
import base64

from django.core.mail import send_mail
from django.conf import settings

LOG = logging.getLogger(__name__)

CLOUD_NAME = getattr(settings, 'CLOUD_NAME', None)

HORIZON_HOST = getattr(settings, 'HORIZON_HOST', None)

EMAIL_HOST_USER = getattr(settings, 'EMAIL_HOST_USER', None)

CLOUD_ADMINISTRATOR_EMAIL = getattr(settings, 'CLOUD_ADMINISTRATOR_EMAIL', None)


class SendHtmlEmail(threading.Thread):
    def __init__(self, subject, recipient_list, html_message):
        LOG.info("SendHtmlEmail init")

        self.subject = subject
        self.message = html_message
        self.from_email = EMAIL_HOST_USER
        self.recipient_list = {recipient_list,} | CLOUD_ADMINISTRATOR_EMAIL
        self.html_message = html_message

        threading.Thread.__init__(self)

    def run(self):
        LOG.info("Sending Html Email ... - %s" % time.ctime())

        try:
            for email_to in self.recipient_list:
                send_mail(
                    self.subject,
                    self.message,
                    self.from_email,
                    [email_to],
                    fail_silently=False,
                    html_message=self.html_message
                )
        except Exception as e:
             LOG.info("Failure: %s" % (e.message))
        except:
            LOG.warning("Sending email failure!")

        LOG.info("Sending Html Email Finish. - %s" % time.ctime())

    def __del__(self):
        LOG.info("SendHtmlEmail del")


def send_email_by_html():
    pass


def send_email_on_user_register_request(register_email):
    register_code = base64.b16encode(zlib.compress(register_email))
    register_link = "http://" + HORIZON_HOST + "/register/verification/" + register_code.lower()

    mail_to = register_email
    mail_subject = '%s: Welcome to Cloud Platform' % (CLOUD_NAME)
    mail_html_msg  = u'<b>点击此链接注册:</b><p/>%s' % (register_link)

    sending = SendHtmlEmail(mail_subject, mail_to, mail_html_msg)
    sending.start()

def send_email_on_user_register_result(register_email):
    mail_to = register_email
    mail_subject = '%s: Welcome to Cloud Platform' % (CLOUD_NAME)
    mail_html_msg  = u'<b>用户注册完成</b>'

    sending = SendHtmlEmail(mail_subject, mail_to, mail_html_msg)
    sending.start()
