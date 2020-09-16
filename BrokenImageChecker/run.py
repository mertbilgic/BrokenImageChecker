from flask import Flask,render_template
from settings import app,socketio

#Blueprints
from task.views import task_blueprint
from websocket.views import websocket_blueprint

app.register_blueprint(task_blueprint)
app.register_blueprint(websocket_blueprint)

@app.route('/')
def index():
    return render_template('index.html')


if __name__=="__main__":
    socketio.run(app, debug=True)