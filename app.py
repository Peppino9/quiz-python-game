from flask import Flask, render_template
from utils.db_connection_utils import DbUtils

app = Flask(__name__)
app.secret_key = 'default_secret_key'

# Initialize the database connection
dbConnector = DbUtils("pgserver.mau.se", "futquiz", "aj2020", "oxbk46tq")

# Register Blueprints
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.quiz_routes import quiz_bp
from routes.user_routes import user_bp

# Register Blueprints with or without defaults
app.register_blueprint(admin_bp, url_prefix='/admin', defaults={'dbConnector': dbConnector})
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(quiz_bp, url_prefix='/quiz', defaults={'dbConnector': dbConnector})
app.register_blueprint(user_bp, url_prefix='/user', defaults={'dbConnector': dbConnector})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
