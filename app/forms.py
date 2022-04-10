# Add any form classes for Flask-WTF here
from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextAreaField
from wtforms.validators import DataRequired
 
class UploadForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    file = FileField("Photo Upload",validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'ONLY SPECIFIED FORMATS ALLOWED!'),FileRequired()])
