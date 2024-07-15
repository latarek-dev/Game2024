from flask import Blueprint, render_template, redirect, url_for, flash
from forms import LoginForm, TaskForm
from models import db, Patrol, Family, Task

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        patrol = Patrol.query.filter_by(id=form.patrol_id.data).first()
        if patrol:
            return redirect(url_for('main.task', patrol_id=patrol.id))
        else:
            flash('Patrol nie istnieje', 'danger')
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
            patrol.time_penalty += 2
            db.session.commit()
            flash('Niepoprawne hasło! Kara: 2 minuty', 'danger')
    return render_template('task.html', form=form, patrol=patrol)
