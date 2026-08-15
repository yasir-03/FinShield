# FinShield AI

**Learn • Analyze • Prevent • Protect**

FinShield AI is an AI-powered Financial Literacy and Digital Fraud Awareness platform, built as a Community Engagement Project (CEP). It educates users on financial literacy, digital banking safety, cyber fraud awareness, and basic investment knowledge, while anonymously collecting community survey data for analysis.

---

## Features

- **Landing Page** — Hero, About, Features, Stats, Fraud Awareness, FAQ, Contact
- **Authentication** — Register, Login, Logout, Profile, hashed passwords, session management
- **User Dashboard** — Quiz scores, progress, recommendations, recent activity
- **Quiz Module** — 9 categories (Savings, UPI, Cyber Fraud, Investment, Insurance, Mutual Funds, Inflation, Budget, Tax), timed MCQs, instant scoring, answer review
- **Learning Module** — 9 in-depth articles with explanations, examples, tips, and common mistakes
- **Community Survey** — Anonymous data collection (age, occupation, education, city, UPI usage, investment experience, fraud experience, financial knowledge)
- **Analytics Dashboard** — Chart.js visualizations powered by Pandas-aggregated survey data
- **AI Recommendation Engine** — Rule-based, personalized learning suggestions based on quiz performance
- **FinBot AI Chatbot** — Built-in knowledge base with automatic fallback; uses an OpenAI-compatible LLM if `OPENAI_API_KEY` is configured
- **Calculators** — Simple Interest, Compound Interest, EMI, SIP, Savings Goal, Budget Planner
- **Contact Page** — Feedback form, FAQ
- **Admin Panel** — Manage users, quiz results, survey responses, and feedback

---

## Tech Stack

| Layer            | Technology                          |
|------------------|--------------------------------------|
| Backend          | Python, Flask                        |
| Database         | SQLite (via Flask-SQLAlchemy)        |
| Auth             | Flask-Login, Werkzeug password hashing |
| Frontend         | HTML5, CSS3, Bootstrap 5, JavaScript |
| Templating       | Jinja2                               |
| Charts           | Chart.js                             |
| Data Analysis    | Pandas                               |
| Data Viz (future)| Plotly                               |
| ML (future-ready)| Scikit-learn                         |
| AI Chatbot       | OpenAI-compatible API with local fallback |
| Security         | Flask-WTF (CSRF), input validation, parameterized ORM queries |

---

## Project Structure

```
FinShield-AI/
├── app.py                 # Flask app factory & entrypoint
├── config.py               # App configuration
├── database.py             # SQLAlchemy/Flask-Login init + seeding
├── models.py                # Database models (User, QuizResult, SurveyResponse, Article, Feedback, ChatHistory)
├── routes.py                 # Main site routes (home, auth, dashboard, learning, calculators, analytics, admin, contact)
├── quiz.py                    # Quiz blueprint: categories, questions, scoring
├── learning_data.py             # Learning module article content
├── recommendation.py             # Rule-based AI recommendation engine
├── survey.py                      # Community survey blueprint
├── chatbot.py                      # FinBot blueprint: knowledge base + LLM integration
├── utils.py                         # Validation helpers, decorators
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html                    # Shared layout: navbar, footer, flash messages
│   ├── index.html                    # Landing page
│   ├── dashboard.html
│   ├── profile.html
│   ├── contact.html
│   ├── faq.html
│   ├── auth/                          # register.html, login.html
│   ├── learning/                       # list.html, article.html
│   ├── quiz/                            # categories.html, quiz.html, result.html
│   ├── survey/                           # survey.html, thankyou.html
│   ├── analytics/                         # dashboard.html
│   ├── chatbot/                            # chatbot.html
│   ├── calculators/                         # calculators.html
│   ├── admin/                                # dashboard, users, quiz_results, survey_results, feedback
│   └── errors/                                # 403.html, 404.html, 500.html
├── static/
│   ├── css/style.css                          # Full design system (theme, components, animations)
│   ├── js/                                     # main.js, counter.js, quiz.js, chatbot.js, calculators.js, charts.js
│   ├── images/
│   └── uploads/
├── database/                                    # (reserved for exported data/backups)
└── instance/
    └── finshield.db                              # SQLite database (auto-created on first run)
```

---

## Installation

### Requirements

- Python 3.10+
- pip

### Setup

1. Navigate to the project folder:
   ```
   cd FinShield-AI
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. (Optional) Configure environment variables for a real AI chatbot backend:
   ```
   set OPENAI_API_KEY=your_api_key_here      # Windows
   export OPENAI_API_KEY=your_api_key_here   # macOS/Linux
   ```
   If not set, FinBot automatically uses its built-in knowledge base — it never crashes.

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser at:
   ```
   http://localhost:5000
   ```

The SQLite database (`instance/finshield.db`) and all tables are created automatically on first run, along with a default admin account:

- **Email:** `admin@finshield.ai`
- **Password:** `Admin@123`

(Change these via the `ADMIN_EMAIL` / `ADMIN_PASSWORD` environment variables before first run in production.)

---

## Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` (never stored in plain text)
- All forms are protected with CSRF tokens via Flask-WTF
- All database queries use the SQLAlchemy ORM (parameterized, no raw SQL injection risk)
- Server-side input validation on registration, login, survey, and contact forms
- Admin-only routes are protected via a custom `@admin_required` decorator

---

## Screenshots

_Add screenshots of the landing page, dashboard, quiz, analytics, and chatbot here._

```
[ Landing Page Screenshot ]
[ Dashboard Screenshot ]
[ Quiz Screenshot ]
[ Analytics Dashboard Screenshot ]
[ FinBot Chatbot Screenshot ]
```

---

## License

Built for educational and community engagement purposes.
