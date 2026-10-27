import os

from flask import Flask
from flask_wtf import CSRFProtect

from config import Config
from database import init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

    init_db(app)

    csrf = CSRFProtect(app)

    from routes import main_bp
    from quiz import quiz_bp
    from survey import survey_bp
    from chatbot import chatbot_bp
    from decision_rehearsal import decision_rehearsal_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(survey_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(decision_rehearsal_bp)
    with app.app_context():
         from database import db
         db.create_all()
    csrf.exempt(chatbot_bp)

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {"current_year": datetime.utcnow().year, "site_name": "FinShield AI"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
