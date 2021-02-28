from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager
from flask_mail import Mail,Message
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

#App Config
app = Flask(__name__)
app.config['SECRET_KEY'] = '878436c0a462c4145fa59eec2c43a66a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/user.db'
app.config['SQLALCHEMY_BINDS'] = {'user':'sqlite:///database/user.db','accesskey':'sqlite:///database/accesskey.db','project':'sqlite:///database/project.db'}

#Remember me
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=120)

#Mail Config
app.config.from_pyfile('mailconfig.cfg')

safe_seralizer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

#Background Function Job
sched = BackgroundScheduler(daemon=True)


#Login Manager
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'user_management.login'
login_manager.login_message_category = 'info'

#Import Blueprint routes objects
from cloudera.user_management.routes import blue
from cloudera.home.routes import blue
from cloudera.access_key.routes import blue
from cloudera.projects.routes import blue
from cloudera.security_group.routes import blue
#Register Blueprint
app.register_blueprint(user_management.routes.blue,url_prefix='/')
app.register_blueprint(home.routes.blue,url_prefix='/')
app.register_blueprint(access_key.routes.blue,url_prefix='/')
app.register_blueprint(projects.routes.blue,url_prefix='/')
app.register_blueprint(security_group.routes.blue,url_prefix='/')