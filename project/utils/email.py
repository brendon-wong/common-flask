from flask import current_app
from flask_mail import Message
from threading import Thread

from project.extensions import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, html):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=recipients)
    msg.html = html
    Thread(target=send_async_email, args=(app, msg)).start()
