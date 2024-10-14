from flask import Flask
from models.user import User
from seed import seed_data
from __init__ import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/animal_shelter'
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

        if app.config.get('SAMPLE_DATA', True):  # True = Seed data / False = Don't seed
            seed_data(db)

    # user_loader callback for flask_login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app


app = create_app()    

if __name__ == "__main__":
    app.run(debug=True)