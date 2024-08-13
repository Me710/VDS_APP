from flask import Blueprint

blueprint = Blueprint(
    'events_blueprint',
    __name__,
    url_prefix='/events'
)
