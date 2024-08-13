from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=256)])
    event_date = DateTimeField('Date de l\'événement', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    creer_par = StringField('Créé par', validators=[Length(max=100)])
    creer_le = DateTimeField('Date de création', format='%Y-%m-%d %H:%M:%S')
    image = StringField('Image', validators=[Length(max=200)])