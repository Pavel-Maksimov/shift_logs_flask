from flask import render_template, flash, redirect

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Павел'}
    post = {
        'text': 'test post',
        'pub_date': '18.02.2022',
        'author': user,
        'group': None,
        'image': None
    }
    return render_template(
        'index.html',
        path='home',
        page=[post]
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Приветстуем, {}'.format(
            form.username.data))
        return redirect('/index')
    return render_template('login.html', title='Вход в систему', form=form)
