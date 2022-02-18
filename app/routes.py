from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Павел'}
    log = {
        'text': 'test log',
        'pub_date': '18.02.2022',
        'author': user,
    }
    return render_template(
        'index.html',
        logs=[log]
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Приветстуем, {}'.format(
            form.username.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход в систему', form=form)
