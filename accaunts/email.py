from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_review_email(username,first_name,email,password,password2):
    context= {
        'username':username,
        'first_name':first_name,
        'email':email,
        'password':password,
        'password2':password2
    }
    email_subject='Rahmat ro\'yxatdan o\'tganingiz uchun'
    email_body=render_to_string('email_message.txt',context)

    email=EmailMessage(
        email_subject,email_body,
        settings.DEFAULT_FROM_EMAIl, [email,],
    )
    return email.send(fail_silently=False)