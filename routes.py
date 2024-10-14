from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from __init__ import db
from models.user import User, Admin, Caretaker, Volunteer, Vet
from models.animal import Animal
from models.examination import Examination, PreventiveCheckUp, Request, Vaccination
from models.walk_schedule import WalkSchedule
from forms.register import RegistrationForm
from forms.login import LoginForm

routes = Blueprint('routes', __name__)

@routes.route('/')
def home_page():
    return render_template('home.html')

@routes.route('/animals')
def animals_page():
    return render_template('animals.html')

@routes.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data

        user = User.query.filter_by(login=login).first()

        if user:
            if user.check_password(password):
                login_user(user)
                flash("Logged in successfuly", 'success')
                if isinstance(user, Admin):            
                    return redirect(url_for('routes.dashboard_admin_page'))
                elif isinstance(user, Vet):
                    return redirect(url_for('routes.dashboard_vet_page'))
                elif isinstance(user, Caretaker):
                    return redirect(url_for('routes.dashboard_caretaker_page'))
                elif isinstance(user, Volunteer):
                    return redirect(url_for('routes.dashboard_volunteer_page'))
                else:
                    flash("Unknow role", 'danger')
            else:
                flash("Wrong password!", 'danger')
        else:
            flash('Non existent user', 'danger')

    return render_template('login.html', form=form)

@routes.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()

    print("Creating new user! ")

    if form.validate_on_submit():        
        login = form.login.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        print(f"Creating new user: {login}, {first_name}, {last_name}, {email}")

        # New User is automaticaly taken as volunteer
        new_user = Volunteer(login=login, 
                            first_name=first_name, 
                            last_name=last_name, 
                            email=email, 
                            password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfuly!', 'success')
        return redirect(url_for('routes.dashboard_volunteer_page'))    
    
    # Handle form errors (flash messages)
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    # Showing all users
    users = User.query.all()
    return render_template('register.html', form=form, users=users)

@routes.route('/logout')
def logout_page():
    logout_user() # flask_login builtin
    flash('You have been logged out', 'info')
    return redirect(url_for('routes.home_page'))


# DASHBOARDS based on roles
@routes.route('/dashboard_admin')
def dashboard_admin_page():
    users = User.query.all()
    return render_template('dashboard_admin.html', users=users)

@routes.route('/dashboard_admin/update_role/<int:user_id>', methods=['POST'])
def update_user_role(user_id):
    new_role = request.form.get("new_role")
    user = User.query.get_or_404(user_id)
    user.role = new_role
    flash(f"Role for user {user.login} has been updated to {new_role}", 'success')
    return redirect(url_for('routes.dashboard_admin_page'))

@routes.route('/dashboard_admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.login} has been deleted", 'success')
    return redirect(url_for('routes.dashboard_admin_page'))

@routes.route('/dashboard_vet')
def dashboard_vet_page():
    return render_template('dashboard_vet.html')

@routes.route('/dashboard_caretaker')
def dashboard_caretaker_page():
    return render_template('dashboard_caretaker.html')

@routes.route('/dashboard_volunteer')
def dashboard_volunteer_page():
    animals = Animal.query.all()

    return render_template('dashboard_volunteer.html', animals=animals)

