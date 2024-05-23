import re

def isBlank(string):
    return not (string and string.strip())

def is_valid_password(password):
    return re.match(r'^(?=.*[A-Z])(?=.*\d).{6,}$', password)

def map_level(difficulty):
    levels = {'easy': 1, 'medium': 2, 'hard': 3}
    return levels.get(difficulty, 1)

def get_questions_from_db(dbConnector, category, level):
    query = "SELECT question, option_a, option_b, option_c, option_d, answer FROM questions WHERE category=%s AND difficulty=%s"
    values = (category, level)
    questions = dbConnector.fetchSQL(query, values)
    return [{'question': q[0], 'options': [q[1], q[2], q[3], q[4]], 'answer': q[5]} for q in questions]

def build_admin_questions_list(dbConnector, adminUser, approved):
    query = "SELECT question, option_a, option_b, option_c, option_d, answer FROM questions WHERE approved=%s"
    values = (approved,)
    questions = dbConnector.fetchSQL(query, values)
    return [{'question': q[0], 'options': [q[1], q[2], q[3], q[4]], 'answer': q[5]} for q in questions]
