from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cloudera.models import User,AccessKey

#Access Key Form
class AccessKeyForm(FlaskForm):
    keyname = StringField('Key Name',validators=[DataRequired(),Length(min=2,max=50)])
    access_keyid = StringField('Access Key Id',validators=[DataRequired(),Length(min=2,max=50)])
    secret_key = PasswordField('Secret Access Key',validators=[DataRequired(),Length(min=2,max=50)])
    submit = SubmitField('Add Key')
    
    def validate_keyname(self,keyname):
        if " " in keyname.data:
            raise ValidationError("Space not allowed in key name")
        
        keyname = AccessKey.query.filter_by(keyname=keyname.data).first()
        if keyname:
            raise ValidationError('Key name already exists.')
    
    def validate_access_keyid(self,access_keyid):
        if " " in access_keyid.data:
            raise ValidationError("Space not allowed in access key id.")
        
        access_keyid =  AccessKey.query.filter_by(accesskeyid=access_keyid.data).first()
        if access_keyid:
            raise ValidationError("Access Key Id already exists.")
    
    def validate_secret_key(self,secret_key):
        if " " in secret_key.data:
            raise ValidationError("Space not allowed in secret key.")
        secret_key = AccessKey.query.filter_by(secretkey=secret_key.data).first()
        if secret_key:
            raise ValidationError("Secret Access Key already exists.")