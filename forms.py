from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (StringField,SubmitField,IntegerField,PasswordField)


class Form(FlaskForm):
    name= StringField('What is Your Name !',validators=[DataRequired()])
    email= StringField('Enter Your Email',validators=[DataRequired()])
    mobile= IntegerField('Enter Your Mobile Number',validators=[DataRequired()])
    submit= SubmitField('Login')
    
    
class Container(FlaskForm):
      name=StringField('Name Of container',validators=[DataRequired()])
      submit= SubmitField('Run Container')
      