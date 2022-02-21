from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LogForm, LoginForm, RegistrationForm
from app.models import Log, User


@app.route('/')
@app.route('/index')
@login_required
def index():
    logs = Log.query.all()
    return render_template(
        'index.html',
        title='Главная страница',
        logs=logs
    )


@app.route('/log/<id>', methods=['GET', 'POST'])
@login_required
def log(id):
    log = Log.query.filter_by(id=id).first_or_404()
    form = LogForm(obj=log)
    if request.method == 'POST' and form.validate_on_submit():
        log.shift_time = form.shift_time.data
        form.populate_obj(log)
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('log', id=log.id))
    return render_template(
        'log.html',
        title='Сменный журнал',
        log=log,
        form=form
    )


@app.route('/pass_shift/<id>')
@login_required
def pass_shift(id):
    log = Log.query.filter_by(id=id).first_or_404()
    log.is_active = False
    db.session.commit()
    flash('Вы сдали смену')
    return redirect(url_for('log', id=log.id))


@app.route('/accept_shift/<id>')
@login_required
def accept_shift(id):
    accepted = Log.query.filter_by(id=id).first()
    accepted.is_accepted = True
    db.session.add(accepted)
    log = Log(
        author=current_user,
        equipment_run=accepted.equipment_run,
        equipment_repair=accepted.equipment_repair,
        oper_notes=accepted.oper_notes,
        defects=accepted.defects
    )
    db.session.add(log)
    db.session.commit()
    flash('Вы приняли смену')
    return redirect(url_for('log', id=log.id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя или пароль')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход в систему', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            post=form.post.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегестрировались в системе!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)
