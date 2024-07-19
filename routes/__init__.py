from flask import Blueprint, render_template, redirect, url_for, flash, session, jsonify
from forms import LoginForm, TaskForm
from models import db, Patrol, UsedKeyword, Family, FamilyTask
import random
from datetime import datetime
from game_status import game_in_progress, time_left, GAME_START_TIME, GAME_END_TIME

main = Blueprint('main', __name__)

# Mapowanie numeru końcowego na hasło
password_map = {
    '1': 'Zabrze',
    '2': 'Zawiercie',
    '3': 'Bydgoszcz',
    '4': 'Konin',
    '5': 'Zielonka'
}

magazines_a = ['A7', 'A8', 'A9', 'A10', 'B2', 'C2', 'C4', 'C6', 'C9', 'D2',
    'D6', 'D9', 'E6', 'E9', 'F3', 'F4', 'F6', 'G6', 'G10', 'H2', 'H6', 'I9',
    'I10', 'J2', 'J3', 'J4', 'J5']

magazines_b = ['A1', 'A2', 'A3', 'A4', 'A8', 'C4', 'C7', 'C9', 'D1', 'D2',
    'D4', 'D9', 'E4', 'E9', 'F4', 'F6', 'F7', 'G4', 'H1', 'H4', 'H7', 'H8',
    'H9', 'J5', 'J6', 'J7', 'J8']

magazines_c = ['A7', 'A8', 'B1', 'B2', 'B3', 'B4', 'C6', 'C9', 'D1', 'D6',
    'D9','E1', 'E6', 'E9', 'F1', 'F3', 'F6', 'G1', 'G10', 'H1', 'H7', 'I1',
     'I4', 'I7', 'I9', 'I10', 'J7']

magazines_d = ['A10', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'C9', 'D4', 'D5',
    'D6','D7', 'D9', 'E9', 'G1', 'G4', 'G5', 'G10', 'H7', 'I2', 'I3', 'I4', 
    'I5', 'I7', 'I9', 'I10', 'J7']

magazines_e = ['A3', 'A4', 'A5', 'A6', 'B9', 'C6', 'C7', 'C9', 'D1', 'D9',
    'E1', 'E9', 'F1', 'F4', 'F5', 'F6', 'F9', 'G9', 'H2', 'H4', 'H6', 'I9', 
    'J2', 'J3', 'J4', 'J5', 'J9']

magazines_f = ['A9', 'B1', 'B2', 'B3', 'B4', 'B9', 'C6', 'C7', 'D1', 'D3', 
    'E1', 'E10', 'F1', 'F4', 'F5', 'F6', 'F10', 'G10', 'H2', 'H8', 'H10', 'I10', 
    'J5', 'J6', 'J7', 'J8', 'J10']

magazine_lists = {
    'a': magazines_a,
    'b': magazines_b,
    'c': magazines_c,
    'd': magazines_d,
    'e': magazines_e,
    'f': magazines_f,
}

def assign_random_magazine(family):
    if family.assigned_magazines is None:
        family.assigned_magazines = []

    if family.discovered_magazines is None:
        family.discovered_magazines = 0

    available_magazines = list(set(magazine_lists[family.magazine_list]) - set(family.assigned_magazines))
    if available_magazines:
        assigned_magazine = random.choice(available_magazines)
        family.assigned_magazines.append(assigned_magazine)
        family.discovered_magazines += 1  # Odkryj magazyn dla rodziny
        db.session.commit()
        print(f"Assigned magazine: {assigned_magazine}")
        print(f"Updated assigned magazines: {family.assigned_magazines}")
        return assigned_magazine
    return None

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if not game_in_progress() and datetime.now() < GAME_START_TIME:
            flash('Gra jeszcze się nie rozpoczęła.', 'warning')
            return redirect(url_for('main.status'))

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
                if not game_in_progress() and datetime.now() > GAME_END_TIME:
                    flash('Gra już dawno się skońćzyła. Nie dostaniesz punktu za pierwsze logowanie.', 'warning')
                else:
                    first_login_keyword = f'{form.password.data}'
                    if not UsedKeyword.query.filter_by(patrol_id=patrol.id, keyword=first_login_keyword).first():

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
    if not game_in_progress() and datetime.now() < GAME_START_TIME:
        flash('Gra jeszcze się nie rozpoczęła.', 'danger')
        return redirect(url_for('main.status'))

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

    game_not_started = datetime.now() < GAME_START_TIME
    game_ended = datetime.now() > GAME_END_TIME

    form = TaskForm()
    if form.validate_on_submit():
        if game_ended:
            flash('Zajrzyj do rankingu by zobaczyć jak sobie poradziła twoja rodzina.', 'info')
        else:
            keyword = form.keyword.data.strip().lower()  # Usuń białe znaki i zmień na małe litery
            
            # Sprawdź, czy hasło zostało już użyte przez ten patrol
            if UsedKeyword.query.filter_by(patrol_id=patrol_id, keyword=keyword).first():
                flash('To hasło zostało już użyte', 'warning')
            else:
                if FamilyTask.query.filter_by(family_id=patrol.family_id, keyword=keyword).first():

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
                        family.end_time = datetime.now()
                        db.session.commit()
                        flash('Rodzina odkryła wszystkie magazyny! Wygraliście grę!', 'success')
                        return redirect(url_for('main.winner'))  # Przekierowanie na stronę wygranej
                else:
                    if family.discovered_magazines < 27:
                        if patrol.time_penalty < 25:
                            patrol.time_penalty += 5
                            db.session.commit()
                            flash('Niepoprawne hasło! Kara: 5 minut', 'danger')
                        else:
                            flash('Osiągnięto maksymalną liczbę kar dla tego patrolu.', 'danger')
                    else:
                        flash('Rodzina odkryła wszystkie magazyny, gra zakończona.', 'info')
        
    return render_template('task.html', form=form, patrol=patrol, family=family, game_not_started=game_not_started, game_ended=game_ended)


@main.route('/winner')
def winner():
    # Pobierz identyfikator patrolu z sesji
    if 'patrol_id' in session:
        patrol = Patrol.query.get(session['patrol_id'])
        family = Family.query.get(patrol.family_id)

        # Sprawdź, czy rodzina odkryła wszystkie magazyny
        if family.discovered_magazines >= 27:
            return render_template('winner.html', patrol=patrol, family=family)
        else:
            flash('Nie masz uprawnień do tej strony.', 'danger')
            return redirect(url_for('main.index'))
    else:
        flash('Nie jesteś zalogowany.', 'danger')
        return redirect(url_for('main.index'))


# routes.py

@main.route('/ranking')
def ranking():
    # Pobierz ID patrolu z sesji
    patrol_id = session.get('patrol_id')
    if not patrol_id:
        flash('Nie jesteś zalogowany.', 'danger')
        return redirect(url_for('main.index'))
    
    # Pobierz patrol i rodzinę z bazy danych
    patrol = Patrol.query.get(patrol_id)
    if not patrol or not patrol.family:
        flash('Nie znaleziono patrolu lub rodziny.', 'danger')
        return redirect(url_for('main.index'))
    
    family = patrol.family
    route = family.route  # Pobierz drogę rodziny

    families = Family.query.filter_by(route=route).all()

    # Filtruj rodziny, które nie odkryły żadnych magazynów
    families = [f for f in families if f.discovered_magazines]

    for family in families:
        # Oblicz sumaryczny czas kar dla rodziny
        total_penalty_time = sum(patrol.time_penalty for patrol in family.patrols if patrol.time_penalty)
        family.total_penalty_time = total_penalty_time  # Dodaj to pole dynamicznie
        family.total_time = ((family.end_time - GAME_START_TIME).total_seconds() + total_penalty_time * 60) if family.end_time else float('inf')

    # Sortuj rodziny po total_time i potem po discovered_magazines
    families = sorted(families, key=lambda f: (
        f.total_time,
        -f.discovered_magazines
    ))

    return render_template('ranking.html', families=families, game_start_time=GAME_START_TIME, route=route)


@main.route('/status')
def status():
    game_started = datetime.now() >= GAME_START_TIME
    game_ended = datetime.now() > GAME_END_TIME
    return render_template('status.html', 
                           game_in_progress=game_in_progress(), 
                           time_left=time_left(), 
                           game_start_time=GAME_START_TIME, 
                           game_end_time=GAME_END_TIME,
                           game_ended=game_ended)