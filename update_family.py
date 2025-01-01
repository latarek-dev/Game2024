from models import db
from app import app  # Import aplikacji Flask
from sqlalchemy import text  # Import funkcji text

with app.app_context():  # Kontekst aplikacji Flask
    # Wykonanie zapytania SQL z użyciem text
    db.session.execute(text("""
        UPDATE Family
        SET
            end_time = '2024-07-30 16:52:10'
        WHERE id = 18;
    """))
    db.session.execute(text("""
        UPDATE Family
        SET
            end_time = '2024-07-30 17:25:56'
        WHERE id = 9;
    """))
    db.session.execute(text("""
        UPDATE Family
        SET
            end_time = '2024-07-30 17:56:36'
        WHERE id = 22;
    """))
    db.session.commit()
    print("Wiersz został zaktualizowany!")
