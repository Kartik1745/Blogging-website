from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length,Email,EqualTo,ValidationError
from packages.models import User,Post

class RegistrationForm(FlaskForm):
    Username=StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])

    Email=StringField('Email',validators=[DataRequired(),Email()])

    Password=PasswordField('Password',validators=[DataRequired()])

    Confirm_Password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('Password')])

    submit=SubmitField('Sign Up')

    def validate_Username(self, Username):
        user = User.query.filter_by(username=Username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_Email(self, Email):
        user = User.query.filter_by(email=Email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):

    Email=StringField('Email',validators=[DataRequired(),Email()])

    Password=PasswordField('Password',validators=[DataRequired()])

    Remember=BooleanField('Remember me')

    submit=SubmitField('Log In')    

class NewPost(FlaskForm):

    title=StringField('Title',validators=[DataRequired()])

    content=TextAreaField('Content',validators=[DataRequired()])

    submit=SubmitField('Post')


