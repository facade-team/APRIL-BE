from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy import DateTime

db = SQLAlchemy()


class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routine_time = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Routine {self.id}>"


class Device(db.Model):
    # Routine 의 PK 를 FK 로 가짐
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey("routine.id"))
    routine = db.relationship("Routine", backref=db.backref("devices", lazy=True))
    device = db.Column(db.String(100), nullable=True)
    power = db.Column(db.String(100), nullable=True)
    level = db.Column(db.Integer, nullable=True)


class DeviceSchema(Schema):
    device = fields.String()
    power = fields.String()
    level = fields.Integer()


class RoutineSchema(Schema):
    routine_id = fields.Integer(attribute="id")
    execute_time = fields.DateTime(
        attribute="routine_time", format="%Y-%m-%dT%H:%M:%S.%f"
    )
    routine_list = fields.Nested(DeviceSchema, attribute="devices", many=True)
