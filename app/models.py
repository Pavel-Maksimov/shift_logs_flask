from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    post = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    logs = db.relationship('Log', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Log {}>'.format(self.body[:100])


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
