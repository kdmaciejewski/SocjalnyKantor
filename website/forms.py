from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from website.models import *

class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):                  #to wywalić raczej
        user = Klient.query.filter_by(imie=username.data).first()
        if user:    #JEŻELI BEDZIE NONE TO NIE WEJDZIE
            raise ValidationError('To imie jest zajęte. WYWALIC')

    def validate_email(self, email):
        user = Klient.query.filter_by(login=email.data).first()
        if user:
            raise ValidationError('Ten email jest zajęty.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    #remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


#CURRENCIES = [('1', 'btc'), ('2', 'eth'), ('3', 'doge'), ('4', 'bnb')]
CURRENCIES = ['BTC', 'ETH', 'DOGE', 'BNB', 'USD']
class ExchangeForm(FlaskForm):
    val1 = IntegerField('Posiadam', validators=[DataRequired(), NumberRange(min=0, max=1000000)])
    cur1 = SelectField('Waluta', choices=CURRENCIES)
    #val2 = IntegerField('Otrzymam', validators=[DataRequired()])
    cur2 = SelectField('Zamień na', choices=CURRENCIES)
    submit = SubmitField('Przelicz')

class PostForm(FlaskForm):
    tytul = StringField('Tytuł', validators=[DataRequired()])
    tresc = TextAreaField('Treść', validators=[DataRequired(), Length(min=2, max=250)])
    dataUtworzenia = StringField('Data Utworzenia')
    status = DateField('Title', validators=[DataRequired()])
    submit = SubmitField('Dodaj post')


#???
# class UpdateForm(FlaskForm):
#     username = StringField('Login', validators=[DataRequired(), Length(min=2, max=25)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Zarejestruj')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:    #JEŻELI BEDZIE NONE TO NIE WEJDZIE
#             raise ValidationError('Ten login jest zajęty.')
#
#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('Ten email jest zajęty.')
