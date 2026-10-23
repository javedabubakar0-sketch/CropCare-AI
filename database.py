"""
CropCare AI - Local SQLite Database Handler
Provides robust, parameterized CRUD operations, connection management,
safe migrations, and indexed queries for crops, scans, and farm tasks.
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from contextlib import contextmanager
import config

DB_PATH = config.DB_PATH

@contextmanager
def get_db():
    """
    Context manager for SQLite connections.
    Enforces foreign key constraints and commits on successful execution.
    Automatically rolls back on exception and closes connection.
    """
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def get_connection():
    """Legacy helper returning a row-configured connection."""
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """
    Initializes SQLite tables and creates indexes safely.
    Performs non-destructive schema migrations if new columns are needed.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Table 1: Leaf Scan History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            crop TEXT NOT NULL,
            crop_ur TEXT,
            disease_name TEXT NOT NULL,
            disease_name_ur TEXT,
            scientific_name TEXT,
            confidence REAL NOT NULL,
            status TEXT NOT NULL,
            status_ur TEXT,
            severity TEXT NOT NULL,
            severity_ur TEXT,
            symptoms TEXT,
            symptoms_ur TEXT,
            prevention_en TEXT,
            prevention_ur TEXT,
            treatment_en TEXT,
            treatment_ur TEXT,
            weather_advisory TEXT,
            weather_advisory_ur TEXT,
            leaf_metrics TEXT,
            notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Table 2: Crops & Fields Managed by Farmer
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL,
            crop_name_ur TEXT,
            field_name TEXT NOT NULL,
            area_acres REAL DEFAULT 1.0,
            variety TEXT,
            sowing_date TEXT NOT NULL,
            soil_type TEXT DEFAULT 'Loam',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Table 3: Farm Tasks & Crop Calendar
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS farm_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_id INTEGER,
            crop_name TEXT,
            task_type TEXT NOT NULL,
            title TEXT NOT NULL,
            title_ur TEXT,
            due_date TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
        );
        """)

        # Performance Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scans_timestamp ON scans(timestamp DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_crops_created ON crops(created_at DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_status ON farm_tasks(status, due_date ASC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_crop_id ON farm_tasks(crop_id);")

        # Safe Column Additions (Migrations)
        _ensure_column(cursor, "scans", "notes", "TEXT")
        _ensure_column(cursor, "crops", "updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(cursor, "farm_tasks", "updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP")

def _ensure_column(cursor, table_name, column_name, column_type):
    """Safely adds a column to an existing table if it does not already exist."""
    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_cols = [row["name"] for row in cursor.fetchall()]
    if column_name not in existing_cols:
        try:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
        except sqlite3.OperationalError:
            pass

# -------------------------------------------------------------
# Leaf Scan Operations (CRUD)
# -------------------------------------------------------------

def save_scan(data):
    """
    Saves a verified scan record into SQLite using parameterized query.
    Returns the inserted scan ID.
    """
    with get_db() as conn:
        cursor = conn.cursor()

        prevention_en = json.dumps(data.get("prevention", [])) if isinstance(data.get("prevention"), list) else data.get("prevention", "")
        prevention_ur = json.dumps(data.get("prevention_ur", [])) if isinstance(data.get("prevention_ur"), list) else data.get("prevention_ur", "")
        leaf_metrics = json.dumps(data.get("leaf_metrics", {})) if isinstance(data.get("leaf_metrics"), dict) else data.get("leaf_metrics", "")

        cursor.execute("""
        INSERT INTO scans (
            filename, filepath, crop, crop_ur,
            disease_name, disease_name_ur, scientific_name,
            confidence, status, status_ur, severity, severity_ur,
            symptoms, symptoms_ur, prevention_en, prevention_ur,
            treatment_en, treatment_ur, weather_advisory, weather_advisory_ur,
            leaf_metrics, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("filename", "unknown.jpg"),
            data.get("filepath", ""),
            data.get("crop", "Unknown"),
            data.get("crop_ur", ""),
            data.get("disease_name", "Unknown Disease"),
            data.get("disease_name_ur", ""),
            data.get("scientific_name", ""),
            float(data.get("confidence", 0.0)),
            data.get("status", "Unknown"),
            data.get("status_ur", ""),
            data.get("severity", "None"),
            data.get("severity_ur", ""),
            data.get("symptoms", ""),
            data.get("symptoms_ur", ""),
            prevention_en,
            prevention_ur,
            data.get("treatment", ""),
            data.get("treatment_ur", ""),
            data.get("weather_advisory", ""),
            data.get("weather_advisory_ur", ""),
            leaf_metrics,
            data.get("notes", "")
        ))
        return cursor.lastrowid

def get_all_scans(limit=100, offset=0, crop=None):
    """Retrieves scans sorted by newest first, with optional filtering and pagination."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM scans WHERE 1=1"
        params = []

        if crop:
            query += " AND crop = ?"
            params.append(crop)

        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        results = []
        for r in rows:
            d = dict(r)
            try:
                d["prevention_en"] = json.loads(d["prevention_en"]) if d.get("prevention_en") else []
            except Exception:
                pass
            try:
                d["prevention_ur"] = json.loads(d["prevention_ur"]) if d.get("prevention_ur") else []
            except Exception:
                pass
            try:
                d["leaf_metrics"] = json.loads(d["leaf_metrics"]) if d.get("leaf_metrics") else {}
            except Exception:
                pass
            results.append(d)

        return results

def get_scan_by_id(scan_id):
    """Retrieves a single scan record by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
        row = cursor.fetchone()
        if not row:
            return None

        d = dict(row)
        try:
            d["prevention_en"] = json.loads(d["prevention_en"]) if d.get("prevention_en") else []
        except Exception:
            pass
        try:
            d["prevention_ur"] = json.loads(d["prevention_ur"]) if d.get("prevention_ur") else []
        except Exception:
            pass
        try:
            d["leaf_metrics"] = json.loads(d["leaf_metrics"]) if d.get("leaf_metrics") else {}
        except Exception:
            pass
        return d

def delete_scan(scan_id):
    """
    Deletes a scan record by ID and safely removes its uploaded image.
    Prevents path traversal by enforcing that deletions stay within uploads/.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filepath FROM scans WHERE id = ?", (scan_id,))
        row = cursor.fetchone()

        if row and row["filepath"]:
            rel_path = row["filepath"].lstrip("/")
            full_path = os.path.abspath(os.path.join(config.BASE_DIR, rel_path))

            # Security: Ensure deletion path is strictly inside UPLOAD_FOLDER
            if full_path.startswith(config.UPLOAD_FOLDER) and os.path.exists(full_path):
                try:
                    os.remove(full_path)
                except OSError:
                    pass

        cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
        return cursor.rowcount > 0

def clear_all_scans():
    """Clears all scan history."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scans")
        return cursor.rowcount

# -------------------------------------------------------------
# Crop / Field Operations (CRUD)
# -------------------------------------------------------------

def save_crop(data):
    """Saves a new crop/field and automatically schedules initial calendar tasks."""
    with get_db() as conn:
        cursor = conn.cursor()

        crop_name = data.get("crop_name", "").strip()
        crop_name_ur = data.get("crop_name_ur", "")
        field_name = data.get("field_name", "").strip()
        area_acres = float(data.get("area_acres", 1.0))
        variety = data.get("variety", "").strip()
        sowing_date = data.get("sowing_date", datetime.now().strftime("%Y-%m-%d"))
        soil_type = data.get("soil_type", "Loam")
        notes = data.get("notes", "").strip()

        cursor.execute("""
        INSERT INTO crops (
            crop_name, crop_name_ur, field_name, area_acres,
            variety, sowing_date, soil_type, notes, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (crop_name, crop_name_ur, field_name, area_acres, variety, sowing_date, soil_type, notes))

        crop_id = cursor.lastrowid

        # Schedule starter agronomic calendar tasks based on sowing date
        try:
            s_date = datetime.strptime(sowing_date, "%Y-%m-%d")
        except Exception:
            s_date = datetime.now()

        default_tasks = [
            {
                "crop_id": crop_id,
                "crop_name": crop_name,
                "task_type": "Irrigation",
                "title": f"First post-sowing irrigation (Kor water) for {field_name}",
                "title_ur": f"{field_name} کے لیے بوائی کے بعد پہلا پانی (کور کا پانی)",
                "due_date": (s_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                "notes": "Ensure shallow and uniform water application."
            },
            {
                "crop_id": crop_id,
                "crop_name": crop_name,
                "task_type": "Weeding",
                "title": f"Initial weeding / hoeing (Godi) for {field_name}",
                "title_ur": f"{field_name} میں جڑی بوٹیوں کی تلفی / پہلی گوڈی",
                "due_date": (s_date + timedelta(days=21)).strftime("%Y-%m-%d"),
                "notes": "Remove seasonal weeds before applying first fertilizer top-dress."
            },
            {
                "crop_id": crop_id,
                "crop_name": crop_name,
                "task_type": "Fertilizer",
                "title": f"First Urea / Nitrogen top-dressing for {field_name}",
                "title_ur": f"{field_name} میں یوریا / نائٹروجن کی پہلی قسط",
                "due_date": (s_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "notes": "Apply immediately before scheduled irrigation."
            },
            {
                "crop_id": crop_id,
                "crop_name": crop_name,
                "task_type": "Scouting",
                "title": f"Pest & foliar disease scouting for {field_name}",
                "title_ur": f"{field_name} میں کیڑوں اور پتوں کی بیماریوں کا معائنہ",
                "due_date": (s_date + timedelta(days=45)).strftime("%Y-%m-%d"),
                "notes": "Examine underside of leaves and check CropCare AI weather spray advisory."
            }
        ]

        for t in default_tasks:
            cursor.execute("""
            INSERT INTO farm_tasks (crop_id, crop_name, task_type, title, title_ur, due_date, status, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, CURRENT_TIMESTAMP)
            """, (t["crop_id"], t["crop_name"], t["task_type"], t["title"], t["title_ur"], t["due_date"], t["notes"]))

        return crop_id

def get_all_crops():
    """Retrieves all registered crops/fields."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crops ORDER BY id DESC")
        return [dict(r) for r in cursor.fetchall()]

def get_crop_by_id(crop_id):
    """Retrieves a single crop by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crops WHERE id = ?", (crop_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_crop(crop_id, data):
    """Updates an existing crop/field."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE crops SET
            crop_name = COALESCE(?, crop_name),
            crop_name_ur = COALESCE(?, crop_name_ur),
            field_name = COALESCE(?, field_name),
            area_acres = COALESCE(?, area_acres),
            variety = COALESCE(?, variety),
            sowing_date = COALESCE(?, sowing_date),
            soil_type = COALESCE(?, soil_type),
            notes = COALESCE(?, notes),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (
            data.get("crop_name"),
            data.get("crop_name_ur"),
            data.get("field_name"),
            float(data["area_acres"]) if "area_acres" in data else None,
            data.get("variety"),
            data.get("sowing_date"),
            data.get("soil_type"),
            data.get("notes"),
            crop_id
        ))
        return cursor.rowcount > 0

def delete_crop(crop_id):
    """Deletes a crop and cascades to associated tasks."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farm_tasks WHERE crop_id = ?", (crop_id,))
        cursor.execute("DELETE FROM crops WHERE id = ?", (crop_id,))
        return cursor.rowcount > 0

# -------------------------------------------------------------
# Farm Calendar & Task Operations (CRUD)
# -------------------------------------------------------------

def save_task(data):
    """Creates a new farm task."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO farm_tasks (crop_id, crop_name, task_type, title, title_ur, due_date, status, notes, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, CURRENT_TIMESTAMP)
        """, (
            data.get("crop_id"),
            data.get("crop_name", "General Farm"),
            data.get("task_type", "General"),
            data.get("title", "").strip(),
            data.get("title_ur", ""),
            data.get("due_date", datetime.now().strftime("%Y-%m-%d")),
            data.get("notes", "").strip()
        ))
        return cursor.lastrowid

def get_all_tasks(crop_id=None, status=None):
    """Retrieves farm tasks with optional crop_id and status filters."""
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM farm_tasks WHERE 1=1"
        params = []

        if crop_id is not None:
            query += " AND crop_id = ?"
            params.append(crop_id)
        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY due_date ASC, id ASC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def get_task_by_id(task_id):
    """Retrieves a single farm task by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farm_tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_task(task_id, data):
    """Updates fields of an existing task."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE farm_tasks SET
            title = COALESCE(?, title),
            title_ur = COALESCE(?, title_ur),
            task_type = COALESCE(?, task_type),
            due_date = COALESCE(?, due_date),
            status = COALESCE(?, status),
            notes = COALESCE(?, notes),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (
            data.get("title"),
            data.get("title_ur"),
            data.get("task_type"),
            data.get("due_date"),
            data.get("status"),
            data.get("notes"),
            task_id
        ))
        return cursor.rowcount > 0

def toggle_task_status(task_id):
    """Toggles status between 'pending' and 'completed'."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM farm_tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        if not row:
            return None

        new_status = "completed" if row["status"] == "pending" else "pending"
        cursor.execute("""
        UPDATE farm_tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
        """, (new_status, task_id))
        return new_status

def delete_task(task_id):
    """Deletes a farm task."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farm_tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0

# -------------------------------------------------------------
# Summary Statistics
# -------------------------------------------------------------

def get_stats():
    """Computes summary statistics for dashboard widgets."""
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM scans")
        total_scans = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scans WHERE status = 'Healthy'")
        healthy_scans = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM scans WHERE status = 'Diseased'")
        diseased_scans = cursor.fetchone()[0]

        cursor.execute("""
            SELECT disease_name, COUNT(*) as cnt
            FROM scans
            WHERE status != 'Healthy'
            GROUP BY disease_name
            ORDER BY cnt DESC
            LIMIT 1
        """)
        top_disease_row = cursor.fetchone()
        most_common_disease = top_disease_row[0] if top_disease_row else "None"

        cursor.execute("SELECT COUNT(*) FROM crops")
        total_crops = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM farm_tasks WHERE status = 'pending'")
        pending_tasks = cursor.fetchone()[0]

        return {
            "total_scans": total_scans,
            "healthy_scans": healthy_scans,
            "diseased_scans": diseased_scans,
            "most_common_disease": most_common_disease,
            "total_crops": total_crops,
            "pending_tasks": pending_tasks
        }
