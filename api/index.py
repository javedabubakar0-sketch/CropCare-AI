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

from app import app
