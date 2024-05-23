from flask import Blueprint, render_template, request, session, redirect, url_for
from helpers import get_questions_from_db, isBlank, map_level
import time

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/start_quiz', methods=['POST'])
def start_quiz(dbConnector):
    difficulty = request.form['difficulty']
    level = map_level(difficulty)
    category = request.form['category']
    userId = request.form.get("userId")
    if isBlank(userId):
        return redirect('/login')
    questions = get_questions_from_db(dbConnector, category, level)
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    session['start_time'] = time.time()
    session['difficulty'] = difficulty
    return show_question(dbConnector, userId)

def show_question(dbConnector, userId):
    if 'current_question' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('quiz.show_results', dbConnector=dbConnector, userId=userId))
    question = session['questions'][session['current_question']]
    question_number = session['current_question'] + 1
    total_questions = len(session['questions'])
    score = session.get('score', 0)
    return render_template('question.html', question=question, question_number=question_number, total_questions=total_questions, score=score, username=userId)

@quiz_bp.route('/next_question', methods=['POST'])
def next_question(dbConnector):
    userId = request.form.get("userId")
    if isBlank(userId):
        return redirect('/login')
    if 'current_question' in session and session['current_question'] < len(session['questions']) - 1:
        session['current_question'] += 1
        session['start_time'] = time.time()
        question = session['questions'][session['current_question']]
        question_number = session['current_question'] + 1
        total_questions = len(session['questions'])
        score = session.get('score', 0)
        return render_template('question.html', question=question, question_number=question_number, total_questions=total_questions, score=score, username=userId)
    return show_results(dbConnector, userId)

@quiz_bp.route('/answer', methods=['POST'])
def answer(dbConnector):
    if 'current_question' not in session or session['current_question'] >= len(session['questions']):
        return redirect(url_for('quiz.show_results', dbConnector=dbConnector))
    current = session['questions'][session['current_question']]
    choice = request.form['option']
    userId = request.form.get("userId")
    if isBlank(userId):
        return redirect('/login')
    correct = choice == current['answer']
    multiplier = {'easy': 1, 'medium': 1.5, 'hard': 2}[session['difficulty']]
    elapsed_time = max(30 - (time.time() - session['start_time']), 0)
    if correct:
        session['score'] += int(elapsed_time * multiplier)
    session['start_time'] = time.time()
    return render_template('answer.html', question=current, chosen=choice, correct=correct, score=session['score'], username=userId)

@quiz_bp.route('/results/<userId>')
def show_results(dbConnector, userId):
    score = session.get('score', 0)
    session.clear()
    try:
        dbConnector.executeSQL("UPDATE Users SET Score=Score+%d WHERE Email=%s", (score, userId))
    except Exception as e:
        print('ERROR: %s' % (str(e)))
    return render_template('results.html', score=score, username=userId)
