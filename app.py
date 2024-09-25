from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for form submissions
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# List of random quotes
quotes = [
    "When you forgive you win.",
    "Forgiveness is the power to choose how things affect you.",
    "Forgiveness is choosing to be happy.",
    "Forgiveness is simply freeing ourselves from wanting to punish.",
    "We experience what we intend for others.",
    "Fear is wisdom as a child.",
    "Forgiveness is always possible, but reconciliation is not always possible.",
    "Forgiveness gives us the freedom to stay and the freedom to walk away."
]

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    random_quote = random.choice(quotes)
    return render_template('index.html', quote=random_quote)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    new_submission = Submission(name=name, email=email)
    db.session.add(new_submission)
    db.session.commit()
    random_quote = random.choice(quotes)
    return render_template('index.html', quote=random_quote)

@app.route('/submissions')
def submissions():
    all_submissions = Submission.query.all()
    return render_template('submissions.html', submissions=all_submissions)

if __name__ == '__main__':
    app.run(debug=True)
