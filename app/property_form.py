from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired

class PropertyForm(FlaskForm):
    title = TextField('Property Title', validators=[InputRequired()])
    numBedroom = TextField('No. of Rooms', validators=[InputRequired()])
    numBathroom = TextField('No. of Bathrooms', validators=[InputRequired()])
    location = TextField('Location', validators=[InputRequired()])
    price = TextField('Price', validators=[InputRequired()])

    propertyType = SelectField('Property Type', choices=['Select Type','House', 'Apartment'], validators=[InputRequired()])

    description = TextAreaField('Description', validators=[InputRequired()])

    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])