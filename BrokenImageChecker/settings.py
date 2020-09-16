from flask import Flask
from celery import Celery
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost'

app.clients = {}
socketio = SocketIO(app)