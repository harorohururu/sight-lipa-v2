from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LandmarkForm(FlaskForm):
    name = StringField('Landmark Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Landmark')

class TouristVisitForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email')
    nationality = StringField('Nationality')
    submit = SubmitField('Log Visit')
