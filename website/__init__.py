from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime
#from models import Administrator

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'  #przechodzimy do strony logowania jeśli nie mamy do czegoś uprawnień
login_manager.login_message_category = 'info'   #ustawiamy styl tej wiadomości z bootstrapa

# from website.models import Administrator
# admin1 = Administrator(imie='Admin2', login='admin@admin2.pl', haslo='12345678')
# db.session.add(admin1)
# db.session.commit()

from website import routes

