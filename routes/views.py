"""
CropCare AI - Web Views Blueprint
Renders server-side templates for the agricultural dashboard.
"""

from flask import Blueprint, render_template
import database as db
from services.inference_service import inference_service

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
@views_bp.route("/index")
@views_bp.route("/home")
@views_bp.route("/dashboard")
def index():
    """Renders the CropCare AI unified agricultural dashboard."""
    stats = db.get_stats()
    recent_scans = db.get_all_scans(limit=8)
    crops = db.get_all_crops()
    pending_tasks = db.get_all_tasks(status="pending")[:6]

    samples = [
        {"name": "tomato_early_blight.jpg", "label_en": "Tomato Early Blight", "label_ur": "ٹماٹر اگیتا جھلساؤ", "crop": "Tomato"},
        {"name": "healthy_tomato.jpg", "label_en": "Healthy Tomato", "label_ur": "صحت مند ٹماٹر", "crop": "Tomato"},
        {"name": "potato_late_blight.jpg", "label_en": "Potato Late Blight", "label_ur": "آلو پچھیتا جھلساؤ", "crop": "Potato"},
        {"name": "corn_common_rust.jpg", "label_en": "Corn Common Rust", "label_ur": "مکئی کا زنگ", "crop": "Corn"},
        {"name": "apple_cedar_rust.jpg", "label_en": "Apple Cedar Rust", "label_ur": "سیب کا زنگ", "crop": "Apple"}
    ]

    return render_template(
        "index.html",
        stats=stats,
        recent_scans=recent_scans,
        crops=crops,
        pending_tasks=pending_tasks,
        samples=samples,
        model_loaded=inference_service.is_loaded,
        model_error=inference_service.load_error
    )
