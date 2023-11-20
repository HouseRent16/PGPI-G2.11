from django.test import TestCase
from django.core import mail
from utils.mailer import send_mail

class MailerTestCase(TestCase):

    def test_enviar_correo(self):
        # Ejecuta la función que envía el correo
        send_mail('destinatario@example.com', 'Asunto de prueba', 'Este es un mensaje de prueba.')

        # Verifica que un correo se haya enviado
        self.assertEqual(len(mail.outbox), 1)

        # Verifica el contenido del correo
        self.assertEqual(mail.outbox[0].subject, 'Asunto de prueba')
        self.assertEqual(mail.outbox[0].body, 'Este es un mensaje de prueba.')
        self.assertEqual(mail.outbox[0].to, ['destinatario@example.com'])