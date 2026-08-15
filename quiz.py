import time

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_required, current_user

from database import db
from models import QuizResult
from utils import grade_label
from recommendation import get_recommendations_for_result

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")

QUIZ_CATEGORIES = {
    "savings": {"name": "Savings", "icon": "bi-piggy-bank", "color": "#10b981"},
    "upi": {"name": "UPI & Digital Payments", "icon": "bi-phone", "color": "#0ea5e9"},
    "cyber-fraud": {"name": "Cyber Fraud", "icon": "bi-shield-exclamation", "color": "#ef4444"},
    "investment": {"name": "Investment", "icon": "bi-graph-up-arrow", "color": "#f59e0b"},
    "insurance": {"name": "Insurance", "icon": "bi-umbrella", "color": "#8b5cf6"},
    "mutual-funds": {"name": "Mutual Funds", "icon": "bi-pie-chart", "color": "#06b6d4"},
    "inflation": {"name": "Inflation", "icon": "bi-graph-down-arrow", "color": "#f97316"},
    "budget": {"name": "Budgeting", "icon": "bi-wallet2", "color": "#22c55e"},
    "tax": {"name": "Tax Basics", "icon": "bi-receipt", "color": "#3b82f6"},
}

QUIZ_QUESTIONS = {
    "savings": [
        {"q": "What is the primary purpose of an emergency fund?", "options": ["To buy luxury items", "To cover unexpected expenses like medical bills or job loss", "To invest in stocks", "To pay regular monthly bills"], "answer": 1},
        {"q": "How many months of expenses should an ideal emergency fund cover?", "options": ["1 month", "3-6 months", "12-18 months", "No need for one"], "answer": 1},
        {"q": "Which account typically offers the highest liquidity for savings?", "options": ["Fixed Deposit", "Savings Account", "Real Estate", "Mutual Fund Lock-in"], "answer": 1},
        {"q": "What does 'paying yourself first' mean?", "options": ["Spending on yourself before saving", "Setting aside savings before spending on other things", "Taking a salary advance", "Investing all your income"], "answer": 1},
        {"q": "Which of these is a benefit of compound interest on savings?", "options": ["Interest is earned only once", "Interest earns interest over time, growing savings faster", "It reduces your principal", "It only applies to loans"], "answer": 1},
        {"q": "A recurring deposit (RD) is best suited for?", "options": ["One-time lump sum investment", "Disciplined monthly saving over a fixed tenure", "High-risk trading", "Daily withdrawals"], "answer": 1},
        {"q": "What is a realistic first savings goal for a beginner?", "options": ["Buying a house in cash", "Building a small emergency fund", "Retiring early", "Becoming a day trader"], "answer": 1},
        {"q": "Which habit most helps long-term saving?", "options": ["Impulse buying", "Automating transfers to a savings account", "Ignoring your budget", "Using only credit cards"], "answer": 1},
    ],
    "upi": [
        {"q": "UPI stands for?", "options": ["Unified Payments Interface", "Universal Product Identity", "United Public Investment", "Unique Payment ID"], "answer": 0},
        {"q": "What should you NEVER share to keep your UPI account safe?", "options": ["Your UPI ID", "Your registered mobile number", "Your UPI PIN or OTP", "Your bank's name"], "answer": 2},
        {"q": "To receive money via UPI, do you need to enter your UPI PIN?", "options": ["Yes, always", "No, PIN is only required to send/pay money", "Only on weekends", "Only for amounts above ₹10,000"], "answer": 1},
        {"q": "A QR code scam typically tricks victims into?", "options": ["Receiving money safely", "Scanning a code that actually authorizes a payment OUT of their account", "Getting a cashback instantly", "Blocking their SIM card"], "answer": 1},
        {"q": "What is the safest way to verify a UPI payment request?", "options": ["Trust any request from an unknown number", "Check the payee name and amount carefully before entering PIN", "Always approve to avoid conflict", "Ignore the app's confirmation screen"], "answer": 1},
        {"q": "If you get a call claiming to be your bank asking for your UPI PIN, you should?", "options": ["Share it since it's your bank", "Never share it — banks never ask for PIN/OTP over calls", "Share only the last 2 digits", "Ask them to call back later"], "answer": 1},
        {"q": "What does 'collect request' in UPI mean?", "options": ["Someone is sending you money automatically", "Someone is requesting you to pay them — approving it deducts money from you", "It's a free reward", "It cancels a past transaction"], "answer": 1},
        {"q": "Which is a good UPI security practice?", "options": ["Using the same PIN as your phone lock", "Enabling app lock and reviewing transaction alerts regularly", "Sharing your screen during any call", "Disabling transaction SMS alerts"], "answer": 1},
    ],
    "cyber-fraud": [
        {"q": "Phishing attacks typically try to steal information via?", "options": ["Fake emails, messages or websites impersonating trusted entities", "Physical mail only", "In-person meetings", "Television ads"], "answer": 0},
        {"q": "What is 'vishing'?", "options": ["Video-based phishing", "Voice call phishing to trick victims into revealing info", "A type of antivirus", "A safe banking app"], "answer": 1},
        {"q": "If you receive an SMS with a suspicious link claiming you won a prize, you should?", "options": ["Click it immediately", "Avoid clicking and verify through official channels", "Forward it to friends", "Reply with your bank details"], "answer": 1},
        {"q": "What is a strong password practice?", "options": ["Using 'password123' everywhere", "Using long, unique passwords with a mix of characters for each account", "Sharing passwords with coworkers", "Never changing passwords"], "answer": 1},
        {"q": "Two-Factor Authentication (2FA) helps by?", "options": ["Removing the need for passwords", "Adding an extra verification step beyond just a password", "Slowing down your login unnecessarily", "Making accounts less secure"], "answer": 1},
        {"q": "'Screen sharing scams' trick victims into installing apps that let fraudsters?", "options": ["Improve phone battery life", "View and control the victim's screen to steal banking info", "Backup photos safely", "Speed up the internet"], "answer": 1},
        {"q": "What should you do if you fall victim to a fraud transaction?", "options": ["Wait a few months to report", "Immediately report to your bank and file a complaint on cybercrime.gov.in / 1930 helpline", "Do nothing", "Only tell friends"], "answer": 1},
        {"q": "Fake job offer or lottery scams usually ask victims to?", "options": ["Provide identity documents for free registration", "Pay an upfront 'processing fee' before receiving a prize/job", "Visit a government office", "Nothing, they are free"], "answer": 1},
        {"q": "Which is a red flag of a fraudulent investment scheme?", "options": ["Registered with SEBI", "Promises guaranteed unusually high returns with no risk", "Transparent fee structure", "Publicly available disclosures"], "answer": 1},
    ],
    "investment": [
        {"q": "What is diversification in investing?", "options": ["Putting all money into one stock", "Spreading investments across different assets to reduce risk", "Avoiding investments completely", "Only investing in gold"], "answer": 1},
        {"q": "Which generally carries higher risk?", "options": ["Fixed Deposits", "Government Bonds", "Equity/Stocks", "Savings Account"], "answer": 2},
        {"q": "What does 'risk-return tradeoff' mean?", "options": ["Higher potential returns usually come with higher risk", "Risk and return are unrelated", "Lower risk always means higher return", "Returns are guaranteed regardless of risk"], "answer": 0},
        {"q": "What is the power of compounding best described as?", "options": ["Earning returns only on your principal", "Earning returns on both principal and previously earned returns", "A one-time bonus", "A type of tax"], "answer": 1},
        {"q": "SEBI is the regulator for?", "options": ["Banking sector", "Securities and stock markets in India", "Insurance sector", "Telecom sector"], "answer": 1},
        {"q": "Before investing, one should primarily consider?", "options": ["Only friends' advice", "Financial goals, risk appetite, and time horizon", "Social media trends only", "Random stock tips"], "answer": 1},
        {"q": "What is a 'bull market'?", "options": ["A market with falling prices", "A market with rising prices and investor optimism", "A market that is closed", "A type of bond"], "answer": 1},
        {"q": "Long-term investing generally benefits from?", "options": ["Panic selling during dips", "Compounding and riding out short-term volatility", "Daily buying and selling", "Ignoring your portfolio forever"], "answer": 1},
    ],
    "insurance": [
        {"q": "What is the main purpose of insurance?", "options": ["To guarantee profits", "To transfer financial risk of unexpected events to an insurer", "To avoid paying taxes", "To replace savings"], "answer": 1},
        {"q": "Term life insurance primarily provides?", "options": ["Investment returns with guaranteed maturity bonus", "Pure life cover for a fixed term at low premium", "Health checkups only", "Car repair coverage"], "answer": 1},
        {"q": "Health insurance typically helps cover?", "options": ["Grocery bills", "Medical treatment and hospitalization expenses", "Vacation costs", "Home renovation"], "answer": 1},
        {"q": "What is a 'premium' in insurance?", "options": ["The payout you receive after a claim", "The amount you pay periodically to keep the policy active", "A bonus given by the insurer", "A tax deduction only"], "answer": 1},
        {"q": "What is a 'claim' in insurance?", "options": ["A request to the insurer for payment after a covered event", "The premium amount", "The policy document", "An agent's commission"], "answer": 0},
        {"q": "Why should you disclose accurate information when buying insurance?", "options": ["It doesn't matter", "Non-disclosure can lead to claim rejection", "It increases premium always", "It's only needed for large policies"], "answer": 1},
        {"q": "What does 'sum insured' mean?", "options": ["The premium paid every year", "The maximum amount the insurer will pay under the policy", "The agent's fee", "The policy start date"], "answer": 1},
    ],
    "mutual-funds": [
        {"q": "A mutual fund pools money from investors to invest in?", "options": ["A single stock only", "A diversified portfolio of stocks, bonds or other assets", "Real estate only", "Gold only"], "answer": 1},
        {"q": "What is NAV in mutual funds?", "options": ["Net Asset Value — per-unit value of the fund", "New Account Verification", "National Average Value", "Nominal Annual Value"], "answer": 0},
        {"q": "SIP stands for?", "options": ["Single Investment Plan", "Systematic Investment Plan", "Stock Index Portfolio", "Secure Income Program"], "answer": 1},
        {"q": "Who manages the investment decisions of a mutual fund?", "options": ["Each individual investor", "A professional fund manager", "The government", "The stock exchange"], "answer": 1},
        {"q": "Equity mutual funds primarily invest in?", "options": ["Stocks/shares of companies", "Only fixed deposits", "Only gold", "Only cash"], "answer": 0},
        {"q": "What is an 'expense ratio' in mutual funds?", "options": ["The annual fee charged by the fund for management", "The total returns guaranteed", "A one-time entry fee only", "The tax on withdrawal"], "answer": 0},
        {"q": "Debt mutual funds generally carry _____ risk compared to equity funds.", "options": ["Higher", "Lower", "Equal", "Unrelated"], "answer": 1},
    ],
    "inflation": [
        {"q": "Inflation refers to?", "options": ["A general decrease in prices over time", "A general increase in prices reducing purchasing power over time", "A fixed exchange rate", "A type of tax refund"], "answer": 1},
        {"q": "Which of these best protects savings from inflation over the long term?", "options": ["Keeping cash under a mattress", "Investments that historically outpace inflation, like equities", "Never saving at all", "Spending everything immediately"], "answer": 1},
        {"q": "If inflation is 6% and your savings account gives 3% interest, your real return is?", "options": ["+9%", "+3%", "-3%", "0%"], "answer": 2},
        {"q": "Who typically measures and reports inflation in India?", "options": ["RBI and government statistical agencies (via CPI/WPI)", "Individual banks", "Private companies only", "Stock exchanges"], "answer": 0},
        {"q": "What is 'purchasing power'?", "options": ["The amount of goods/services money can buy", "The interest rate on loans", "The stock market index", "A type of bank account"], "answer": 0},
        {"q": "High and unpredictable inflation generally makes financial planning?", "options": ["Easier", "Harder, as future costs become uncertain", "Irrelevant", "Guaranteed profitable"], "answer": 1},
    ],
    "budget": [
        {"q": "What is a budget?", "options": ["A plan to track and manage income and expenses", "A type of loan", "A government tax", "A stock market term"], "answer": 0},
        {"q": "The 50-30-20 rule suggests allocating income to?", "options": ["50% needs, 30% wants, 20% savings/debt repayment", "50% wants, 30% needs, 20% gifts", "100% needs, 0% savings", "50% savings only"], "answer": 0},
        {"q": "Tracking expenses helps you primarily?", "options": ["Identify spending patterns and cut unnecessary costs", "Increase impulse purchases", "Avoid saving money", "Ignore financial goals"], "answer": 0},
        {"q": "A 'fixed expense' is one that?", "options": ["Changes every month unpredictably", "Stays roughly the same each month, like rent or EMI", "Never has to be paid", "Only occurs once a year"], "answer": 1},
    ],
    "tax": [
        {"q": "What is income tax?", "options": ["A tax on goods purchased", "A tax levied by the government on individual/business income", "A fee for opening a bank account", "A charge for using UPI"], "answer": 1},
        {"q": "In India, which section is commonly used for tax-saving investments (like PPF, ELSS)?", "options": ["Section 80C", "Section 420", "Section 144", "Section 302"], "answer": 0},
        {"q": "What is a 'tax deduction'?", "options": ["An amount subtracted from taxable income to reduce tax liability", "A penalty for late filing", "A type of refund only for businesses", "A tax on savings accounts"], "answer": 0},
        {"q": "Filing an Income Tax Return (ITR) is generally required when?", "options": ["Never, it's optional for everyone", "Income exceeds the basic exemption limit set by law", "Only if you are a business owner", "Only once in a lifetime"], "answer": 1},
        {"q": "GST (Goods and Services Tax) is a type of?", "options": ["Direct tax on income", "Indirect tax on the supply of goods and services", "Tax only on salaries", "Tax refund scheme"], "answer": 1},
        {"q": "What is TDS?", "options": ["Tax Deducted at Source, withheld by the payer before payment", "A type of savings account", "A stock market index", "A government subsidy"], "answer": 0},
    ],
}

# Clean up any malformed placeholder entries defensively (defensive data hygiene)
QUIZ_QUESTIONS["budget"] = [
    {"q": "What is a budget?", "options": ["A plan to track and manage income and expenses", "A type of loan", "A government tax", "A stock market term"], "answer": 0},
    {"q": "The 50-30-20 rule suggests allocating income to?", "options": ["50% needs, 30% wants, 20% savings/debt repayment", "50% wants, 30% needs, 20% gifts", "100% needs, 0% savings", "50% savings only"], "answer": 0},
    {"q": "Tracking expenses helps you primarily?", "options": ["Identify spending patterns and cut unnecessary costs", "Increase impulse purchases", "Avoid saving money", "Ignore financial goals"], "answer": 0},
    {"q": "A 'fixed expense' is one that?", "options": ["Changes every month unpredictably", "Stays roughly the same each month, like rent or EMI", "Never has to be paid", "Only occurs once a year"], "answer": 1},
    {"q": "What is a good first step to start budgeting?", "options": ["List all sources of income and monthly expenses", "Spend first, plan later", "Ignore small purchases", "Borrow to cover a shortfall"], "answer": 0},
    {"q": "A 'discretionary expense' refers to?", "options": ["A mandatory bill like rent", "Optional, non-essential spending like dining out or entertainment", "Loan repayment", "Insurance premium"], "answer": 1},
    {"q": "What does a budget surplus mean?", "options": ["Expenses exceed income", "Income exceeds expenses", "Income equals zero", "Expenses are unknown"], "answer": 1},
]


def get_category_meta(category_key):
    return QUIZ_CATEGORIES.get(category_key)


@quiz_bp.route("/")
def categories():
    user_results = {}
    if current_user.is_authenticated:
        for r in current_user.quiz_results:
            if r.category not in user_results or r.taken_at > user_results[r.category].taken_at:
                user_results[r.category] = r
    return render_template("quiz/categories.html", categories=QUIZ_CATEGORIES, user_results=user_results)


@quiz_bp.route("/<category>", methods=["GET"])
@login_required
def take_quiz(category):
    if category not in QUIZ_QUESTIONS:
        abort(404)
    questions = QUIZ_QUESTIONS[category]
    meta = QUIZ_CATEGORIES[category]
    session[f"quiz_start_{category}"] = time.time()
    return render_template(
        "quiz/quiz.html",
        category=category,
        meta=meta,
        questions=questions,
        time_per_question=30,
    )


@quiz_bp.route("/<category>/submit", methods=["POST"])
@login_required
def submit_quiz(category):
    if category not in QUIZ_QUESTIONS:
        abort(404)
    questions = QUIZ_QUESTIONS[category]

    score = 0
    review = []
    for idx, q in enumerate(questions):
        selected = request.form.get(f"q{idx}")
        selected_idx = int(selected) if selected is not None and selected != "" else None
        is_correct = selected_idx == q["answer"]
        if is_correct:
            score += 1
        review.append({
            "question": q["q"],
            "options": q["options"],
            "correct": q["answer"],
            "selected": selected_idx,
            "is_correct": is_correct,
        })

    total = len(questions)
    percentage = round((score / total) * 100, 1) if total else 0

    start_time = session.pop(f"quiz_start_{category}", None)
    time_taken = int(time.time() - start_time) if start_time else None

    result = QuizResult(
        user_id=current_user.id,
        category=category,
        score=score,
        total_questions=total,
        percentage=percentage,
        time_taken=time_taken,
    )
    db.session.add(result)
    db.session.commit()

    label, color = grade_label(percentage)
    recommendations = get_recommendations_for_result(category, percentage)

    return render_template(
        "quiz/result.html",
        category=category,
        meta=QUIZ_CATEGORIES[category],
        score=score,
        total=total,
        percentage=percentage,
        label=label,
        color=color,
        review=review,
        recommendations=recommendations,
        time_taken=time_taken,
    )
