import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
from climbinghero import db

# Create a custom JsonEncodedDict class in a file accessed by your models
#Enables JSON storage by encoding and decoding on the fly
class JSONEncodedDict(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return json.loads(value)

class Continent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(11), nullable=False)
    name = db.Column(db.String(255))

    country = db.relationship('Country', lazy=True)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    cca2 = db.Column(db.String(2), nullable=False)
    cca3 = db.Column(db.String(3), nullable=False)
    ccn3 = db.Column(db.Integer, nullable=False)

    continent_id = db.Column(db.Integer, db.ForeignKey('continent.id'), nullable=False)

    province = db.relationship('Province', lazy=True)
    user = db.relationship('User', lazy=True)

class Province(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=True)
    hasc = db.Column(db.String(60), nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    sector = db.relationship('Sector', lazy=True)

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    descr = db.Column(db.Text)
    getin = db.Column(db.Text)
    coord = db.Column(JSONEncodedDict)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    province_id = db.Column(db.Integer, db.ForeignKey('province.id'), nullable=False)

    subsector = db.relationship('Subsector', lazy=True)
    route = db.relationship('Route', lazy=True)


class Subsector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    descr = db.Column(db.Text)
    getin = db.Column(db.Text)
    area = db.Column(JSONEncodedDict)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)

    route = db.relationship('Route', lazy=True)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    leng = db.Column(db.Integer)
    pitch = db.Column(db.Integer)
    grade = db.Column(db.String(4), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    descr = db.Column(db.Text)
    equip = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    subsector_id = db.Column(db.Integer, db.ForeignKey('subsector.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    country_name = db.Column(db.Integer, db.ForeignKey('country.name'), nullable=False)

class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    american = db.Column(db.String(12))
    british = db.Column(db.String(12))
    french = db.Column(db.String(12))
    uiaa = db.Column(db.String(12))
    saxon = db.Column(db.String(12))
    australian = db.Column(db.String(12))
    finnish = db.Column(db.String(12))
    norwegian = db.Column(db.String(12))
    brazilian = db.Column(db.String(12))