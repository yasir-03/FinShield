from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"


def init_db(app):
    db.init_app(app)
    login_manager.init_app(app)

    import models  # noqa: F401 — registers models on SQLAlchemy metadata before create_all()

    with app.app_context():
        db.create_all()
        _seed_initial_data()


def _seed_initial_data():
    from models import User, Article
    from learning_data import LEARNING_ARTICLES
    from config import Config

    if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
        admin = User(
            name="FinShield Admin",
            email=Config.ADMIN_EMAIL,
            occupation="Administrator",
            city="N/A",
            is_admin=True,
        )
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)

    if Article.query.count() == 0:
        for slug, data in LEARNING_ARTICLES.items():
            article = Article(
                slug=slug,
                title=data["title"],
                category=data["category"],
                icon=data.get("icon", "bi-book"),
                summary=data.get("summary", ""),
            )
            db.session.add(article)

    db.session.commit()
