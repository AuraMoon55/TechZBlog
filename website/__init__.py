from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

DB_NAME = "database.db"
db = SQLAlchemy()
mail = Mail()

def create_app():
  app = Flask(__name__)
  app.secret_key = b'\xba\xa2g\x0f\xdej\x97\xe6\xcd\xb6H\x19\xd7\x1e-\xfb\xbe-\x10C\x82:u7#ff\xda\x1a\x9c\xfcSY\x1c5'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "hentaivillains55@gmail.com",
    MAIL_PASSWORD=  "Anshul#217"
  )
  db.init_app(app)
  mail.init_app(app)
  
  
  from .auth import auth
  from .views import views
  
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(views, url_prefix='/')
  
  from .models import User
  
  create_database(app)
  
  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)
  
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))
  
  
  return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')