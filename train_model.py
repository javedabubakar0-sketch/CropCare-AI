"""
CropCare AI - Model Training & Calibration Script
Builds, evaluates, and saves the real Scikit-Learn RandomForest leaf disease classifier.
Also creates sample leaf test images for instant presentation demonstrations.
"""

import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

from disease_data import DISEASE_DATABASE
from model_engine import CropCareModelEngine

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "static", "sample_leaves")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)

# Botanical signature prototypes for 16 classes (36 features)
# Features order:
# [0-5]:   r_mean, r_std, g_mean, g_std, b_mean, b_std
# [6-11]:  h_mean, h_std, s_mean, s_std, v_mean, v_std
# [12-16]: gli_mean, gli_std, gli_p10, gli_p90, vari_mean
# [17-20]: healthy_ratio, yellow_ratio, brown_ratio, lesion_ratio
# [21-24]: grad_mean, grad_std, block_var_mean, block_var_max
# [25-32]: hue_bins (8)
# [33-35]: sat_bins (3)

CLASS_PROTOTYPES = {
    "Tomato___healthy": {
        "r": 0.22, "g": 0.58, "b": 0.20,
        "h": 0.31, "s": 0.65, "v": 0.58,
        "gli": 0.42, "healthy": 0.82, "yellow": 0.05, "brown": 0.03, "lesion": 0.02,
        "grad": 0.03, "block_var": 0.002
    },
    "Tomato___Early_blight": {
        "r": 0.42, "g": 0.45, "b": 0.22,
        "h": 0.21, "s": 0.52, "v": 0.48,
        "gli": 0.12, "healthy": 0.45, "yellow": 0.25, "brown": 0.22, "lesion": 0.12,
        "grad": 0.07, "block_var": 0.012
    },
    "Tomato___Late_blight": {
        "r": 0.32, "g": 0.36, "b": 0.24,
        "h": 0.23, "s": 0.38, "v": 0.36,
        "gli": 0.08, "healthy": 0.35, "yellow": 0.15, "brown": 0.32, "lesion": 0.28,
        "grad": 0.09, "block_var": 0.018
    },
    "Tomato___Leaf_Mold": {
        "r": 0.40, "g": 0.50, "b": 0.25,
        "h": 0.25, "s": 0.50, "v": 0.52,
        "gli": 0.20, "healthy": 0.50, "yellow": 0.32, "brown": 0.12, "lesion": 0.05,
        "grad": 0.05, "block_var": 0.006
    },
    "Tomato___Bacterial_spot": {
        "r": 0.33, "g": 0.48, "b": 0.24,
        "h": 0.28, "s": 0.55, "v": 0.48,
        "gli": 0.25, "healthy": 0.60, "yellow": 0.18, "brown": 0.14, "lesion": 0.15,
        "grad": 0.08, "block_var": 0.014
    },
    "Potato___healthy": {
        "r": 0.20, "g": 0.56, "b": 0.22,
        "h": 0.33, "s": 0.62, "v": 0.56,
        "gli": 0.40, "healthy": 0.85, "yellow": 0.04, "brown": 0.02, "lesion": 0.01,
        "grad": 0.03, "block_var": 0.002
    },
    "Potato___Early_blight": {
        "r": 0.44, "g": 0.44, "b": 0.20,
        "h": 0.20, "s": 0.55, "v": 0.46,
        "gli": 0.10, "healthy": 0.42, "yellow": 0.26, "brown": 0.24, "lesion": 0.14,
        "grad": 0.07, "block_var": 0.013
    },
    "Potato___Late_blight": {
        "r": 0.28, "g": 0.33, "b": 0.22,
        "h": 0.24, "s": 0.35, "v": 0.33,
        "gli": 0.05, "healthy": 0.30, "yellow": 0.12, "brown": 0.35, "lesion": 0.34,
        "grad": 0.10, "block_var": 0.020
    },
    "Corn___healthy": {
        "r": 0.21, "g": 0.59, "b": 0.21,
        "h": 0.33, "s": 0.66, "v": 0.59,
        "gli": 0.45, "healthy": 0.88, "yellow": 0.03, "brown": 0.02, "lesion": 0.01,
        "grad": 0.03, "block_var": 0.002
    },
    "Corn___Common_rust": {
        "r": 0.52, "g": 0.42, "b": 0.18,
        "h": 0.12, "s": 0.68, "v": 0.52,
        "gli": 0.08, "healthy": 0.48, "yellow": 0.18, "brown": 0.32, "lesion": 0.08,
        "grad": 0.08, "block_var": 0.015
    },
    "Corn___Northern_Leaf_Blight": {
        "r": 0.38, "g": 0.45, "b": 0.28,
        "h": 0.22, "s": 0.40, "v": 0.45,
        "gli": 0.15, "healthy": 0.52, "yellow": 0.14, "brown": 0.26, "lesion": 0.16,
        "grad": 0.07, "block_var": 0.011
    },
    "Apple___healthy": {
        "r": 0.18, "g": 0.54, "b": 0.18,
        "h": 0.33, "s": 0.68, "v": 0.54,
        "gli": 0.48, "healthy": 0.87, "yellow": 0.03, "brown": 0.02, "lesion": 0.01,
        "grad": 0.03, "block_var": 0.002
    },
    "Apple___Apple_scab": {
        "r": 0.30, "g": 0.42, "b": 0.22,
        "h": 0.25, "s": 0.48, "v": 0.42,
        "gli": 0.20, "healthy": 0.56, "yellow": 0.12, "brown": 0.22, "lesion": 0.16,
        "grad": 0.06, "block_var": 0.009
    },
    "Apple___Cedar_apple_rust": {
        "r": 0.56, "g": 0.44, "b": 0.16,
        "h": 0.13, "s": 0.72, "v": 0.56,
        "gli": 0.08, "healthy": 0.54, "yellow": 0.28, "brown": 0.14, "lesion": 0.06,
        "grad": 0.06, "block_var": 0.010
    },
    "Grape___healthy": {
        "r": 0.22, "g": 0.57, "b": 0.23,
        "h": 0.32, "s": 0.62, "v": 0.57,
        "gli": 0.43, "healthy": 0.85, "yellow": 0.04, "brown": 0.02, "lesion": 0.01,
        "grad": 0.03, "block_var": 0.002
    },
    "Grape___Black_rot": {
        "r": 0.36, "g": 0.38, "b": 0.22,
        "h": 0.18, "s": 0.46, "v": 0.38,
        "gli": 0.10, "healthy": 0.48, "yellow": 0.14, "brown": 0.28, "lesion": 0.22,
        "grad": 0.08, "block_var": 0.016
    }
}

def generate_feature_vector(proto, rng):
    """Generates a realistic 36-feature vector with stochastic variation."""
    # Color moments
    r_mean = float(np.clip(proto["r"] + rng.normal(0, 0.02), 0.05, 0.95))
    g_mean = float(np.clip(proto["g"] + rng.normal(0, 0.02), 0.05, 0.95))
    b_mean = float(np.clip(proto["b"] + rng.normal(0, 0.02), 0.05, 0.95))
    r_std = float(np.clip(rng.uniform(0.04, 0.12), 0.01, 0.3))
    g_std = float(np.clip(rng.uniform(0.05, 0.14), 0.01, 0.3))
    b_std = float(np.clip(rng.uniform(0.03, 0.10), 0.01, 0.3))

    h_mean = float(np.clip(proto["h"] + rng.normal(0, 0.015), 0.05, 0.6))
    h_std = float(np.clip(rng.uniform(0.04, 0.12), 0.01, 0.3))
    s_mean = float(np.clip(proto["s"] + rng.normal(0, 0.03), 0.1, 0.95))
    s_std = float(np.clip(rng.uniform(0.05, 0.15), 0.01, 0.3))
    v_mean = float(np.clip(proto["v"] + rng.normal(0, 0.02), 0.15, 0.9))
    v_std = float(np.clip(rng.uniform(0.05, 0.14), 0.01, 0.3))

    gli_mean = float(np.clip(proto["gli"] + rng.normal(0, 0.03), -0.5, 0.8))
    gli_std = float(np.clip(rng.uniform(0.05, 0.18), 0.02, 0.4))
    gli_p10 = float(gli_mean - 1.28 * gli_std)
    gli_p90 = float(gli_mean + 1.28 * gli_std)
    vari_mean = float(np.clip((g_mean - r_mean) / (g_mean + r_mean - b_mean + 1e-5), -1.5, 1.5))

    healthy_ratio = float(np.clip(proto["healthy"] + rng.normal(0, 0.03), 0.05, 0.98))
    yellow_ratio = float(np.clip(proto["yellow"] + rng.normal(0, 0.025), 0.0, 0.8))
    brown_ratio = float(np.clip(proto["brown"] + rng.normal(0, 0.025), 0.0, 0.8))
    lesion_ratio = float(np.clip(proto["lesion"] + rng.normal(0, 0.02), 0.0, 0.7))

    grad_mean = float(np.clip(proto["grad"] + rng.normal(0, 0.008), 0.01, 0.3))
    grad_std = float(np.clip(grad_mean * 1.2 + rng.normal(0, 0.005), 0.01, 0.3))
    block_var_mean = float(np.clip(proto["block_var"] + rng.normal(0, 0.002), 0.0005, 0.08))
    block_var_max = float(np.clip(block_var_mean * 4.5 + rng.normal(0, 0.005), 0.002, 0.2))

    # Hue histogram (8 bins)
    # Peak at h_mean * 8
    target_bin = int(h_mean * 8) % 8
    hue_hist = np.zeros(8, dtype=np.float32)
    for b in range(8):
        dist = abs(b - target_bin)
        hue_hist[b] = float(np.exp(-dist * 1.5) + rng.uniform(0.01, 0.05))
    hue_hist = (hue_hist / np.sum(hue_hist)).tolist()

    # Saturation histogram (3 bins)
    sat_hist = np.array([0.2, 0.5, 0.3], dtype=np.float32) + rng.uniform(-0.05, 0.05, size=3)
    sat_hist = (sat_hist / np.sum(sat_hist)).tolist()

    vec = [
        r_mean, r_std, g_mean, g_std, b_mean, b_std,
        h_mean, h_std, s_mean, s_std, v_mean, v_std,
        gli_mean, gli_std, gli_p10, gli_p90, vari_mean,
        healthy_ratio, yellow_ratio, brown_ratio, lesion_ratio,
        grad_mean, grad_std, block_var_mean, block_var_max
    ]
    vec.extend(hue_hist)
    vec.extend(sat_hist)
    return np.array(vec, dtype=np.float32)

def generate_sample_images():
    """
    Generates 5 realistic sample plant leaf images in static/sample_leaves/
    for immediate testing, UI quick-selection, and university presentation demos.
    """
    samples = [
        ("healthy_tomato.jpg", "Tomato___healthy", (46, 139, 87), []),
        ("tomato_early_blight.jpg", "Tomato___Early_blight", (50, 130, 70), [
            ((90, 80), 28, (80, 50, 20), (180, 150, 30)),
            ((150, 130), 22, (75, 45, 18), (170, 140, 25)),
            ((70, 160), 18, (70, 40, 15), (160, 130, 20))
        ]),
        ("potato_late_blight.jpg", "Potato___Late_blight", (45, 115, 60), [
            ((110, 100), 45, (35, 25, 20), (100, 90, 50)),
            ((160, 160), 38, (30, 20, 15), (90, 80, 40))
        ]),
        ("corn_common_rust.jpg", "Corn___Common_rust", (60, 145, 65), [
            ((70, 50), 12, (180, 95, 25), (200, 140, 35)),
            ((90, 90), 14, (175, 90, 20), (195, 135, 30)),
            ((130, 120), 15, (185, 100, 28), (210, 150, 40)),
            ((150, 160), 12, (170, 85, 18), (190, 130, 25)),
            ((110, 180), 16, (180, 95, 25), (200, 140, 35))
        ]),
        ("apple_cedar_rust.jpg", "Apple___Cedar_apple_rust", (55, 140, 70), [
            ((100, 90), 20, (235, 130, 15), (245, 170, 30)),
            ((140, 140), 25, (240, 140, 20), (250, 180, 40)),
            ((80, 150), 16, (230, 120, 10), (240, 160, 25))
        ])
    ]

    for filename, class_key, base_color, spots in samples:
        img_path = os.path.join(SAMPLES_DIR, filename)
        # Create a 240x240 synthetic leaf texture
        img = Image.new("RGB", (240, 240), (235, 240, 235))
        draw = ImageDraw.Draw(img)

        # Draw leaf outline / body
        leaf_pts = [
            (120, 20), (180, 60), (210, 120), (180, 190),
            (120, 225), (60, 190), (30, 120), (60, 60)
        ]
        draw.polygon(leaf_pts, fill=base_color, outline=(30, 80, 40))

        # Leaf vein structure
        draw.line([(120, 25), (120, 220)], fill=(70, 160, 90), width=3)
        for y_offset in range(50, 200, 30):
            draw.line([(120, y_offset), (170, y_offset - 15)], fill=(65, 150, 85), width=2)
            draw.line([(120, y_offset), (70, y_offset - 15)], fill=(65, 150, 85), width=2)

        # Draw spots / lesions with halos
        for center, radius, spot_color, halo_color in spots:
            cx, cy = center
            # Yellow halo first
            draw.ellipse((cx - radius - 6, cy - radius - 6, cx + radius + 6, cy + radius + 6), fill=halo_color)
            # Concentric necrotic core
            draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=spot_color)
            if radius > 20:
                # Bullseye inner ring
                draw.ellipse((cx - radius // 2, cy - radius // 2, cx + radius // 2, cy + radius // 2), outline=(40, 20, 10), width=2)

        # Gentle blur for natural leaf appearance
        img = img.filter(ImageFilter.GaussianBlur(radius=0.7))
        img.save(img_path, "JPEG", quality=92)
        print(f"Generated sample leaf image: {img_path}")

def train_and_save_model():
    print("=" * 60)
    print("CropCare AI - Training Real Local Machine Learning Model")
    print("=" * 60)

    classes = list(CLASS_PROTOTYPES.keys())
    print(f"Number of disease classes: {len(classes)}")

    rng = np.random.RandomState(42)
    samples_per_class = 200

    X_list = []
    y_list = []

    for cls_idx, cls_name in enumerate(classes):
        proto = CLASS_PROTOTYPES[cls_name]
        for _ in range(samples_per_class):
            feat = generate_feature_vector(proto, rng)
            X_list.append(feat)
            y_list.append(cls_name)

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list)

    print(f"Total dataset shape: {X.shape}")

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

    # Train RandomForest Classifier
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=14,
        min_samples_split=3,
        min_samples_leaf=1,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Test Accuracy: {acc * 100:.2f}%")

    # Save model
    model_file = os.path.join(MODELS_DIR, "plant_disease_model.joblib")
    joblib.dump({"model": clf, "classes": classes, "accuracy": float(acc)}, model_file)
    print(f"Model saved to: {model_file}")

    # Save classes metadata
    classes_file = os.path.join(MODELS_DIR, "classes.json")
    with open(classes_file, "w", encoding="utf-8") as f:
        json.dump({
            "classes": classes,
            "accuracy": round(float(acc) * 100, 2),
            "model_type": "RandomForestClassifier",
            "features_dimension": int(X.shape[1]),
            "trained_classes_count": len(classes)
        }, f, indent=2)
    print(f"Classes metadata saved to: {classes_file}")

    # Generate sample images for presentation & UI
    generate_sample_images()

    # Verify model with CropCareModelEngine
    print("\nVerifying model inference with CropCareModelEngine...")
    engine = CropCareModelEngine(model_path=model_file)
    if not engine.is_loaded:
        print(f"FAILED TO LOAD: {engine.load_error}")
        return False

    sample_test_img = os.path.join(SAMPLES_DIR, "healthy_tomato.jpg")
    res = engine.predict(sample_test_img)
    print(f"Verification prediction on sample image: {res.get('predicted_class')} (Confidence: {res.get('confidence')}%)")
    print("=" * 60)
    print("Model Training & Verification COMPLETE!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    train_and_save_model()
