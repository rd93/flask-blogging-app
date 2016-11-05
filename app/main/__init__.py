from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

from ..models import Permission

@main.app_context_processor 		
def inject_permissions():		#Context processors make variables globally available to all templates.
	return dict(Permission=Permission)