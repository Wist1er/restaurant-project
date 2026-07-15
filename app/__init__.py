from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    @app.context_processor
    def inject_current_user():
        from app.models import User
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        return dict(current_user=user)

    return app
