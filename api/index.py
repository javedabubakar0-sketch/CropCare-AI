"""
CropCare AI - Vercel Serverless Function Entry Point
Initializes the Flask WSGI application with dynamic path translation for Vercel.
"""

import sys
import os
import urllib.parse

# Ensure the root project directory is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app as flask_app

class VercelWSGIHandler:
    """
    WSGI wrapper to ensure Vercel rewrites map accurately to Flask's router.
    Resolves both query-parameterized rewrites (?path=...) and internal prefixes.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        query_string = environ.get("QUERY_STRING", "")
        params = urllib.parse.parse_qs(query_string)

        # 1. If Vercel rewrote the route and passed the original path via query
        if "path" in params and params["path"]:
            orig_path = params["path"][0]
            if not orig_path.startswith("/"):
                orig_path = "/" + orig_path
            environ["PATH_INFO"] = orig_path

            # Clean 'path' parameter from query string so request.args stays pristine
            clean_params = {k: v for k, v in params.items() if k != "path"}
            environ["QUERY_STRING"] = urllib.parse.urlencode(clean_params, doseq=True)
        else:
            # 2. Fallback prefix stripping for direct serverless function calls
            path = environ.get("PATH_INFO", "")
            for prefix in ("/api/index.py", "/api/index"):
                if path == prefix:
                    environ["PATH_INFO"] = "/"
                    break
                elif path.startswith(prefix + "/"):
                    environ["PATH_INFO"] = path[len(prefix):]
                    break

        return self.wsgi_app(environ, start_response)

app = VercelWSGIHandler(flask_app)
