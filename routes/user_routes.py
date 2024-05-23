from flask import Blueprint, render_template, request, redirect
from helpers import isBlank, is_valid_password

user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def show_users(dbConnector):
    try:
        users = dbConnector.fetchSQL("SELECT user_id, email FROM users")
        return render_template('users.html', users=users)
    except Exception as e:
        return str(e)

@user_bp.route('/new_user_view', methods=['POST'])
def new_user_view(dbConnector):
    email = request.form.get("email").lower()
    passwd = request.form.get("password")
    re_passwd = request.form.get("confirm-password")

    if isBlank(email) or isBlank(passwd) or isBlank(re_passwd) or passwd != re_passwd:
        return redirect('/signup/msg/passwordMissMatch')
    if not is_valid_password(passwd):
        return redirect('/signup/msg/wrongPassword')

    try:
        dbConnector.executeSQL("INSERT INTO users (email, password, score) VALUES (%s, %s, 0)", (email, passwd))
        return redirect('/login/msg/accountCreated')
    except Exception as e:
        print(str(e))
        return redirect('/signup/msg/cantCreateUser')
