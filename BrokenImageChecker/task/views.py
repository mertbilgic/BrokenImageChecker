from flask import Flask,render_template,url_for,jsonify,Blueprint,request
from settings import app
from celery import Celery
import time,random
from crawler.img_spider import BrokenImageChecker
from billiard import Pool
import uuid


task_blueprint = Blueprint('task', __name__, template_folder='templates')

celery = Celery('tasks', backend='redis://localhost', broker='amqp://localhost')
celery.conf.update(app.config)

@celery.task(bind=True,name='crawl_task')
def crawl_task(self,url):
    guid = str(uuid.uuid4())
    BrokenImageChecker.work(url)
    return 'Task completed!'

@task_blueprint.route('/taskrun', methods=['POST'])
def taskrun():
    url = request.form.get("url",'')
    task = crawl_task.apply_async(args=[url])
    return jsonify({}), 202, {'Location': url_for('task.taskstatus',
                                                  task_id=task.id)}
@task_blueprint.route('/status/<task_id>')
def taskstatus(task_id):
    task = crawl_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)