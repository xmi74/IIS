from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
from api.api_animals import *
from api.api_requests import filter_request, get_request, delete_request, edit_request, create_request
from api.api_schedules import *
from forms import edit_schedules
from forms.add_schedule import AddSchedule
from forms.edit_animal import EditAnimalForm
from forms.edit_request import EditRequest
from forms.edit_schedules import EditSchedules
from models.user import User, Admin, Caretaker, Volunteer, Vet
from models.animal import Animal
from models.examination import Examination, PreventiveCheckUp, Vaccination
from models.request import Request
from models.walk_schedule import WalkSchedule
from forms.register import RegistrationForm
from forms.login import LoginForm
from forms.edit_user import EditUserForm
from api.api_users import *
from models.enums.schedule_state import ScheduleState
from utils.decorators import role_required

routes = Blueprint('routes', __name__)

################ HOME PAGE ################

@routes.route('/')
def home_page():
    caretakers = filter_request({'role': 'caretaker'})
    animals = get_animal_photos()
    return render_template('public/home.html', caretakers=caretakers, animals=animals)

################ ANIMALS PAGE ################

@routes.route('/animals', methods=['GET'])
def animals_page():
    query = Animal.query

    name = request.args.get('name')
    species = request.args.get('species')

    if name:
        query = query.filter(Animal.name.ilike(name))
    if species:
        query = query.filter_by(species=species)

    animals = query.all()
    return render_template('public/animals.html', animals=animals)


# Route: Animal Detail View
@routes.route('/animals/<int:animal_id>')
def animal_detail(animal_id):

    animal = get_animal(animal_id)
    
    schedules = get_incoming_animal_schedules(animal_id)

    return render_template('public/animal_detail.html', animal=animal, schedules=schedules)


@routes.route('/schedules/reserve/<int:schedule_id>', methods=['POST'])
@role_required('volunteer')
@login_required
def reserve_schedule_view(schedule_id):
    if not current_user.verified:
        flash("You aren't verified yet.", "warning")
        return redirect(url_for('routes.login_page'))
    
    success = reserve_schedule(schedule_id, current_user.id)
    if success:
        return redirect(request.referrer or url_for('routes.animals_page'))
    
    return "Error reserving schedule", 400


@routes.route('/schedules/cancel/<int:schedule_id>', methods=['POST'])
@role_required('volunteer')
@login_required
def cancel_schedule_view_animal(schedule_id):
    if not current_user.verified:
        flash("You aren't verified yet.", "warning")
        return redirect(url_for('routes.home_page'))

    success = cancel_volunteer_schedule(schedule_id, current_user.id)
    if success:
        flash("Schedule canceled successfully.", "success")
        return redirect(request.referrer or url_for('routes.animals_page'))
    
    flash("Error canceling reservation. Ensure you are the one who reserved it.", "danger")
    return redirect(url_for('routes.animals_page'))

#################################################
#              DASHBOARD VOLUNTEER              #
#################################################

@routes.route('/dashboard_volunteer')
@role_required('volunteer')
@login_required
def dashboard_volunteer_page(): 
    closest_schedule = get_closest_schedule(current_user.id)
    past_schedules = get_past_schedules(current_user.id)
    future_schedules = get_future_schedules(current_user.id)

    return render_template('volunteer/dashboard_volunteer.html', 
                           closest_schedule=closest_schedule,
                           past_schedules=past_schedules, 
                           future_schedules=future_schedules)

    
@routes.route('/schedules/cancel/<int:schedule_id>', methods=['POST'])
@role_required('volunteer')
@login_required
def cancel_schedule_view(schedule_id):
    if not current_user.verified:
        flash("You aren't verified yet.", "warning")
        return redirect(url_for('routes.home_page'))

    success = cancel_volunteer_schedule(schedule_id, current_user.id)
    if success:
        flash('Schedule has been canceled successfully.', 'success')
    else:
        flash("Error canceling reservation. Ensure you are the one who reserved it.", "danger")

    return redirect(url_for('routes.dashboard_volunteer_page'))





################ LOGIN PAGE ################

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

################ REGISTER PAGE ################

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

        # New User is automatically taken as volunteer
        new_user = Volunteer(login=login, 
                            first_name=first_name, 
                            last_name=last_name, 
                            email=email, 
                            password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('routes.dashboard_volunteer_page'))    
    
    # Handle form errors (flash messages)
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    # Showing all users
    users = User.query.all()
    return render_template('register.html', form=form, users=users)

################ LOGOUT REDIRECTION ################

@routes.route('/logout')
def logout_page():
    logout_user() # flask_login builtin
    flash('You have been logged out', 'info')
    return redirect(url_for('routes.home_page'))


#################################################
#                DASHBOARD ADMIN                #
#################################################

################ BASIC DASHBOARD ################
@routes.route('/dashboard_admin')
@role_required('admin')
@login_required
def dashboard_admin_page():
    # users = get_users()

    ################ FILTERING USERS ################
    filters = {
        'role': request.args.get('role'),
        'login': request.args.get('login'),
        'first_name': request.args.get('first_name'),
        'last_name': request.args.get('last_name'),
        'email': request.args.get('email')
    }

    users=filter_users(filters)

    role_format = {
        "admin": "Admin",
        "caretaker": "Caretaker",
        "vet": "Vet",
        "volunteer": "Volunteer"
    }

    ################ ADDING USERS ?? ################

    return render_template('dashboard_admin.html', users=users, role_format=role_format)

################ EDIT USER ################
@routes.route('/dashboard_admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
@login_required
def update_user_page(user_id):    
    user = get_user(user_id)        
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        # If Cancel button
        if form.cancel.data:
            return redirect(url_for('routes.dashboard_admin_page'))
        
        # If Delete button
        if form.delete.data:
            try:
                delete_user(user_id)
                flash(f"User {user_id} has been deleted successfully", 'success')
            except Exception as e:
                flash(f"Error deleting user: {str(e)}", "danger")

            return redirect(url_for('routes.dashboard_admin_page'))

        # Save button
        data = {
            'login': form.login.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'role': form.role.data
        }

        try:
            edit_user(user_id, data)
            flash(f"User {user_id} has been updated successfully", 'success')
        except Exception as e:
            flash(f"Error updating user: {str(e)}", "danger")
        return redirect(url_for('routes.dashboard_admin_page'))
    
    return render_template('edit_user.html', form=form, user=user)        


#################################################
#                 DASHBOARD VET                 #
#################################################

@routes.route('/dashboard_vet')
@role_required('vet')
@login_required
def dashboard_vet_page():
    vet_requests = get_requests_by_vet(current_user.id)

    return render_template('dashboard_vet.html', vet_requests=vet_requests)


@routes.route('/dashboard_vet/request_detail')
@role_required('vet')
@login_required
def request_detail_page():
    return render_template('request_detail.html')




#######################################################
#                 DASHBOARD CARETAKER                 #
#######################################################

@routes.route('/dashboard_caretaker', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def dashboard_caretaker_page():

    #POST
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        validate = eval(request.form.get('validate'))
        edit_user_verified(user_id,validate)
        return redirect(url_for('routes.dashboard_caretaker_page'))

    # GET
    volunteer_filter = {'role': 'volunteer'}
    users = filter_users(volunteer_filter)
    return render_template('caretaker/verify_users.html', users=users)

@routes.route('/caretaker/animals', methods=['GET'])
@role_required('caretaker')
@login_required
def animals_caretaker_page():
    filters = dict()
    filters['name'] = request.args.get('name') or None
    filters['species'] = request.args.get('species') or None

    animals = get_animals(filters)
    species = set()
    for animal in animals:
        species.add(animal.species)
    return render_template('caretaker/animals.html', animals=animals, species=species)

@routes.route('/caretaker/animals/add', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def animals_add_page():
    edit = {
        'title': 'Add',
        'route': 'routes.animals_add_page',
    }
    form = EditAnimalForm()

    #POST
    if form.validate_on_submit():
        # Delete button
        if form.delete.data:
            return redirect(url_for('routes.animals_caretaker_page'))

        # Save button
        data = {
            'name': form.name.data,
            'species': form.species.data,
            'weight': form.weight.data,
            'birth_date': form.birth_date.data,
            'photo': form.photo.data
        }

        try:
            animal = add_animal(data)
            flash(f"User {animal.name} has been updated successfully", 'success')
        except Exception as e:
            flash(f"Error updating user: {str(e)}", "danger")
        return redirect(url_for('routes.animals_caretaker_page'))

    #GET
    return render_template('caretaker/edit_animal.html', edit = edit, form=form)

@routes.route('/caretaker/animals/edit/<int:animal_id>', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def animals_edit_page(animal_id):
    edit = {
        'title': 'Edit',
        'route': 'routes.animals_edit_page',
    }
    animal = get_animal(animal_id)
    form = EditAnimalForm(obj=animal)

    # POST
    if form.validate_on_submit():
        # Delete button
        if form.delete.data:
            try:
                delete_animal(animal_id)
                flash(f"User {animal.name} has been deleted successfully", 'success')
            except Exception as e:
                flash(f"Error deleting user: {str(e)}", "danger")

            return redirect(url_for('routes.animals_caretaker_page'))

        # Save button
        data = {
            'name': form.name.data,
            'species': form.species.data,
            'weight': form.weight.data,
            'birth_date': form.birth_date.data,
            'photo': form.photo.data
        }

        try:
            animal = edit_animal(animal_id ,data)
            flash(f"User {animal.name} has been updated successfully", 'success')
        except Exception as e:
            flash(f"Error updating user: {str(e)}", "danger")
        return redirect(url_for('routes.animals_caretaker_page'))

    #GET
    return render_template('caretaker/edit_animal.html', edit = edit, form=form, animal_id=animal_id)

@routes.route('/caretaker/animals/<int:animal_id>/schedules', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def animal_schedules_page(animal_id):
    #POST
    if request.method == 'POST':
        schedule_id = request.form.get('schedule_id')
        try:
            delete_schedule(schedule_id)
            flash(f"Schedule has been deleted successfully", 'success')
        except Exception as e:
            flash(f"Error deleting schedule: {str(e)}", "danger")
        return redirect(url_for('routes.animal_schedules_page', animal_id=animal_id))

    #GET
    filters = dict()
    filters['animal'] = animal_id
    filters['state'] = request.args.get('state') or None
    if request.args.get('old') is None:
        filters['date'] = date.today()
    schedules = get_schedules(filters)
    return render_template('caretaker/schedules.html', schedules=schedules, animal_id=animal_id, ScheduleState=ScheduleState)

@routes.route('/caretaker/schedules/edit/<int:schedule_id>', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def schedules_edit_page(schedule_id):
    schedule = get_schedule(schedule_id)
    form = EditSchedules(obj=schedule)

    # POST
    if form.validate_on_submit():
        # Delete button
        if form.delete.data:
            try:
                delete_schedule(schedule_id)
                flash(f"Schedule has been deleted successfully", 'success')
            except Exception as e:
                flash(f"Error deleting schedule: {str(e)}", "danger")

            return redirect(url_for('routes.animal_schedules_page', animal_id=schedule.animal_id))

        # Save button
        data = {
            'date': form.date.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data,
            'state': form.state.data,
        }

        try:
            edit_schedule(schedule_id, data)
            flash(f"Schedule has been updated successfully", 'success')
        except Exception as e:
            flash(f"Error updating schedule: {str(e)}", "danger")
            print(str(e))
        return redirect(url_for('routes.animal_schedules_page', animal_id=schedule.animal_id))

    #GET
    return render_template('caretaker/edit_schedules.html', form=form, schedule=schedule)

@routes.route('/caretaker/animal/<int:animal_id>/schedules/add', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def schedules_add_page(animal_id):
    form = AddSchedule()

    #POST
    if form.validate_on_submit():
        #DELETE IS CANCEL
        if form.delete.data:
            return redirect(url_for('routes.animal_schedules_page', animal_id=animal_id))

        #SAVE
        data = {
            'date': form.date.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data,
            'state': form.state.data,
            'animal_id': animal_id,
            'caretaker_id': current_user.id,
            'interval': form.interval.data,
            'count': form.count.data,
        }

        try:
            if form.repeat.data:
                create_multiple_schedules(data)
                flash(f"{form.count.data} schedules have been created successfully", 'success')
            else:
                create_schedule(data)
                flash(f"Schedule has been created successfully", 'success')
        except Exception as e:
            flash(f"Error creating schedule: {str(e)}", "danger")
            print(str(e))
        return redirect(url_for('routes.animal_schedules_page', animal_id=animal_id))

    #GET
    return render_template('caretaker/add_schedule.html', form=form, animal_id=animal_id)

@routes.route('/caretaker/animals/<int:animal_id>/requests', methods=['GET'])
@role_required('caretaker')
@login_required
def animal_med_page(animal_id):

    #GET
    filters = dict()
    filters['animal_id'] = animal_id
    filters['confirmed'] = False
    requests = filter_request(filters)

    return render_template('caretaker/requests.html', requests = requests, animal_id=animal_id)

@routes.route('/caretaker/request/<int:request_id>/edit', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def edit_request_page(request_id):
    request = get_request(request_id)
    form = EditRequest(obj=request)

    #POST
    if form.validate_on_submit():
        #DELETE
        if form.delete.data:
            try:
                delete_request(request_id)
                flash(f"Request has been deleted successfully", 'success')
            except Exception as e:
                flash(f"Error deleting request: {str(e)}", "danger")
            return redirect(url_for('routes.animal_med_page', animal_id=request.animal_id))

        #SAVE
        data = {
            'title': form.title.data,
            'description': form.description.data,
        }
        try:
            edit_request(request.id, data)
            flash(f"Request has been updated successfully", 'success')
        except Exception as e:
            flash(f"Error updating request: {str(e)}", "danger")
        return redirect(url_for('routes.animal_med_page', animal_id=request.animal_id))

    #GET
    edit = {
        'title': 'Edit',
        'route': 'routes.edit_request_page',
        'animal_id': request.animal_id,
    }
    return render_template('caretaker/edit_request.html', form=form, edit=edit, request_id=request_id)

@routes.route('/caretaker/animal/<int:animal_id>/request/add', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def add_request_page(animal_id):
    form = EditRequest()

    #POST
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'description': form.description.data,
            'animal_id': animal_id,
            'caretaker_id': current_user.id,
        }
        try:
            create_request(data)
            flash(f"Request has been created successfully", 'success')
        except Exception as e:
            flash(f"Error creating request: {str(e)}", "danger")
        return redirect(url_for('routes.animal_med_page', animal_id=animal_id))

    #GET
    edit = {
        'title': 'Add',
        'route': 'routes.add_request_page',
        'animal_id': animal_id,
    }
    return render_template('caretaker/edit_request.html', form=form, edit=edit)