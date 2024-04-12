# app.py Import Flask and render_template
from flask import Flask, render_template, request, redirect
from quiz_logic import generate_random_questions  # Importing function from quiz_logic module
from data.questions import question_bank
from db_connection_utils import DbUtils

import psycopg2
from psycopg2 import OperationalError
import datetime


dbConnector = DbUtils("pgserver.mau.se", "futquiz", "aj2020", "zfdix2uu")

#Connection to PgAdmin database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            database="futquiz",
            host="pgserver.mau.se",
            user="aj2020",
            password="zfdix2uu",
            port="5432" 
        )
        return conn
    except OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

def isBlank(checked_str):
    if not checked_str or checked_str.strip() == "" or checked_str.strip() == "None":
        return True
    return False


# Create Flask app / # Create an instance of the Flask class
app = Flask(__name__)

# Define route for the homepage
@app.route('/', methods=['GET'])
def index():
    """Render the index page. (Render initial page with a form to start a new game.)"""
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/user_view', methods=['POST'])
def user_view():
    userId = request.form.get("userId")
    uname = None
    passwd = None

    '''
    This if statement is needed if the user is already logged in and it's redirected here from other page.
    In order to avoid requesting credentials again!!!
    Of course, that page should post the userId.
    '''
    if isBlank(userId):
        uname = request.form.get("uname")
        passwd = request.form.get("psw")
        try:
            results = dbConnector.executeSQL("SELECT password_hash FROM users WHERE email='%s'" % uname)
            if not results:
                return redirect("/")
            for row in results:
                c_pass = row[0]
                if c_pass != passwd:
                    return redirect("/")
        except Exception as e:
            print("ERROR: %s" % str(e))
            return redirect("/")
    else:
        uname = userId

    return render_template('quiz.html', user_name=uname, questions=generate_random_questions(3))


@app.route('/new_user_view', methods=['POST'])
def new_user_view():
    email = request.form.get("email")
    passwd = request.form.get("psw")
    re_passwd = request.form.get("psw-repeat")

    if isBlank(email) or isBlank(passwd) or isBlank(re_passwd) or passwd != re_passwd:
        render_template('index.html')
    try:
        dbConnector.executeSQL("INSERT INTO users (email,password_hash,created_at) VALUES ('%s','%s',CURRENT_TIMESTAMP)" % (email, passwd))
    except Exception:
        render_template('index.html')

    #return template("user_view", user_name=email)
    return render_template('quiz.html', user_name=email, questions=generate_random_questions(3))


# Define route for the quiz page
@app.route('/quiz')
def quiz():
    """Render the quiz page with random questions."""
    num_questions = 3  # Adjust the number of questions as needed
    if num_questions > len(question_bank):
        return "Error: Not enough questions available for the quiz."
    else:
        questions = generate_random_questions(num_questions)
        return render_template('quiz.html', questions=questions)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=False)
    
# Database connection and cursor setup