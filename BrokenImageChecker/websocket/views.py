import json
import uuid

from flask import Flask,jsonify,Blueprint,request,Response
from flask_socketio import SocketIO,emit,disconnect
from bson import json_util

from settings import app,socketio
from helpers.mongo_helper import broken_img,crawl_links
from helpers.response_helper import create_response

websocket_blueprint = Blueprint('websocket', __name__, template_folder='templates')

@websocket_blueprint.route('/clients', methods=['GET'])
def clients():
    return jsonify({'clients': app.clients.keys()})

@websocket_blueprint.route('/event', methods=['POST'])
def event():
    room = request.json['room']
    g_id = request.json['g_id']
    result = json.dumps(list(broken_img.find({"group_id" : g_id})),default=json_util.default)
    response = create_response(result)
    socketio.emit('crawlerstatus',response,namespace='/events',room=room)
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