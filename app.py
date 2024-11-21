from flask import Flask, session, flash, redirect, url_for
from models.user import User
from seed import seed_data
from datetime import datetime, timedelta
from __init__ import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/animal_shelter'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'bf59e2d6497318f7fc560703'
    
    # Timeout configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = 7200  # seconds

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
    # Register API
    from api import api
    app.register_blueprint(api)

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
    app.run(debug=True)