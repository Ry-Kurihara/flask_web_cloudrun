from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_apscheduler import APScheduler
from flask_login import LoginManager

from google.cloud.sql.connector import Connector 
from sqlalchemy import create_engine

db = SQLAlchemy()
# scheduler = APScheduler()

# バックグラウンド処理タスク
# from rq import Queue
# from worker import conn 
# q = Queue(connection=conn)

# Google Cloud SQL Connector 
# initialize Connector object 
connector = Connector()

# function to return the database connection
def getconn():
    conn = connector.connect(
        "selen-autopurchase:asia-northeast1:autopurchaser-ins",
        "pg8000",
        user="postgres",
        password="purchase7",
        db="autopurchaser_db"
    )
    return conn

engine = create_engine(
    "postgresql+pg8000://",
    creator=getconn
)

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('app.config')
    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'webpage.login'
    login_manager.init_app(app)

    from app.models.users import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Add Blueprint
    from app.views.webpage import webpage
    app.register_blueprint(webpage, url_prefix='/')

    # initialize scheduler 
    # scheduler.init_app(app)
    # scheduler.start()

    return app 