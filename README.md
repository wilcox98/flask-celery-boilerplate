# Flask Celery Biolerplate
This a minimal flask application with celery and mysql database

## Setting Up

Create virtual environment
```bash
$ python -m env
```
Activate the environment 
```bash
$ source env/bin/activate
```
Install the require packages 
```bash
$ pip install -r requirements.txt
```

Start the API service
```bash
$ cd backend/backend
$ flask run --debug
```
The API will be running on http://127.0.0.1:5000
#
Setup celery worker and beat
```bash
$ celery -A manage beat --schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid
$ celery -A manage worker --loglevel INFO
```