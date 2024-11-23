import datetime
from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
from forms.create_user import CreateUserForm
from models.enums.animal_species import Species
from forms.add_examination import AddExaminationForm
from models.user import User, Admin, Caretaker, Volunteer, Vet
from models.animal import Animal
from models.examination import Examination, PreventiveCheckUp, Vaccination
from models.request import Request
from models.walk_schedule import WalkSchedule
from forms.register import RegistrationForm
from forms.login import LoginForm
from forms.edit_user import EditUserForm
from api.api_users import *
from api.api_requests import *
from api.api_examinations import *
from models.enums.schedule_state import ScheduleState
from models.enums.animal_species import Species
from utils.decorators import role_required

routes = Blueprint('routes', __name__)

################ HOME PAGE ################

@routes.route('/')
def home_page():
    caretakers = filter_users({'role': 'caretaker'})
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
        query = query.filter(Animal.species == species)

    animals = query.all()
    return render_template('public/animals.html', animals=animals, Species=Species)


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
    session.clear()  # Prevents cache exploitation
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

    return render_template('admin/dashboard_admin.html', users=users, role_format=role_format)

@routes.route('/admin/create_user', methods=['GET', 'POST'])
@role_required('admin')
@login_required
def admin_create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        new_user = User(
            login=form.login.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            role=form.role.data,
            password=form.password.data  # Hash
        )
        # Save the new user
        db.session.add(new_user)
        db.session.commit()
        flash("User successfully created!", "success")
        return redirect(url_for('routes.dashboard_admin_page'))

    return render_template('admin/admin_create_user.html', form=form)


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
    
    return render_template('admin/edit_user.html', form=form, user=user)        


#################################################
#                 DASHBOARD VET                 #
#################################################

@routes.route('/dashboard_vet')
@role_required('vet')
@login_required
def dashboard_vet_page():    
    confirmed_filter = request.args.get('confirmed')

    if confirmed_filter == "true":
        confirmed_filter = True
    elif confirmed_filter == "false":
        confirmed_filter = False
    else:
        confirmed_filter = None

    vet_requests = get_requests_by_vet(current_user.id, confirmed_filter)

    return render_template('vet/dashboard_vet.html', vet_requests=vet_requests)

################ REQUEST SECTION ################

@routes.route('/dashboard_vet/request_detail/<int:request_id>', methods=['GET', 'POST'])
@role_required('vet')
@login_required
def request_detail_page(request_id):
    specific_request = get_request(request_id)

    form = AddExaminationForm()

    if form.validate_on_submit():
        data = {
            'date': form.date.data,
            'type': form.type.data,
            'description': form.description.data,
            'vet_id': current_user.id,
            'animal_id': specific_request.animal_id
        }
        try:
            print(f"Data received: {data}")
            edit_request_confirmed(request_id, True)
            create_examination(data)
            flash("Request confirmed and examination created.", "success")
            return redirect(url_for('routes.dashboard_vet_page'))
        except Exception as e:
            flash(f"Error confirming and creating examination: {str(e)}", "danger")
        
    now = datetime.now()
    return render_template('vet/request_detail.html', specific_request=specific_request, form=form, now=now)


################ EXAMINATIONS SECTION ################

@routes.route('/dashboard_vet/vets_examinations', methods=['GET', 'POST'])
@role_required('vet')
@login_required
def vets_examinations_page():
    vet_examinations = get_examinations_by_vet(current_user.id)

    return render_template('vet/vets_examinations.html', vet_examinations=vet_examinations)


@routes.route('/dashboard_vet/vets_examinations/<int:examination_id>', methods=['GET', 'POST'])
@role_required('vet')
@login_required
def examination_detail_page(examination_id):
    specific_examination = get_examination(examination_id)    

    return render_template('vet/examination_detail.html', specific_examination=specific_examination)


@routes.route('/dashboard_vet/create_examination', methods=['GET', 'POST'])
@role_required('vet')
@login_required
def create_examination_page():
    form = AddExaminationForm()

    animals = get_animals(filters=None) 
    form.animal_id.choices = [(animal.id, f"ID: {animal.id} | {animal.name} | {animal.species}") for animal in animals]

    if form.validate_on_submit():
        data = {
            'animal_id': form.animal_id.data,
            'date': form.date.data,
            'type': form.type.data,
            'vaccination_type': form.vaccination_type.data if form.type.data == 'vaccination' else None,
            'description': form.description.data,
            'vet_id': current_user.id
        }

        try:
            create_examination(data) 
            flash("Examination successfully created.", "success")
            return redirect(url_for('routes.vets_examinations_page'))
        except Exception as e:
            flash(f"Error creating examination: {str(e)}", "danger")

    return render_template('vet/create_examination.html', form=form)


@routes.route('/dashboard_vet/edit_examination/<int:examination_id>', methods=['GET', 'POST'])
@role_required('vet')
@login_required
def edit_examination_page(examination_id):
    examination = get_examination(examination_id)
    if not examination:
        flash(f"Examination with ID {examination_id} not found.", "danger")
        return redirect(url_for('routes.vets_examinations_page'))

    form = AddExaminationForm(obj=examination)

    if examination.type != 'vaccination':
        form.vaccination_type.data = None

    if form.validate_on_submit():
        examination.date = form.date.data
        examination.type = form.type.data
        examination.description = form.description.data
        if form.type.data == 'vaccination':
            examination.vaccination_type = form.vaccination_type.data

        try:
            db.session.commit()
            flash("Examination successfully updated.", "success")
            return redirect(url_for('routes.vets_examinations_page'))
        except Exception as e:
            flash(f"Error updating examination: {str(e)}", "danger")

    return render_template('vet/edit_examination.html', form=form, examination=examination)


@routes.route('/dashboard_vet/delete_examination/<int:examination_id>', methods=['POST'])
@role_required('vet')
@login_required
def delete_examination_page(examination_id):
    try:
        delete_examination(examination_id)
        flash("Examination successfully deleted.", "success")
    except Exception as e:
        flash(f"Error deleting examination: {str(e)}", "danger")

    return redirect(url_for('routes.vets_examinations_page'))

################ HEALTH RECORDS SECTION ################

@routes.route('/dashboard_vet/animal_hr', methods=['GET'])
@role_required('vet')
@login_required
def animal_health_records_page():
    animals = get_animals(filters=None)

    animals_hrecords_count = [
        {
            'animal': animal,
            'health_records_count': len(animal.examinations)  # Predpokladáme vzťah examinations
        }
        for animal in animals
    ]
    
    return render_template('vet/animal_hr.html', animals_hrecords_count=animals_hrecords_count)

@routes.route('/dashboard_vet/animal_hr/<int:animal_id>', methods=['GET'])
@role_required('vet')
@login_required
def animal_health_records_detail_page(animal_id):
    health_records = get_examinations_by_animal(animal_id)

    return render_template('vet/animal_hr_detail.html', health_records=health_records)

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
    return render_template('caretaker/animals.html', animals=animals, species=Species)

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
        data = {
            'name': form.name.data,
            'species': form.species.data,
            'weight': form.weight.data,
            'birth_date': form.birth_date.data,
            'photo': form.photo.data,
            'description': form.description.data,
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
            'photo': form.photo.data,
            'description': form.description.data,
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
    
    animal = get_animal(animal_id)
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
    filters['animal_id'] = animal_id
    filters['state'] = request.args.get('state') or None
    if request.args.get('old') is None: filters['upcoming'] = True
    schedules = get_schedules(filters)
    # schedules = get_incoming_animal_schedules(animal_id)
    return render_template('caretaker/schedules.html', schedules=schedules, animal_id=animal_id, animal_name=animal.name, ScheduleState=ScheduleState)

@routes.route('/caretaker/schedules/edit/<int:id>', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def schedules_edit_page(id):
    schedule = get_schedule(id)
    form = EditSchedules(obj=schedule)

    # POST
    if form.validate_on_submit():
        # Delete button
        if form.delete.data:
            try:
                delete_schedule(id)
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
        #delete volunteer is switching to FREE state
        if form.state.data != ScheduleState.FREE.value: data['volunteer_id'] = schedule.volunteer_id

        try:
            edit_schedule(id, data)
            flash(f"Schedule has been updated successfully", 'success')
        except Exception as e:
            flash(f"Error updating schedule: {str(e)}", "danger")
            print(str(e))
        return redirect(url_for('routes.animal_schedules_page', animal_id=schedule.animal_id))

    #GET
    edit = {
        'title': 'Edit',
        'route': 'routes.schedules_edit_page',
        'id': schedule.id,
        'animal_id': schedule.animal_id,
    }
    return render_template('caretaker/edit_schedule.html', form=form, edit=edit)

@routes.route('/caretaker/animal/<int:id>/schedules/add', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def schedules_add_page(id):
    form = AddSchedule()

    #POST
    if form.validate_on_submit():
        #SAVE
        data = {
            'date': form.date.data,
            'start_time': form.start_time.data,
            'end_time': form.end_time.data,
            'state': form.state.data,
            'animal_id': id,
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
        return redirect(url_for('routes.animal_schedules_page', animal_id=id))

    #GET
    edit = {
        'title': 'Add',
        'route': 'routes.schedules_add_page',
        'id': id,
        'animal_id': id,
    }
    return render_template('caretaker/edit_schedule.html', form=form, edit=edit)

@routes.route('/caretaker/animals/<int:animal_id>/requests', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def animal_request_page(animal_id):
    animal = get_animal(animal_id)
    
    #POST
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        print(request_id)
        try:
            delete_request(request_id)
            flash(f"Request has been deleted successfully", 'success')
        except Exception as e:
            flash(f"Error deleting request: {str(e)}", "danger")

    #GET
    filters = dict()
    filters['animal_id'] = animal_id
    if request.args.get('confirmed') is None: filters['confirmed'] = False
    requests = filter_request(filters)

    return render_template('caretaker/requests.html', requests = requests, animal_name=animal.name, animal_id=animal_id)

@routes.route('/caretaker/request/<int:id>/edit', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def edit_request_page(id):
    request = get_request(id)
    form = EditRequest(obj=request)

    #POST
    if form.validate_on_submit():
        #DELETE
        if form.delete.data:
            try:
                delete_request(id)
                flash(f"Request has been deleted successfully", 'success')
            except Exception as e:
                flash(f"Error deleting request: {str(e)}", "danger")
            return redirect(url_for('routes.animal_request_page', animal_id=request.animal_id))

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
        return redirect(url_for('routes.animal_request_page', animal_id=request.animal_id))

    #GET
    edit = {
        'title': 'Edit',
        'route': 'routes.edit_request_page',
        'id': id,
        'animal_id': request.animal_id,
    }
    return render_template('caretaker/edit_request.html', form=form, edit=edit, request_id=id)

@routes.route('/caretaker/animal/<int:id>/request/add', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def add_request_page(id):
    form = EditRequest()

    #POST
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'description': form.description.data,
            'id': id,
            'animal_id': id,
            'caretaker_id': current_user.id,
        }
        try:
            create_request(data)
            flash(f"Request has been created successfully", 'success')
        except Exception as e:
            flash(f"Error creating request: {str(e)}", "danger")
        return redirect(url_for('routes.animal_request_page', animal_id=id))

    #GET
    edit = {
        'title': 'Add',
        'route': 'routes.add_request_page',
        'id': id,
        'animal_id': id,
    }
    return render_template('caretaker/edit_request.html', form=form, edit=edit)



@routes.route('/caretaker/confirm_reservations', methods=['GET', 'POST'])
@role_required('caretaker')
@login_required
def confirm_reservations_page():
    now = datetime.now()
    fifteen_minutes = timedelta(minutes=15)
    five_minutes = timedelta(minutes=5)

    # Fetch schedules for the caretaker
    pending_schedules = WalkSchedule.query.filter_by(state=ScheduleState.RESERVED.value).all()
    ready_for_in_progress = WalkSchedule.query.filter(
        WalkSchedule.state == ScheduleState.CONFIRMED.value,
        WalkSchedule.start_time <= (now + five_minutes).time(),
        WalkSchedule.start_time >= (now - fifteen_minutes).time()
    ).all()
    in_progress_schedules = WalkSchedule.query.filter_by(state=ScheduleState.IN_PROGRESS.value).all()

    return render_template(
        'caretaker/confirm_reservations.html',
        pending_schedules=pending_schedules,
        ready_for_in_progress=ready_for_in_progress,
        in_progress_schedules=in_progress_schedules
    )

@routes.route('/schedule/confirm/<int:schedule_id>', methods=['POST'])
@role_required('caretaker')
@login_required
def confirm_schedule(schedule_id):
    schedule = WalkSchedule.query.get_or_404(schedule_id)
    if schedule.state == ScheduleState.RESERVED.value:
        schedule.state = ScheduleState.CONFIRMED.value
        db.session.commit()
        flash("Schedule confirmed successfully!", "success")
    return redirect(url_for('routes.confirm_reservations_page'))

@routes.route('/schedule/start/<int:schedule_id>', methods=['POST'])
@role_required('caretaker')
@login_required
def start_schedule(schedule_id):
    schedule = WalkSchedule.query.get_or_404(schedule_id)
    if schedule.state == ScheduleState.CONFIRMED.value:
        schedule.state = ScheduleState.IN_PROGRESS.value
        db.session.commit()
        flash("Schedule started successfully!", "success")
    return redirect(url_for('routes.confirm_reservations_page'))

@routes.route('/schedule/complete/<int:schedule_id>', methods=['POST'])
@role_required('caretaker')
@login_required
def complete_schedule(schedule_id):
    schedule = WalkSchedule.query.get_or_404(schedule_id)
    if schedule.state == ScheduleState.IN_PROGRESS.value:
        schedule.state = ScheduleState.COMPLETED.value
        db.session.commit()
        flash("Schedule completed successfully!", "success")
    return redirect(url_for('routes.confirm_reservations_page'))