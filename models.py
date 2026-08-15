from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    occupation = db.Column(db.String(120))
    city = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quiz_results = db.relationship("QuizResult", backref="user", lazy=True, cascade="all, delete-orphan")
    chat_history = db.relationship("ChatHistory", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def quiz_count(self):
        return len(self.quiz_results)

    @property
    def average_score(self):
        if not self.quiz_results:
            return 0
        return round(sum(r.percentage for r in self.quiz_results) / len(self.quiz_results), 1)

    def __repr__(self):
        return f"<User {self.email}>"


class QuizResult(db.Model):
    __tablename__ = "quiz_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer)  # seconds
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<QuizResult {self.category} {self.percentage}%>"


class SurveyResponse(db.Model):
    __tablename__ = "survey_responses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    occupation = db.Column(db.String(120), nullable=False)
    education = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    upi_usage = db.Column(db.String(50), nullable=False)
    investment_experience = db.Column(db.String(50), nullable=False)
    fraud_experience = db.Column(db.String(50), nullable=False)
    financial_knowledge_level = db.Column(db.String(50), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SurveyResponse {self.id}>"


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    icon = db.Column(db.String(50), default="bi-book")
    summary = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article {self.slug}>"


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feedback {self.email}>"


class ChatHistory(db.Model):
    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(20), default="local")  # local | llm
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatHistory {self.id}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
