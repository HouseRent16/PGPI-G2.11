from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage

def send_mail(subject, body, receivers, template="mailer/email.html", context=None, attachments=None):
    if context is None:
        context = {}
    context['body'] = body
    mail = EmailMessage(
        subject,
        render_to_string(template, context),
        settings.EMAIL_HOST_USER,
        receivers,
    )
    mail.content_subtype = "html"

    with open("static/assets/Logo_S_T.png", 'rb') as f:
        attached_image = MIMEImage(f.read())
        attached_image.add_header('Content-ID', '<attached_image>')
        mail.attach(attached_image)

    if attachments:
        for attachment in attachments:
            with open(attachment['file'], 'rb') as file:
                mail.attach(attachment['name'], file.read(), attachment['type'])

    mail.send()