from flask_login import UserMixin
from app import db

# TODO: db.Modelから定義する
class User(UserMixin, db.Model):
    __tablename__ = 'user_auth'
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Text, unique=True, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, user_id=None, username=None, password=None):
        self.user_id = user_id 
        self.username = username 
        self.password = password

    def get_id(self):
        return (self.user_id)
