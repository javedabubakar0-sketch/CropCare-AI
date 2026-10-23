"""
CropCare AI - Vercel Serverless Function Entry Point
Initializes the Flask WSGI application for deployment on Vercel.
"""

import sys
import os

# Ensure the root project directory is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app as flask_app

class VercelWSGIHandler:
    """
    WSGI wrapper to ensure Vercel rewrites map accurately to Flask's router,
    stripping /api/index or /api/index.py internal prefixes if present.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        # Normalize internal Vercel function path prefixes
        for prefix in ("/api/index.py", "/api/index"):
            if path == prefix:
                environ["PATH_INFO"] = "/"
                break
            elif path.startswith(prefix + "/"):
                environ["PATH_INFO"] = path[len(prefix):]
                break
        return self.wsgi_app(environ, start_response)

app = VercelWSGIHandler(flask_app)
