from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
from app.models import Scout, Player, Club, Sponsor, Academy, Video

login_manager = LoginManager()

def create_app():
    """Creates our app instance"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Import and register blueprints
    from app.routes import main_app
    app.register_blueprint(main_app)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'


    @login_manager.user_loader
    def load_user(user_id):
        """Defines user load up using user id for the flask login"""
        users = [Player, Scout, Club, Academy, Sponsor]
        for User in users:
            usr = User.query.get(user_id)
            if usr:
                return usr
        return None
    
    return app
