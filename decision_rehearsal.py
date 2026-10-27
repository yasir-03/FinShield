"""FinShield Decision Rehearsal

Self-contained Flask blueprint. Drop this file into the project root and register
its blueprint in app.py. Core evaluation is rule/metadata based; AI is not used
for financial decision logic.
"""
from datetime import datetime
from flask import Blueprint, render_template_string, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text
from database import db


decision_rehearsal_bp = Blueprint("decision_rehearsal", __name__, url_prefix="/decision-rehearsal")

SCENARIOS = [
    {
        "id": "kyc_001",
        "category": "KYC & Fraud",
        "title": "Urgent KYC request",
        "prompt": "Your bank account will be blocked today. Complete KYC immediately using this link.",
        "options": [
            "Click the link",
            "Call the number in the SMS",
            "Verify through the official bank app",
            "Reply to the SMS",
        ],
        "safe": 2,
        "concept": "Phishing and KYC safety",
        "signals": ["Urgency", "Unknown link", "Unverified source"],
        "consequence": "An unverified link can lead to a phishing page that attempts to steal sensitive information.",
        "explanation": "KYC may be legitimate, but the request should be independently verified through the official bank app or website.",
        "retry": {
            "prompt": "A message says your KYC expires tonight and asks you to verify through a shortened link. What should you do first?",
            "options": [
                "Open the shortened link",
                "Verify the request through the official bank channel",
                "Share OTP to confirm identity",
                "Forward the message to a friend",
            ],
            "safe": 1,
        },
    },
    {
        "id": "upi_001",
        "category": "UPI Safety",
        "title": "Receiving money on UPI",
        "prompt": "Someone says they are sending you money and asks you to enter your UPI PIN to receive it.",
        "options": [
            "Enter the UPI PIN",
            "Share the OTP",
            "Do not enter the PIN; verify the request",
            "Scan any QR code they send",
        ],
        "safe": 2,
        "concept": "UPI PIN safety",
        "signals": ["Receiving money should not require your UPI PIN", "Unexpected request", "Pressure to act"],
        "consequence": "Entering a UPI PIN authorizes a payment; it is not a requirement for simply receiving money.",
        "explanation": "A UPI PIN is used to authorize payments. Never share your PIN or OTP with another person.",
        "retry": {
            "prompt": "A caller says they need your UPI PIN to refund a failed payment. What is the safer response?",
            "options": [
                "Share the PIN only once",
                "Share the OTP instead",
                "Refuse and verify through the official app or bank channel",
                "Give the last two PIN digits",
            ],
            "safe": 2,
        },
    },
    {
        "id": "invest_001",
        "category": "Investment Safety",
        "title": "Guaranteed return offer",
        "prompt": "A social-media account promises guaranteed 25% monthly returns with zero risk if you invest today.",
        "options": [
            "Invest immediately before the offer ends",
            "Ask for the account number and transfer money",
            "Verify the product, provider and risk before investing",
            "Share the offer with friends",
        ],
        "safe": 2,
        "concept": "Risk, return and investment fraud",
        "signals": ["Guaranteed high return", "Zero-risk claim", "Urgency"],
        "consequence": "Promises of unusually high guaranteed returns can be a major warning sign of fraud or misleading investment offers.",
        "explanation": "Higher potential returns generally involve risk. Verify the provider and product independently before committing money.",
        "retry": {
            "prompt": "An unknown person promises a 'risk-free' investment with double your money in six months. What should you do?",
            "options": [
                "Pay a small amount to test it",
                "Verify the provider and product independently before considering it",
                "Trust the screenshots of profits",
                "Send money before the offer expires",
            ],
            "safe": 1,
        },
    },
    {
        "id": "card_001",
        "category": "Credit Cards",
        "title": "Minimum payment trap",
        "prompt": "Your credit-card statement shows a total due of ₹20,000 and a minimum due of ₹1,000.",
        "options": [
            "Pay ₹1,000 and assume the bill is fully settled",
            "Ignore the statement",
            "Understand the interest and charges before choosing how much to pay",
            "Take another loan without checking the cost",
        ],
        "safe": 2,
        "concept": "Credit-card interest and minimum payment",
        "signals": ["Minimum due is not the full balance", "Interest can accrue", "Cost of borrowing"],
        "consequence": "Paying only the minimum amount may leave an unpaid balance that can attract interest and increase the cost of borrowing.",
        "explanation": "The minimum due is not the same as clearing the full statement balance. Understand the applicable interest and charges.",
        "retry": {
            "prompt": "You can pay the full card balance or only the minimum due. What should you check first?",
            "options": [
                "Only the minimum amount",
                "The interest, charges and outstanding balance",
                "Whether a friend paid the minimum",
                "Nothing; the minimum always costs the same",
            ],
            "safe": 1,
        },
    },
]


def _ensure_table():
    """Create the small module table without changing the existing models.py."""
    db.session.execute(text("""
        CREATE TABLE IF NOT EXISTS decision_rehearsal_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scenario_id VARCHAR(80) NOT NULL,
            attempt_type VARCHAR(20) NOT NULL,
            selected_option INTEGER,
            is_safe BOOLEAN NOT NULL,
            concept VARCHAR(160),
            created_at DATETIME NOT NULL
        )
    """))
    db.session.commit()


def _scenario(sid):
    return next((s for s in SCENARIOS if s["id"] == sid), None)


def _record(scenario_id, attempt_type, selected, is_safe, concept):
    _ensure_table()
    db.session.execute(
        text("""INSERT INTO decision_rehearsal_attempts
               (user_id, scenario_id, attempt_type, selected_option, is_safe, concept, created_at)
               VALUES (:uid, :sid, :atype, :selected, :safe, :concept, :created)"""),
        {
            "uid": current_user.id,
            "sid": scenario_id,
            "atype": attempt_type,
            "selected": selected,
            "safe": bool(is_safe),
            "concept": concept,
            "created": datetime.utcnow(),
        },
    )
    db.session.commit()


PAGE = """
{% extends 'base.html' %}
{% block title %}Decision Rehearsal — FinShield AI{% endblock %}
{% block extra_css %}
<style>
.dr-wrap{padding-top:6.8rem;padding-bottom:4rem;background:linear-gradient(180deg,#f8fafc,#fff)}
.dr-hero{background:linear-gradient(135deg,#0a1128,#1e3a8a);color:#fff;border-radius:28px;padding:2rem;box-shadow:0 18px 50px rgba(10,17,40,.14)}
.dr-eyebrow{color:#4ade80;font-size:.78rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.dr-title{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;margin:.45rem 0}.dr-sub{color:rgba(255,255,255,.72);max-width:760px}
.dr-step{display:flex;gap:.65rem;align-items:center;margin-top:1.25rem;flex-wrap:wrap}.dr-step span{padding:.45rem .8rem;border-radius:999px;background:rgba(255,255,255,.1);font-size:.82rem;font-weight:700}.dr-step .active{background:#10b981;color:#06131a}
.dr-card{background:#fff;border:1px solid #e5eaf0;border-radius:22px;padding:1.5rem;box-shadow:0 8px 30px rgba(10,17,40,.06);height:100%}
.dr-option{display:block;width:100%;text-align:left;border:1px solid #dbe4ee;background:#fff;border-radius:14px;padding:.9rem 1rem;margin:.65rem 0;font-weight:600;color:#16265a;transition:.18s}.dr-option:hover{border-color:#2563eb;background:#f5f9ff}.dr-option input{margin-right:.65rem}
.dr-badge{display:inline-block;padding:.35rem .7rem;border-radius:999px;background:#eef6ff;color:#2563eb;font-size:.78rem;font-weight:800}.dr-safe{background:#e7f7f0;color:#08744f}.dr-risk{background:#fff0ef;color:#b63830}
.dr-progress{height:8px;background:#e7edf4;border-radius:99px;overflow:hidden}.dr-progress>div{height:100%;background:linear-gradient(90deg,#2563eb,#10b981);width:var(--p)}
.dr-signal{background:#fff4f3;border:1px solid #ffd7d2;border-radius:12px;padding:.55rem .75rem;color:#9f2e27;font-size:.88rem;font-weight:700;margin:.4rem 0}.dr-good{background:#effaf5;border-color:#c8eadb;color:#08744f}
.dr-btn{border:0;border-radius:999px;padding:.72rem 1.35rem;font-weight:700}.dr-primary{background:linear-gradient(135deg,#2563eb,#10b981);color:#fff}.dr-secondary{background:#eef3f8;color:#16265a}
.dr-stat{border-radius:18px;padding:1rem;background:#f8fafc;border:1px solid #e7edf4}.dr-stat strong{font-size:1.55rem;color:#16265a}.dr-muted{color:#64748b;font-size:.9rem}
</style>
{% endblock %}
{% block content %}
<div class="dr-wrap"><div class="container">
  <div class="dr-hero mb-4">
    <div class="dr-eyebrow">FinShield Innovation</div>
    <div class="dr-title">Decision Rehearsal</div>
    <div class="dr-sub">Practice financial decisions before they cost you money. Face a realistic situation, choose an action, understand the risk, and try a related situation.</div>
    <div class="dr-step"><span class="active">1 SEE</span><span>2 DECIDE</span><span>3 UNDERSTAND</span><span>4 REPLAY</span><span>5 RETEST</span><span>6 REMEMBER</span></div>
  </div>

  {% if view == 'home' %}
  <div class="row g-4">
    <div class="col-lg-8"><div class="dr-card">
      <div class="d-flex justify-content-between align-items-center mb-3"><div><span class="dr-badge">Scenario library</span><h3 class="mt-2 mb-1">Choose a situation to rehearse</h3><div class="dr-muted">Short, realistic situations across common financial decisions.</div></div><i class="bi bi-shield-check fs-1 text-primary"></i></div>
      <div class="row g-3">
      {% for s in scenarios %}<div class="col-md-6"><div class="p-3 border rounded-4 h-100 bg-light"><div class="dr-badge mb-2">{{ s.category }}</div><h5>{{ s.title }}</h5><p class="dr-muted mb-3">{{ s.prompt }}</p><a class="btn dr-btn dr-primary" href="{{ url_for('decision_rehearsal.play', scenario_id=s.id) }}">Start rehearsal <i class="bi bi-arrow-right ms-1"></i></a></div></div>{% endfor %}
      </div>
    </div></div>
    <div class="col-lg-4"><div class="dr-card"><h5><i class="bi bi-graph-up-arrow me-2 text-success"></i>Your rehearsal progress</h5>
      <div class="row g-2 mt-2"><div class="col-6"><div class="dr-stat"><div class="dr-muted">Attempts</div><strong>{{ stats.attempts }}</strong></div></div><div class="col-6"><div class="dr-stat"><div class="dr-muted">Safe choices</div><strong>{{ stats.safe_pct }}%</strong></div></div></div>
      <hr><div class="dr-muted mb-2">Concepts practised</div>{% if stats.concepts %}{% for c in stats.concepts %}<span class="dr-badge m-1">{{ c }}</span>{% endfor %}{% else %}<p class="dr-muted">Complete a scenario to start building your progress.</p>{% endif %}
    </div></div>
  </div>
  {% elif view == 'play' %}
  <div class="row justify-content-center"><div class="col-lg-9"><div class="dr-card">
    <div class="d-flex justify-content-between mb-3"><span class="dr-badge">{{ scenario.category }}</span><span class="dr-muted">Scenario {{ index + 1 }} of {{ total }}</span></div>
    <div class="dr-progress mb-4" style="--p:{{ progress }}%"><div></div></div>
    <h3>{{ scenario.title }}</h3><p class="lead mt-3">{{ scenario.prompt }}</p>
    <form method="post" action="{{ url_for('decision_rehearsal.submit', scenario_id=scenario.id) }}">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      {% for option in scenario.options %}<label class="dr-option"><input type="radio" name="choice" value="{{ loop.index0 }}" required>{{ option }}</label>{% endfor %}
      <div class="d-flex justify-content-between align-items-center mt-4"><a class="btn dr-btn dr-secondary" href="{{ url_for('decision_rehearsal.index') }}">Back</a><button class="btn dr-btn dr-primary" type="submit">Analyse my decision <i class="bi bi-arrow-right ms-1"></i></button></div>
    </form>
  </div></div></div>
  {% elif view == 'result' %}
  <div class="row g-4"><div class="col-lg-8"><div class="dr-card">
    {% if safe %}<span class="dr-badge dr-safe">SAFER DECISION</span>{% else %}<span class="dr-badge dr-risk">RISKY DECISION</span>{% endif %}
    <h2 class="mt-3">{{ 'Good choice.' if safe else 'Here is what you missed.' }}</h2>
    <p class="lead">{{ scenario.explanation }}</p>
    <h5 class="mt-4">Why it matters</h5><p>{{ scenario.consequence }}</p>
    <h5 class="mt-4">Warning signs</h5>{% for sig in scenario.signals %}<div class="dr-signal {{ 'dr-good' if safe else '' }}">{{ sig }}</div>{% endfor %}
    <div class="p-3 rounded-4 bg-light mt-4"><strong>Linked concept:</strong> {{ scenario.concept }}</div>
    <div class="d-flex gap-2 mt-4"><a class="btn dr-btn dr-primary" href="{{ url_for('decision_rehearsal.retry', scenario_id=scenario.id) }}">Retest with a new scenario <i class="bi bi-arrow-right ms-1"></i></a><a class="btn dr-btn dr-secondary" href="{{ url_for('decision_rehearsal.index') }}">Scenario library</a></div>
  </div></div><div class="col-lg-4"><div class="dr-card"><h5><i class="bi bi-lightbulb me-2 text-warning"></i>Decision Replay</h5><p class="dr-muted">The system connects your selected action to the scenario's structured safety signals and concept.</p><div class="p-3 rounded-4 bg-light"><div class="dr-muted">Your choice</div><strong>{{ scenario.options[selected] }}</strong></div><div class="text-center my-3"><i class="bi bi-arrow-down-circle text-primary fs-2"></i></div><div class="p-3 rounded-4 {% if safe %}dr-good{% else %}dr-risk{% endif %}"><div class="dr-muted">Next learning action</div><strong>{{ 'Apply the same principle in a new situation.' if safe else 'Notice the warning signs before acting.' }}</strong></div></div></div></div>
  {% elif view == 'retry' %}
  <div class="row justify-content-center"><div class="col-lg-9"><div class="dr-card">
    <span class="dr-badge">RETEST</span><h3 class="mt-3">Apply the lesson to a new situation</h3><p class="lead mt-3">{{ retry.prompt }}</p>
    <form method="post" action="{{ url_for('decision_rehearsal.retry_submit', scenario_id=scenario.id) }}">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      {% for option in retry.options %}<label class="dr-option"><input type="radio" name="choice" value="{{ loop.index0 }}" required>{{ option }}</label>{% endfor %}
      <div class="d-flex justify-content-between mt-4"><a class="btn dr-btn dr-secondary" href="{{ url_for('decision_rehearsal.index') }}">Skip</a><button class="btn dr-btn dr-primary" type="submit">Check decision</button></div>
    </form>
  </div></div></div>
  {% elif view == 'retry_result' %}
  <div class="row justify-content-center"><div class="col-lg-8"><div class="dr-card text-center">
    <span class="dr-badge {% if safe %}dr-safe{% else %}dr-risk{% endif %}">{{ 'SAFEER RESPONSE' if safe else 'TRY AGAIN' }}</span>
    <h2 class="mt-3">{{ 'You applied the principle.' if safe else 'The warning sign is still there.' }}</h2>
    <p class="lead">{{ explanation }}</p>
    <div class="p-3 rounded-4 bg-light text-start mt-4"><strong>Concept:</strong> {{ scenario.concept }}</div>
    <a class="btn dr-btn dr-primary mt-4" href="{{ url_for('decision_rehearsal.recall', scenario_id=scenario.id) }}">Quick recall <i class="bi bi-arrow-right ms-1"></i></a>
  </div></div></div>
  {% elif view == 'recall' %}
  <div class="row justify-content-center"><div class="col-lg-8"><div class="dr-card">
    <span class="dr-badge">REMEMBER</span><h3 class="mt-3">Quick recall</h3><p class="lead">Which warning sign should make you pause before acting?</p>
    <form method="post" action="{{ url_for('decision_rehearsal.recall_submit', scenario_id=scenario.id) }}">
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
      {% for option in recall_options %}<label class="dr-option"><input type="radio" name="choice" value="{{ loop.index0 }}" required>{{ option }}</label>{% endfor %}
      <button class="btn dr-btn dr-primary mt-3" type="submit">Check recall</button>
    </form>
  </div></div></div>
  {% endif %}
</div></div>
{% endblock %}
"""


def _stats():
    _ensure_table()
    row = db.session.execute(text("SELECT COUNT(*) attempts, COALESCE(SUM(CASE WHEN is_safe=1 THEN 1 ELSE 0 END),0) safe FROM decision_rehearsal_attempts WHERE user_id=:uid"), {"uid": current_user.id}).mappings().first()
    attempts = int(row["attempts"] or 0)
    safe = int(row["safe"] or 0)
    concepts = [r[0] for r in db.session.execute(text("SELECT DISTINCT concept FROM decision_rehearsal_attempts WHERE user_id=:uid AND concept IS NOT NULL ORDER BY concept"), {"uid": current_user.id}).all()]
    return {"attempts": attempts, "safe_pct": round(safe * 100 / attempts) if attempts else 0, "concepts": concepts}


@decision_rehearsal_bp.route("/")
@login_required
def index():
    return render_template_string(PAGE, view="home", scenarios=SCENARIOS, stats=_stats())


@decision_rehearsal_bp.route("/<scenario_id>")
@login_required
def play(scenario_id):
    scenario = _scenario(scenario_id)
    if not scenario:
        return redirect(url_for("decision_rehearsal.index"))
    idx = SCENARIOS.index(scenario)
    return render_template_string(PAGE, view="play", scenario=scenario, index=idx, total=len(SCENARIOS), progress=round((idx+1)*100/len(SCENARIOS)))


@decision_rehearsal_bp.route("/<scenario_id>/submit", methods=["POST"])
@login_required
def submit(scenario_id):
    scenario = _scenario(scenario_id)
    if not scenario:
        return redirect(url_for("decision_rehearsal.index"))
    try:
        selected = int(request.form.get("choice"))
    except (TypeError, ValueError):
        flash("Please select an option.", "warning")
        return redirect(url_for("decision_rehearsal.play", scenario_id=scenario_id))
    if selected < 0 or selected >= len(scenario["options"]):
        flash("Invalid option.", "danger")
        return redirect(url_for("decision_rehearsal.play", scenario_id=scenario_id))
    safe = selected == scenario["safe"]
    _record(scenario_id, "initial", selected, safe, scenario["concept"])
    return render_template_string(PAGE, view="result", scenario=scenario, safe=safe, selected=selected)


@decision_rehearsal_bp.route("/<scenario_id>/retry")
@login_required
def retry(scenario_id):
    scenario = _scenario(scenario_id)
    if not scenario:
        return redirect(url_for("decision_rehearsal.index"))
    return render_template_string(PAGE, view="retry", scenario=scenario, retry=scenario["retry"])


@decision_rehearsal_bp.route("/<scenario_id>/retry/submit", methods=["POST"])
@login_required
def retry_submit(scenario_id):
    scenario = _scenario(scenario_id)
    if not scenario:
        return redirect(url_for("decision_rehearsal.index"))
    try:
        selected = int(request.form.get("choice"))
    except (TypeError, ValueError):
        flash("Please select an option.", "warning")
        return redirect(url_for("decision_rehearsal.retry", scenario_id=scenario_id))
    retry_data = scenario["retry"]
    safe = selected == retry_data["safe"]
    _record(scenario_id, "retry", selected, safe, scenario["concept"])
    explanation = ("You independently verify the request before acting, which applies the lesson from the first scenario."
                   if safe else "Pause and verify the source first. The safer response is to use an official channel rather than the message or caller.")
    return render_template_string(PAGE, view="retry_result", scenario=scenario, safe=safe, explanation=explanation)


@decision_rehearsal_bp.route("/<scenario_id>/recall")
@login_required
def recall(scenario_id):
    scenario = _scenario(scenario_id)
    if not scenario:
        return redirect(url_for("decision_rehearsal.index"))
    options = [scenario["signals"][0], scenario["signals"][1], "A familiar logo is always proof"]
    return render_template_string(PAGE, view="recall", scenario=scenario, recall_options=options)


@decision_rehearsal_bp.route("/<scenario_id>/recall/submit", methods=["POST"])
@login_required
def recall_submit(scenario_id):
    scenario = _scenario(scenario_id)
    if not scenario:
        return redirect(url_for("decision_rehearsal.index"))
    try:
        selected = int(request.form.get("choice"))
    except (TypeError, ValueError):
        flash("Please select an option.", "warning")
        return redirect(url_for("decision_rehearsal.recall", scenario_id=scenario_id))
    # For recall, any of the first two warning signals are valid signals.
    safe = selected in (0, 1)
    _record(scenario_id, "recall", selected, safe, scenario["concept"])
    flash("Recall checked — keep practising the signal, not just the definition." if safe else "Recall missed — revisit the scenario and warning signs.", "success" if safe else "warning")
    return redirect(url_for("decision_rehearsal.index"))
