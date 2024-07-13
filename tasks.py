from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_email_task(recipient_email):
    from flask import Flask
    from flask_mail import Mail, Message

    app = Flask(_name_)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'jotham577@gmail.com'
    app.config['MAIL_PASSWORD'] = 'Jotham577@'

    mail = Mail(app)

    msg = Message('Hello from Flask-Mail', sender='jotham577@gmail.com', recipients=[recipient_email])
    msg.body = 'This is a test email sent from a background Celery task.'
    with app.app_context():
        mail.send(msg)
