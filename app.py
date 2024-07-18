from flask import Flask
from flask_migrate import Migrate
from models import db, Family
from routes import main
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')

# Inicjalizacja bazy danych
db.init_app(app)
migrate = Migrate(app, db)

# Rejestracja blueprinta
app.register_blueprint(main)

# Czas rozpoczęcia i zakończenia gry
#GAME_START_TIME = datetime(2024, 7, 18, 2, 40, 0)
#GAME_END_TIME = datetime(2024, 7, 18, 2, 45, 0)

def end_game():
    with app.app_context():
        families = Family.query.all()
        for family in families:
            if family.end_time is None:
                family.end_time = GAME_END_TIME
        db.session.commit()
        print("Gra zakończona dla wszystkich rodzin.")

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
 #   scheduler.add_job(func=end_game, trigger='date', run_date=GAME_END_TIME)
    scheduler.start()

    app.run(debug=True)
