# app.py Import Flask and render_template
from flask import Flask, render_template
from quiz_logic import generate_random_questions  # Importing function from quiz_logic module
from data.questions import question_bank

import psycopg2
from psycopg2 import OperationalError
import datetime

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


# Create Flask app / # Create an instance of the Flask class
app = Flask(__name__)

# Define route for the homepage
@app.route('/', methods=['GET'])
def index():
    """Render the index page. (Render initial page with a form to start a new game.)"""
    return render_template('index.html')

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
    app.run(debug=True)
    
# Database connection and cursor setup