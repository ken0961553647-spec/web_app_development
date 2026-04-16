from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
recipes_bp = Blueprint('recipes', __name__)

from . import auth, recipes
