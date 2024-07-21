from flask import Flask, flash, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db,Question,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html', username=current_user.username)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/create_question', methods=['GET', 'POST'])
@login_required
def create_question():
    if request.method == 'POST':
        question_text = request.form['question_text']
        answer_1 = request.form['answer_1']
        answer_2 = request.form['answer_2']
        answer_3 = request.form['answer_3']
        answer_4 = request.form['answer_4']
        answer_5 = request.form['answer_5']
        correct_answer = request.form['correct_answer']

        # Calculate user_question_id
        last_question = Question.query.filter_by(user_id=current_user.id).order_by(Question.user_question_id.desc()).first()
        if last_question:
            user_question_id = last_question.user_question_id + 1
        else:
            user_question_id = 1

        new_question = Question(
            user_question_id=user_question_id,
            question_text=question_text,
            answer_1=answer_1,
            answer_2=answer_2,
            answer_3=answer_3,
            answer_4=answer_4,
            answer_5=answer_5,
            correct_answer=correct_answer,
            user_id=current_user.id
        )

        db.session.add(new_question)
        db.session.commit()

        flash('Question created successfully!')
        return redirect(url_for('index'))

    return render_template('create_question.html')


@app.route('/view_questions')
@login_required
def view_questions():
    user_id = current_user.id
    questions = Question.query.filter_by(user_id=user_id).all()
    return render_template('view_questions.html', questions=questions)

@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.user_id != current_user.id:
        flash('You are not authorized to edit this question.')
        return redirect(url_for('view_questions'))
    
    if request.method == 'POST':
        question.question_text = request.form['question_text']
        question.answer_1 = request.form['answer_1']
        question.answer_2 = request.form['answer_2']
        question.answer_3 = request.form['answer_3']
        question.answer_4 = request.form['answer_4']
        question.answer_5 = request.form['answer_5']
        question.correct_answer = request.form['correct_answer']
        db.session.commit()
        flash('Question updated successfully!')
        return redirect(url_for('view_questions'))

    return render_template('edit_question.html', question=question)

@app.route('/index')
def goIndex():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)