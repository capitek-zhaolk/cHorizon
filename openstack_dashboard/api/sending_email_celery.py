'''
在发送邮件的时候可以先把"已经发送激活邮件到邮箱"返回给用户，
同时把邮件发送任务提交到异步处理线程中

专门用来处理异步的框架  --  celery

celery用redis做消息通信
'''

from celery import Celery



