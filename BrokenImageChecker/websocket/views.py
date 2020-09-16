from flask import Flask,render_template,url_for,jsonify,Blueprint,request
from settings import app,socketio
from flask_socketio import SocketIO,emit,disconnect
import uuid

websocket_blueprint = Blueprint('websocket', __name__, template_folder='templates')


@socketio.on('connect', namespace='/events')
def events_connect():
    pass