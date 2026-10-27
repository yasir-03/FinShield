# -*- coding: utf-8 -*-
"""
One-off script that generates 'FinShield_AI_Explained.pdf' - a simple,
beginner-friendly, file-by-file walkthrough of the entire FinShield AI
codebase. Not part of the running app; run manually with:
    venv\\Scripts\\python.exe generate_docs.py
"""

from fpdf import FPDF

NAVY = (10, 17, 40)
GREEN = (16, 185, 129)
BLUE = (37, 99, 235)
GRAY = (100, 116, 139)
LIGHT_BG = (241, 245, 249)
BLACK = (30, 41, 59)


class DocPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.set_y(10)
        self.cell(0, 6, "FinShield AI - Code Explained", align="L")
        self.cell(0, 6, f"Page {self.page_no()}", align="R")
        self.set_draw_color(*LIGHT_BG)
        self.line(15, 17, self.w - 15, 17)
        self.ln(8)

    def footer(self):
        pass


pdf = DocPDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(18, 18, 18)

# ---------------------------------------------------------------------------
# Helper renderers
# ---------------------------------------------------------------------------

def cover_page():
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, pdf.h, "F")
    pdf.set_y(90)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 30)
    pdf.cell(0, 16, "FinShield AI", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 15)
    pdf.set_text_color(*[int(c) for c in (110, 231, 183)])
    pdf.cell(0, 10, "Explained Simply, File by File", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(14)
    pdf.set_text_color(220, 225, 235)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7,
        "A plain-language walkthrough of every file in your project:\n"
        "what it does, why it exists, and how each part works.",
        align="C")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(150, 160, 180)
    pdf.cell(0, 6, "Generated for the FinShield AI Community Engagement Project", align="C")


def chapter(title, subtitle=""):
    pdf.add_page()
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, 28, "F")
    pdf.set_xy(18, 8)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 17)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
    if subtitle:
        pdf.set_x(18)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*[int(c) for c in (110, 231, 183)])
        pdf.cell(0, 6, subtitle, new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(38)
    pdf.set_text_color(*BLACK)


def h2(text):
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12.5)
    pdf.set_text_color(*BLUE)
    pdf.multi_cell(0, 7, text)
    pdf.set_text_color(*BLACK)
    pdf.ln(1)


def p(text):
    pdf.set_font("Helvetica", "", 10.3)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 5.8, text)
    pdf.ln(1.5)


def bullet(text):
    pdf.set_font("Helvetica", "", 10.3)
    pdf.set_text_color(*BLACK)
    pdf.set_x(pdf.l_margin)
    x = pdf.get_x()
    pdf.cell(5, 5.8, "-")
    pdf.set_x(x + 5)
    pdf.multi_cell(pdf.w - pdf.r_margin - (x + 5), 5.8, text)
    pdf.set_x(pdf.l_margin)


def code(text):
    pdf.set_font("Courier", "", 9)
    pdf.set_text_color(30, 41, 59)
    pdf.set_fill_color(*LIGHT_BG)
    lines = text.strip("\n").split("\n")
    pdf.ln(1)
    pdf.set_x(pdf.l_margin)
    for line in lines:
        pdf.set_x(pdf.l_margin)
        pdf.cell(0, 5.6, "  " + line, fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def line_ref(range_text, explanation):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Courier", "B", 9.5)
    pdf.set_text_color(*GREEN)
    pdf.write(5.8, range_text + "  ")
    pdf.set_font("Helvetica", "", 10.3)
    pdf.set_text_color(*BLACK)
    pdf.write(5.8, explanation)
    pdf.ln(8)
    pdf.set_x(pdf.l_margin)


def divider():
    pdf.ln(2)
    pdf.set_draw_color(*LIGHT_BG)
    pdf.line(18, pdf.get_y(), pdf.w - 18, pdf.get_y())
    pdf.ln(4)


# ===========================================================================
# COVER
# ===========================================================================
cover_page()

# ===========================================================================
# INTRODUCTION
# ===========================================================================
chapter("How to Read This Document", "Start here")
p("This document explains every file in your FinShield AI project in plain "
  "English. You don't need to be a programmer to follow it. Each file gets "
  "its own section that answers three questions: what is this file for, "
  "what are its main parts, and how do those parts work together.")
h2("The Big Picture: How a Website Like This Works")
p("Think of the website in three layers:")
bullet("The Brain (Python files) - decides WHAT happens. It talks to the database, "
       "checks passwords, grades quizzes, and decides which page to show.")
bullet("The Face (HTML template files) - decides WHAT THE PAGE LOOKS LIKE. These "
       "are the actual page layouts the browser displays.")
bullet("The Style and Behavior (CSS and JavaScript files) - CSS makes it look "
       "pretty (colors, spacing, rounded corners). JavaScript makes it interactive "
       "(timers, chat bubbles, calculators) without needing to reload the page.")
p("When you type a web address, your browser sends a request to Flask (the Python "
  "web framework this app is built on). Flask looks at the address, finds the "
  "matching 'route' (a Python function), runs it, and that function usually reads "
  "or writes something in the database and then hands an HTML template back to "
  "the browser to display.")
h2("Project Folders")
bullet("Root folder - the main Python files (app.py, routes.py, models.py, etc.)")
bullet("templates/ - every HTML page, organized into subfolders by feature")
bullet("static/css/ - the one stylesheet controlling the whole look")
bullet("static/js/ - JavaScript files for interactive features")
bullet("instance/ - where the SQLite database file lives (created automatically)")

# ===========================================================================
# PART 1 - BACKEND
# ===========================================================================
chapter("Part 1: The Brain", "Python backend files")
p("These files run on the server (your computer, or later a hosting service). "
  "None of this code is ever visible to someone visiting the site - only the "
  "HTML/CSS/JS it produces is sent to their browser.")

# ---- config.py ----
chapter("config.py", "App settings, in one place")
p("This file holds settings the rest of the app needs, so nothing is hard-coded "
  "in multiple places. It defines one Python class called Config.")
line_ref("SECRET_KEY", "A random string Flask uses to cryptographically sign "
         "session cookies and CSRF tokens, so users can't tamper with them.")
line_ref("SQLALCHEMY_DATABASE_URI", "Tells the database toolkit (SQLAlchemy) where "
         "the SQLite database file lives: instance/finshield.db.")
line_ref("WTF_CSRF_ENABLED", "Turns on CSRF protection (explained in the security "
         "note at the end of this document) for every form on the site.")
line_ref("OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL", "Optional settings for "
         "FinBot's AI upgrade. If OPENAI_API_KEY is empty (the default), FinBot uses "
         "its built-in knowledge base instead - it never breaks either way.")
line_ref("ADMIN_EMAIL / ADMIN_PASSWORD", "The login used to create the first admin "
         "account automatically the first time the app runs.")
p("All of these read from 'environment variables' first (os.environ.get(...)), "
  "with a safe default if none is set. That's how you can change settings on a "
  "real server without editing code.")

# ---- database.py ----
chapter("database.py", "Connecting Flask to the database and login system")
p("This file sets up two tools and wires them into the app: SQLAlchemy (talks to "
  "the SQLite database) and Flask-Login (remembers who is logged in).")
line_ref("db = SQLAlchemy()", "Creates the database toolkit object that every "
         "model file (models.py) will use to define tables.")
line_ref("login_manager = LoginManager()", "Creates the login-tracking object. "
         "login_view tells it which page to send someone to if they try to view a "
         "login-only page without being logged in.")
line_ref("def init_db(app):", "Called once when the app starts. It connects both "
         "tools to the Flask app, imports models.py (so the database toolkit knows "
         "about every table), then creates any missing tables and seeds starter data.")
line_ref("def _seed_initial_data():", "Runs automatically on first start. It creates "
         "the default admin account (if one doesn't exist yet) and copies the 9 "
         "learning articles from learning_data.py into the Articles database table.")

# ---- models.py ----
chapter("models.py", "The shape of the database - six tables")
p("A 'model' is a Python class that becomes a database table. Each attribute on "
  "the class becomes a column. This keeps you from writing raw SQL by hand.")
h2("User")
p("One row per registered person: name, email, a hashed password (never the real "
  "password), occupation, city, whether they're an admin, and when they joined. "
  "set_password() scrambles a password before saving it; check_password() checks a "
  "typed password against that scramble without ever un-scrambling it. "
  "average_score is a computed shortcut used on the dashboard.")
h2("QuizResult")
p("One row per quiz attempt: which user, which category, score, total questions, "
  "percentage, how long it took, and when. Linked to User by user_id.")
h2("SurveyResponse")
p("One row per community survey submission: age, occupation, education, city, and "
  "four multiple-choice answers about UPI usage, investing, fraud experience, and "
  "financial knowledge. user_id is optional since the survey can be filled out "
  "anonymously (without logging in).")
h2("Article")
p("One row per learning topic (Savings, UPI Safety, etc.) - mainly used so the "
  "admin panel and database have a record of what content exists. The actual "
  "article text lives in learning_data.py, not in this table.")
h2("Feedback")
p("One row per message submitted through the Contact page.")
h2("ChatHistory")
p("One row per message sent to FinBot, storing both what the user asked and what "
  "FinBot answered, plus whether the answer came from the local knowledge base or "
  "a real AI model.")
h2("load_user(user_id)")
p("A small function Flask-Login calls automatically to look up 'who is this?' on "
  "every page request, using the ID stored in the browser's session cookie.")

# ---- utils.py ----
chapter("utils.py", "Small reusable helper functions")
line_ref("is_valid_email()", "Checks an email address roughly matches the "
         "name@domain.com shape using a regular expression.")
line_ref("is_valid_password()", "Requires at least 6 characters with at least one "
         "letter and one number.")
line_ref("sanitize_text()", "Trims whitespace and cuts text down to a maximum "
         "length before it's saved to the database - a basic safety net against "
         "someone submitting huge or messy form data.")
line_ref("admin_required", "A 'decorator' - you stick @admin_required above a route "
         "function and it automatically blocks anyone who isn't logged in as an "
         "admin, before the function's own code even runs.")
line_ref("grade_label()", "Turns a percentage score into a friendly label and "
         "Bootstrap color: 80%+ = Excellent (green), 60%+ = Good (blue), "
         "40%+ = Fair (yellow), below that = Needs Improvement (red).")

# ---- learning_data.py ----
chapter("learning_data.py", "All 9 learning articles, as plain data")
p("This file has no logic - it's just one big Python dictionary called "
  "LEARNING_ARTICLES. Each of the 9 topics (Savings, Digital Banking, UPI Safety, "
  "Cyber Security, Mutual Funds, Inflation, Insurance, Tax Basics, Budgeting) is a "
  "key, and its value holds the title, category, icon, a short summary, and four "
  "lists of text: explanation paragraphs, real-world examples, practical tips, and "
  "common mistakes.")
p("Keeping content as data (instead of writing it directly into HTML files) means "
  "one Jinja template (learning/article.html) can display any of the 9 topics just "
  "by looping over whichever dictionary entry was requested - so adding a 10th "
  "topic later only means adding one more dictionary entry, not a new page.")
p("LEARNING_CATEGORY_ORDER is a simple list controlling what order the topics "
  "appear in on the Learning page.")

# ---- quiz.py ----
chapter("quiz.py", "The quiz engine - 9 categories, scoring, and results")
h2("QUIZ_CATEGORIES")
p("A dictionary describing each of the 9 quiz categories - display name, icon, "
  "and accent color - used to build the category picker cards.")
h2("QUIZ_QUESTIONS")
p("A dictionary where each category maps to a list of question dictionaries. Each "
  "question has: q (the question text), options (a list of 4 possible answers), "
  "and answer (the index, 0-3, of the correct option in that list).")
h2("def categories():")
p("Handles the '/quiz/' page. It also looks up the logged-in user's most recent "
  "attempt in each category (if any) so the page can show 'Retake Quiz' instead "
  "of 'Start Quiz' where relevant.")
h2("def take_quiz(category):")
p("Handles loading one specific quiz, like '/quiz/upi'. It grabs that category's "
  "question list, records the start time in the session (used for the timer), and "
  "renders the quiz page. @login_required above it means only logged-in users can "
  "reach this - Flask-Login redirects anyone else to the login page automatically.")
h2("def submit_quiz(category):")
p("Handles the form submission when someone clicks 'Submit Quiz'. For each "
  "question it reads which option index the user picked from the submitted form "
  "data, compares it to the correct answer, and builds a 'review' list recording "
  "whether each answer was right or wrong. It totals the score, calculates a "
  "percentage, saves a new QuizResult row to the database, asks recommendation.py "
  "for suggested articles based on the score, and renders the result page.")
p("This is the exact function whose matching HTML template had the radio-button "
  "bug you found - the Python grading logic here was always correct; the bug was "
  "in how the form was drawn (see the quiz.html section under Part 2).")

# ---- recommendation.py ----
chapter("recommendation.py", "Rule-based 'AI' suggestions")
p("This is the recommendation engine mentioned in the project brief. It's called "
  "'rule-based' because it uses simple if/else logic rather than a trained "
  "machine-learning model - fast, predictable, and easy to explain, which is "
  "exactly what a quiz feedback feature needs.")
line_ref("CATEGORY_TO_ARTICLES", "A lookup table connecting each quiz category to "
         "the 1-2 learning articles most relevant to it - e.g. a low score in "
         "'cyber-fraud' points to the Cyber Security and UPI Safety articles.")
line_ref("get_recommendations_for_result()", "Called right after one quiz is "
         "graded. If the score is below 40%, it recommends the beginner Savings "
         "and Budgeting articles first. Then it always adds the articles matched "
         "to that quiz's category, and writes a short plain-English reason for "
         "each suggestion.")
line_ref("get_dashboard_recommendations()", "Called on the main Dashboard page. It "
         "looks across a user's entire quiz history, finds their 3 weakest "
         "categories (any scoring under 60%), and recommends articles for those - "
         "so the dashboard always points at whatever needs the most work.")

# ---- chatbot.py ----
chapter("chatbot.py", "FinBot - the AI assistant that can never crash")
h2("KNOWLEDGE_BASE")
p("A list of about 18 topic entries. Each has a list of trigger 'keywords' and a "
  "pre-written answer. For example, if a message contains 'upi', it matches the "
  "UPI entry and returns its answer.")
h2("get_local_answer(message)")
p("Lower-cases the user's message and checks it against every keyword in "
  "KNOWLEDGE_BASE. First match wins. If nothing matches, it returns a friendly "
  "FALLBACK_ANSWER listing what topics FinBot can actually help with.")
h2("get_llm_answer(message, ...)")
p("Only used if an OpenAI-compatible API key is configured. It sends the "
  "conversation to an external AI service over the internet and returns whatever "
  "it replies with.")
h2("get_bot_response(message)")
p("This is the important part for reliability. It first checks whether an API key "
  "exists. If yes, it TRIES the real AI service inside a try/except block - if "
  "that call fails for any reason (no internet, bad key, service down), the "
  "except silently catches the error and falls through to the local knowledge "
  "base instead of crashing the page. If no API key is set at all, it skips "
  "straight to the local knowledge base. Either way, the user always gets an "
  "answer.")
h2("chat_api()")
p("The route the chat page's JavaScript calls every time you send a message. It "
  "reads the JSON message from the request, asks get_bot_response() for a reply, "
  "saves the exchange to ChatHistory (wrapped in its own try/except so a database "
  "hiccup can't break the chat either), and sends the answer back as JSON.")

# ---- survey.py ----
chapter("survey.py", "The anonymous community survey")
p("This blueprint defines the fixed lists of allowed answers for each survey "
  "question (occupation, education, UPI usage frequency, investment experience, "
  "fraud experience, and knowledge level) as Python lists, then uses one route to "
  "handle both showing the form and processing its submission.")
h2("def survey_form():")
p("On a GET request (someone just visiting the page), it shows the empty form. "
  "On a POST request (the form was submitted), it reads every field, checks the "
  "age is realistic and that every dropdown answer is actually one of the allowed "
  "choices (this stops someone from tampering with the form and submitting a "
  "value that was never an option), and if anything is invalid, it re-shows the "
  "form with error messages instead of saving. If everything is valid, it creates "
  "a SurveyResponse row - linked to the current user if they're logged in, or left "
  "anonymous otherwise - and redirects to the thank-you page.")

# ---- routes.py ----
chapter("routes.py", "The main hub - most pages live here")
p("This is the biggest file. It defines the main_bp 'blueprint' (Flask's way of "
  "grouping related routes) and handles everything that isn't quiz-specific, "
  "survey-specific, or chatbot-specific: the landing page, login/register, "
  "dashboard, profile, learning articles, calculators, analytics, contact form, "
  "and the entire admin panel.")
h2("home() and faq()")
p("home() counts users, quizzes taken, survey responses, and articles, and passes "
  "those numbers to the landing page for the animated statistics section.")
h2("register() and login()")
p("register() validates the signup form (matching passwords, a real-looking "
  "email, a strong-enough password, and that the email isn't already taken), "
  "creates the User row with a hashed password, and logs them in immediately. "
  "login() looks up the account by email and uses user.check_password() to verify "
  "the password without ever storing or comparing it in plain text.")
h2("dashboard() and profile()")
p("dashboard() gathers the user's 5 most recent quiz results, their total quiz "
  "count, how many different categories they've tried, their average score, "
  "personalized recommendations, and whether they've completed the survey yet. "
  "profile() lets them update their name/occupation/city and shows their full "
  "quiz history.")
h2("learning_list() and learning_article(slug)")
p("learning_list() shows all 9 topics as cards. learning_article() looks up one "
  "topic by its 'slug' (the short id in the URL, like 'upi-safety') in the "
  "LEARNING_ARTICLES dictionary from learning_data.py; if the slug doesn't exist "
  "it returns a proper 404 Not Found page instead of crashing.")
h2("calculators()")
p("Just renders the calculators page - all six calculators actually run inside "
  "the browser using calculators.js, so this route doesn't need any special logic.")
h2("analytics()")
p("This is where Pandas (the data-analysis library from the tech stack) is used. "
  "It pulls every SurveyResponse row into a Pandas DataFrame (a table structure "
  "good for analysis), groups ages into buckets like '18-25' using pd.cut(), then "
  "counts how many responses fall into each category for six different questions "
  "(age, occupation, investment experience, UPI usage, fraud experience, "
  "knowledge level). Each count gets turned into the {labels, values} shape that "
  "Chart.js expects on the front end. It also computes an overall 'average "
  "awareness score' by mapping each knowledge level to a number (Beginner=25, "
  "Basic=50, Intermediate=75, Advanced=100) and averaging.")
h2("contact()")
p("Validates and saves messages from the Contact page into the Feedback table.")
h2("The admin_* routes")
p("Every one of these is wrapped in @admin_required, so Flask blocks non-admins "
  "before the function body even runs. They mostly follow the same pattern: fetch "
  "a list of records (users, quiz results, survey responses, or feedback) and "
  "render a table, with a matching admin_delete_* route that removes one record "
  "when the admin clicks the trash icon. admin_delete_user() has one extra safety "
  "check - it refuses to delete any account marked as admin, so you can't "
  "accidentally lock yourself out.")
h2("Error handlers")
p("Three small functions catch 404 (page not found), 403 (access denied), and 500 "
  "(server error) situations anywhere in the whole app and show a matching "
  "friendly page instead of an ugly default error screen.")

# ---- app.py ----
chapter("app.py", "The entry point - starts everything")
p("This is the file you actually run (python app.py). It's short on purpose - "
  "its job is just to wire all the other files together.")
line_ref("create_app()", "Builds the Flask application: loads settings from "
         "config.py, makes sure the instance/ folder exists, calls init_db() from "
         "database.py to set up the database and login system, turns on CSRF "
         "protection for the whole site, and then registers all four blueprints "
         "(main_bp, quiz_bp, survey_bp, chatbot_bp) so their routes become part of "
         "the live app.")
line_ref("csrf.exempt(chatbot_bp)", "The one deliberate exception: the chat API is "
         "excluded from CSRF checks because it's called via plain JavaScript "
         "fetch() requests (not an HTML form), and it only ever stores a chat "
         "message - never anything sensitive like money or account changes.")
line_ref("inject_globals()", "Makes 'current_year' and 'site_name' automatically "
         "available inside every single template, without having to pass them "
         "manually from every route - that's how the footer's copyright year "
         "updates itself.")
line_ref("if __name__ == \"__main__\":", "Only runs when you start the file "
         "directly (not when a production server like gunicorn imports it). It "
         "starts Flask's built-in development server on port 5000.")

# ===========================================================================
# PART 2 - TEMPLATES
# ===========================================================================
chapter("Part 2: The Face", "HTML templates (Jinja2)")
p("Every file in templates/ is HTML mixed with Jinja2 - a mini templating "
  "language that lets Python data flow into a page. Anything inside {{ double "
  "curly braces }} gets replaced with a real value; anything inside {% percent "
  "signs %} is logic, like loops and if-statements, that never shows up on the "
  "actual page.")

chapter("base.html", "The shared skeleton every page extends")
p("Almost every other template starts with {% extends \"base.html\" %}, which "
  "means: 'use this file's structure, and slot my own content into it.' base.html "
  "defines the parts that repeat on every page:")
bullet("The <head> section - loads Bootstrap 5, Bootstrap Icons, the Google Font, "
       "and your own style.css.")
bullet("The navbar - links to every section, changes what it shows depending on "
       "whether current_user.is_authenticated is true (Dashboard/Profile/Logout) "
       "or false (Login/Get Started), and adds an extra Admin link only if "
       "current_user.is_admin is true.")
bullet("The flash message area - loops over get_flashed_messages() so any "
       "success/error message set by a route (like 'Invalid email or password') "
       "appears as a dismissible colored banner.")
bullet("{% block content %}{% endblock %} - an empty placeholder. Every page that "
       "extends base.html fills this block with its own unique content.")
bullet("The footer and the floating FinBot chat button, shown on every page.")
p("Individual pages can also override {% block title %} (the browser tab text) "
  "and {% block extra_js %} (extra scripts only that one page needs, like "
  "quiz.js only loading on the quiz page).")

chapter("index.html", "The landing page")
p("This extends base.html and fills in one long page of sections stacked "
  "top to bottom: a Hero section with the tagline and a live-looking mock "
  "'Awareness Score' card, an animated Stats section (the numbers count up using "
  "counter.js when you scroll to them), About, Features (6 cards, generated by "
  "looping over a small Python-style list defined right in the template with "
  "{% set features = [...] %}), a Fraud Awareness section with warning cards, a "
  "call-to-action banner, an FAQ accordion, and a Contact preview.")

chapter("Auth Templates", "auth/register.html and auth/login.html")
p("Both are fairly short forms styled with the fs-auth-card class. Every form in "
  "this project includes a hidden input: <input type=\"hidden\" name=\"csrf_token\" "
  "value=\"{{ csrf_token() }}\">. This is the CSRF protection mentioned earlier - "
  "Flask-WTF generates a secret token per session, embeds it invisibly in the "
  "form, and rejects any submission that doesn't include the matching token. "
  "That stops a malicious website from tricking your browser into submitting a "
  "form to FinShield AI without you knowing.")
p("register.html includes name, email, occupation, city, password, and confirm "
  "password fields. login.html includes email, password, and a 'remember me' "
  "checkbox, plus a small hint showing the demo admin login.")

chapter("dashboard.html and profile.html", "Logged-in user pages")
p("dashboard.html shows four stat cards (quizzes taken, categories explored, "
  "average score, survey status), a table of recent quiz activity built by "
  "looping {% for r in results %}, and a recommendations panel built by looping "
  "over whatever recommendation.py returned. profile.html is a two-column layout: "
  "an editable form on the left, and the user's complete quiz history table on "
  "the right.")

chapter("Quiz Templates", "categories.html, quiz.html, result.html")
h2("quiz/categories.html")
p("Loops over the 9 QUIZ_CATEGORIES to draw one card per category, checking "
  "user_results (passed from quiz.py) to decide whether each card's button says "
  "'Start Quiz' or 'Retake Quiz'.")
h2("quiz/quiz.html")
p("This is the template with the bug you found and reported. It has two nested "
  "loops: an outer one over each question, and an inner one over that question's "
  "4 answer options. The fix was making sure each question's radio buttons get a "
  "unique name (q0, q1, q2... one per question) instead of accidentally reusing "
  "the inner loop's own counter (0-3, repeating for every question). It also "
  "includes a hidden JavaScript block passing TOTAL_QUESTIONS and "
  "TIME_PER_QUESTION into quiz.js for the countdown timer.")
h2("quiz/result.html")
p("Shows the score as a circular progress ring (drawn with a CSS conic-gradient "
  "trick, not an image), the recommended articles, and a full 'Answer Review' "
  "list - looping over the review list submit_quiz() built, highlighting the "
  "correct answer in green and, if the user got it wrong, their own wrong choice "
  "in red.")

chapter("Learning Templates", "learning/list.html and learning/article.html")
p("list.html loops over all 9 articles as clickable cards. article.html displays "
  "one article's explanation paragraphs, examples, tips, and common mistakes - "
  "each pulled straight from the matching entry in learning_data.py - plus a "
  "sidebar suggesting 3 other related articles.")

chapter("Survey Templates", "survey/survey.html and survey/thankyou.html")
p("survey.html builds dropdown menus directly from the option lists defined in "
  "survey.py (so the template and the backend validation always agree on what "
  "choices are allowed), and re-fills whatever the user already typed if the form "
  "had to be re-shown because of a validation error. thankyou.html is a simple "
  "confirmation page shown after a successful submission.")

chapter("analytics/dashboard.html", "The charts page")
p("Shows 4 summary stat cards, then 6 <canvas> elements (one per chart). The "
  "actual chart data computed by Pandas in routes.py is passed into the page as "
  "one Python dictionary using {{ chart_data | tojson }} - which safely converts "
  "it into a block of JavaScript that charts.js then reads to draw each chart "
  "with Chart.js.")

chapter("chatbot/chatbot.html", "The FinBot chat page")
p("A two-column layout: a sidebar with FinBot's avatar, a list of clickable "
  "suggested questions, and topic tags, next to the main chat window. It "
  "pre-loads any earlier chat history for a logged-in user, then hands control "
  "over to chatbot.js for everything that happens after the page loads.")

chapter("calculators/calculators.html", "The 6 calculators")
p("Uses Bootstrap's 'pills' tab component so all 6 calculators live on one page "
  "without a reload - clicking a tab just shows/hides a section. Each calculator "
  "is a simple form of number inputs plus a 'Calculate' button with an "
  "onclick=\"calcXxx()\" attribute that calls the matching function in "
  "calculators.js.")

chapter("contact.html and faq.html")
p("contact.html is a feedback form (pre-filling name/email automatically if "
  "you're logged in) next to a card reminding users this form is for feedback "
  "only, not fraud reporting. faq.html is a longer, dedicated version of the "
  "accordion also previewed on the landing page.")

chapter("Admin Templates", "dashboard.html, users.html, quiz_results.html, survey_results.html, feedback.html")
p("All five share the same fs-admin-tabs navigation strip at the top so the "
  "admin can jump between sections. Each list page (users/quiz results/survey "
  "responses/feedback) is a simple HTML table built by looping over the records "
  "routes.py fetched, with a small delete form (posting to a matching "
  "admin_delete_* route) in the last column of every row.")

chapter("Error Pages", "404.html, 403.html, 500.html")
p("Each is a short, on-brand page extending base.html, so even a broken link or "
  "permission error still looks like part of the site instead of a scary default "
  "browser error page.")

# ===========================================================================
# PART 3 - CSS & JS
# ===========================================================================
chapter("Part 3: Style and Behavior", "CSS and JavaScript")

chapter("static/css/style.css", "The entire visual design, in one file")
p("Every custom class in this project starts with fs- (short for FinShield) so "
  "it never clashes with Bootstrap's own class names. The file is organized into "
  "clearly labeled sections, from top to bottom:")
bullet(":root variables - all the theme colors (navy, blue, green), gradients, "
       "border-radius sizes, and shadow styles are defined ONCE at the top as CSS "
       "variables (like --fs-green-500), then reused everywhere with var(...). "
       "Changing the whole site's color scheme means editing values in one place.")
bullet("Navbar, Buttons, Hero, Stats, Sections, Feature Cards, Fraud Section, FAQ, "
       "Footer - one block per area of the landing page.")
bullet("Panels, Dashboard, Tables, Forms, Auth, Quiz, Learning, Calculators, "
       "Chatbot, Admin, Errors - one block per inner page.")
bullet("Glassmorphism effect - classes like .fs-glass-card use "
       "backdrop-filter: blur(...) combined with a semi-transparent background, "
       "which is what creates the frosted-glass look on the hero card.")
bullet("Animations - @keyframes blocks like fsFadeUp (sections sliding in) and "
       "fsPulse (the pulsing chat button) define the reusable animations.")
bullet("A responsive section at the very bottom using @media (max-width: 991px) "
       "to adjust spacing and layout for tablets/phones.")

chapter("static/js/main.js", "Runs on every page")
p("Loaded by base.html, so it runs everywhere. It does three small jobs: adds "
  "the 'scrolled' class to the navbar once you scroll down 40 pixels (which "
  "style.css uses to darken the navbar background), makes clicking any link with "
  "a # in it scroll smoothly instead of jumping instantly, and auto-dismisses "
  "flash alert banners after 6 seconds.")

chapter("static/js/counter.js", "Animated statistics on the landing page")
p("Uses an IntersectionObserver - a browser feature that watches an element and "
  "fires a callback the moment it scrolls into view. When a stat number scrolls "
  "into view for the first time, animateCounter() counts it up from 0 to its real "
  "value over about 1.4 seconds using requestAnimationFrame for a smooth, "
  "efficient animation, then stops observing that element so it only happens "
  "once.")

chapter("static/js/quiz.js", "The countdown timer and progress bar")
p("Reads TOTAL_QUESTIONS and TIME_PER_QUESTION (30 seconds each) from the quiz "
  "page and counts down from their product every second, updating the on-screen "
  "timer. If it reaches zero, it automatically submits whatever answers were "
  "selected so far. Separately, it listens for any radio button being changed, "
  "recalculates how many distinct questions have been answered (using a Set so "
  "each question only counts once even if you change your answer), and updates "
  "the green progress bar and the 'X of Y answered' counter live.")

chapter("static/js/chatbot.js", "The chat interface")
p("Listens for the chat form being submitted (or a suggested-question chip being "
  "clicked), immediately shows your message as a blue bubble, shows an animated "
  "'typing...' bubble with 3 bouncing dots, then sends your message to the "
  "/chatbot/api/message endpoint using fetch(). When the reply arrives, it "
  "removes the typing bubble and shows FinBot's real answer. escapeHtml() makes "
  "sure anything you type is displayed as plain text rather than being "
  "interpreted as HTML, which prevents a type of attack called script injection.")

chapter("static/js/calculators.js", "All six calculator formulas")
p("Pure math with no server involved - every calculation happens instantly in "
  "your browser. Each function reads its input boxes with getVal(), does the "
  "financial formula (written as a comment right above each function so the math "
  "is easy to check), and calls renderResult() to display a neat breakdown:")
bullet("Simple Interest: Interest = Principal x Rate x Time / 100")
bullet("Compound Interest: Amount = Principal x (1 + rate/n)^(n x time)")
bullet("EMI: the standard bank loan installment formula")
bullet("SIP: future value of investing a fixed amount every month")
bullet("Savings Goal: works the SIP formula backwards to find the monthly amount "
       "needed to hit a target")
bullet("Budget Planner: simple 50/30/20 split of monthly income")

chapter("static/js/charts.js", "Drawing the analytics charts")
p("Reads the CHART_DATA object that routes.py's analytics() function computed "
  "with Pandas and embedded into the page. makeBarChart() and makeDoughnutChart() "
  "are two small reusable functions that each build one Chart.js chart from a "
  "{labels, values} pair - bar charts for the age, investment, and fraud "
  "questions, and doughnut charts for occupation, UPI usage, and knowledge level.")

# ===========================================================================
# CLOSING - SECURITY + QUICK REFERENCE
# ===========================================================================
chapter("A Few Security Ideas You'll See Repeated", "Explained once, used everywhere")
h2("Password hashing")
p("Real passwords are never stored anywhere. set_password() runs the password "
  "through a one-way scrambling function (Werkzeug's generate_password_hash). "
  "Logging in re-scrambles the typed password the same way and compares the "
  "scrambles - so even if the database were stolen, the actual passwords "
  "couldn't be recovered from it.")
h2("CSRF tokens")
p("A hidden, unique, per-session value in every form (the {{ csrf_token() }} you "
  "saw across templates). It stops a malicious website from silently submitting "
  "forms to FinShield AI on your behalf without your knowledge.")
h2("Server-side validation")
p("Every form is checked again in Python (routes.py, survey.py) even though the "
  "HTML also has basic checks like required. Browser-side checks are only a "
  "convenience - they can be bypassed, so the real safety net always lives on "
  "the server.")
h2("The ORM instead of raw SQL")
p("Every database query in this project goes through SQLAlchemy "
  "(User.query.filter_by(...), etc.) instead of writing raw SQL text. This "
  "automatically protects against SQL injection, a common attack where "
  "malicious text typed into a form could otherwise manipulate the database.")

chapter("Quick Reference", "Where to look when you want to change something")
bullet("Change quiz questions -> quiz.py, the QUIZ_QUESTIONS dictionary")
bullet("Change or add a learning article -> learning_data.py")
bullet("Change FinBot's built-in answers -> chatbot.py, the KNOWLEDGE_BASE list")
bullet("Change colors/fonts/spacing -> static/css/style.css, the :root section at "
       "the top")
bullet("Change the admin login -> config.py, ADMIN_EMAIL / ADMIN_PASSWORD (or set "
       "them as environment variables)")
bullet("Add a brand-new page -> add a route function in routes.py, add a matching "
       "template in templates/, add a link in templates/base.html's navbar")
bullet("Change a calculator's formula -> static/js/calculators.js")

pdf.output("FinShield_AI_Explained.pdf")
print("PDF generated: FinShield_AI_Explained.pdf")
