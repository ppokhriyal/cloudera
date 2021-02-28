from flask_wtf import FlaskForm
from cloudera import app,db,bcrypt,login_manager,mail,safe_seralizer
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cloudera.models import User,AccessKey,Project
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import botocore
import boto3


#Project Form
class ProjectForm(FlaskForm):
    projectname = StringField('Project Name',validators=[DataRequired(),Length(min=5,max=50)])
    access_keyname = StringField('Access Key Name',validators=[DataRequired()])
    awsregion = SelectField('Region',choices=[('us-east-1','US East (N. Varginia)'),('us-east-2','US East (Ohio)'),
		('us-west-1','US West (N. California)'),('us-west-2','US West (Oregon)'),('af-south-1','Africa (CapeTown)'),
		('ap-east-1','Asia Pacific (Hong Kong)'),('ap-south-1','Asia Pacific (Mumbai)'),('ap-northeast-2','Asia Pacific (Seoul)'),
		('ap-southeast-1','Asia Pacific (Singapore)'),('ap-southeast-2','Asia Pacific (Sydney)'),
		('ap-northeast-1','Asia Pacific (Tokyo)'),('ca-central-1','Canada (Central)'),('eu-central-1','Europe (Frankfurt)'),
		('eu-west-1','Europe (Irekand)'),('eu-west-2','Europe (London)'),('eu-south-1','Europe (Milan)'),
		('eu-west-3','Europe (Paris)'),('eu-north-1','Europe (Stockholm)'),('me-south-1','Middle East (Bahrin)')])
    submit = SubmitField('Create Project')
    
    def validate_projectname(self,projectname):
        if " " in projectname.data:
            raise ValidationError("Space not allowed")
        
        projectname = Project.query.filter_by(project_name=projectname.data).first()
        if projectname:
            raise ValidationError('Project already exists')
        
    def validate_access_keyname(self,access_keyname):
        if " " in access_keyname.data:
            raise ValidationError("Space not allowed")
            