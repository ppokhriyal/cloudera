from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from cloudera import app,db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	try:
		return User.query.get(int(user_id))
	except:
		return None

#User DataBase
class User(db.Model,UserMixin):
    __bind_key__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    confirm_email = db.Column(db.Boolean,default=False)
    profile_img = db.Column(db.String(20),nullable=False,default='default_user.png')
    access_key = db.relationship('AccessKey',backref='user',lazy=True,cascade='all,delete-orphan')
    project = db.relationship('Project',backref='user',lazy=True,cascade='all,delete-orphan')
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

#AWS Access Key
class AccessKey(db.Model):
    __bind_key__ = 'accesskey'
    id = db.Column(db.Integer,primary_key=True)
    keyname = db.Column(db.String(20),unique=True,nullable=False)
    accesskeyid = db.Column(db.String(50),unique=True,nullable=False)
    secretkey = db.Column(db.String(50),unique=True,nullable=False)
    date_created = db.Column(db.DateTime(),nullable=False,default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
    
    def __repr__(self):
        return f"AccessKey('{self.keyname}')"

#Project DB
class Project(db.Model):
    __bind_key__ = 'project'
    id = db.Column(db.Integer,primary_key=True)
    project_name = db.Column(db.String(20),unique=True,nullable=False)
    project_region = db.Column(db.String(10),nullable=False)
    accesskeyname = db.Column(db.String(20),unique=True,nullable=False)
    date_created = db.Column(db.DateTime(),nullable=False,default=datetime.now)
    accesskey = db.relationship('AccessKey',backref='project',uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)