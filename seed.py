from datetime import datetime, time, date

from models.enums.schedule_state import ScheduleState
from models.user import Admin, Vet, Caretaker, Volunteer
from models.animal import Animal
from models.walk_schedule import WalkSchedule
from models.examination import Examination, Vaccination, PreventiveCheckUp
from models.request import Request
from models.enums.vaccination_type import VaccinationType
from models.metadata import Metadata
# from db import db

def seed_data(db):
    # Ověření, zda již byla data nasazena
    if Metadata.query.filter_by(name='seed_data').first():
        print("seed.py: Sample data already exist, skipping seeding")
        return

    # Vytvoření uživatelů (specializované třídy User)
    admin1 = Admin(login='admin1', first_name='John', last_name='Doe', password='1234', role='admin', email='admin1@example.com')
    vet1 = Vet(login='vet1', first_name='James', last_name='Smith', password='1234', role='vet', email='vet1@example.com')
    caretaker1 = Caretaker(login='caretaker1', first_name='Robert', last_name='Adams', password ='1234', role='caretaker', email='caretaker1@example.com')
    volunteer1 = Volunteer(login='volunteer1', first_name='Teresa', last_name='Gilbert', password ='1234', role='volunteer', email='volunteer1@example.com')

    # Přidání uživatelů do session
    db.session.add_all([admin1, vet1, caretaker1, volunteer1])
    db.session.commit()

    # Vytvoření zvířat a přiřazení ke konkrétnímu pečovateli
    animal1 = Animal(name='Bob', species='Dog', weight=30, birth_date=datetime(2020, 10, 1, 12, 0), photo='https://images.pexels.com/photos/5265677/pexels-photo-5265677.jpeg')
    animal2 = Animal(name='Greg', species='Cat', weight=30, birth_date=datetime(2021, 10, 1, 12, 0), photo='https://images.pexels.com/photos/20787/pexels-photo.jpg')

    # Přidání zvířat do session
    db.session.add_all([animal1, animal2])
    db.session.commit()

    # Vytvoření záznamů o zdravotních prohlídkách
    vaccination1 = Vaccination(date=datetime(2024, 10, 6, 12, 0), description='Rabies vaccination', type='vaccination', animal_id=animal1.id, vet_id=vet1.id, vaccination_type=VaccinationType.RABIES.value)
    checkup1 = PreventiveCheckUp(date=datetime(2024, 10, 6, 15, 0), description='General health checkup', type='checkup', animal_id=animal2.id, vet_id=vet1.id)
    db.session.add_all([vaccination1, checkup1])
    db.session.commit()

    request1 = Request(
        description="Animal needs a preventive checkup",
        caretaker_id=caretaker1.id,
        animal_id=animal1.id,
        vet_id=vet1.id)
    
    request2 = Request(
        description="Animal needs to get checked for ticks",
        caretaker_id=caretaker1.id,
        animal_id=animal2.id,
        vet_id=vet1.id)

    # Přidání záznamů do session
    db.session.add_all([request1, request2])
    db.session.commit()

    # Vytvoření rozvrhu pro procházky
    schedule1 = WalkSchedule(
        date= date(2024, 10, 6),
        start_time=time( 12, 0),
        end_time=time(13, 0),
        description='Morning walk',
        state=ScheduleState.FREE.value,
        animal_id=animal1.id,
        caretaker_id=caretaker1.id)
    schedule2 = WalkSchedule(
        date=date(2024, 10, 7),
        start_time=time(12, 0),
        end_time=time(13, 0),
        description='Evening walk',
        state=ScheduleState.FREE.value,
        animal_id=animal2.id,
        caretaker_id=caretaker1.id)

    # Přidání rozvrhu do session
    db.session.add_all([schedule1, schedule2])
    db.session.commit()

    # Vytvoření záznamu o nasazení dat
    seed_flag = Metadata(name='seed_data', value='true')
    db.session.add(seed_flag)
    db.session.commit()

    print("Seed.py: Finished seeding data")
