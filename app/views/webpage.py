from flask import request, redirect, url_for, render_template, flash, session
from flask import Blueprint
# from flask_line_api import line

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from app.models.users import User
from app import db

webpage = Blueprint('webpage', __name__)

@webpage.route('/')
def display_top_page():
    return render_template('top.html')

@webpage.app_errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('webpage.login'))


# TODO: signUP画面の更新!
@webpage.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            flash('Email address already exists!!')
            return redirect(url_for('webpage.signup'))
        new_user = User(user_id=user_id, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('正常に登録できました。ログインしてください！')
        return redirect(url_for('webpage.login'))

    else:
        return render_template('signup.html')


@webpage.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False 

        user = User.query.filter_by(user_id=user_id).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again!!')
            return redirect(url_for('webpage.login'))
        
        login_user(user, remember=remember)
        flash('ログインしました！')
        return redirect(url_for('webpage.display_top_page'))
    
    # GETメソッドの場合
    else:
        return render_template('login.html')

@webpage.route('/mail', methods=['GET', 'POST'])
def send_message_to_change_password():
    pass
    # form = AddressForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     # TODO: 現存するuser_idか確認
    #     token = _create_token(form.userid.data, app.secret_key,  salt='shio')
    #     url = url_for('view.new_pwd', token=token, _external=True)

    #     line.send_url_for_change_password(form.userid.data, url)
    #     flash(f'入力されたLINEユーザーにパスワード変更用URLを送信しました')

    # # ページ表示
    # return render_template('mail.html', form=form)

@webpage.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for('webpage.display_top_page'))

@webpage.route('/userlist')
@login_required
def display_user_list():
    user_list = User.query.all()
    return render_template('userlist.html', user_list=user_list)

@webpage.route('/profile')
@login_required 
def display_my_profile():
    return render_template('profile.html')

@webpage.route('/linebot')
def display_linebot_info():
    return render_template('linebot.html')
