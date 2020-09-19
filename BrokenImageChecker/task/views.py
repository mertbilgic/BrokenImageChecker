import uuid
from requests import post

from flask import url_for,jsonify,Blueprint,request
from celery import Celery

from settings import app
from crawler.img_spider import BrokenImageChecker

task_blueprint = Blueprint('task', __name__, template_folder='templates')

celery = Celery('tasks', backend='redis://localhost', broker='amqp://localhost')
celery.conf.update(app.config)

@celery.task(bind=True,name='crawl_task')
def crawl_task(self,url,room,event_url):
    g_id = str(uuid.uuid4())
    BrokenImageChecker.work(url,g_id)
    meta = {'g_id': g_id, 'room': room}
    print(f"url:{url}")
    post(event_url, json=meta)
    return 'Task completed!'

@task_blueprint.route('/taskrun', methods=['POST'])
def taskrun():
    url = request.form.get("url",'')
    room = request.form.get("room",'')
    event_url = url_for('websocket.event', _external=True)
    crawl_task.apply_async(args=[url,room,event_url])
    return jsonify({}), 202, {'Location': event_url}