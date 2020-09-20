import uuid

from flask import Flask,jsonify,Blueprint,request,Response
from flask_socketio import SocketIO,emit,disconnect

from settings import app,socketio
from helpers.mongo_helper import broken_img,crawl_links

websocket_blueprint = Blueprint('websocket', __name__, template_folder='templates')

@websocket_blueprint.route('/clients', methods=['GET'])
def clients():
    return jsonify({'clients': app.clients.keys()})

@websocket_blueprint.route('/event', methods=['POST'])
def event():
    room = request.json['room']
    result = request.json['result']
    socketio.emit('crawlerstatus',{'result':result},namespace='/events',room=room)
    response = Response("",status=204)
    return response

@socketio.on('connect', namespace='/events')
def events_connect():
    room = request.sid
    emit('room', {'room': room})

@socketio.on('crawlerstatus', namespace='/events')
def crawler_status():
    print("crawlerstatus")

@socketio.on('disconnect', namespace='/events')
def disconnect():
    print('Client disconnected', request.sid)