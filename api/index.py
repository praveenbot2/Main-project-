"""
Vercel Serverless Function Entry Point
Wraps the Flask backend for deployment on Vercel's Python runtime.

Vercel routes /api/* to this handler.  The WSGI middleware strips the
/api prefix so Flask routes (/health, /predict, …) match as-is.
"""

import sys
import os

# Ensure project root is on the Python path so modules/ and config.py
# can be imported by web_server.py
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from web_server import app as flask_app


class _StripApiPrefix:
    """WSGI middleware that removes the /api prefix from PATH_INFO."""

    def __init__(self, wsgi_app, prefix="/api"):
        self.wsgi_app = wsgi_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path.startswith(self.prefix):
            environ["PATH_INFO"] = path[len(self.prefix) :] or "/"
            environ["SCRIPT_NAME"] = environ.get("SCRIPT_NAME", "") + self.prefix
        return self.wsgi_app(environ, start_response)


# Vercel picks up `app` as the WSGI handler
app = _StripApiPrefix(flask_app)
