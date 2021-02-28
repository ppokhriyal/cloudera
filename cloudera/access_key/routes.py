from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session, jsonify
from cloudera import app,db,bcrypt,login_manager,mail,safe_seralizer,sched
from cloudera.access_key.forms import AccessKeyForm
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from cloudera.models import User,AccessKey
import botocore
import boto3
import json

#Blueprint object
blue = Blueprint('access_key',__name__,template_folder='templates')

#Access Key Dashboard
@blue.route('/accesskey',methods=['GET','POST'])
def access_key_dashboard():
    page = request.args.get('page',1,type=int)
    accesskey_len = len(AccessKey.query.filter_by(user_id=current_user.id).all())
    accesskey_record = AccessKey.query.filter_by(user=current_user).paginate(page=page,per_page=10)
    return render_template('access_key/accesskey_dashboard.html',title="Access Key",accesskey_len=accesskey_len,accesskey_record=accesskey_record)

#Add Access Key
@blue.route('/addaccesskey',methods=['GET','POST'])
def add_accesskey():
    form = AccessKeyForm()
    if form.validate_on_submit():
        sts = boto3.client('sts',aws_access_key_id=form.access_keyid.data,aws_secret_access_key=form.secret_key.data)
        try:
            sts.get_caller_identity()
            response = sts.get_caller_identity()
            accesskey_db = AccessKey(keyname=form.keyname.data,accesskeyid=form.access_keyid.data,secretkey=form.secret_key.data,user=current_user)
            db.session.add(accesskey_db)
            db.session.commit()
            flash(f"Access Key added successfuly",'success')
        except botocore.exceptions.ClientError:
            flash(f"Error while adding AWS Access Key.",'danger')
    return render_template('access_key/add_accesskey.html',title='Add Access Key',form=form)

#Verify Access Key
@blue.route('/awsaccesskey/verify_accesskey/<string:accesskey>/<string:secretkey>',methods=['GET','POST'])
def verify_accesskey(accesskey,secretkey):
    sts = boto3.client('sts',aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    try:
        sts.get_caller_identity()
        response = sts.get_caller_identity()
        return jsonify({'result':'pass','msg':response})
    except botocore.exceptions.ClientError:
        return jsonify({'result': 'fail'})
    