from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length

class ServiceForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=256)])
    acronyme = StringField('Acronyme', validators=[Length(max=20)])
    responsable = StringField('Responsable', validators=[Length(max=100)])
    saint_patron = StringField('Saint Patron', validators=[Length(max=100)])
    creer_le = DateTimeField('Date de création', format='%Y-%m-%d %H:%M:%S')
    creer_par = StringField('Créé par', validators=[Length(max=100)])
    horaire_standard = StringField('Horaire standard', validators=[Length(max=100)])
    image = StringField('Image', validators=[Length(max=200)])