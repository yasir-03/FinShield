import pandas as pd

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user

from database import db
from models import User, QuizResult, SurveyResponse, Feedback, ChatHistory
from learning_data import LEARNING_ARTICLES, LEARNING_CATEGORY_ORDER
from recommendation import get_dashboard_recommendations
from utils import is_valid_email, is_valid_password, sanitize_text, admin_required, grade_label

main_bp = Blueprint("main", __name__)


# ---------------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------------

@main_bp.route("/")
def home():
    stats = {
        "users": User.query.count(),
        "quizzes_taken": QuizResult.query.count(),
        "survey_responses": SurveyResponse.query.count(),
        "articles": len(LEARNING_ARTICLES),
    }
    return render_template("index.html", stats=stats)


@main_bp.route("/faq")
def faq():
    return render_template("faq.html")


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        name = sanitize_text(request.form.get("name"), 120)
        email = sanitize_text(request.form.get("email"), 150).lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        occupation = sanitize_text(request.form.get("occupation"), 120)
        city = sanitize_text(request.form.get("city"), 120)

        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not is_valid_password(password):
            errors.append("Password must be at least 6 characters and include a letter and a number.")
        if password != confirm_password:
            errors.append("Passwords do not match.")
        if email and User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/register.html", form_data=request.form)

        user = User(name=name, email=email, occupation=occupation, city=city)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome to FinShield AI, {user.name}!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("auth/register.html", form_data={})


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = sanitize_text(request.form.get("email"), 150).lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")
        return render_template("auth/login.html", form_data=request.form)

    return render_template("auth/login.html", form_data={})


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))


# ---------------------------------------------------------------------------
# Dashboard & Profile
# ---------------------------------------------------------------------------

@main_bp.route("/dashboard")
@login_required
def dashboard():
    results = (
        QuizResult.query.filter_by(user_id=current_user.id)
        .order_by(QuizResult.taken_at.desc())
        .all()
    )
    recent_results = results[:5]
    recommendations = get_dashboard_recommendations(results)

    categories_attempted = {r.category for r in results}
    survey_done = SurveyResponse.query.filter_by(user_id=current_user.id).first() is not None

    return render_template(
        "dashboard.html",
        results=recent_results,
        total_quizzes=len(results),
        categories_attempted=len(categories_attempted),
        average_score=current_user.average_score,
        recommendations=recommendations,
        survey_done=survey_done,
        grade_label=grade_label,
    )


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        name = sanitize_text(request.form.get("name"), 120)
        occupation = sanitize_text(request.form.get("occupation"), 120)
        city = sanitize_text(request.form.get("city"), 120)

        if not name:
            flash("Name cannot be empty.", "danger")
        else:
            current_user.name = name
            current_user.occupation = occupation
            current_user.city = city
            db.session.commit()
            flash("Profile updated successfully.", "success")
        return redirect(url_for("main.profile"))

    results = (
        QuizResult.query.filter_by(user_id=current_user.id)
        .order_by(QuizResult.taken_at.desc())
        .all()
    )
    return render_template("profile.html", results=results)


# ---------------------------------------------------------------------------
# Learning Module
# ---------------------------------------------------------------------------

@main_bp.route("/learning")
def learning_list():
    articles = [(slug, LEARNING_ARTICLES[slug]) for slug in LEARNING_CATEGORY_ORDER if slug in LEARNING_ARTICLES]
    return render_template("learning/list.html", articles=articles)


@main_bp.route("/learning/<slug>")
def learning_article(slug):
    article = LEARNING_ARTICLES.get(slug)
    if not article:
        abort(404)
    other_slugs = [s for s in LEARNING_CATEGORY_ORDER if s != slug][:3]
    others = [(s, LEARNING_ARTICLES[s]) for s in other_slugs]
    return render_template("learning/article.html", slug=slug, article=article, others=others)


# ---------------------------------------------------------------------------
# Calculators
# ---------------------------------------------------------------------------

@main_bp.route("/calculators")
def calculators():
    return render_template("calculators/calculators.html")


# ---------------------------------------------------------------------------
# Analytics Dashboard
# ---------------------------------------------------------------------------

@main_bp.route("/analytics")
def analytics():
    responses = SurveyResponse.query.all()
    total = len(responses)

    age_order = ["Under 18", "18-25", "26-35", "36-50", "51+"]
    knowledge_score_map = {"Beginner": 25, "Basic": 50, "Intermediate": 75, "Advanced": 100}

    def series_to_chart(series, label_order=None):
        if label_order:
            series = series.reindex([l for l in label_order if l in series.index]).dropna()
        return {"labels": series.index.tolist(), "values": series.values.astype(int).tolist()}

    if total:
        df = pd.DataFrame([{
            "age": r.age,
            "occupation": r.occupation,
            "education": r.education,
            "city": r.city,
            "upi_usage": r.upi_usage,
            "investment_experience": r.investment_experience,
            "fraud_experience": r.fraud_experience,
            "financial_knowledge_level": r.financial_knowledge_level,
        } for r in responses])

        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 17, 25, 35, 50, 150],
            labels=age_order,
        )

        chart_data = {
            "age": series_to_chart(df["age_group"].value_counts(), age_order),
            "occupation": series_to_chart(df["occupation"].value_counts()),
            "investment": series_to_chart(df["investment_experience"].value_counts()),
            "upi": series_to_chart(df["upi_usage"].value_counts()),
            "fraud": series_to_chart(df["fraud_experience"].value_counts()),
            "knowledge": series_to_chart(df["financial_knowledge_level"].value_counts()),
        }

        avg_awareness = round(df["financial_knowledge_level"].map(knowledge_score_map).fillna(0).mean(), 1)
    else:
        empty = {"labels": [], "values": []}
        chart_data = {"age": empty, "occupation": empty, "investment": empty, "upi": empty, "fraud": empty, "knowledge": empty}
        avg_awareness = 0

    quiz_total = QuizResult.query.count()
    avg_quiz_score = 0
    all_results = QuizResult.query.all()
    if all_results:
        avg_quiz_score = round(sum(r.percentage for r in all_results) / len(all_results), 1)

    return render_template(
        "analytics/dashboard.html",
        total_participants=total,
        avg_awareness=avg_awareness,
        chart_data=chart_data,
        quiz_total=quiz_total,
        avg_quiz_score=avg_quiz_score,
    )


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = sanitize_text(request.form.get("name"), 120)
        email = sanitize_text(request.form.get("email"), 150)
        subject = sanitize_text(request.form.get("subject"), 200)
        message = sanitize_text(request.form.get("message"), 2000)

        errors = []
        if not name:
            errors.append("Please enter your name.")
        if not is_valid_email(email):
            errors.append("Please enter a valid email address.")
        if not message:
            errors.append("Please enter a message.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("contact.html", form_data=request.form)

        feedback = Feedback(name=name, email=email, subject=subject, message=message)
        db.session.add(feedback)
        db.session.commit()

        flash("Thank you for reaching out! We'll get back to you soon.", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html", form_data={})


# ---------------------------------------------------------------------------
# Admin Panel
# ---------------------------------------------------------------------------

@main_bp.route("/admin")
@admin_required
def admin_dashboard():
    stats = {
        "users": User.query.count(),
        "quizzes": QuizResult.query.count(),
        "survey_responses": SurveyResponse.query.count(),
        "feedback": Feedback.query.count(),
        "chats": ChatHistory.query.count(),
    }
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_feedback = Feedback.query.order_by(Feedback.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, recent_users=recent_users, recent_feedback=recent_feedback)


@main_bp.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@main_bp.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Cannot delete an admin account.", "danger")
        return redirect(url_for("main.admin_users"))
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.email} deleted.", "success")
    return redirect(url_for("main.admin_users"))


@main_bp.route("/admin/quiz-results")
@admin_required
def admin_quiz_results():
    results = QuizResult.query.order_by(QuizResult.taken_at.desc()).all()
    return render_template("admin/quiz_results.html", results=results)


@main_bp.route("/admin/quiz-results/<int:result_id>/delete", methods=["POST"])
@admin_required
def admin_delete_quiz_result(result_id):
    result = QuizResult.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    flash("Quiz result deleted.", "success")
    return redirect(url_for("main.admin_quiz_results"))


@main_bp.route("/admin/survey-results")
@admin_required
def admin_survey_results():
    responses = SurveyResponse.query.order_by(SurveyResponse.submitted_at.desc()).all()
    return render_template("admin/survey_results.html", responses=responses)


@main_bp.route("/admin/survey-results/<int:response_id>/delete", methods=["POST"])
@admin_required
def admin_delete_survey_response(response_id):
    response = SurveyResponse.query.get_or_404(response_id)
    db.session.delete(response)
    db.session.commit()
    flash("Survey response deleted.", "success")
    return redirect(url_for("main.admin_survey_results"))


@main_bp.route("/admin/feedback")
@admin_required
def admin_feedback():
    items = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template("admin/feedback.html", items=items)


@main_bp.route("/admin/feedback/<int:feedback_id>/delete", methods=["POST"])
@admin_required
def admin_delete_feedback(feedback_id):
    item = Feedback.query.get_or_404(feedback_id)
    db.session.delete(item)
    db.session.commit()
    flash("Feedback deleted.", "success")
    return redirect(url_for("main.admin_feedback"))


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@main_bp.app_errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@main_bp.app_errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403


@main_bp.app_errorhandler(500)
def server_error(e):
    return render_template("errors/500.html"), 500
