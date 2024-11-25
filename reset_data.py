# Nepotrebny na odovzdanie

from __init__ import db
from app import app

def destroy_database():
    with app.app_context():
        with db.engine.connect() as connection:
            connection.execute(db.text('SET FOREIGN_KEY_CHECKS = 0;'))
            
            try:
                # Drop dependent tables first
                connection.execute(db.text('DROP TABLE IF EXISTS schedules;'))
                connection.execute(db.text('DROP TABLE IF EXISTS health_records;'))
                connection.execute(db.text('DROP TABLE IF EXISTS reservations;'))                
            except Exception as e:
                print(f"Error while dropping dependent tables: {e}")

            try:
                db.drop_all()
                print("All other tables dropped")
            except Exception as e:
                print(f"Error while dropping tables: {e}")
            
            connection.execute(db.text('SET FOREIGN_KEY_CHECKS = 1;'))

if __name__ == "__main__":
    destroy_database()
