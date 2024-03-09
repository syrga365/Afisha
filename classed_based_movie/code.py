from django.contrib.auth.models import User
from django.core.mail import send_mail
import random


def send_email_confirm(email):
    subject = 'Подтверждение регистрации'
    code = random.randint(100000, 999999)
    message = f'ваш код {code}'
    email_from = 'kundolukkg5@gmail.com'
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.code = code
    user_obj.save()
