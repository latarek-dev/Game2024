from flask import Blueprint, render_template, redirect, url_for, flash
from forms import LoginForm, TaskForm
from models import db, Patrol, UsedKeyword

main = Blueprint('main', __name__)

# Mapowanie numeru końcowego na hasło
password_map = {
    '1': 'Zabrze',
    '2': 'Zawiercie',
    '3': 'Bydgoszcz',
    '4': 'Konin',
    '5': 'Zielonka'
}

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
                patrol.score += 1
                db.session.commit()
                return redirect(url_for('main.task', patrol_id=patrol.id))
            else:
                flash('Niepoprawna nazwa patrolu lub hasło', 'danger')
        else:
            flash('Niepoprawna nazwa patrolu lub hasło', 'danger')
    return render_template('index.html', form=form)


# Pula haseł
valid_keywords = [
    'skłodowska', 'skała', 'żyrafa', 'hipopotam', 'cytryna', 
    'barć', 'hełm', 'chrobry', 'baron'
]

@main.route('/task/<int:patrol_id>', methods=['GET', 'POST'])
def task(patrol_id):
    patrol = Patrol.query.get_or_404(patrol_id)
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
                db.session.commit()
                flash('Hasło poprawne!', 'success')
            else:
                patrol.time_penalty += 5
                db.session.commit()
                flash('Niepoprawne hasło! Kara: 5 minut', 'danger')
    
    return render_template('task.html', form=form, patrol=patrol)