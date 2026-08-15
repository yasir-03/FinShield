from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from database import db
from models import SurveyResponse
from utils import sanitize_text

survey_bp = Blueprint("survey", __name__, url_prefix="/survey")

OCCUPATION_CHOICES = ["Student", "Salaried Employee", "Self-Employed / Business", "Homemaker", "Unemployed", "Retired", "Other"]
EDUCATION_CHOICES = ["Below High School", "High School", "Undergraduate", "Postgraduate", "Doctorate", "Other"]
UPI_USAGE_CHOICES = ["Never Used", "Rarely (few times a month)", "Occasionally (weekly)", "Daily / Very Frequently"]
INVESTMENT_EXPERIENCE_CHOICES = ["No Experience", "Beginner (less than 1 year)", "Intermediate (1-5 years)", "Experienced (5+ years)"]
FRAUD_EXPERIENCE_CHOICES = ["Never Experienced", "Received Suspicious Messages/Calls", "Experienced Attempted Fraud", "Experienced Financial Loss Due to Fraud"]
KNOWLEDGE_LEVEL_CHOICES = ["Beginner", "Basic", "Intermediate", "Advanced"]


@survey_bp.route("/", methods=["GET", "POST"])
def survey_form():
    if request.method == "POST":
        try:
            age = int(request.form.get("age", 0))
        except ValueError:
            age = 0

        occupation = sanitize_text(request.form.get("occupation"), 120)
        education = sanitize_text(request.form.get("education"), 120)
        city = sanitize_text(request.form.get("city"), 120)
        upi_usage = sanitize_text(request.form.get("upi_usage"), 50)
        investment_experience = sanitize_text(request.form.get("investment_experience"), 50)
        fraud_experience = sanitize_text(request.form.get("fraud_experience"), 50)
        financial_knowledge_level = sanitize_text(request.form.get("financial_knowledge_level"), 50)

        errors = []
        if age < 10 or age > 110:
            errors.append("Please enter a valid age.")
        if not occupation or occupation not in OCCUPATION_CHOICES:
            errors.append("Please select a valid occupation.")
        if not education or education not in EDUCATION_CHOICES:
            errors.append("Please select a valid education level.")
        if not city:
            errors.append("Please enter your city.")
        if upi_usage not in UPI_USAGE_CHOICES:
            errors.append("Please select your UPI usage frequency.")
        if investment_experience not in INVESTMENT_EXPERIENCE_CHOICES:
            errors.append("Please select your investment experience.")
        if fraud_experience not in FRAUD_EXPERIENCE_CHOICES:
            errors.append("Please select your fraud experience.")
        if financial_knowledge_level not in KNOWLEDGE_LEVEL_CHOICES:
            errors.append("Please select your financial knowledge level.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "survey/survey.html",
                occupations=OCCUPATION_CHOICES,
                educations=EDUCATION_CHOICES,
                upi_options=UPI_USAGE_CHOICES,
                investment_options=INVESTMENT_EXPERIENCE_CHOICES,
                fraud_options=FRAUD_EXPERIENCE_CHOICES,
                knowledge_options=KNOWLEDGE_LEVEL_CHOICES,
                form_data=request.form,
            )

        response = SurveyResponse(
            user_id=current_user.id if current_user.is_authenticated else None,
            age=age,
            occupation=occupation,
            education=education,
            city=city,
            upi_usage=upi_usage,
            investment_experience=investment_experience,
            fraud_experience=fraud_experience,
            financial_knowledge_level=financial_knowledge_level,
        )
        db.session.add(response)
        db.session.commit()

        return redirect(url_for("survey.thank_you"))

    return render_template(
        "survey/survey.html",
        occupations=OCCUPATION_CHOICES,
        educations=EDUCATION_CHOICES,
        upi_options=UPI_USAGE_CHOICES,
        investment_options=INVESTMENT_EXPERIENCE_CHOICES,
        fraud_options=FRAUD_EXPERIENCE_CHOICES,
        knowledge_options=KNOWLEDGE_LEVEL_CHOICES,
        form_data={},
    )


@survey_bp.route("/thank-you")
def thank_you():
    return render_template("survey/thankyou.html")
