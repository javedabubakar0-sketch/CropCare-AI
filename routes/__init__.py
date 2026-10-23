"""
CropCare AI - Route Modules
Exports Flask blueprints for web dashboard views and the REST API.
"""

from routes.views import views_bp
from routes.api import api_bp

__all__ = ["views_bp", "api_bp"]
