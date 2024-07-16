from flask import Blueprint, render_template, redirect, url_for, flash
from forms import LoginForm, TaskForm
from models import db, Patrol, Task

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


@main.route('/task/<int:patrol_id>', methods=['GET', 'POST'])
def task(patrol_id):
    patrol = Patrol.query.get_or_404(patrol_id)
    form = TaskForm()
    if form.validate_on_submit():
        task = Task.query.filter_by(keyword=form.keyword.data, family_id=patrol.family_id).first()
        if task:
            patrol.score += 1
            db.session.commit()
            flash('Hasło poprawne!', 'success')
        else:
            patrol.time_penalty += 5
            db.session.commit()
            flash('Niepoprawne hasło! Kara: 5 minuty', 'danger')
    return render_template('task.html', form=form, patrol=patrol)
