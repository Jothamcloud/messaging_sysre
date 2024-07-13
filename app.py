import os
import time
from flask import Flask, request
from dotenv import load_dotenv
from celery import Celery
from flask_mail import Mail, Message

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask-Mail configuration for Gmail using SSL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Gmail SMTP SSL port
app.config['MAIL_USE_SSL'] = True  # Enable SSL encryption
app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')

# Celery configuration
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')

# Initialize Flask-Mail and Celery
mail = Mail(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    celery.autodiscover_tasks(['app'])  # Ensure the app module is discovered
    return celery

celery = make_celery(app)

@celery.task(name='app.send_email')  # Register the task with a specific name
def send_email(to):
    msg = Message("Test Email", sender=os.getenv('GMAIL_USER'), recipients=[to])
    msg.body = "This is a test email."

    try:
        with app.app_context():
            mail.send(msg)
        print(f"Sent email to {to}")
    except Exception as e:
        print(f"Error sending email: {e}")

    return True  # Optionally, return a value indicating success

@app.route("/")
def home():
    return "Welcome to the Messaging System!"

@app.route("/sendmail")
def sendmail():
    to = request.args.get('sendmail')
    if to:
        send_email.delay(to)
        return f'Sending email to {to}...'
    else:
        return 'Error: Missing "sendmail" parameter.'

@app.route("/talktome")
def talktome():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log_message = f'Logged at {current_time}\n'
    log_file = 'logs/messaging_system.log'  # Ensure it writes to a location with write permissions
    with open(log_file, 'a') as f:
        f.write(log_message)
    return 'Logging message...'

if __name__ == "__main__":
    app.run(debug=True)
