"""
CropCare AI - Agricultural Decision Support & Plant Health Platform
Designed for Pakistani farmers, field advisers, and agricultural students.

Architecture:
- Application Factory Pattern (create_app)
- Modular Blueprints: routes.views, routes.api
- Services: services.inference_service, services.weather_service, services.guidance_service
- Local SQLite Database Handler: database.py
- Centralized Configuration: config.py
"""

import os
import logging
from flask import Flask, jsonify, render_template

import config
import database as db
from routes.views import views_bp
from routes.api import api_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("cropcare.app")

def create_app(test_config=None):
    """
    Application factory for CropCare AI.
    Initializes Flask application, configuration, database,
    blueprints, and global error handlers.
    """
    app = Flask(__name__)

    # Default application configuration
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
    app.config["JSON_SORT_KEYS"] = False

    # Apply test config overrides if provided
    if test_config:
        app.config.update(test_config)

    # Ensure required directories exist safely
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        os.makedirs(config.SAMPLES_FOLDER, exist_ok=True)
    except OSError:
        pass

    # Initialize SQLite database schema and indexes
    try:
        db.init_db()
        logger.info("SQLite database verified and initialized.")
    except Exception as e:
        logger.error(f"Database initialization failure: {e}")

    # Register Blueprints
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    # Dynamic route to serve uploaded leaf images (from /tmp/uploads on Vercel or local static/uploads)
    from flask import send_from_directory

    @app.route("/static/uploads/<path:filename>")
    def serve_uploaded_file(filename):
        upload_dir = app.config.get("UPLOAD_FOLDER", config.UPLOAD_FOLDER)
        if os.path.exists(os.path.join(upload_dir, filename)):
            return send_from_directory(upload_dir, filename)
        fallback_dir = os.path.join(config.STATIC_FOLDER, "uploads")
        if os.path.exists(os.path.join(fallback_dir, filename)):
            return send_from_directory(fallback_dir, filename)
        return jsonify({"error": "File not found"}), 404

    # ---------------------------------------------------------
    # Global Error Handlers (Security & Clean REST Contracts)
    # ---------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": getattr(error, "description", "The server could not understand the request.")
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "The requested endpoint or resource was not found on this server."
        }), 404

    @app.errorhandler(413)
    def payload_too_large(error):
        return jsonify({
            "success": False,
            "error": "Payload Too Large",
            "message": f"Uploaded file exceeds the maximum allowed limit of {config.MAX_CONTENT_LENGTH // (1024 * 1024)} MB."
        }), 413

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": "Unprocessable Entity",
            "message": getattr(error, "description", "Request content was syntactically correct but could not be processed.")
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        # Log error securely on server console, without exposing traces to external client
        logger.error(f"Internal Server Error: {error}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected server error occurred. Please try again later or contact support."
        }), 500

    return app

# Default application instance
app = create_app()

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("CropCare AI - Agricultural Decision Support Platform")
    print(f"Server starting on http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print(f"Debug Mode: {config.FLASK_DEBUG}")
    print("=" * 65 + "\n")
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
