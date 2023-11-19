from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_mail(subject, body, receivers, template="mail.html", context=None, attachments=None):
    if context is None:
        context = {}
    context['image_path'] = 'media/assets/Logo_S_T.png'
    mail = EmailMessage(
        subject,
        render_to_string(template, context),
        settings.EMAIL_HOST_USER,
        receivers,
    )
    mail.content_subtype = "html"

    if attachments:
        for attachment in attachments:
            with open(attachment['file'], 'rb') as file:
                mail.attach(attachment['nombre'], file.read(), attachment['tipo'])

    mail.send()