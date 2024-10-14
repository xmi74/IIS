from __init__ import db
from app import app

def destroy_database():
    with app.app_context():
        # Otvorenie spojenia s databázou
        with db.engine.connect() as connection:
            # Vypnutie cudzieho kľúčového obmedzenia
            connection.execute(db.text('SET FOREIGN_KEY_CHECKS = 0;'))
            
            # Manuálne odstránenie tabuliek s cudzími kľúčmi najprv
            try:
                # Drop dependent tables first
                connection.execute(db.text('DROP TABLE IF EXISTS schedules;'))
                connection.execute(db.text('DROP TABLE IF EXISTS health_records;'))
                connection.execute(db.text('DROP TABLE IF EXISTS reservations;'))                
            except Exception as e:
                print(f"Error while dropping dependent tables: {e}")

            # Pokus o zmazanie všetkých ostatných tabuliek
            try:
                db.drop_all()  # Zmazať všetky ostatné tabuľky
                print("All other tables dropped")
            except Exception as e:
                print(f"Error while dropping tables: {e}")
            
            # Znovu zapnutie cudzieho kľúčového obmedzenia
            connection.execute(db.text('SET FOREIGN_KEY_CHECKS = 1;'))

        # Vytvorenie tabuliek odznova
        # db.create_all()
        # print("All tables recreated")

if __name__ == "__main__":
    destroy_database()
