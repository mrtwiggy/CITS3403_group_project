# my_app/routes/__init__.py
from my_app.routes.auth import auth_bp
from my_app.routes.main import main_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)