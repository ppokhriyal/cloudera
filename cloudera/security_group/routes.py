from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session, jsonify
from cloudera import app,db,bcrypt,login_manager,mail,safe_seralizer
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from cloudera.models import User,AccessKey,Project
import botocore
import boto3
import json

#Blueprint object
blue = Blueprint('security_group',__name__,template_folder='templates')

#Security Group Dashbaord
@blue.route('/security_group')
def security_group_dashboard():
    return render_template('security_group/security_group_dashboard.html',title="Security Group")