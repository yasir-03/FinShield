import re
from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(email) and bool(EMAIL_REGEX.match(email.strip()))


def is_valid_password(password):
    """At least 6 characters, one letter and one number."""
    if not password or len(password) < 6:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True


def sanitize_text(value, max_len=500):
    if value is None:
        return ""
    value = str(value).strip()
    return value[:max_len]


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("main.login"))
        if not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)

    return wrapped


def grade_label(percentage):
    if percentage >= 80:
        return ("Excellent", "success")
    if percentage >= 60:
        return ("Good", "info")
    if percentage >= 40:
        return ("Fair", "warning")
    return ("Needs Improvement", "danger")


def format_currency(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "0"
    return f"{value:,.2f}"
