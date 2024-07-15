from flask import Flask
from flask_migrate import Migrate
from routes import main
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')

# Inicjalizacja bazy danych
db.init_app(app)
migrate = Migrate(app, db)

# Rejestracja blueprinta
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
