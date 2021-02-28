from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session, jsonify
from cloudera import app,db,bcrypt,login_manager,mail,safe_seralizer
from cloudera.projects.forms import ProjectForm
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from cloudera.models import User,AccessKey,Project
import botocore
import boto3
import json

#Blueprint object
blue = Blueprint('projects',__name__,template_folder='templates')

#Project Dashboard
@blue.route('/projects')
def project_dashboard():
    region_dict = {'us-east-1':'US East (N. Varginia)','us-east-2':'US East (Ohio)',
		'us-west-1':'US West (N. California)','us-west-2':'US West (Oregon)','af-south-1':'Africa (CapeTown)',
		'ap-east-1':'Asia Pacific (Hong Kong)','ap-south-1':'Asia Pacific (Mumbai)','ap-northeast-2':'Asia Pacific (Seoul)',
		'ap-southeast-1':'Asia Pacific (Singapore)','ap-southeast-2':'Asia Pacific (Sydney)',
		'ap-northeast-1':'Asia Pacific (Tokyo)','ca-central-1':'Canada (Central)','eu-central-1':'Europe (Frankfurt)',
		'eu-west-1':'Europe (Irekand)','eu-west-2':'Europe (London)','eu-south-1':'Europe (Milan)',
		'eu-west-3':'Europe (Paris)','eu-north-1':'Europe (Stockholm)','me-south-1':'Middle East (Bahrin)'}
    page = request.args.get('page',1,type=int)
    project_len = len(Project.query.filter_by(user_id=current_user.id).all())
    project_record = Project.query.filter_by(user=current_user).paginate(page=page,per_page=10)
    return render_template('projects/project_dashboard.html',title="Projects",project_len=project_len,project_record=project_record,region_dict=region_dict)

#Create Project
@blue.route('/create_project',methods=['GET','POST'])
def create_project():
    form = ProjectForm()
    page = request.args.get('page',1,type=int)
    accesskey_len = len(AccessKey.query.filter_by(user_id=current_user.id).all())
    accesskey_record = AccessKey.query.filter_by(user_id=current_user.id).paginate(page=page,per_page=8)
    
    if form.validate_on_submit():
        #Add new project details
        project_db = Project(project_name=form.projectname.data,accesskeyname=form.access_keyname.data,project_region=form.awsregion.data,user=current_user)
        db.session.add(project_db)
        db.session.commit()
        #Update Access Key DB with new Project id
        project_db = db.session.query(Project).filter(Project.project_name==form.projectname.data).first()
        accesskey_db = db.session.query(AccessKey).filter(AccessKey.keyname==form.access_keyname.data).first()
        accesskey_db.project_id = project_db.id
        db.session.commit()
        flash(f"Project Created successfully in {form.awsregion.data} region",'success')
    return render_template('projects/create_project.html',title='Create Project',form=form,accesskey_len=accesskey_len,accesskey_record=accesskey_record)
    

