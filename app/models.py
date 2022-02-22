from datetime import date
from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from app import db, login
from app.enums import ChoiceType, ShiftTime, Team, ValueEnum
from app.choises import equipment, team_composition


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(60),
        index=True,
        unique=True,
        nullable=False
    )
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    post = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    logs = db.relationship('Log', backref='author', lazy='dynamic')

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.Date, default=date.today)
    shift_time = db.Column(
        ValueEnum(ShiftTime),
        default='00:00-08:00'
    )
    team = db.Column(
        ValueEnum(Team),
        default='А'
    )
    team_composition = db.Column(ChoiceType(team_composition))
    equipment_run = db.Column(ChoiceType(equipment))
    equipment_repair = db.Column(ChoiceType(equipment))
    oper_notes = db.Column(db.Text)
    defects = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_accepted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Log {}, {}>'.format(self.pub_date, self.shift_time)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
