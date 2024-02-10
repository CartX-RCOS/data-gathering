from flask import Flask
from flask_mysqldb import MySQL

def create_app():
    app = Flask(__name__)
    
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    from .parser import parser as parsing_routes
    app.register_blueprint(parsing_routes)

    from .database import database as database_routes
    app.register_blueprint(database_routes)

    # MySQL database settings
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'your_mysql_username'
    app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
    app.config['MYSQL_DB'] = 'your_mysql_db_name'

    # Initialize MySQL with app
    mysql = MySQL(app)
    return app, mysql