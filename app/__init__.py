from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
from app.models import Scout, Player, Club, Sponsor, Academy
login_manager = LoginManager()

def create_app():
    """Creates our app instance"""
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes import app as main_bp
    app.register_blueprint(main_bp)
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        """Defines user load up using user id for the flask login"""
        users = [Player, Scout, Club, Academy, Sponsor]
        for User in users:
            usr = User.query.get(user_id)
            if usr:
                return usr
        return None

    with app.app_context():
        db.create_all
    
    return app
