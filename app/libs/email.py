from threading import Thread

from app import mail
from flask_mail import Message
from flask import current_app, render_template


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    msg = Message('[鱼书] ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()
