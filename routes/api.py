"""
CropCare AI - REST API Blueprint
Provides canonical REST endpoints for:
- System Health & Diagnostics (/api/health, /api/model-status, /api/stats)
- Real Machine Learning Leaf Scan Inference (/api/scan, /api/scan-sample)
- Leaf Scan History CRUD (/api/scans, /api/scans/<id>, /api/history aliases)
- Field & Crop Management CRUD (/api/crops, /api/crops/<id>)
- Farm Calendar & Tasks CRUD (/api/tasks, /api/tasks/<id>)
- Meteorological Advisory & Spray Windows (/api/weather)
- Agronomic Services (/api/irrigation-advisory, /api/mandi-rates, /api/knowledge-center)
"""

import os
import uuid
import logging
from datetime import datetime, timezone
import requests
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

import config
import database as db
from services.inference_service import inference_service
from services.weather_service import get_farm_weather
from services.guidance_service import (
    get_mandi_benchmarks,
    get_field_practical_guides,
    estimate_irrigation_schedule
)

logger = logging.getLogger("cropcare.api")
api_bp = Blueprint("api", __name__, url_prefix="/api")

def allowed_file(filename):
    """Checks whether the filename has an authorized image extension."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in config.ALLOWED_EXTENSIONS

# -------------------------------------------------------------
# 1. System Health & Diagnostics
# -------------------------------------------------------------

@api_bp.route("/health", methods=["GET"])
def health_check():
    """
    Returns system operational status, verifying SQLite connectivity,
    ML model readiness, and filesystem storage health.
    """
    db_ok = False
    db_details = {}
    try:
        with db.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as c FROM sqlite_master WHERE type='table';")
            tbl_count = cursor.fetchone()["c"]
            db_ok = True
            db_details = {"status": "connected", "table_count": tbl_count}
    except Exception as e:
        db_details = {"status": "error", "message": str(e)}

    model_status = inference_service.get_status()
    uploads_writable = os.access(config.UPLOAD_FOLDER, os.W_OK)

    status_code = 200 if (db_ok and model_status["is_loaded"]) else 503
    return jsonify({
        "status": "healthy" if status_code == 200 else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_details,
        "model": {
            "is_loaded": model_status["is_loaded"],
            "classes_count": model_status["classes_count"],
            "architecture": model_status["architecture"],
            "load_error": model_status["load_error"]
        },
        "storage": {
            "uploads_writable": uploads_writable,
            "upload_folder": config.UPLOAD_FOLDER
        }
    }), status_code

@api_bp.route("/model-status", methods=["GET"])
def get_model_status():
    """Returns detailed diagnostics of the local Scikit-Learn classifier."""
    return jsonify(inference_service.get_status())

@api_bp.route("/stats", methods=["GET"])
def get_stats():
    """Returns aggregate counts for scans, crops, and pending tasks."""
    return jsonify({
        "success": True,
        "stats": db.get_stats()
    })

# -------------------------------------------------------------
# 2. Disease Scan Inference & Samples
# -------------------------------------------------------------

@api_bp.route("/scan", methods=["POST"])
def scan_leaf():
    """
    Uploads a foliar image, executes botanical validation and real ML inference,
    persists scan record to SQLite, and returns diagnosis with prevention guidance.
    """
    if not inference_service.is_loaded:
        return jsonify({
            "success": False,
            "error": "Model Not Loaded",
            "message": inference_service.load_error or "Machine learning model weights were not found.",
            "solution": "Run 'python train_model.py' to generate and calibrate the local model weights."
        }), 503

    if "leaf_image" not in request.files:
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "Missing required 'leaf_image' file field in multipart form-data."
        }), 400

    file = request.files["leaf_image"]
    if not file or file.filename == "":
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "No file was selected for upload."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "Invalid File Type",
            "message": f"Unsupported format. Allowed image formats: {', '.join(sorted(config.ALLOWED_EXTENSIONS)).upper()}."
        }), 400

    # Sanitize and generate safe server-side filename
    original_ext = file.filename.rsplit(".", 1)[1].lower()
    timestamp_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_token = uuid.uuid4().hex[:8]
    safe_name = f"{timestamp_prefix}_{random_token}.{original_ext}"
    saved_path = os.path.join(config.UPLOAD_FOLDER, safe_name)

    try:
        file.save(saved_path)
    except Exception as e:
        logger.error(f"Failed to save upload to disk: {e}")
        return jsonify({
            "success": False,
            "error": "Storage Error",
            "message": "Unable to save uploaded image to local storage."
        }), 500

    # Run real ML inference
    result = inference_service.predict(saved_path)

    # If botanical validation or inference failed, remove invalid upload
    if not result.get("success"):
        if os.path.exists(saved_path):
            try:
                os.remove(saved_path)
            except OSError:
                pass
        return jsonify(result), 422

    # Save verified scan record to SQLite
    relative_path = f"/static/uploads/{safe_name}"
    scan_record = {
        "filename": safe_name,
        "filepath": relative_path,
        "crop": result.get("crop"),
        "crop_ur": result.get("crop_ur"),
        "disease_name": result.get("disease_name"),
        "disease_name_ur": result.get("disease_name_ur"),
        "scientific_name": result.get("scientific_name"),
        "confidence": result.get("confidence"),
        "status": result.get("status"),
        "status_ur": result.get("status_ur"),
        "severity": result.get("severity"),
        "severity_ur": result.get("severity_ur"),
        "symptoms": result.get("symptoms"),
        "symptoms_ur": result.get("symptoms_ur"),
        "prevention": result.get("prevention"),
        "prevention_ur": result.get("prevention_ur"),
        "treatment": result.get("treatment"),
        "treatment_ur": result.get("treatment_ur"),
        "weather_advisory": result.get("weather_advisory"),
        "weather_advisory_ur": result.get("weather_advisory_ur"),
        "leaf_metrics": result.get("leaf_metrics"),
        "notes": request.form.get("notes", "")
    }

    scan_id = db.save_scan(scan_record)
    result["scan_id"] = scan_id
    result["image_url"] = relative_path

    return jsonify(result), 200

@api_bp.route("/scan-sample", methods=["POST"])
def scan_sample():
    """Scans one of the bundled demo leaf sample images without uploading."""
    if not inference_service.is_loaded:
        return jsonify({
            "success": False,
            "error": "Model Not Loaded",
            "message": inference_service.load_error or "ML model is not loaded."
        }), 503

    data = request.get_json(silent=True) or {}
    sample_name = data.get("sample_name", "").strip()
    if not sample_name:
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "Missing 'sample_name' in JSON body."
        }), 400

    # Ensure no path traversal in sample filename
    clean_sample_name = os.path.basename(sample_name)
    sample_path = os.path.join(config.SAMPLES_FOLDER, clean_sample_name)

    if not os.path.exists(sample_path):
        return jsonify({
            "success": False,
            "error": "Sample Not Found",
            "message": f"Sample leaf '{clean_sample_name}' was not found in sample library."
        }), 404

    result = inference_service.predict(sample_path)
    if not result.get("success"):
        return jsonify(result), 422

    relative_path = f"/static/sample_leaves/{clean_sample_name}"
    scan_record = {
        "filename": clean_sample_name,
        "filepath": relative_path,
        "crop": result.get("crop"),
        "crop_ur": result.get("crop_ur"),
        "disease_name": result.get("disease_name"),
        "disease_name_ur": result.get("disease_name_ur"),
        "scientific_name": result.get("scientific_name"),
        "confidence": result.get("confidence"),
        "status": result.get("status"),
        "status_ur": result.get("status_ur"),
        "severity": result.get("severity"),
        "severity_ur": result.get("severity_ur"),
        "symptoms": result.get("symptoms"),
        "symptoms_ur": result.get("symptoms_ur"),
        "prevention": result.get("prevention"),
        "prevention_ur": result.get("prevention_ur"),
        "treatment": result.get("treatment"),
        "treatment_ur": result.get("treatment_ur"),
        "weather_advisory": result.get("weather_advisory"),
        "weather_advisory_ur": result.get("weather_advisory_ur"),
        "leaf_metrics": result.get("leaf_metrics"),
        "notes": "Bundled botanical calibration sample"
    }

    scan_id = db.save_scan(scan_record)
    result["scan_id"] = scan_id
    result["image_url"] = relative_path

    return jsonify(result), 200

# -------------------------------------------------------------
# 3. Leaf Scan History (Canonical REST & Aliases)
# -------------------------------------------------------------

@api_bp.route("/scans", methods=["GET"])
@api_bp.route("/history", methods=["GET"])
def get_scans():
    """Retrieves paginated scan history, sorted by newest first."""
    limit = min(request.args.get("limit", default=100, type=int), 200)
    offset = max(request.args.get("offset", default=0, type=int), 0)
    crop_filter = request.args.get("crop", default=None)

    scans = db.get_all_scans(limit=limit, offset=offset, crop=crop_filter)
    return jsonify({
        "success": True,
        "count": len(scans),
        "scans": scans
    }), 200

@api_bp.route("/scans/<int:scan_id>", methods=["GET"])
@api_bp.route("/history/<int:scan_id>", methods=["GET"])
def get_scan(scan_id):
    """Retrieves a single scan record by ID."""
    scan = db.get_scan_by_id(scan_id)
    if not scan:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Scan record with ID {scan_id} does not exist."
        }), 404
    return jsonify({
        "success": True,
        "scan": scan
    }), 200

@api_bp.route("/scans/<int:scan_id>", methods=["DELETE"])
@api_bp.route("/history/<int:scan_id>", methods=["DELETE"])
def delete_scan_route(scan_id):
    """Deletes a scan record and safely removes its associated image file."""
    deleted = db.delete_scan(scan_id)
    if not deleted:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Scan with ID {scan_id} was not found."
        }), 404
    return jsonify({
        "success": True,
        "message": f"Scan ID {scan_id} removed successfully."
    }), 200

@api_bp.route("/history/clear", methods=["POST"])
def clear_history_route():
    """Clears all scan history."""
    count = db.clear_all_scans()
    return jsonify({
        "success": True,
        "message": f"Cleared {count} scan records."
    }), 200

# -------------------------------------------------------------
# 4. Crop & Field Management (CRUD)
# -------------------------------------------------------------

@api_bp.route("/crops", methods=["GET"])
def list_crops():
    """Retrieves all registered crops and fields."""
    crops = db.get_all_crops()
    return jsonify({
        "success": True,
        "crops": crops
    }), 200

@api_bp.route("/crops", methods=["POST"])
def create_crop():
    """
    Registers a new field/crop with automatic starter calendar scheduling.
    Validates required fields: crop_name, field_name, sowing_date.
    """
    data = request.get_json(silent=True) or {}
    crop_name = data.get("crop_name", "").strip()
    field_name = data.get("field_name", "").strip()

    if not crop_name or not field_name:
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Both 'crop_name' and 'field_name' are required."
        }), 400

    try:
        area_acres = float(data.get("area_acres", 1.0))
        if area_acres <= 0:
            return jsonify({
                "success": False,
                "error": "Validation Error",
                "message": "Area (acres) must be a positive number."
            }), 400
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Area (acres) must be a valid numeric value."
        }), 400

    crop_id = db.save_crop(data)
    return jsonify({
        "success": True,
        "crop_id": crop_id,
        "message": f"Field '{field_name}' ({crop_name}) registered with agronomic reminders."
    }), 201

@api_bp.route("/crops/<int:crop_id>", methods=["GET"])
def get_crop(crop_id):
    """Retrieves single crop details by ID."""
    crop = db.get_crop_by_id(crop_id)
    if not crop:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Crop with ID {crop_id} was not found."
        }), 404
    return jsonify({
        "success": True,
        "crop": crop
    }), 200

@api_bp.route("/crops/<int:crop_id>", methods=["PUT"])
def update_crop_route(crop_id):
    """Updates fields of an existing crop record."""
    crop = db.get_crop_by_id(crop_id)
    if not crop:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Crop with ID {crop_id} does not exist."
        }), 404

    data = request.get_json(silent=True) or {}
    if "area_acres" in data:
        try:
            val = float(data["area_acres"])
            if val <= 0:
                return jsonify({"success": False, "error": "Validation Error", "message": "Acreage must be > 0"}), 400
        except (ValueError, TypeError):
            return jsonify({"success": False, "error": "Validation Error", "message": "Invalid numeric acreage"}), 400

    updated = db.update_crop(crop_id, data)
    return jsonify({
        "success": updated,
        "message": f"Crop ID {crop_id} updated successfully."
    }), 200

@api_bp.route("/crops/<int:crop_id>", methods=["DELETE"])
def delete_crop_route(crop_id):
    """Deletes a crop and cascades deletion to linked farm tasks."""
    deleted = db.delete_crop(crop_id)
    if not deleted:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Crop ID {crop_id} was not found."
        }), 404
    return jsonify({
        "success": True,
        "message": f"Crop ID {crop_id} and associated tasks deleted."
    }), 200

# -------------------------------------------------------------
# 5. Farm Calendar & Tasks (CRUD)
# -------------------------------------------------------------

@api_bp.route("/tasks", methods=["GET"])
def list_tasks():
    """Retrieves farm tasks, optionally filtered by crop_id or status."""
    crop_id = request.args.get("crop_id", type=int)
    status = request.args.get("status")
    tasks = db.get_all_tasks(crop_id=crop_id, status=status)
    return jsonify({
        "success": True,
        "tasks": tasks
    }), 200

@api_bp.route("/tasks", methods=["POST"])
def create_task():
    """Creates a new farm task or reminder."""
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    due_date = data.get("due_date", "").strip()

    if not title or not due_date:
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Both 'title' and 'due_date' are required."
        }), 400

    task_id = db.save_task(data)
    return jsonify({
        "success": True,
        "task_id": task_id,
        "message": "Farm task created successfully."
    }), 201

@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Retrieves a single task by ID."""
    task = db.get_task_by_id(task_id)
    if not task:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Task with ID {task_id} not found."
        }), 404
    return jsonify({
        "success": True,
        "task": task
    }), 200

@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    """Updates fields of an existing task."""
    task = db.get_task_by_id(task_id)
    if not task:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Task with ID {task_id} not found."
        }), 404

    data = request.get_json(silent=True) or {}
    updated = db.update_task(task_id, data)
    return jsonify({
        "success": updated,
        "message": f"Task ID {task_id} updated."
    }), 200

@api_bp.route("/tasks/<int:task_id>/toggle", methods=["POST", "PUT"])
def toggle_task_route(task_id):
    """Toggles status between pending and completed."""
    new_status = db.toggle_task_status(task_id)
    if not new_status:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Task with ID {task_id} not found."
        }), 404
    return jsonify({
        "success": True,
        "new_status": new_status
    }), 200

@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    """Deletes a farm task."""
    deleted = db.delete_task(task_id)
    if not deleted:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Task with ID {task_id} not found."
        }), 404
    return jsonify({
        "success": True,
        "message": f"Task ID {task_id} deleted."
    }), 200

# -------------------------------------------------------------
# 6. Meteorological Advisory (Open-Meteo)
# -------------------------------------------------------------

@api_bp.route("/weather", methods=["GET"])
def get_weather_route():
    """
    Fetches real-time farm weather and 5-day forecast from Open-Meteo.
    Calculates chemical spray safety windows, rain alerts, and fungal risk.
    """
    lat = request.args.get("lat", "31.5204")
    lon = request.args.get("lon", "74.3587")
    city_name = request.args.get("city", "Lahore, Pakistan")

    weather_result = get_farm_weather(lat=lat, lon=lon, city_name=city_name)
    if not weather_result.get("success"):
        return jsonify(weather_result), 502

    return jsonify(weather_result), 200

# -------------------------------------------------------------
# 7. Agricultural Intelligence & Guidance
# -------------------------------------------------------------

@api_bp.route("/irrigation-advisory", methods=["POST"])
def irrigation_advisory_route():
    """
    Provides cautious agronomic irrigation estimation based on crop,
    soil texture, sowing stage, and 3-day rainfall forecast from Open-Meteo.
    """
    data = request.get_json(silent=True) or {}
    crop_type = data.get("crop_type", "Wheat").strip()
    soil_type = data.get("soil_type", "Loam").strip()
    sowing_date = data.get("sowing_date", "")
    lat = data.get("lat", "31.5204")
    lon = data.get("lon", "74.3587")

    # Fetch 3-day rainfall prediction from Open-Meteo
    rain_next_3_days = 0.0
    try:
        w_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&daily=precipitation_sum&forecast_days=3&timezone=auto"
        )
        w_res = requests.get(w_url, timeout=config.WEATHER_REQUEST_TIMEOUT).json()
        precip_sums = w_res.get("daily", {}).get("precipitation_sum", [])
        rain_next_3_days = round(sum(precip_sums), 1)
    except Exception as e:
        logger.warning(f"Could not fetch rainfall for irrigation advisory: {e}")
        rain_next_3_days = 0.0

    result = estimate_irrigation_schedule(
        crop_type=crop_type,
        soil_type=soil_type,
        sowing_date_str=sowing_date,
        rain_next_3_days_mm=rain_next_3_days
    )
    result["success"] = True
    result["rain_next_3_days_mm"] = rain_next_3_days
    return jsonify(result), 200

@api_bp.route("/mandi-rates", methods=["GET"])
def mandi_rates_route():
    """Provides authentic wholesale mandi benchmarks (AMIS Punjab / Sindh)."""
    data = get_mandi_benchmarks()
    data["success"] = True
    return jsonify(data), 200

@api_bp.route("/knowledge-center", methods=["GET"])
def knowledge_center_route():
    """Returns practical bilingual guides on pesticide safety, bio-remedies, and NPK."""
    guides = get_field_practical_guides()
    return jsonify({
        "success": True,
        "guides": guides
    }), 200
