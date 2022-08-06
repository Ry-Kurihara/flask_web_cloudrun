import os 
import sys
import json

# sys.path.append(os.path.join(os.path.dirname(__file__), '../my_lib'))
# import param_store as ps

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app import getconn

# モデルの変更を追跡する機能。メモリを少し圧迫するためFalseにしている。
SQLALCHEMY_TRACK_MODIFICATIONS = False
GOOGLE_APPLICATION_CREDENTIALS  = "シェルの環境変数でしか指定できないようだ"


SQLALCHEMY_DATABASE_URI = "postgresql+pg8000://"
SQLALCHEMY_ENGINE_OPTIONS = {
    'creator': getconn
}

DEBUG = True
# TODO paramストアから取ってくる
SECRET_KEY = 'secret key'
SALT = 'shio'

# flask-apscheduler
# SCHEDULER_API_ENABLED = True
# SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(engine=engine, tablename='line_ps5_jobstore')}