# BrokenImageChecker

**Dependencies:** Python 3.8.0, Pip, Virtualenv, Npm, Rabbitmq, MongoDB

### Create virtual environment 

```sh
git clone https://github.com/mertbilgic/BrokenImageChecker
cd BrokenImageChecker
virtualenv venv
```

### Install depedencies

```sh
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Install Styles and Scripts

```sh
cd static
$ npm install
```
### Start

```sh
$ python run.py 
$ celery worker -A task.views.celery --logleve=info
```
