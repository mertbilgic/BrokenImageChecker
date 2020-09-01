from flask import Flask,url_for,jsonify,Blueprint
from settings import celery
import time,random

task_blueprint = Blueprint('task', __name__, template_folder='templates')

@task_blueprint.route('/taskrun', methods=['POST'])
def taskrun():
    return "Run Task Demo"
