from flask import Blueprint

blueprint = Blueprint(
    'services_blueprint',
    __name__,
    url_prefix='/services'
)
