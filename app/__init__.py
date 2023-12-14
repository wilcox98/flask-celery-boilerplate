from flask import Flask
from celery import Celery, Task
import celeryconfig
from app.exts.extensions import db
import os


def make_celery(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    # create context tasks in celery
    celery = Celery(app.import_name, broker=app.config["BROKER_URL"])

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)

    celery.Task = ContextTask
    celery.set_default()
    app.extensions["celery"] = celery
    return celery


def create_app() -> Flask:
    app = Flask(__name__)
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)
    app.config.from_object("config")
    app.config.from_prefixed_env()
    make_celery(app)

    @app.route("/")
    def view():
        return "Hello, Flask is up and running!"

    with app.app_context():
        db.create_all()
    return app
