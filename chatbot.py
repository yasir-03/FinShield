"""FinBot — FinShield AI's financial literacy chatbot.

Uses a built-in keyword-matched knowledge base by default. If an
OpenAI-compatible API key is configured, it will attempt to use the LLM
first and gracefully fall back to the local knowledge base on any error,
so the chatbot never crashes and never leaves the user without an answer.
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import current_user

from database import db
from models import ChatHistory

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")

SYSTEM_PROMPT = (
    "You are FinBot, the friendly financial literacy assistant for FinShield AI, "
    "a financial literacy and digital fraud awareness platform. Answer questions about "
    "savings, budgeting, inflation, UPI, digital banking, cyber fraud, mutual funds, "
    "insurance, investment, RBI, SEBI, financial planning, emergency funds, loans, and "
    "credit scores. Keep answers concise, beginner-friendly, and practical. Never give "
    "specific stock picks or guaranteed-return promises. If asked about anything unrelated "
    "to personal finance or fraud safety, politely redirect to financial topics."
)

# Knowledge base: each entry has trigger keywords and a canned, well-written answer.
KNOWLEDGE_BASE = [
    {
        "keywords": ["saving", "savings", "save money", "emergency fund"],
        "answer": "Saving means setting aside part of your income for future needs instead of spending it all now. A great starting point is building an emergency fund covering 3-6 months of expenses, kept in a liquid savings account. Try automating a fixed transfer to savings right when you get paid — it's called 'paying yourself first'.",
    },
    {
        "keywords": ["budget", "budgeting", "spending plan"],
        "answer": "A budget helps you plan how you'll spend and save your income. A popular framework is the 50-30-20 rule: 50% of income on needs, 30% on wants, and 20% on savings/debt repayment. Try our Budget Planner calculator to build your own!",
    },
    {
        "keywords": ["inflation"],
        "answer": "Inflation is the general rise in prices over time, which reduces how much your money can buy in the future. To protect against it, avoid keeping too much idle cash — consider investments that historically outpace inflation, like equity mutual funds, for long-term goals.",
    },
    {
        "keywords": ["upi", "unified payments"],
        "answer": "UPI (Unified Payments Interface) lets you transfer money instantly between bank accounts using a mobile app. Key safety rule: you NEVER need to enter your UPI PIN to RECEIVE money — only to SEND it. Any 'collect request' asking for your PIN to 'get' money is likely a scam.",
    },
    {
        "keywords": ["digital banking", "net banking", "mobile banking", "banking app"],
        "answer": "Digital banking lets you manage your money via websites or apps — checking balances, transferring funds, and paying bills without visiting a branch. Always download banking apps only from official app stores, and never use public Wi-Fi for banking transactions.",
    },
    {
        "keywords": ["fraud", "scam", "phishing", "cyber", "vishing", "smishing", "hacked", "hack"],
        "answer": "Cyber fraud often uses phishing (fake emails/websites), vishing (scam calls), or smishing (scam SMS) to steal your money or data. Remember: banks NEVER ask for your PIN, OTP, or CVV over calls, SMS, or email. If you're ever defrauded, report immediately at cybercrime.gov.in or call the 1930 helpline.",
    },
    {
        "keywords": ["mutual fund", "sip", "systematic investment"],
        "answer": "A mutual fund pools money from many investors to invest in a diversified portfolio managed by professionals. SIP (Systematic Investment Plan) lets you invest a fixed amount regularly — a great way to build long-term wealth with discipline. Try our SIP Calculator to estimate your returns!",
    },
    {
        "keywords": ["insurance", "term plan", "health insurance", "life insurance"],
        "answer": "Insurance transfers financial risk (like death, illness, or accidents) to an insurance company in exchange for a premium. Term life insurance offers pure protection at low cost, while health insurance protects your savings from being wiped out by medical bills. Buy early — premiums are cheaper when you're young and healthy.",
    },
    {
        "keywords": ["investment", "invest", "stocks", "equity", "share market"],
        "answer": "Investing means putting money into assets (stocks, bonds, mutual funds) with the goal of growing it over time. Key principles: diversify across assets, match your risk to your time horizon, and think long-term rather than chasing quick gains. Higher potential returns generally come with higher risk.",
    },
    {
        "keywords": ["rbi", "reserve bank"],
        "answer": "The RBI (Reserve Bank of India) is India's central bank. It regulates the banking system, controls monetary policy (like interest rates), manages inflation, and issues currency. It also protects consumers by regulating banks and NBFCs.",
    },
    {
        "keywords": ["sebi", "securities and exchange"],
        "answer": "SEBI (Securities and Exchange Board of India) is the regulator for India's securities and stock markets. It protects investors, ensures fair practices by brokers and mutual funds, and takes action against fraud in the markets. Always check that an investment platform is SEBI-registered.",
    },
    {
        "keywords": ["financial planning", "financial plan", "plan my finances"],
        "answer": "Financial planning means setting clear goals (short, medium, long-term), budgeting your income, building an emergency fund, getting adequate insurance, and then investing systematically toward your goals. Start with our Learning Modules and Calculators to build your personalized plan!",
    },
    {
        "keywords": ["loan", "emi", "borrow", "borrowing"],
        "answer": "A loan lets you borrow money that you repay over time with interest, usually via EMI (Equated Monthly Installments). Before taking a loan, compare interest rates, check the total cost over the loan tenure, and ensure your EMI doesn't exceed roughly 30-40% of your monthly income. Try our EMI Calculator!",
    },
    {
        "keywords": ["credit score", "cibil"],
        "answer": "A credit score (like CIBIL in India) is a number (usually 300-900) reflecting your creditworthiness based on your repayment history. A higher score gets you better loan interest rates. Improve it by paying bills/EMIs on time, keeping credit card usage low, and avoiding too many loan applications at once.",
    },
    {
        "keywords": ["tax", "income tax", "itr", "80c"],
        "answer": "Income tax is levied by the government on your income. You can reduce taxable income through deductions like Section 80C (PPF, ELSS, life insurance, up to ₹1.5 lakh in India). Filing your Income Tax Return (ITR) on time is a legal requirement once income crosses the exemption limit, and it also helps with loan/visa applications.",
    },
    {
        "keywords": ["quiz", "test my knowledge"],
        "answer": "You can test your financial knowledge in our Quiz section! We have quizzes on Savings, UPI, Cyber Fraud, Investment, Insurance, Mutual Funds, Inflation, Budgeting, and Tax. After each quiz, you'll get a personalized recommendation based on your score.",
    },
    {
        "keywords": ["calculator", "emi calculator", "sip calculator", "interest calculator"],
        "answer": "We offer several calculators: Simple Interest, Compound Interest, EMI, SIP, Savings Goal, and Budget Planner. You'll find them all in the Calculators section — just enter your numbers and get instant results!",
    },
    {
        "keywords": ["hello", "hi", "hey", "namaste"],
        "answer": "Hello! I'm FinBot, your financial literacy assistant. Ask me about savings, budgeting, UPI safety, cyber fraud, investments, insurance, and more!",
    },
    {
        "keywords": ["thank", "thanks"],
        "answer": "You're welcome! Feel free to ask me anything else about personal finance or digital safety.",
    },
]

FALLBACK_ANSWER = (
    "I'm not fully sure about that one yet, but I can help with savings, budgeting, inflation, "
    "UPI safety, digital banking, cyber fraud, mutual funds, insurance, investments, RBI, SEBI, "
    "financial planning, loans, and credit scores. Try asking about one of these topics!"
)

SUGGESTED_QUESTIONS = [
    "What is an emergency fund?",
    "How can I stay safe from UPI fraud?",
    "What is a SIP?",
    "How does inflation affect my savings?",
    "What is a good credit score?",
    "What does SEBI do?",
]


def get_local_answer(message):
    text = message.lower()
    for entry in KNOWLEDGE_BASE:
        if any(keyword in text for keyword in entry["keywords"]):
            return entry["answer"]
    return FALLBACK_ANSWER


def get_llm_answer(message, api_key, base_url, model):
    """Attempt to use an OpenAI-compatible chat completion endpoint."""
    import requests

    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            "max_tokens": 300,
            "temperature": 0.4,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def get_bot_response(message):
    """Returns (answer, source) where source is 'llm' or 'local'. Never raises."""
    api_key = current_app.config.get("OPENAI_API_KEY")
    if api_key:
        try:
            answer = get_llm_answer(
                message,
                api_key,
                current_app.config.get("OPENAI_BASE_URL"),
                current_app.config.get("OPENAI_MODEL"),
            )
            if answer:
                return answer, "llm"
        except Exception:
            pass  # Silently fall back to local knowledge base — chatbot must never crash.

    return get_local_answer(message), "local"


@chatbot_bp.route("/")
def chatbot_page():
    history = []
    if current_user.is_authenticated:
        history = (
            ChatHistory.query.filter_by(user_id=current_user.id)
            .order_by(ChatHistory.created_at.asc())
            .limit(50)
            .all()
        )
    return render_template("chatbot/chatbot.html", history=history, suggested=SUGGESTED_QUESTIONS)


@chatbot_bp.route("/api/message", methods=["POST"])
def chat_api():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400
    if len(message) > 500:
        message = message[:500]

    answer, source = get_bot_response(message)

    try:
        entry = ChatHistory(
            user_id=current_user.id if current_user.is_authenticated else None,
            message=message,
            response=answer,
            source=source,
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()

    return jsonify({"answer": answer, "source": source})
