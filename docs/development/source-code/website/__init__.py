# enable the folder 'website' to be python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '12345'
    if test_config is not None:
        # Wenn test_config vorhanden ist, überschreibe die Standardkonfiguration
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .infoBox import box

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/') # kann dazu fuehren, wenn url /"hier" koennen wir modulieren was auftaucht nach /
    app.register_blueprint(box, url_prefix='/')

    from .models import User#, Note
    
    with app.app_context():
        create_database()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # primary key of user

    return app



def create_database():

    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')

