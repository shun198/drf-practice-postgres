from django.core import mail
from django.template.loader import render_to_string

import schedule
from time import sleep
from datetime import datetime, date


def send_welcome_email(email):
    plaintext = render_to_string("../templates/welcome_email.txt")
    html_text = render_to_string("../templates/welcome_email.html")

    mail.send_mail(
        subject="ようこそ",
        message=plaintext,
        from_email="example@mail.com",
        recipient_list=[email],
        html_message=html_text,
    )


def send_refusal_email(email):
    plaintext = render_to_string("../templates/refusal_email.txt")
    html_text = render_to_string("../templates/refusal_email.html")

    mail.send_mail(
        subject="ようこそ",
        message=plaintext,
        from_email="example@mail.com",
        recipient_list=[email],
        html_message=html_text,
    )


def send_refusal_email_per_hour():
    print("タスク実行中")


schedule.every(1).hours.do(send_refusal_email_per_hour)


# 03 イベント実行
while True:
    schedule.run_pending()
    sleep(1)
