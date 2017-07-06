# -*- coding:utf-8 -*-  

import threading
import logging
import time

LOG = logging.getLogger(__name__)

class SendHtmlEmail(threading.Thread):
    def __init__(self):
        LOG.info("SendHtmlEmail init")
        threading.Thread.__init__(self)

    def run(self):
        LOG.info("Sending Html Email ... - %s" % time.ctime())
        time.sleep(5)
        LOG.info("Sending Html Email OK. - %s" % time.ctime())
        pass

    def __del__(self):
        LOG.info("SendHtmlEmail del")
        pass

