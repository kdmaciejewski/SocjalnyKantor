from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime
#from models import Administrator

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site4.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'  #przechodzimy do strony logowania jeśli nie mamy do czegoś uprawnień
login_manager.login_message_category = 'info'   #ustawiamy styl tej wiadomości z bootstrapa

# from website.models import *
# # admin1 = Klient(imie='Admin', login='admin11@admin.com', haslo='12345678', jestAdminem=True)
# # db.session.add(admin1)
# # db.session.commit()
#
from website import routes

