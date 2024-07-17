from flask import Blueprint, render_template, redirect, url_for, flash, session
from forms import LoginForm, TaskForm
from models import db, Patrol, UsedKeyword, Family
import random

main = Blueprint('main', __name__)

# Mapowanie numeru końcowego na hasło
password_map = {
    '1': 'Zabrze',
    '2': 'Zawiercie',
    '3': 'Bydgoszcz',
    '4': 'Konin',
    '5': 'Zielonka'
}

# Pula haseł
valid_keywords = [
    'skłodowska', 'skała', 'żyrafa', 'hipopotam', 'cytryna', 
    'barć', 'hełm', 'chrobry', 'baron'
]

magazines_a = ['A7', 'A8', 'A9', 'A10', 'B2', 'C2', 'C4', 'C6', 'C9', 'D2',
    'D6', 'D9', 'E6', 'E9', 'F3', 'F4', 'F6', 'G6', 'G10', 'H2', 'H6', 'I9',
    'I10', 'J2', 'J3', 'J4', 'J5'
    ]


# Funkcja do przypisywania losowej współrzędnej magazynu rodzinie
def assign_random_magazine(family):
    if family.assigned_magazines is None:
        family.assigned_magazines = []

    if family.discovered_magazines is None:
        family.discovered_magazines = 0

    if not hasattr(family, 'assigned_magazines'):
        family.assigned_magazines = []
    
    available_magazines = list(set(magazines_a) - set(family.assigned_magazines))
    if available_magazines:
        assigned_magazine = random.choice(available_magazines)
        family.assigned_magazines.append(assigned_magazine)
        family.discovered_magazines += 1  # Odkryj magazyn dla rodziny
        db.session.commit()
        return assigned_magazine
    return None

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        patrol_id = form.patrol_id.data
        # Pobierz numer końcowy z patrol_id
        patrol_number = patrol_id[-1]
        patrol_name = patrol_id[:-1]
        
        # Sprawdź, czy numer końcowy jest w mapowaniu
        if patrol_number in password_map:
            expected_password = password_map[patrol_number]
            patrol = Patrol.query.filter_by(name=patrol_id).first()

            if patrol and form.password.data == expected_password:
                # Zapisz identyfikator patrolu w sesji
                session['patrol_id'] = patrol.id
                
                family = Family.query.get_or_404(patrol.family_id)
                # Sprawdź czy punkt za pierwsze logowanie został już przyznany
                first_login_keyword = f'{form.password.data}'
                if not UsedKeyword.query.filter_by(patrol_id=patrol.id, keyword=first_login_keyword).first():
                    patrol.score += 1
                    new_used_keyword = UsedKeyword(keyword=first_login_keyword, patrol_id=patrol.id)
                    db.session.add(new_used_keyword)


                    # Przypisz losową współrzędną magazynu rodzinie przy pierwszym logowaniu
                    assigned_magazine = assign_random_magazine(family)
                    if assigned_magazine:
                        flash(f'Punkt za pierwsze logowanie! Odkryto magazyn na współrzędnych: {assigned_magazine}', 'success')

                    db.session.commit()
                else:
                    flash('Zalogowano ponownie.', 'info')
                db.session.commit()
                return redirect(url_for('main.task', patrol_id=patrol.id))
            else:
                flash('Niepoprawna nazwa patrolu lub hasło', 'danger')
        else:
            flash('Niepoprawna nazwa patrolu lub hasło', 'danger')
    return render_template('index.html', form=form)


@main.route('/task/<int:patrol_id>', methods=['GET', 'POST'])
def task(patrol_id):
    # Sprawdź, czy patrol_id w sesji jest taki sam jak w URL
    if 'patrol_id' not in session or session['patrol_id'] != patrol_id:
        flash('Nie jesteś zalogowany jako ten patrol', 'danger')
        return redirect(url_for('main.index'))
    
    patrol = Patrol.query.get_or_404(patrol_id)
    family = Family.query.get_or_404(patrol.family_id)

    # Inicjalizuj discovered_magazines, jeśli jest None
    if family.discovered_magazines is None:
        family.discovered_magazines = 0

    # Inicjalizuj assigned_magazines, jeśli jest None
    if family.assigned_magazines is None:
        family.assigned_magazines = []

    print(family.assigned_magazines)

    form = TaskForm()
    if form.validate_on_submit():
        keyword = form.keyword.data.strip().lower()  # Usuń białe znaki i zmień na małe litery
        patrol_name_without_number = ''.join(filter(str.isalpha, patrol.name)).lower()  # Nazwa patrolu bez cyfry
        
        # Sprawdź, czy hasło zostało już użyte przez ten patrol
        if UsedKeyword.query.filter_by(patrol_id=patrol_id, keyword=keyword).first():
            flash('To hasło zostało już użyte', 'warning')
        else:
            if keyword in valid_keywords or keyword == patrol_name_without_number:
                patrol.score += 1

                # Dodaj używane hasło do bazy danych tylko jeśli jest prawidłowe
                new_used_keyword = UsedKeyword(keyword=keyword, patrol_id=patrol_id)
                db.session.add(new_used_keyword)

                # Przypisz losową współrzędną magazynu rodzinie
                assigned_magazine = assign_random_magazine(family)
                if assigned_magazine:
                    flash(f'Hasło poprawne! Odkryto magazyn na współrzędnych: {assigned_magazine}', 'success')
                else:
                    flash('Hasło poprawne, ale wszystkie magazyny zostały już odkryte.', 'success')
                
                db.session.commit()

                # Sprawdź, czy rodzina odkryła wszystkie magazyny
                if family.discovered_magazines >= 27:
                    flash('Rodzina odkryła wszystkie magazyny! Wygraliście grę!', 'success')
            else:
                patrol.time_penalty += 5
                db.session.commit()
                flash('Niepoprawne hasło! Kara: 5 minut', 'danger')
    
    return render_template('task.html', form=form, patrol=patrol, family=family)
