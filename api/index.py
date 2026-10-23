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
    Resolves query-parameterized rewrites (?path=...), Vercel headers, and prefixes.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        orig_path = None
        query_string = environ.get("QUERY_STRING", "")
        params = urllib.parse.parse_qs(query_string)

        # 1. Check if Vercel passed the original path in the rewrite query string
        if "path" in params and params["path"]:
            orig_path = params["path"][0]
            clean_params = {k: v for k, v in params.items() if k != "path"}
            environ["QUERY_STRING"] = urllib.parse.urlencode(clean_params, doseq=True)

        # 2. Check standard Vercel request path headers
        elif environ.get("HTTP_X_MATCHED_PATH"):
            orig_path = environ.get("HTTP_X_MATCHED_PATH")
        elif environ.get("HTTP_X_FORWARDED_URI"):
            orig_path = environ.get("HTTP_X_FORWARDED_URI").split("?")[0]

        # 3. Apply the resolved path if found
        if orig_path:
            if not orig_path.startswith("/"):
                orig_path = "/" + orig_path
            environ["PATH_INFO"] = orig_path
        else:
            # Fallback: strip internal function file prefixes
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
