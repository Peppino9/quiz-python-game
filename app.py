# app.py Import Flask and render_template
import time
from flask import Flask, render_template, request, redirect, session, url_for
from db_connection_utils import DbUtils

import psycopg2
from psycopg2 import OperationalError
import datetime

app = Flask(__name__)
app.secret_key = 'default_secret_key'
questions_in_quiz = 10

dbConnector = DbUtils("pgserver.mau.se", "futquiz", "aj2020", "oxbk46tq")

def isBlank(checked_str):
    if not checked_str or checked_str.strip() == "" or checked_str.strip() == "None":
        return True
    return False

@app.route('/users', methods=['POST']) 
def show_users():
    userId = request.form.get("userId")
    try:
        users = dbConnector.executeSQL("SELECT user_id, email, Score FROM users ORDER BY Score DESC") 
        return render_template('users.html', users=users, username=userId)
    except Exception as e:
        return str(e)

def is_valid_password(password):
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    return has_upper and has_digit

def build_admin_questions_list(adminName, liveQuestions):
    admin_questions_list = []
    if liveQuestions:
        template_str = "admin_question_bank_template.html"
    else: 
        template_str = "admin_question_template.html"
    try:
        results = dbConnector.executeSQL("SELECT * FROM Questionz WHERE Accepted=%r" % liveQuestions)
        for row in results:
            ans = []
            ans.append(row[1])
            ans.append(row[2])
            ans.append(row[3])
            ans.append(row[4])
            admin_questions_list.append(render_template(template_str,
                                                        admin=adminName,
                                                        question=row[0],
                                                        answers=ans,
                                                        rightAns=row[5],
                                                        level=row[7],
                                                        cat=row[6]))
    except Exception as e:
        print("ERROR: %s" % str(e))

    return admin_questions_list

def build_admin_users_list(adminName):
    admin_users_list = []
    try:
        results = dbConnector.executeSQL("SELECT Email FROM Users")
        for row in results:
            admin_users_list.append(render_template('admin_user_template.html',
                                                        admin=adminName,
                                                        email=row[0]))
    except Exception as e:
        print("ERROR: %s" % str(e))

    return admin_users_list


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

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


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

#admin uses the same route to log on
#Only user email makes diffrence between admin and ordinary user
@app.route('/user_view', methods=['POST', 'GET'])
def user_view():
    userId = request.form.get("userId")
    admin_str = request.form.get("admin")
    uname = None
    passwd = None

    '''
    This if statement is needed if the user is already logged in and it's redirected here from other page.
    In order to avoid requesting credentials again!!!
    Of course, that page should post the userId.
    '''
    isAdmin = False
    if isBlank(userId):
        try:
            uname = request.form.get("uname").lower()
        except Exception:
            return redirect('/login')
        passwd = request.form.get("psw")
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
        if not isBlank(admin_str):
            isAdmin = True

    if isAdmin:
        q_list = build_admin_questions_list(uname, False)
        b_list = build_admin_questions_list(uname, True)
        u_list = build_admin_users_list(uname)
        return render_template('admin.html', admin=uname, questions_list=q_list, bank_list=b_list, users_list=u_list)

    try:
        results = dbConnector.executeSQL("SELECT Score FROM users WHERE email='%s'" % uname)
        top_u = dbConnector.executeSQL("SELECT Email, Score FROM users ORDER BY Score DESC LIMIT 3")
        for row in results:
            if not isAdmin:
                g_score = row[0]
    except Exception as e:
        print("ERROR: %s" % str(e))
    return render_template('main.html', username=uname, gen_score=g_score, top_players=top_u)

@app.route('/admin', methods=['POST', 'GET'])
def admin_view():
    adminUser = request.form.get("adminId")
    if isBlank(adminUser):
        return redirect('/login')
    qName = request.form.get("q_name")
    delQ = request.form.get("deleteQuestion")
    delU = request.form.get("deleteUser")

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
    elif not isBlank(delU):
        try:
            dbConnector.executeSQL("DELETE FROM Users WHERE Email='%s'" % delU)
        except Exception as e:
            print("ERROR: %s" % str(e))
    q_list = build_admin_questions_list(adminUser, False)
    b_list = build_admin_questions_list(adminUser, True)
    u_list = build_admin_users_list(adminUser)
    return render_template('admin.html', admin=adminUser, questions_list=q_list, bank_list=b_list, users_list=u_list)

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
        top_u = dbConnector.executeSQL("SELECT Email, Score FROM users ORDER BY Score DESC LIMIT 3")
    except Exception:
        return redirect('/signup/msg/cantCreateUser')

    #return template
    return render_template('main.html', username=email, gen_score="0", top_players=top_u)

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

@app.route('/restart_quiz', methods=['POST'])
def restart_quiz():
    difficulty = request.form.get("difficulty")
    category = request.form.get("category")
    userId = request.form.get("userId")
    if isBlank(userId):
        return redirect('/login')

    print('param rest q: %s %s %s' % (userId, category, difficulty))
    return initialize_question(userId, category, difficulty)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    difficulty = request.form['difficulty']
    category = request.form['category']
    userId = request.form.get("userId")
    if isBlank(userId):
        return redirect('/login')

    print('param start q: %s %s %s' % (userId, category, difficulty))
    return initialize_question(userId, category, difficulty)


def initialize_question(userId, category, difficulty):
    level = map_level(difficulty)
    questions = get_questions_from_db(category, level)
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    session['start_time'] = time.time()
    session['difficulty'] = difficulty
    return show_question(userId, category, difficulty)

#@app.route('/question')
def show_question(userId, category, difficulty):
    if 'current_question' not in session or session['current_question'] >= len(session['questions']):
        return show_results(userId, category, difficulty)
    question = session['questions'][session['current_question']]
    question_number = session['current_question'] + 1
    total_questions = len(session['questions'])
    score = session.get('score', 0)
    return render_template('question.html', question=question,
                           question_number=question_number,
                           total_questions=total_questions,
                           score=score,
                           username=userId,
                           cat=category,
                           diff=difficulty)

@app.route('/suggest', methods=['POST'])
def suggest():
    userId = request.form.get("userId")
    isAdmin = request.form.get("admin")
    if isBlank(userId):
        return redirect('/login')
    if isBlank(isAdmin):
        isAdmin = "" 
    return render_template('suggest.html', user=userId, admin=isAdmin)

@app.route('/submit_question', methods=['POST'])
def submit_question():
    userId = request.form.get("userId")
    admin = request.form.get("admin")
    if isBlank(userId):
        return redirect('/login')
    accepted = False
    if not isBlank(admin):
        accepted = True
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
        dbConnector.executeSQL("INSERT INTO Questionz (Question,ANS1,ANS2,ANS3,ANS4,CorrectAns,CAT,Level,Accepted) VALUES ('%s','%s','%s','%s','%s','%d','%s','%d',%r)" %
                               (question, answer1, answer2, answer3, answer4, CorrectAnswer, category, difficulty, accepted))
    except Exception as e:
        print('ERROR: %s' % (str(e)))
        return render_template('suggest.html', user=userId)

    if not isBlank(admin):
        q_list = build_admin_questions_list(userId, False)
        b_list = build_admin_questions_list(userId, True)
        u_list = build_admin_users_list(userId)
        return render_template('admin.html', admin=userId, questions_list=q_list, bank_list=b_list, users_list=u_list)

    try:
        results = dbConnector.executeSQL("SELECT Score FROM users WHERE email='%s'" % userId)
        top_u = dbConnector.executeSQL("SELECT Email, Score FROM users ORDER BY Score DESC LIMIT 3")
        for row in results:
            g_score = row[0]
    except Exception as e:
        print("ERROR: %s" % str(e))
    return render_template('main.html', username=userId, gen_score=g_score, top_players=top_u)


@app.route('/next_question', methods=['POST'])
def next_question():
    userId = request.form.get("userId")
    difficulty = request.form.get("difficulty")
    category = request.form.get("category")
    if isBlank(userId):
        return redirect('/login')
    print('user nc: %s' % userId)
    if 'current_question' in session and session['current_question'] < len(session['questions']) - 1:
        session['current_question'] += 1
        session['start_time'] = time.time()  # Reset start time for the new question
        #return redirect(url_for('show_question'))
        question = session['questions'][session['current_question']]
        question_number = session['current_question'] + 1
        total_questions = len(session['questions'])
        score = session.get('score', 0)
        return render_template('question.html',
                               question=question,
                               question_number=question_number,
                               total_questions=total_questions,
                               score=score,
                               username=userId,
                               cat=category,
                               diff=difficulty)
    #return redirect(url_for('show_results'))
    return show_results(userId, category, difficulty)

@app.route('/answer', methods=['POST'])
def answer():
    if 'current_question' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('show_results'))
    current = session['questions'][session['current_question']]
    choice = request.form['option']
    userId = request.form.get("userId")
    difficulty = request.form.get("difficulty")
    category = request.form.get("category")
    if isBlank(userId):
        return redirect('/login')
    print('user ans: %s' % userId)
    correct = choice == current['answer']
    multiplier = {'easy': 1, 'medium': 1.5, 'hard': 2}[session['difficulty']]
    elapsed_time = max(30 - (time.time() - session['start_time']), 0)
    if correct:
        session['score'] += int(elapsed_time * multiplier)
    session['start_time'] = time.time()  # Reset the timer
    return render_template('answer.html', question=current, chosen=choice, correct=correct, score=session['score'],
                           username=userId,
                           cat=category,
                           diff=difficulty)

@app.route('/results', methods=['POST'])
def result():
    userId = request.form.get("userId")
    difficulty = request.form.get("difficulty")
    category = request.form.get("category")
    if isBlank(userId):
        return redirect('/login')
    print('param result: %s %s %s' % (userId, category, difficulty))
    return show_results(userId, category, difficulty)

def show_results(userId, category, difficulty):
    score = session.get('score', 0)
    session.clear()
    try:
        dbConnector.executeSQL("UPDATE Users SET Score=Score+%d WHERE Email='%s'" % (score, userId))
    except Exception as e:
        print('ERROR: %s' % (str(e)))
    print('param show result: %s %s %s' % (userId, category, difficulty))
    return render_template('results.html', score=score, username=userId, cat=category, diff=difficulty)

# Run the application
if __name__ == '__main__':
    app.run(debug=False)
