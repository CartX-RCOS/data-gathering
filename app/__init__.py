from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    from .parser import parser as parsing_routes
    app.register_blueprint(parsing_routes)
    
    return app