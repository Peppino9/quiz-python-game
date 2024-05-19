# app.py Import Flask and render_template
import random
import time
from flask import Flask, render_template, request, redirect, session, url_for
from data.questions import question_bank
from db_connection_utils import DbUtils

import psycopg2
from psycopg2 import OperationalError
import datetime

app = Flask(__name__)
app.secret_key = 'default_secret_key'
questions_in_quiz = 3

questions_easy = [
    {
      "question": "Which team won the UEFA Champions League in 2017?",
      "options": ["Real Madrid", "Barcelona", "Bayern Munich", "Liverpool"],
      "answer": "Real Madrid"
    },
    {
      "question": "Who is the all-time leading goal scorer for the German national team?",
      "options": ["Miroslav Klose", "Thomas Muller", "Gerd Muller", "Lukas Podolski"],
      "answer": "Miroslav Klose"
    },
    {
      "question": "Which country hosted the UEFA European Championship in 2008?",
      "options": ["Austria & Switzerland", "Germany", "France", "Spain"],
      "answer": "Austria & Switzerland"
    }
]

questions_medium = [
    {
      "question": "Who is the only goalkeeper to have won the Ballon d'Or?",
      "options": ["Lev Yashin", "Iker Casillas", "Manuel Neuer", "Gianluigi Buffon"],
      "answer": "Lev Yashin"
    },
    {
      "question": "Which club has won the most Bundesliga titles?",
      "options": ["Bayern Munich", "Borussia Dortmund", "Borussia Monchengladbach", "Hamburger SV"],
      "answer": "Bayern Munich"
    },
    {
      "question": "Who is the youngest player to win the UEFA European Championship?",
      "options": ["Renato Sanches", "Wayne Rooney", "Mario Gotze", "Cristiano Ronaldo"],
      "answer": "Renato Sanches"
    }
]

dbConnector = DbUtils("pgserver.mau.se", "futquiz", "aj2020", "oxbk46tq")

def isBlank(checked_str):
    if not checked_str or checked_str.strip() == "" or checked_str.strip() == "None":
        return True
    return False


@app.route('/users') #Ej slutfört, ska bli LEADERBOARD HÄR.
def show_users():
    try:
        users = dbConnector.executeSQL("SELECT user_id, email FROM users")  # Adjust the query with correct column names
        return render_template('users.html', users=users)
    except Exception as e:
        return str(e)

def is_valid_password(password):
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    return has_upper and has_digit

def build_admin_questions_list(adminName):
    admin_questions_list = []
    try:
        results = dbConnector.executeSQL("SELECT * FROM Questionz WHERE Accepted=FALSE")
        for row in results:
            ans = []
            ans.append(row[1])
            ans.append(row[2])
            ans.append(row[3])
            ans.append(row[4])
            admin_questions_list.append(render_template("admin_question_template.html",
                                                        admin=adminName,
                                                        question=row[0],
                                                        answers=ans,
                                                        rightAns=row[5],
                                                        level=row[7],
                                                        cat=row[6]))
    except Exception as e:
        print("ERROR: %s" % str(e))

    return admin_questions_list


# Homepage Route
@app.route('/', methods=['GET'])
def index():
    """Render the index page. (Render initial page with a form to start a new game.)"""
    return render_template('index.html')

@app.route('/login')
@app.route('/login/msg/<alert>')
def login(alert=""):
    alert_message = alert
    if not isBlank(alert):
        if alert == "wrongUserPass":
            alert_message = "Wrong user name or password!"
        elif alert == "passwordMissMatch":
            alert_message = "Wrong password or password missmatch!"
        elif alert == "loginError":
            alert_message = "Login error!"

    return render_template('login.html', alert_msg=alert_message)


@app.route('/signup')
@app.route('/signup/msg/<alert>')
def signup(alert=""):
    alert_message = alert
    if not isBlank(alert):
        if alert == "passwordMissMatch":
            alert_message = "Wrong password or password missmatch!"
        elif alert == "wrongPassword":
            alert_message = "Password must contain atleast\none digit and one capital letter."
        elif alert == "cantCreateUser":
            alert_message = "Can't create user!\nUser may already exists."

    return render_template('signup.html', alert_msg=alert_message)


@app.route('/user_view', methods=['POST', 'GET'])
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
        try:
            uname = request.form.get("uname").lower()
        except Exception:
            return redirect('/login')
        passwd = request.form.get("psw")
        isAdmin = False
        try:
            results = dbConnector.executeSQL("SELECT password_hash FROM users WHERE email='%s'" % uname)
            if not results:
                results = dbConnector.executeSQL("SELECT password FROM admins WHERE email='%s'" % uname)
                if not results:
                    return redirect("/login/msg/wrongUserPass")
                isAdmin = True
            for row in results:
                c_pass = row[0]
                if c_pass != passwd:
                    return redirect("/login/msg/wrongUserPass")
        except Exception as e:
            print("ERROR: %s" % str(e))
            return redirect("/login/msg/loginError")
    else:
        uname = userId

    if isAdmin:
        q_list = build_admin_questions_list(uname)
        return render_template('admin.html', admin=uname, questions_list=q_list)
    return render_template('main.html', username=uname)

@app.route('/admin', methods=['POST', 'GET'])
def admin_view():
    adminUser = request.form.get("adminId")
    print('Admin: %s' % adminUser)
    if isBlank(adminUser):
        return redirect('/login')
    qName = request.form.get("q_name")
    delQ = request.form.get("deleteQuestion")

    if not isBlank(qName):
        try:
            dbConnector.executeSQL("UPDATE Questionz SET Accepted=TRUE WHERE Question='%s'" % qName)
        except Exception as e:
            print("ERROR: %s" % str(e))
    elif not isBlank(delQ):
        try:
            dbConnector.executeSQL("DELETE FROM Questionz WHERE Question='%s'" % delQ)
        except Exception as e:
            print("ERROR: %s" % str(e))
    q_list = build_admin_questions_list(adminUser)
    return render_template('admin.html', admin=adminUser, questions_list=q_list)

@app.route('/new_user_view', methods=['POST'])
def new_user_view():
    email = request.form.get("email").lower()
    passwd = request.form.get("password")
    re_passwd = request.form.get("confirm-password")

    if isBlank(email) or isBlank(passwd) or isBlank(re_passwd) or passwd != re_passwd:
        return redirect('/signup/msg/passwordMissMatch')
    if not is_valid_password(passwd):
        return redirect('/signup/msg/wrongPassword')
    try:
        dbConnector.executeSQL("INSERT INTO users (email,password_hash,created_at) VALUES ('%s','%s',CURRENT_TIMESTAMP)" % (email, passwd))
    except Exception:
        return redirect('/signup/msg/cantCreateUser')

    #return template
    return render_template('main.html', username=email)


# Quiz page r
def get_questions(difficulty):
    if difficulty == "medium":
        return questions_medium
    #elif difficulty == "hard":
        #return questions_hard
    return questions_easy


def map_level(difficulty):
    if difficulty == "easy":
        return 1
    if difficulty == "medium":
        return 2
    if difficulty == "hard":
        return 3
    return 1

def get_questions_from_db(cat, level):
    sql_str = "SELECT * FROM Questionz WHERE ACCEPTED=TRUE AND Level=%d " % level
    if not cat == "AllAround":
        sql_str += "AND CAT='%s' " % cat
    sql_str += "ORDER BY RANDOM() LIMIT %d" % questions_in_quiz
    questions = []
    try:
        results = dbConnector.executeSQL(sql_str)
        for row in results:
            question = {"question" : "%s" % row[0],
                        "options" : [row[1], row[2], row[3], row[4]],
                        "answer" : row[row[5]]}
            questions.append(question)
    except Exception as e:
        print("ERROR: %s" % str(e))
    return questions

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    difficulty = request.form['difficulty']
    level = map_level(difficulty)
    category = request.form['category']
    userId = request.form.get("userId")
    #questions = get_questions(difficulty)
    #random.shuffle(questions)
    questions = get_questions_from_db(category, level)
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    session['start_time'] = time.time()
    session['difficulty'] = difficulty
    return redirect(url_for('show_question'))
    #return show_question(userId)

@app.route('/question')
def show_question():
    if 'current_question' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('show_results'))
    question = session['questions'][session['current_question']]
    score = session.get('score', 0)
    return render_template('question.html', question=question, score=score)

@app.route('/suggest', methods=['POST'])
def suggest():
    userId = request.form.get("userId")
    return render_template('suggest.html', user=userId)

@app.route('/submit_question', methods=['POST'])
def submit_question():
    userId = request.form.get("userId")
    difficulty = int(request.form.get("difficulty"))
    category = request.form.get("category")
    question = request.form.get("question")
    answer1 = request.form.get("answer1")
    answer2 = request.form.get("answer2")
    answer3 = request.form.get("answer3")
    answer4 = request.form.get("answer4")
    CorrectAnswer = int(request.form.get("CorrectAnswer"))
    print(CorrectAnswer)
    try:
        dbConnector.executeSQL("INSERT INTO Questionz (Question,ANS1,ANS2,ANS3,ANS4,CorrectAns,CAT,Level,Accepted) VALUES ('%s','%s','%s','%s','%s','%d','%s','%d',FALSE)" %
                               (question, answer1, answer2, answer3, answer4, CorrectAnswer, category, difficulty))
    except Exception as e:
        print('ERROR: %s' % (str(e)))
        return render_template('suggest.html', user=userId)
    return render_template('main.html', username=userId)

@app.route('/next_question', methods=['GET'])
def next_question():
    if 'current_question' in session and session['current_question'] < len(session['questions']) - 1:
        session['current_question'] += 1
        session['start_time'] = time.time()  # Reset start time for the new question
        return redirect(url_for('show_question'))
    return redirect(url_for('show_results'))

@app.route('/answer', methods=['POST'])
def answer():
    if 'current_question' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('show_results'))
    current = session['questions'][session['current_question']]
    choice = request.form['option']
    correct = choice == current['answer']
    multiplier = {'easy': 1, 'medium': 1.5, 'hard': 2}[session['difficulty']]
    elapsed_time = max(30 - (time.time() - session['start_time']), 0)
    if correct:
        session['score'] += int(elapsed_time * multiplier)
    session['start_time'] = time.time()  # Reset the timer
    return render_template('answer.html', question=current, chosen=choice, correct=correct, score=session['score'])

#@app.route('/results')
def show_results(userId):
    score = session.get('score', 0)
    session.clear()
    try:
        dbConnector.executeSQL("UPDATE Users SET Score=Score+%d WHERE Email='%s'" % (score, userId))
    except Exception as e:
        print('ERROR: %s' % (str(e)))
    return render_template('results.html', score=score, username=userId)

# Run the application
if __name__ == '__main__':
    app.run(debug=False)
    
