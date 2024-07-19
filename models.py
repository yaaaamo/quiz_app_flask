from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_1 = db.Column(db.String(255), nullable=False)
    answer_2 = db.Column(db.String(255), nullable=False)
    answer_3 = db.Column(db.String(255), nullable=True)
    answer_4 = db.Column(db.String(255), nullable=True)
    answer_5 = db.Column(db.String(255), nullable=True)
    correct_answer = db.Column(db.Integer, nullable=False)  # Stores the index of the correct answer (1-5)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming a 'User' model exists

    def __repr__(self):
        return f'<Question {self.id}>'
