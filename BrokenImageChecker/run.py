from flask import Flask,render_template
from settings import app

#Blueprints
from task.views import task_blueprint

app.register_blueprint(task_blueprint)

@app.route('/')
def index():
    return render_template('index.html')
