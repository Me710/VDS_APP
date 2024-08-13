from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length
from apps.authentication.models import Service

class PublicationForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=64)])
    content = TextAreaField('Contenu', validators=[DataRequired(), Length(max=256)])
    publication_date = DateTimeField('Date de publication', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    auteur = StringField('Auteur', validators=[Length(max=100)])
    statut = SelectField('Statut', choices=[('draft', 'Brouillon'), ('published', 'Publié')])
    chemin_image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField('Description')
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.service_id.choices = [(service.id, service.name) for service in Service.query.all()]