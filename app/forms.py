from flask_wtf import FlaskForm
from wtforms import (
    PasswordField, SelectField, SelectMultipleField,
    StringField, SubmitField, TextAreaField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import CheckboxInput

from app.models import User
from app.enums import ShiftTime, Team
from app.choises import equipment, team_composition
from app.custom_widgets import select_multi_checkbox


class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Придумайте логин', validators=[DataRequired()])
    first_name = StringField('Ваше имя', validators=[DataRequired()])
    last_name = StringField('Ваша фамилия', validators=[DataRequired()])
    post = StringField('Ваша должность', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Придумайте пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Польлзователь с таким именем уже существует'
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким email уже существует')


class LogForm(FlaskForm):
    shift_time = SelectField(
        'Часы смены',
        choices=[
            v for k, v in ShiftTime.__dict__.items() if not k.startswith('_')
        ]
    )
    team = SelectField(
        'Смена',
        choices=[
            v for k, v in Team.__dict__.items() if not k.startswith('_')
        ]
    )
    team_composition = SelectMultipleField(
        'Состав смены',
        choices=[(i, i) for i in team_composition],
        widget=select_multi_checkbox
    )
    equipment_run = SelectMultipleField(
        'Оборудование в работе',
        choices=[(i, i) for i in equipment],
        widget=select_multi_checkbox
    )
    equipment_repair = SelectMultipleField(
        'Оборудование в ремонте',
        choices=[(i, i) for i in equipment],
        widget=select_multi_checkbox
    )
    oper_notes = TextAreaField('Оперативные сменные записи')
    defects = TextAreaField('Замечания и неполадки в работе оборудования')
    submit = SubmitField('Сохранить изменения')

    def validate_equipment_repair(self, equipment_repair):
        for item in equipment_repair:
            if item in self.equipment_run:
                raise ValidationError(
                    'Данное оборудование находится в работе'
                )
