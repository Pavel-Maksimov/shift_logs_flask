import enum
from enum import Enum

from app import db


class ValueEnum(db.TypeDecorator):
    impl = db.String()

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, ValueEnum):
            return value
        elif isinstance(value, str):
            return value
        return value.value

    def process_result_value(self, value, dialect):
        if isinstance(value, str):
            return value
        return self._enumtype(value)


class ChoiceType(db.TypeDecorator):

    impl = db.PickleType

    def __init__(self, choices, **kw):
        self.choices = list(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, values, dialect):
        return [k for k in self.choices if k in values]

    def process_result_value(self, value, dialect):
        return value


class ShiftTime(ValueEnum):
    FIRST = '00:00-08:00'
    SECOND = '08:00-16:00'
    THIRD = '16:00-00:00'


class Team(ValueEnum):
    FIRST = 'А'
    SECOND = 'Б'
    THIRD = 'В'
    FORTH = 'Г'
    FIFTH = 'Д'
