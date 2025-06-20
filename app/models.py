from .extensions import db
from flask_login import UserMixin

class Klient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    klientname = db.Column(db.String(64), nullable=False)
    number_phone = db.Column(db.String(120), nullable=False)
    VIP_status = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Klient {self.klientname}>'

class Menenger(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    menengername = db.Column(db.String(64), nullable=False)
    number_phone = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f'<Menenger {self.menengername}>'
    def get_id(self):
        return str(self.id)  # Flask-Login ожидает строку
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    data = db.Column(db.DATE, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    
    def __repr__(self):
        return f'<Klient {self.klientname}>'