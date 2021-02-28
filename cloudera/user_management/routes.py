from flask import Blueprint,render_template,url_for, flash, redirect, request, abort, session
from cloudera import app,db,bcrypt,login_manager,mail,safe_seralizer,sched
from cloudera.user_management.forms import LoginForm,RegisterForm,ForgotPasswordForm,ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from itsdangerous.exc import SignatureExpired,BadTimeSignature
from cloudera.models import User
from flask_mail import Message
import schedule
import time

#Blueprint object
blue = Blueprint('user_management',__name__,template_folder='templates')
sched.start()        

#Background DB Check
def monitor_db():
    print("Monitor DB is alive")
    check_user = User.query.filter_by(confirm_email=False).first()
    if check_user is None:
        print("All users confirmed there email-ids")
    else:
        print("Its been 30 min. user email-id is not confirmed")
        db.session.delete(check_user)
        db.session.commit()
#Login
@blue.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #Check if email,password and confirm email is True
        if user and bcrypt.check_password_hash(user.password,form.password.data) and user.confirm_email == True:
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful. Please check email or password or your email id is not yet confirmed.','danger')
        
    return render_template('user_management/login.html',title="Cloudera : Login",form=form)

#Registration
@blue.route('/registration',methods=['GET','POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        #Add new user to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #Send Confirmation mail to new user
        email = form.email.data
        token = safe_seralizer.dumps(email,salt='email-confirm')
        msg = Message('Cloudera : Account creation confirmation',sender='ppokhriyal4@gmail.com',recipients=[email])
        link = url_for('user_management.confirm_email',token=token,user_id=user.id,_external=True)
        msg.body= 'Please navigate to below link, for your account confirmation \n\n {}'.format(link)
        mail.send(msg)
        #send the mail_confirm job
        sched.add_job(monitor_db,'interval',minutes=1)
        
        return redirect(url_for('user_management.message',message='mail_sent'))
    return render_template('user_management/registration.html',title="Cloudera : Registration",form=form)

#Mail session token
@blue.route('/confirm_email/<token>/<int:user_id>')
def confirm_email(token,user_id):
    try:
        email = safe_seralizer.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return redirect(url_for('user_management.message',message='mail_expired'))
    except BadTimeSignature:
        return redirect(url_for('user_management.message',message='mail_linkerror'))

    #Confirm User Email Verification
    user = User.query.get(user_id)
    
    if user is None:
        return redirect(url_for('user_management.message',message='user_not_found'))
        
    email_confirm_status = user.confirm_email

    if email_confirm_status == True:
        return redirect(url_for('user_management.message',message='email_confirm_already'))
    else:
        user.confirm_email = True
        db.session.commit()
        return redirect(url_for('user_management.message',message='email_confirm'))

#Message Page
@blue.route('/message/<message>')
def message(message):
    return render_template('user_management/message.html',title="Message",message=message)        

#Forgot Password
@blue.route('/forgot-password',methods=['GET','POST'])
def forgotpasswd():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #Generate Password reset link mail
        email = form.email.data
        token = safe_seralizer.dumps(email,salt='email-confirm')
        msg = Message('Cloudera : Password Reset',sender='ppokhriyal4@gmail.com',recipients=[email])
        link = url_for('user_management.password_reset_email',token=token,user_id=user.id,_external=True)
        msg.body= 'Please navigate to below link, for your password reset \n\n {}'.format(link)
        mail.send(msg)
        return redirect(url_for('user_management.message',message='passwordreset_mail_sent'))
    return render_template('user_management/forgotpassword.html',title='Cloudera : ForgotPassword',form=form)

#Password Reset Mail Token
@blue.route('/passwordrest/<token>/<int:user_id>')
def password_reset_email(token,user_id):
    try:
        email = safe_seralizer.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return redirect(url_for('user_management.message',msg='mail_expired'))
    except BadTimeSignature:
        return redirect(url_for('user_management.message',msg='mail_linkerror'))
    
    form = ResetPasswordForm()
    return render_template('user_management/resetpassword.html',title="Reset Password",form=form,userid=user_id)

#Reset Password
@blue.route('/reset_password/<int:userid>',methods=['POST','GET'])
def reset_password(userid):
    form = ResetPasswordForm()
    
    user = User.query.get(userid)
    if user is None:
        return redirect(url_for('user_management.message',message='user_not_found'))
    
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('user_management.message',message='password_reset_done'))
        