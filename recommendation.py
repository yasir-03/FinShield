"""Rule-based AI recommendation engine.

Maps quiz performance (by category and overall) to suggested learning
articles. Built to be simple, deterministic, and easy to extend with
scikit-learn based scoring later without changing the calling interface.
"""

from learning_data import LEARNING_ARTICLES

# Maps a quiz category to the most relevant learning article slug(s)
CATEGORY_TO_ARTICLES = {
    "savings": ["savings", "budgeting"],
    "upi": ["upi-safety", "digital-banking"],
    "cyber-fraud": ["cyber-security", "upi-safety"],
    "investment": ["mutual-funds", "inflation"],
    "insurance": ["insurance"],
    "mutual-funds": ["mutual-funds", "inflation"],
    "inflation": ["inflation", "mutual-funds"],
    "budget": ["budgeting", "savings"],
    "tax": ["tax-basics"],
}

BEGINNER_ARTICLES = ["savings", "budgeting"]


def _article_card(slug):
    article = LEARNING_ARTICLES.get(slug)
    if not article:
        return None
    return {
        "slug": slug,
        "title": article["title"],
        "summary": article["summary"],
        "icon": article.get("icon", "bi-book"),
        "category": article["category"],
    }


def get_recommendations_for_result(category, percentage):
    """Rule-based recommendation for a single quiz attempt."""
    recommendations = []
    reasons = []

    if percentage < 40:
        reasons.append("Your score suggests reviewing beginner-friendly fundamentals first.")
        for slug in BEGINNER_ARTICLES:
            card = _article_card(slug)
            if card and card not in recommendations:
                recommendations.append(card)

    if category == "cyber-fraud" and percentage < 50:
        reasons.append("Strengthen your cyber fraud awareness — this protects your money directly.")
    if category == "investment" and percentage < 50:
        reasons.append("Build your investment basics before increasing exposure to markets.")

    for slug in CATEGORY_TO_ARTICLES.get(category, []):
        card = _article_card(slug)
        if card and card not in recommendations:
            recommendations.append(card)

    if not reasons:
        if percentage >= 80:
            reasons.append("Great job! Explore related topics to broaden your financial knowledge.")
        else:
            reasons.append("Keep learning — a quick review of these topics will boost your score.")

    return {"reasons": reasons, "articles": recommendations[:4]}


def get_dashboard_recommendations(quiz_results):
    """Aggregate recommendations across a user's full quiz history for the dashboard."""
    if not quiz_results:
        return {
            "reasons": ["Take your first quiz to get personalized recommendations!"],
            "articles": [_article_card(s) for s in BEGINNER_ARTICLES],
        }

    weakest = {}
    for r in quiz_results:
        if r.category not in weakest or r.percentage < weakest[r.category].percentage:
            weakest[r.category] = r

    sorted_weak = sorted(weakest.values(), key=lambda r: r.percentage)

    recommendations = []
    reasons = []
    for r in sorted_weak[:3]:
        if r.percentage < 60:
            reasons.append(f"You scored {r.percentage}% in {r.category.replace('-', ' ').title()} — here's targeted content to help.")
            for slug in CATEGORY_TO_ARTICLES.get(r.category, []):
                card = _article_card(slug)
                if card and card not in recommendations:
                    recommendations.append(card)

    if not recommendations:
        reasons.append("You're doing great across all categories! Explore advanced topics to keep growing.")
        recommendations = [_article_card(s) for s in ["mutual-funds", "tax-basics"]]

    return {"reasons": reasons, "articles": recommendations[:4]}
