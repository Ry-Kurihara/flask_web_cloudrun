from flask import request, redirect, url_for, render_template, flash, session, abort, flash
from functools import wraps
from flask import Blueprint
from flask import current_app as app 

from werkzeug.security import generate_password_hash, check_password_hash
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../models/'))
from histories import User
from flask_login import login_user, logout_user, login_required
from flask_data import db 
from flask_data.models.histories import AddressForm

from itsdangerous.url_safe import URLSafeTimedSerializer
from flask_wtf import FlaskForm
from wtforms import validators, HiddenField, PasswordField

def _create_token(user_id, secret_key, salt):
    ''' user_idからtokenを生成
    '''
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(user_id, salt=salt)

def _load_token(token, secret_key, salt, max_age=600):
    ''' tokenからuser_idとtimeを取得
    '''
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.loads(token, salt=salt, max_age=max_age)

class NewPwdForm(FlaskForm):
    token = HiddenField('token', [
        validators.InputRequired()] )
    new_pwd1 = PasswordField('パスワード', [
        validators.InputRequired(),
        validators.EqualTo('new_pwd2')] )
    new_pwd2 = PasswordField('パスワード(確認用)', [
        validators.InputRequired()] )

