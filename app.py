import os
from flask import Flask, session, flash, redirect, url_for
from models.user import User
from seed import seed_data
from datetime import datetime, timedelta
from __init__ import db, bcrypt, login_manager
import getpass

def create_app():
    app = Flask(__name__)

    # Local database config
    # localdb_user = input("Enter your MySQL username: ")
    # localdb_password = getpass.getpass("Enter your MySQL password: ")
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{localdb_user}:{localdb_password}@localhost/animal_shelter'

    # Database config for deployed app
    db_user = os.getenv('DB_USER', 'root') 
    db_password = os.getenv('DB_PASSWORD', 'password123') 
    db_name = os.getenv('DB_NAME', 'animal-shelter') 
    cloud_sql_connection_name = os.getenv('CLOUD_SQL_CONNECTION_NAME')
    
    if cloud_sql_connection_name:        
        # Connecting to online database on Google Cloud through deployed app
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'mysql+pymysql://{db_user}:{db_password}@/{db_name}'
            f'?unix_socket=/cloudsql/{cloud_sql_connection_name}'
        )
    else:
        # Connecting to online database on Google Cloud
        db_host = os.getenv('DB_HOST', '34.116.182.73') 
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

    # Shared parameters of database config
    app.config['PERMANENT_SESSION_LIFETIME'] = 7200
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'bf59e2d6497318f7fc560703'    


    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Set the login view
    login_manager.login_view = 'routes.login_page'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from routes import routes
    app.register_blueprint(routes)

    # Create tables and seed data if necessary
    with app.app_context():
        db.create_all()

        if app.config.get('SAMPLE_DATA', True):  # True = Seed data
            seed_data(db)
            
    @app.after_request
    def add_cache_control_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, public, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response


    # user_loader callback for flask_login
    @login_manager.user_loader
    def load_user(user_id):
        # Check for idle timeout
        now = datetime.now()
        last_activity = session.get('last_activity')
        
        if last_activity:
            last_activity = datetime.fromisoformat(last_activity)
            if now - last_activity > timedelta(seconds=app.config['PERMANENT_SESSION_LIFETIME']):
                from flask_login import logout_user
                logout_user()
                return None
        
        # Update the last activity
        session['last_activity'] = now.isoformat()
        
        return User.query.get(int(user_id))
    
    # Middleware to update last activity
    @app.before_request
    def update_last_activity():
        if 'last_activity' in session:
            session['last_activity'] = datetime.now().isoformat()
            
            
    return app


app = create_app()    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)