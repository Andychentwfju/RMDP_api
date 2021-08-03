from __future__ import absolute_import, unicode_literals
from celery import task

from django.core.mail import send_mail

from django.conf import settings


@task
def send_email(recipient_email, recipient_name):
    try:
        subject = 'Test sending email'
        message = 'hello {}'.format(recipient_name)
        mail_sent = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # 寄件人的信箱
            [recipient_email]  # 收件人的信箱
        )
        print(mail_sent)
        return mail_sent
    except ValueError:
        print(ValueError)


