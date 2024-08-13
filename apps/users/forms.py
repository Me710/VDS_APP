from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6, max=128)])
    adresse = StringField('Adresse', validators=[Length(max=200)])
    ville = StringField('Ville', validators=[Length(max=100)])
    pays = StringField('Pays', validators=[Length(max=100)])
    bio = TextAreaField('Biographie')
    pp = StringField('Photo de profil', validators=[Length(max=200)])