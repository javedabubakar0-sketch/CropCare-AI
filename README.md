# 🌿 CropCare AI — Agricultural Decision Support & Plant Health Platform

[![CI](https://github.com/javedabubakar0-sketch/CropCare-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/javedabubakar0-sketch/CropCare-AI/actions)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fjavedabubakar0-sketch%2FCropCare-AI&env=VERCEL_SUPPORT_LARGE_FUNCTIONS&envDescription=Enables%20large%20function%20support%20for%20scikit-learn%20and%20scipy&envLink=https%3A%2F%2Fvercel.com%2Fdocs%2Ffunctions%2Fconfiguring-functions%2Flarge-functions)

> **A Secure, Reliable, Fully Functional Agricultural Decision Support System**  
> Tailored for Pakistani farmers, field advisers, and university BSCS semester evaluations.  
> Built with **Python Flask**, **Scikit-Learn**, **SQLite 3**, **Pillow/NumPy**, and **Open-Meteo**.  
> 100% Free, Local-First, Offline-Ready, and Beginner-Friendly.

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Modular Architecture & Technologies](#-modular-architecture--technologies)
3. [Database Schema & SQLite Persistence](#-database-schema--sqlite-persistence)
4. [Complete REST API Reference](#-complete-rest-api-reference)
5. [Machine Learning Botanical Diagnostic Engine](#-machine-learning-botanical-diagnostic-engine)
6. [Windows Setup & Installation Guide](#-windows-setup--installation-guide)
7. [Running the Application](#-running-the-application)
8. [Automated Quality Assurance & Test Suite](#-automated-quality-assurance--test-suite)
9. [Project Folder Structure](#-project-folder-structure)
10. [Security & Reliability Features](#-security--reliability-features)
11. [University Presentation & Viva Defense Guide](#-university-presentation--viva-defense-guide)
12. [Known Limitations & Technical Transparency](#-known-limitations--technical-transparency)

---

## 🌾 Project Overview

**CropCare AI** is a professional agricultural decision support platform designed specifically for real-world farming environments in Pakistan. Rejecting the generic AI SaaS aesthetic of neon gradients and fake mockups, CropCare AI provides an authentic, high-contrast, paper-and-field design system crafted for legibility in direct sunlight on mobile screens.

The system addresses three daily operational questions on the very first screen:
1. **What is happening with my crops?** (Managed sown acreage, sowing dates, crop age, and recent diagnosis records)
2. **What should I pay attention to today?** (Wind drift alerts, chemical spray safety windows, fungal spore risks, and pending field tasks)
3. **What can I do next?** (Instant access to diagnose foliage, register new fields, calculate irrigation requirements, or check wholesale market rates)

The application provides full **bilingual localization (English & Urdu)** with authentic agronomic terminology and complete Right-to-Left (RTL) layout support.

---

## 🛠️ Modular Architecture & Technologies

The codebase follows a clean, decoupled modular architecture suitable for first-semester BSCS evaluation:

```
┌─────────────────────────────────────────────────────────────┐
│                       Browser Client                        │
│       Vanilla HTML5, Modern CSS3, JavaScript ES6 (Fetch)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP / JSON
┌──────────────────────────────▼──────────────────────────────┐
│                    Flask Application Core                   │
│   app.py (create_app Factory)  &  config.py (Env / Limits)  │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
┌──────────────▼──────────────┐ ┌──────────────▼──────────────┐
│        Route Layer          │ │        Service Layer        │
│ routes.views  (Dashboard)   │ │ services.inference_service  │
│ routes.api    (REST Endpoints)│ services.weather_service    │
└──────────────┬──────────────┘ │ services.guidance_service   │
               │                └──────────────┬──────────────┘
┌──────────────▼───────────────────────────────▼──────────────┐
│                  Local Persistence Layer                    │
│    database.py (SQLite 3 with Foreign Keys & B-Tree Indexes)│
│    cropcare.db (Persistent Tables: scans, crops, farm_tasks)│
└─────────────────────────────────────────────────────────────┘
```

| Layer | Component | Implementation Details |
| :--- | :--- | :--- |
| **Framework** | Python 3.10 – 3.14+ / Flask 3.x | Decoupled Application Factory (`create_app`), Blueprints, JSON Error Handlers |
| **Model Inference** | Scikit-Learn, Pillow, NumPy | 36-dimensional botanical feature extraction + RandomForest Classifier |
| **Persistence** | SQLite 3 (`cropcare.db`) | Parameterized queries, foreign key cascading, automatic index optimization |
| **Weather Service**| Open-Meteo REST API | In-memory TTL caching (10 min), 6s timeouts, chemical spray safety algorithms |
| **Crop Guidance** | Bilingual Agronomic Engine | AMIS Punjab mandi benchmarks, irrigation scheduling, expert safety disclaimers |
| **3D Graphics** | Local Three.js (WebGL) | Realistic Wheat Botanical Model, Furrowed Field Parcel, Diagnostic Specimen |
| **Frontend** | Vanilla HTML, CSS, JavaScript | No heavy build steps or Tailwind; fast, accessible, native SVG icons |

---

## 🗄️ Database Schema & SQLite Persistence

CropCare AI uses SQLite 3 with parameterized queries to prevent SQL injection vulnerabilities and enforce database integrity (`PRAGMA foreign_keys = ON;`). Data survives server restarts.

### 1. `scans` Table (Leaf Scan & Diagnostic History)
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `filename` (TEXT NOT NULL) — Safe server-side generated image filename
- `filepath` (TEXT NOT NULL) — Web-accessible relative asset path
- `crop`, `crop_ur` (TEXT) — Botanical host plant name (e.g., Tomato / ٹماٹر)
- `disease_name`, `disease_name_ur` (TEXT) — Identified pathology or Healthy status
- `scientific_name` (TEXT) — Latin pathogen taxonomy (e.g., *Alternaria solani*)
- `confidence` (REAL NOT NULL) — Actual model probability score (e.g., 94.2%)
- `status`, `severity` (TEXT) — Categorical status (*Healthy / Diseased*, *Low / Moderate / High*)
- `symptoms`, `prevention_en`, `treatment_en` (TEXT) — Practical agricultural guidance
- `weather_advisory`, `leaf_metrics`, `notes` (TEXT) — Telemetry and farmer notes
- `timestamp` (DATETIME DEFAULT CURRENT_TIMESTAMP)
- **Index**: `CREATE INDEX idx_scans_timestamp ON scans(timestamp DESC);`

### 2. `crops` Table (Managed Fields & Sown Plots)
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `crop_name`, `crop_name_ur` (TEXT NOT NULL) — Crop type (Wheat, Rice, Cotton, etc.)
- `field_name` (TEXT NOT NULL) — Farmer-assigned identifier (e.g., "North Canal Plot")
- `area_acres` (REAL DEFAULT 1.0) — Physical plot size
- `variety` (TEXT) — Certified seed variety (e.g., "Akbar-2019", "Super Basmati")
- `sowing_date` (TEXT NOT NULL) — Sowing timestamp in `YYYY-MM-DD`
- `soil_type` (TEXT DEFAULT 'Loam') — Soil texture (*Clay, Loam, Sandy*)
- `notes` (TEXT) — Local field observations
- `created_at`, `updated_at` (DATETIME)
- **Index**: `CREATE INDEX idx_crops_created ON crops(created_at DESC);`

### 3. `farm_tasks` Table (Agronomic Calendar & Reminders)
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `crop_id` (INTEGER, FOREIGN KEY REFERENCES crops(id) ON DELETE CASCADE)
- `crop_name` (TEXT) — Associated crop label
- `task_type` (TEXT NOT NULL) — Category (*Irrigation, Fertilizer, Weeding, Scouting*)
- `title`, `title_ur` (TEXT NOT NULL) — Actionable agronomic title
- `due_date` (TEXT NOT NULL) — Target completion date
- `status` (TEXT DEFAULT 'pending') — Status (*pending* or *completed*)
- `notes` (TEXT), `created_at`, `updated_at` (DATETIME)
- **Indexes**: `CREATE INDEX idx_tasks_due_status ON farm_tasks(status, due_date ASC);`

---

## 🔌 Complete REST API Reference

All API routes return uniform JSON structures and appropriate HTTP status codes (200, 201, 400, 404, 413, 422, 502, 503).

### Diagnostics & System Health
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Verifies DB connection, model readiness, and filesystem storage | `200` / `503` |
| `GET` | `/api/model-status` | Returns model architecture, class labels, and loaded status | `200` |
| `GET` | `/api/stats` | Aggregated counts of scans, registered crops, and pending tasks | `200` |

### Leaf Disease Inference & History
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/scan` | Uploads foliar image (`leaf_image`), validates foliage, runs ML inference | `200` / `400` / `422` / `503` |
| `POST` | `/api/scan-sample` | Instantly diagnoses a pre-packaged bundled sample leaf | `200` / `404` / `422` |
| `GET` | `/api/scans` | Paginated scan history (`?limit=50&offset=0&crop=Tomato`) | `200` |
| `GET` | `/api/scans/<id>` | Retrieves single scan record with botanical details | `200` / `404` |
| `DELETE` | `/api/scans/<id>` | Deletes scan record and safely removes image from disk | `200` / `404` |
| `GET` | `/api/history` | Backward-compatible alias for `/api/scans` | `200` |
| `POST` | `/api/history/clear`| Clears entire scan history | `200` |

### Crops & Field Management
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/crops` | Lists all registered crops and managed fields | `200` |
| `POST` | `/api/crops` | Registers field; auto-schedules starter crop calendar tasks | `201` / `400` |
| `GET` | `/api/crops/<id>` | Retrieves single crop record | `200` / `404` |
| `PUT` | `/api/crops/<id>` | Updates crop or acreage details | `200` / `400` / `404` |
| `DELETE`| `/api/crops/<id>` | Deletes crop record and cascades deletion to linked tasks | `200` / `404` |

### Farm Tasks & Crop Calendar
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/tasks` | Lists farm reminders (`?crop_id=1&status=pending`) | `200` |
| `POST` | `/api/tasks` | Creates a new farm reminder or task | `201` / `400` |
| `GET` | `/api/tasks/<id>` | Retrieves single task record | `200` / `404` |
| `PUT` | `/api/tasks/<id>` | Updates task fields | `200` / `404` |
| `POST` | `/api/tasks/<id>/toggle`| Toggles task status between pending and completed | `200` / `404` |
| `DELETE`| `/api/tasks/<id>` | Deletes a farm task | `200` / `404` |

### Weather & Agronomic Services
| Method | Endpoint | Description | Status Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/weather` | Open-Meteo telemetry, spray safety windows, and fungal risk | `200` / `502` |
| `POST` | `/api/irrigation-advisory`| Estimates watering intervals based on soil texture and rain | `200` |
| `GET` | `/api/mandi-rates` | Authentic wholesale price benchmarks (AMIS Punjab / Sindh) | `200` |
| `GET` | `/api/knowledge-center`| Bilingual field guides (pesticide safety, neem extract, NPK) | `200` |

---

## 🌾 Realistic 3D Botanical & Agricultural Visualizations

CropCare AI features local-first, low-overhead 3D visuals using **Three.js** designed specifically for the Pakistani agricultural context without relying on cartoonish neon graphics or paid cloud 3D platforms:

1. **3D Botanical Wheat Hero (*Triticum aestivum*)**:
   - **Soil Mound**: Loam soil clod with organic crumb texture, surface nodules, and root crown emerging from canal-irrigated silt loam.
   - **Foliar Architecture**: Tapered strap-like leaves with central midrib grooves and natural gravitational arching droop.
   - **Awned Head (Ear)**: Distichous overlapping spikelets with slender photosynthetic awns catching directional sunlight.
   - **Harmonic Wind Sway**: Multi-joint sinusoidal harmonic sway modeling natural breeze motion, automatically synchronized with live Open-Meteo wind velocities (Calm, Gentle, or Field Wind).
   - **Interactive Stage Switcher**: Toggle between young leafy **Tillering** stage and mature **Heading** grain stage.

2. **Interactive 3D Field Parcel**:
   - Miniature agricultural parcel with furrow ridges, irrigation canal boundary, and crop rows.
   - **Directly mapped to SQLite farm records**: Adding or deleting fields dynamically updates corresponding 3D crop rows (Wheat, Cotton, Rice, Maize, Tomato, Potato).
   - Hover raycasting displays field metadata and clicking scrolls and highlights the respective row in the fields table.

3. **3D Foliage Diagnostic Specimen & Optical Scanner**:
   - Calibrated laboratory inspection stage with compound foliar specimen.
   - Active optical laser plane sweep during model inference.
   - Post-scan morphological lesion mapping illustrating identified pathology (e.g. Early Blight target rings, Rust pustules, or clean healthy foliage).
   - Prominently labeled with a scientific disclaimer clarifying that 3D visuals are illustrative, while diagnosis is computed directly from uploaded photos.

4. **Performance & Accessibility**:
   - **IntersectionObserver** pauses 3D rendering loops when sections scroll out of view, saving 100% of GPU/CPU.
   - **Tab Awareness**: Only the active tab's scene is animated.
   - **Reduced Motion**: Respects `prefers-reduced-motion` accessibility preferences.
   - **Clean Fallback**: Elegant SVG botanical anatomical diagram rendered gracefully if WebGL is unavailable.

---

## 🧠 Machine Learning Botanical Diagnostic Engine

### Why 36 Quantitative Botanical Features?
Modern Python (such as Python 3.14 on Windows) lacks precompiled TensorFlow wheels. Rather than fabricating mock predictions or forcing unstable dependencies, CropCare AI implements a genuine computer vision pipeline using **Scikit-Learn** and **Pillow**:

1. **RGB Color Moments (6 features)**: Mean and standard deviation across Red, Green, and Blue channels.
2. **HSV Pigment Moments (6 features)**: Hue, Saturation, and Value moments capturing chlorotic or necrotic discoloration.
3. **Foliar Vegetation Indices (5 features)**:
   - Green Leaf Index (GLI): `(2*G - R - B) / (2*G + R + B)`
   - Visible Atmospherically Resistant Index (VARI): `(G - R) / (G + R - B)`
   - Percentile distribution (10th and 90th percentiles of GLI).
4. **Tissue State Masks (4 features)**:
   - Healthy Green tissue ratio (`Hue 65°–160°`)
   - Chlorotic Yellow tissue ratio (`Hue 35°–65°`)
   - Necrotic Brown tissue ratio (`Hue 10°–35°`)
   - Dark lesion spot ratio (`Value < 0.22`)
5. **Spatial Texture & Gradients (4 features)**: Horizontal/vertical Sobel gradients and 8x8 block variance measuring spot clustering.
6. **Color Histograms (11 features)**: 8-bin Hue histogram and 3-bin Saturation distribution.

Trained and persisted via `joblib` in `models/plant_disease_model.joblib`. Model inference executes in **< 50 milliseconds** locally without GPU requirements.

---

## 💻 Windows Setup & Installation Guide

Follow these exact commands in **PowerShell** or **Command Prompt**:

### Step 1: Open Terminal in Project Folder
```powershell
cd "c:\Users\HMAT Technologies\Desktop\CropCare AI"
```

### Step 2: Create a Virtual Environment (Recommended)
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- In **PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays an Execution Policy warning, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once).*
- In **Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Initialize the SQLite Database
The database initializes automatically when running the app or tests, but can be verified manually:
```powershell
python -c "import database as db; db.init_db(); print('SQLite Database Initialized Successfully!')"
```

---

## 🚀 Running the Application

Start the local Flask development server:
```powershell
python app.py
```

*Console Output:*
```
=================================================================
CropCare AI - Agricultural Decision Support Platform
Server starting on http://127.0.0.1:5000
Debug Mode: False
=================================================================
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🧪 Automated Quality Assurance & Test Suite

The project includes an automated test suite verifying system health, ML inference, database CRUD operations, failure handling, and mocked external network requests.

Run the test suite:
```powershell
python test_app.py
```

*Expected Output:*
```
2026-10-22 21:24:09,176 [INFO] cropcare.app: SQLite database verified and initialized.
....................
----------------------------------------------------------------------
Ran 20 tests in 1.021s

OK
```

### What the 20 Tests Validate:
1. `test_01_health_endpoint`: HTTP 200, system health, DB status, and model readiness.
2. `test_02_model_status_endpoint`: Verification of 16 trained disease classes and model architecture.
3. `test_03_feature_extraction_dimension`: Confirms exact 36-dimensional botanical vector output.
4. `test_04_non_leaf_validation_rejection`: White/uniform non-leaf rejection guard.
5. `test_05_undersized_image_rejection`: Rejection of images under 32x32px.
6. `test_06_model_offline_handling`: Graceful HTTP 503 response if model weights are missing.
7. `test_07_scan_missing_file`: HTTP 400 validation for empty upload forms.
8. `test_08_scan_invalid_extension`: HTTP 400 rejection for unauthorized file types (.exe, .txt).
9. `test_09_sample_scan_valid`: Fast inference on bundled demo leaves.
10. `test_10_sample_scan_nonexistent`: HTTP 404 for missing sample names.
11. `test_11_scans_rest_crud`: Complete database lifecycle (Insert, Get All, Get Single, Delete).
12. `test_12_scan_not_found`: HTTP 404 validation for missing scan records.
13. `test_13_crops_crud_and_validation`: Crop creation, negative acreage rejection, update, and cascade delete.
14. `test_14_tasks_crud_and_toggle`: Task creation, status toggle (pending → completed), update, and deletion.
15. `test_15_weather_api_mocked_success`: Mocked Open-Meteo payload verifying spray window evaluation.
16. `test_16_weather_api_mocked_failure`: Mocked network timeout verifying graceful HTTP 502 handling.
17. `test_17_irrigation_advisory_api`: Agronomic interval and rainfall impact calculations.
18. `test_18_mandi_rates_api`: Verified wholesale pricing benchmarks (AMIS Punjab).
19. `test_19_knowledge_center_api`: Bilingual guides on pesticide safety and organic remedies.
20. `test_20_stats_api`: Integer metric reporting for dashboard badges.

---

## 🔒 Security & Reliability Features

1. **Upload Size Restrictions**: Enforces `MAX_CONTENT_LENGTH = 16 * 1024 * 1024` (16 MB). Files exceeding this limit are halted immediately by Flask and return HTTP 413.
2. **Safe Filename Generation**: User-supplied filenames are never written to disk directly. Files are assigned sanitized, timestamped, random UUID filenames (`YYYYMMDD_HHMMSS_<token>.ext`) using `secure_filename`.
3. **Path Traversal Prevention**: All file operations verify paths are strictly confined within `static/uploads/` or `static/sample_leaves/`.
4. **Parameterized SQL Queries**: 100% of SQLite database queries use `?` parameterization, preventing SQL injection attacks.
5. **No Leaked Stack Traces**: Global error handlers catch 400, 404, 413, 422, and 500 errors. Internal exceptions are logged to the server console and never exposed to clients.
6. **Network Failure Resilience**: The Open-Meteo weather client features a 6-second timeout, in-memory caching with a 10-minute TTL, and stale-cache fallback during network outages.

---

## 📁 Project Folder Structure

```
CropCare AI/
│
├── app.py                     # Flask application factory (create_app) & error handlers
├── config.py                  # Centralized configuration (upload limits, timeouts, paths)
├── database.py                # Parameterized SQLite CRUD & migration helpers
├── disease_data.py            # Bilingual botanical database (symptoms, prevention, treatments)
├── model_engine.py            # Backward-compatibility wrapper for inference_service
├── train_model.py             # Script to calibrate & build the RandomForest model
├── test_app.py                # Comprehensive 20-test automated suite (with mocking)
├── requirements.txt           # Verified dependencies (Flask, Pillow, Scikit-Learn, NumPy)
├── cropcare.db                # Persistent SQLite database file
├── README.md                  # Comprehensive documentation
│
├── routes/                    # Modular Flask Blueprints
│   ├── __init__.py            # Blueprint exports
│   ├── views.py               # Web dashboard rendering route (/)
│   └── api.py                 # Complete REST API (/api/health, /api/scans, /api/crops, etc.)
│
├── services/                  # Decoupled Business Logic
│   ├── inference_service.py   # Model loading, 36-feature extraction, image validation
│   ├── weather_service.py     # Open-Meteo client, in-memory cache, spray window logic
│   └── guidance_service.py    # AMIS Punjab rates, irrigation scheduler, field guides
│
├── models/                    # Model Weights & Class Labels
│   ├── plant_disease_model.joblib  # Calibrated model weights
│   └── classes.json                # Metadata & 16 class names
│
├── templates/
│   └── index.html             # High-contrast bilingual agricultural dashboard
│
└── static/
    ├── css/
    │   └── style.css          # Deep forest green & warm paper design system
    ├── js/
    │   ├── main.js            # Controller for tabs, scanner, crops, tasks, and modals
    │   ├── translations.js    # Bilingual English & Urdu dictionaries
    │   └── weather.js         # Weather widget controller
    ├── sample_leaves/         # Built-in demo leaves for viva presentation
    │   ├── healthy_tomato.jpg
    │   ├── tomato_early_blight.jpg
    │   ├── potato_late_blight.jpg
    │   ├── corn_common_rust.jpg
    │   └── apple_cedar_rust.jpg
    └── uploads/               # User-uploaded foliage images
```

---

## 🎓 University Presentation & Viva Defense Guide

### ⏱️ 4-Minute Demonstration Script

1. **Architecture & Dashboard (45 seconds)**:
   > *"Good morning professors. I am presenting CropCare AI, an agricultural decision support system built using Python Flask, Scikit-Learn, SQLite, and Open-Meteo. Notice the interface: it utilizes a high-contrast forest-green and natural-paper palette designed for outdoor visibility on mobile devices. The dashboard answers what is happening on the farm, displays today's chemical spray safety window, and lists due field tasks."*
2. **Bilingual RTL Localization (30 seconds)**:
   > *"To support Pakistani growers, the application includes a complete Right-to-Left (RTL) Urdu mode. Clicking 'اردو میں دیکھیں' transitions the interface with authentic agricultural vocabulary (آبپاشی, کھاد, اسپرے, منڈی کے نرخ)."*
3. **Live Foliage Diagnosis (90 seconds)**:
   > *"In the Leaf Diagnosis section, we select 'Tomato Early Blight' from our bundled presentation tray. In less than 50 milliseconds, our local 36-feature botanical computer vision model extracts color moments and vegetation indices, classifies Alternaria solani with 94% confidence, provides symptoms, and gives organic neem remedies alongside chemical options."*
4. **Crop Management & Auto-Calendar (45 seconds)**:
   > *"When registering a plot in 'Fields & Crops', CropCare AI automatically schedules critical agronomic tasks in the 'Farm Calendar'—such as first Kor irrigation 7 days post-sowing and first Urea top-dressing at 30 days."*
5. **Weather & Mandi Rates (30 seconds)**:
   > *"In 'Irrigation Helper', the app calculates watering intervals based on soil texture and alerts farmers if rain is forecast in the next 72 hours. In 'Guides & Mandi', farmers can view official AMIS wholesale price benchmarks."*

---

### ❓ Top 5 Viva Questions & Rock-Solid Answers

#### Q1: Why did you build a feature-based Scikit-Learn classifier instead of a Deep Learning CNN?
> **Answer**: *"Python 3.14 lacks precompiled TensorFlow binaries on Windows. Rather than using mock predictions, I implemented an authentic computer vision pipeline using Scikit-Learn and Pillow that extracts 36 genuine botanical features (RGB/HSV color moments, GLI, VARI, necrotic ratios, and Sobel gradient textures). It is reproducible, runs 100% locally on standard PC hardware, and executes in under 50 milliseconds without requiring a dedicated GPU."*

#### Q2: What prevents the model from classifying non-leaf images like a car or a face?
> **Answer**: *"We implemented a biological validation guard in `services/inference_service.py`. Before classification, the image is checked for chlorophyll pixel dominance and vegetation color variance. If an image lacks botanical foliage characteristics (plant pixel ratio < 8%), it is rejected with an explanatory message instead of hallucinating a diagnosis."*

#### Q3: How is data structured and persisted?
> **Answer**: *"We use SQLite 3 across three relational tables: `scans` (diagnostic history), `crops` (managed fields), and `farm_tasks` (calendar tasks). All queries use parameterized SQL to prevent SQL injection, and foreign keys cascade deletions when a crop is removed."*

#### Q4: How is the chemical spray advisory calculated?
> **Answer**: *"Chemical spraying is evaluated against agronomic safety thresholds: wind speed must be below 15 km/h to prevent dangerous drift, precipitation must be 0 mm to prevent wash-off, and temperature must be below 36°C to avoid foliar chemical burn."*

#### Q5: Is any paid API or external subscription required?
> **Answer**: *"No. CropCare AI is 100% free and open-source. The model runs locally, the database is local SQLite, and the meteorological data is fetched from the free Open-Meteo REST API."*

---

## 🔍 Known Limitations & Technical Transparency

1. **Botanical Scope**: The classifier is calibrated for 16 major botanical conditions across Tomato, Potato, Corn, Apple, and Grape.
2. **Irrigation Advisory**: Serves as decision support based on crop coefficients and weather forecasts; physical soil moisture (*Vattar / وتر*) should always be inspected.
3. **Mandi Benchmarks**: Market rates reflect official wholesale terminal benchmarks (AMIS Punjab); local commission agent deductions may vary.

---

## 📜 License
This project is open-source and created for educational purposes. Feel free to use and modify it for your university coursework!
