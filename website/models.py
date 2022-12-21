from datetime import datetime
from website import db, login_manager
from flask_login import UserMixin
from abc import ABCMeta, abstractmethod
from enum import Enum
# import datetime

class StatusPostu(Enum):
    nowy = 'Nowy'
    edytowany = 'Edytowany'
    usuniety = 'Usunięty'

class User(metaclass=ABCMeta):
    login = ''
    haslo = ''
    imie = ''
    nazwisko = ''
    dataUrodzenia = datetime.utcnow

class Klient(db.Model, UserMixin):
    # __tablename__ = "klient"
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(20), unique=True, nullable=True)
    login = db.Column(db.String(100), unique=True, nullable=False) #login to email
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    haslo = db.Column(db.String(60), nullable=False)
    jestAdminem = db.Column(db.Boolean, nullable=True, default=False)
    dataUrodzenia = db.Column(db.Date, nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)    #relacja

    #rachunki = db.relationship('Rachunek', backref='author', lazy=True)
    #transakcje

    @login_manager.user_loader
    def load_user(user_id):
        return Klient.query.get(int(user_id))  # był tu user
    def __repr__(self):
        return f"Użytkownik {self.imie}, {self.login}, {self.image_file}, {self.haslo}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tytul = db.Column(db.String(150), nullable=False)
    dataUtworzenia = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    # status = db.Column(db.String(20), nullable=False, default='Nowy')
    tresc = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("klient.id"), nullable=False) # user.id z małej bo odwołujemy się do tablicy

    def __repr__(self):
        return f"Post {self.tytul}, {self.dataUtworzenia}"

class Rachunek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numer = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Integer, nullable=False)
    #uzytkownik_id = db.Column(db.Integer, db.ForeignKey("Klient.id"), nullable=False)
    # waluta_id = db.Column(db.Integer, db.ForeignKey("Waluta.id"), nullable=False)

class Waluta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(5), nullable=False)
    nazwa = db.Column(db.String(20), unique=True, nullable=False)

class Transakcja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ilosc = db.Column(db.Float, nullable=False)
    cena_jednostkowa = db.Column(db.Float, nullable=False)
    cena_calkowita = db.Column(db.Float, nullable=False)
    # waluta_id = db.Column(db.Integer, db.ForeignKey("Waluta.id"), nullable=False)
    # rachunek_id = db.Column(db.Integer, db.ForeignKey("Rachunek.id"), nullable=False)
    numer_karty = db.Column(db.String(40), nullable=True)
    # uzytkownik_login



