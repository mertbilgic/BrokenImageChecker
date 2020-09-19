import uuid
import json

from flask import Flask,jsonify,Blueprint,request
from flask_socketio import SocketIO,emit,disconnect
from bson import json_util

from settings import app,socketio
from helpers.mongo_helper import broken_img,crawl_links

websocket_blueprint = Blueprint('websocket', __name__, template_folder='templates')

@websocket_blueprint.route('/clients', methods=['GET'])
def clients():
    return jsonify({'clients': app.clients.keys()})

@websocket_blueprint.route('/event', methods=['POST'])
def event():
    room = request.json['room']
    g_id = request.json['g_id']
    response = json.dumps(list(crawl_links.find({"group_id" : g_id})),default=json_util.default)
    socketio.emit('crawlerstatus',{'response':response},namespace='/events',room=room)
    return 'ok'

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