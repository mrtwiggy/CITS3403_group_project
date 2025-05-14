# my_app/routes/__init__.py
from my_app.routes.auth import auth_bp
from my_app.routes.main import main_bp
from my_app.routes.reviews import reviews_bp
from my_app.routes.friends import friend_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(reviews_bp, url_prefix='/review')
    app.register_blueprint(friend_bp, url_prefix='/friends')
    app.register_blueprint(main_bp)