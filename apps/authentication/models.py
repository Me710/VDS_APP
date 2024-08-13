from flask_login import UserMixin
from apps import db, login_manager
#from werkzeug.security import generate_password_hash, check_password_hash
from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    services = db.relationship("Service", secondary="user_in_service", back_populates="users")
    adresse = db.Column(db.String(200))
    ville = db.Column(db.String(100))
    pays = db.Column(db.String(100))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    bio = db.Column(db.Text)
    pp = db.Column(db.String(200)) 

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    users = db.relationship("Users", secondary="user_in_service", back_populates="services")
    acronyme = db.Column(db.String(20))
    responsable = db.Column(db.String(100))
    saint_patron = db.Column(db.String(100))
    creer_le = db.Column(db.DateTime)
    creer_par = db.Column(db.String(100))
    horaire_standard = db.Column(db.String(100))
    image = db.Column(db.String(200))

class UserInService(db.Model):
    __tablename__ = 'user_in_service'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))

class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    content = db.Column(db.String(256))
    publication_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users", backref="publications")
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    auteur = db.Column(db.String(100))
    statut = db.Column(db.String(50))
    date_publication = db.Column(db.DateTime)
    creer_par = db.Column(db.String(100))
    creer_le = db.Column(db.DateTime)
    chemin_image = db.Column(db.String(200))
    description = db.Column(db.Text)

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    event_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("Users", backref="events")
    creer_par = db.Column(db.String(100))
    creer_le = db.Column(db.DateTime)
    image = db.Column(db.String(200))

class UserInEvent(db.Model):
    __tablename__ = 'user_in_event'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))


@login_manager.user_loader
def user_loader(id):
    return Users.query.get(int(id))

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None