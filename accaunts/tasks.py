# from django.core.mail import send_mail
# # from celery.decorators import task
# from celery.utils.log import get_task_logger
#
# from news_project.settings import DEFAULT_FROM_EMAIL
# from .email import send_review_email
# from   news_project.celery import app
# logger=get_task_logger((__name__))
#
#
# # @app.task()
# # def send_email(subject,message,recipient_list):
# #     send_mail(
# #         subject,
# #         message,
# #         'nodirbekhakimjonovsvm@gmail.com',
# #         recipient_list
# #     )
# @app.task(name='send_review_email_task)')
#
# def send_review_email_task(username,fist_name,email,password,password2):
#     logger.info('Sent email Tasks')
#     return send_review_email(username,fist_name,email,password,password2)
#
#
# from celery import shared_task
# from django.core.mail import send_mail
#
#
# @shared_task
# def send_email(subject, message, recipient_list):
#     """
#     Celery task to send an email asynchronously.
#
#     Args:
#         subject (str): The subject of the email.
#         message (str): The message content of the email.
#         recipient_list (list): A list of recipient email addresses.
#     """
#     try:
#         # Send email using Django's send_mail function
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=DEFAULT_FROM_EMAIL,  # Use default sender specified in settings.py
#             recipient_list=recipient_list,
#             fail_silently=False,  # Raise an exception if sending fails
#         )
#         return True  # Return True if email sent successfully
#     except Exception as e:
#         # Log or handle any exceptions that occur during email sending
#         return False  # Return False if email sending fails
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task
def send_email(subject, message, recipient_list):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info('Email sent successfully.')
        return True
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        return False
logger = get_task_logger(__name__)

from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger
from django.template.loader import render_to_string


@shared_task
def send_review_email_task(username, first_name, email, password, password2):
    try:
        # Construct the email subject
        subject = 'Account Registration Confirmation'

        # Construct the email body using a template
        context = {
            'username': username,
            'first_name': first_name,
            'email': email,
            'password': password,
            'password2': password2
        }
        email_body = render_to_string('email_message.txt', context)

        # Create an EmailMessage object and send the email
        email_message = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.send()

        logger.info('Review email sent successfully.')
        return True
    except Exception as e:
        logger.error(f'Error sending review email: {e}')
        return False