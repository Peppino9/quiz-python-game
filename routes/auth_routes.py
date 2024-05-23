from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db_connection_utils import DbUtils
from helpers import isBlank

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/login/msg/<alert>')
def login(alert=""):
    alert_message = ""
    if not isBlank(alert):
        if alert == "wrongUserPass":
            alert_message = "Wrong user name or password!"
        elif alert == "passwordMissMatch":
            alert_message = "Wrong password or password mismatch!"
        elif alert == "loginError":
            alert_message = "Login error!"
    return render_template('login.html', alert_msg=alert_message)

@auth_bp.route('/signup')
@auth_bp.route('/signup/msg/<alert>')
def signup(alert=""):
    alert_message = ""
    if not isBlank(alert):
        if alert == "passwordMissMatch":
            alert_message = "Wrong password or password mismatch!"
        elif alert == "wrongPassword":
            alert_message = "Password must contain at least one digit and one capital letter."
        elif alert == "cantCreateUser":
            alert_message = "Can't create user! User may already exist."
    return render_template('signup.html', alert_msg=alert_message)
