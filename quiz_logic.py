# quiz_logic.py
import random
from data.questions import question_bank  # Importing question_bank from data/questions.py


# Function to generate random questions
def generate_random_questions(num_questions):
    """Generate random questions from the question bank."""
    return random.sample(question_bank, num_questions)

# Function to calculate score
def calculate_score(answers):
    """Calculate the score based on user answers."""
    score = 0
    for answer in answers:
        question = question_bank[answer['question_index']]
        if answer['selected_option'] == question['correct_answer']:
            score += 1
    return score
