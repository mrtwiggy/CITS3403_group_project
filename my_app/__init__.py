from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import os

# Create extensions outside of create_app
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Load config from Python class
    if config_class:
        app.config.from_object(config_class)
    else:
        # Default to DeploymentConfig if no config class is specified
        from config import DeploymentConfig
        app.config.from_object(DeploymentConfig)
    

    csrf = CSRFProtect(app)
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate = Migrate(app, db)

    # Import your models here so they are registered before creating the tables
    from my_app.models import User, Review, Franchise, Location, Drink, FranchiseDrink, FranchiseLocation

    # Create tables
    with app.app_context():
        db.create_all()
        
        # Import and call the database populator
        from my_app.utils.db_populator import populate_database
        populate_database()
    
    # Import and register blueprints
    from my_app.routes import register_blueprints
    register_blueprints(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app