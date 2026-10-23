"""
CropCare AI - Real Botanical Disease Inference Service
Provides safe model loading, biological feature extraction (36 dimensions),
image validation (size, readability, non-foliage checks), and real inference.
"""

import os
import json
import logging
import numpy as np
from PIL import Image
import joblib

import config
from disease_data import get_disease_info

logger = logging.getLogger("cropcare.inference")

MODEL_PATH = config.MODEL_PATH
CLASSES_PATH = config.CLASSES_PATH

class PlantDiseaseInferenceService:
    """
    Encapsulates local Scikit-Learn model loading, validation,
    and botanical feature extraction for foliar disease classification.
    """

    def __init__(self, model_path=config.MODEL_PATH, classes_path=config.CLASSES_PATH):
        self.model_path = model_path
        self.classes_path = classes_path
        self.model = None
        self.classes = []
        self.metadata = {}
        self.is_loaded = False
        self.load_error = None
        self._load_model()

    def _load_model(self):
        """Loads model weights and class labels from local disk."""
        if not os.path.exists(self.model_path):
            self.is_loaded = False
            self.load_error = (
                f"Model file '{os.path.basename(self.model_path)}' was not found in models/ directory. "
                f"Please ensure models/plant_disease_model.joblib exists or run 'python train_model.py'."
            )
            logger.warning(self.load_error)
            return False

        try:
            saved_data = joblib.load(self.model_path)
            if isinstance(saved_data, dict) and "model" in saved_data:
                self.model = saved_data["model"]
                self.classes = list(saved_data.get("classes", []))
            else:
                self.model = saved_data
                self.classes = list(getattr(self.model, "classes_", []))

            # Load metadata from classes.json if present
            if os.path.exists(self.classes_path):
                try:
                    with open(self.classes_path, "r", encoding="utf-8") as f:
                        self.metadata = json.load(f)
                except Exception as meta_err:
                    logger.warning(f"Could not read classes.json metadata: {meta_err}")

            self.is_loaded = True
            self.load_error = None
            logger.info(f"Loaded plant disease model with {len(self.classes)} classes.")
            return True

        except Exception as e:
            self.is_loaded = False
            self.load_error = f"Error loading model weights: {str(e)}"
            logger.error(self.load_error)
            return False

    def reload(self):
        """Allows manual reloading of model weights."""
        return self._load_model()

    def get_status(self):
        """Returns the readiness state and diagnostics of the ML engine."""
        return {
            "is_loaded": self.is_loaded,
            "classes_count": len(self.classes) if self.classes else 0,
            "classes": self.classes,
            "load_error": self.load_error,
            "architecture": "RandomForest Botanical Classifier (36 Quantitative Features)",
            "model_path": self.model_path,
            "metadata": self.metadata
        }

    def validate_and_preprocess_image(self, image_input):
        """
        Validates whether image is readable, sufficiently sized, and exhibits plant leaf characteristics.
        Returns: (PIL.Image or None, error_message or None, leaf_metrics or None)
        """
        try:
            if isinstance(image_input, str):
                if not os.path.exists(image_input):
                    return None, f"Image file not found: {image_input}", None
                img = Image.open(image_input)
            elif isinstance(image_input, Image.Image):
                img = image_input
            else:
                img = Image.open(image_input)

            # Convert to RGB (handles RGBA, Grayscale, etc.)
            img = img.convert("RGB")
            width, height = img.size

            if width < 32 or height < 32:
                return None, f"Image resolution is too low ({width}x{height}px). Minimum required is 32x32px.", None

            # Thumbnail check for foliage detection & uniformity
            img_thumb = img.resize((100, 100))
            arr = np.asarray(img_thumb, dtype=np.float32) / 255.0
            r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

            # Green index & vegetation dominance
            green_dominance = (g > (r * 0.85)) & (g > (b * 0.85))
            chlorophyll_pct = float(np.mean(green_dominance) * 100)

            # Diseased / chlorotic / necrotic leaf tissue: r > b, g > 0.8*b
            diseased_tissue = (r > b) & (g > b * 0.8) & (r > 0.2) & (g > 0.15)
            plant_pixel_pct = float(np.mean(green_dominance | diseased_tissue) * 100)

            # Contrast / variation check (detects solid blanks or uniform color blocks)
            std_dev = float(np.std(arr))
            if std_dev < 0.03:
                return None, "Uploaded image appears completely uniform or blank. Please upload a clear photo of a plant leaf.", None

            metrics = {
                "width": width,
                "height": height,
                "chlorophyll_pct": round(chlorophyll_pct, 1),
                "plant_pixel_pct": round(plant_pixel_pct, 1),
                "contrast": round(std_dev, 3)
            }

            # Guard against uploading non-botanical images (e.g. blue cars, grey concrete)
            if plant_pixel_pct < 8.0:
                return None, "The uploaded image does not appear to be a plant leaf (insufficient foliar vegetation detected). Please upload a clear leaf photo.", metrics

            return img, None, metrics

        except Exception as e:
            return None, f"Unable to parse image file: {str(e)}", None

    def extract_features(self, pil_image):
        """
        Extracts the 36-dimensional quantitative botanical feature vector:
        - Color moments in RGB & HSV (12 features)
        - Vegetation indices GLI & VARI (5 features)
        - Tissue state ratios (healthy, chlorotic, necrotic, lesions) (4 features)
        - Spatial gradient & block texture variance (4 features)
        - Color histograms (11 features: 8 hue bins, 3 saturation bins)
        """
        # Standardize size to 224x224
        img = pil_image.resize((224, 224), Image.Resampling.BILINEAR)
        arr_rgb = np.asarray(img, dtype=np.float32) / 255.0
        r = arr_rgb[:, :, 0]
        g = arr_rgb[:, :, 1]
        b = arr_rgb[:, :, 2]

        # Convert to HSV in pure numpy
        max_c = np.maximum(np.maximum(r, g), b)
        min_c = np.minimum(np.minimum(r, g), b)
        delta = max_c - min_c

        # Value
        v = max_c
        # Saturation
        s = np.zeros_like(max_c)
        nonzero_mask = max_c > 1e-6
        s[nonzero_mask] = delta[nonzero_mask] / max_c[nonzero_mask]

        # Hue (in degrees [0, 360])
        h = np.zeros_like(max_c)
        valid_delta = delta > 1e-6

        # When R is max
        r_mask = valid_delta & (max_c == r)
        h[r_mask] = 60.0 * (((g[r_mask] - b[r_mask]) / delta[r_mask]) % 6)

        # When G is max
        g_mask = valid_delta & (max_c == g)
        h[g_mask] = 60.0 * (((b[g_mask] - r[g_mask]) / delta[g_mask]) + 2)

        # When B is max
        b_mask = valid_delta & (max_c == b)
        h[b_mask] = 60.0 * (((r[b_mask] - g[b_mask]) / delta[b_mask]) + 4)

        # 1. Color moments (12 features)
        r_mean, r_std = float(np.mean(r)), float(np.std(r))
        g_mean, g_std = float(np.mean(g)), float(np.std(g))
        b_mean, b_std = float(np.mean(b)), float(np.std(b))

        h_norm = h / 360.0
        h_mean, h_std = float(np.mean(h_norm)), float(np.std(h_norm))
        s_mean, s_std = float(np.mean(s)), float(np.std(s))
        v_mean, v_std = float(np.mean(v)), float(np.std(v))

        # 2. Vegetation indices (5 features)
        denom_gli = 2 * g + r + b + 1e-6
        gli = (2 * g - r - b) / denom_gli
        gli_mean = float(np.mean(gli))
        gli_std = float(np.std(gli))
        gli_p10 = float(np.percentile(gli, 10))
        gli_p90 = float(np.percentile(gli, 90))

        vari = (g - r) / (g + r - b + 1e-6)
        vari_mean = float(np.clip(np.mean(vari), -2.0, 2.0))

        # 3. Tissue state classification masks (4 features)
        healthy_green = (h >= 65) & (h <= 160) & (s >= 0.25) & (v >= 0.20)
        healthy_ratio = float(np.mean(healthy_green))

        chlorotic_yellow = (h >= 35) & (h < 65) & (s >= 0.30) & (v >= 0.35)
        yellow_ratio = float(np.mean(chlorotic_yellow))

        necrotic_brown = (h >= 10) & (h < 35) & (s >= 0.25) & (v <= 0.65)
        brown_ratio = float(np.mean(necrotic_brown))

        dark_lesions = (v < 0.22) & (v > 0.04)
        lesion_ratio = float(np.mean(dark_lesions))

        # 4. Spatial gradient & local texture features (4 features)
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        grad_x = np.abs(gray[:, 1:] - gray[:, :-1])
        grad_y = np.abs(gray[1:, :] - gray[:-1, :])
        grad_mean = float((np.mean(grad_x) + np.mean(grad_y)) / 2.0)
        grad_std = float((np.std(grad_x) + np.std(grad_y)) / 2.0)

        blocks = gray.reshape(28, 8, 28, 8).transpose(0, 2, 1, 3).reshape(-1, 64)
        block_vars = np.var(blocks, axis=1)
        block_var_mean = float(np.mean(block_vars))
        block_var_max = float(np.max(block_vars))

        # 5. Color histograms (11 features: 8 hue bins, 3 saturation bins)
        hue_bins, _ = np.histogram(h, bins=8, range=(0, 360), density=True)
        sat_bins, _ = np.histogram(s, bins=3, range=(0, 1), density=True)

        features = [
            r_mean, r_std, g_mean, g_std, b_mean, b_std,
            h_mean, h_std, s_mean, s_std, v_mean, v_std,
            gli_mean, gli_std, gli_p10, gli_p90, vari_mean,
            healthy_ratio, yellow_ratio, brown_ratio, lesion_ratio,
            grad_mean, grad_std, block_var_mean, block_var_max
        ]
        features.extend(hue_bins.tolist())
        features.extend(sat_bins.tolist())

        return np.array(features, dtype=np.float32)

    def predict(self, image_input):
        """
        Runs real botanical ML classification on image_input (filepath, PIL Image, or FileStorage).
        Returns a rich prediction result dictionary or error dictionary.
        """
        if not self.is_loaded:
            return {
                "success": False,
                "error": "Model Not Loaded",
                "message": self.load_error or "Machine learning model is not available.",
                "solution": "Run 'python train_model.py' to generate and calibrate the local model weights."
            }

        pil_image, val_error, metrics = self.validate_and_preprocess_image(image_input)
        if val_error:
            return {
                "success": False,
                "error": "Validation Error",
                "message": val_error,
                "metrics": metrics
            }

        try:
            feat = self.extract_features(pil_image)
            feat_batch = np.expand_dims(feat, axis=0)

            probs = self.model.predict_proba(feat_batch)[0]
            classes = list(self.model.classes_)

            top_idx = int(np.argmax(probs))
            top_class = classes[top_idx]
            confidence = float(probs[top_idx])

            # Top 3 candidates
            sorted_indices = np.argsort(probs)[::-1]
            top_predictions = []
            for idx in sorted_indices[:3]:
                cls_name = classes[idx]
                info = get_disease_info(cls_name)
                top_predictions.append({
                    "class": cls_name,
                    "crop": info.get("crop", "Plant"),
                    "crop_ur": info.get("crop_ur", "پودا"),
                    "disease_name": info.get("disease_name", cls_name),
                    "disease_name_ur": info.get("disease_name_ur", ""),
                    "confidence": round(float(probs[idx]) * 100, 1)
                })

            disease_info = get_disease_info(top_class)

            return {
                "success": True,
                "predicted_class": top_class,
                "confidence": round(confidence * 100, 1),
                "crop": disease_info.get("crop"),
                "crop_ur": disease_info.get("crop_ur"),
                "disease_name": disease_info.get("disease_name"),
                "disease_name_ur": disease_info.get("disease_name_ur"),
                "scientific_name": disease_info.get("scientific_name"),
                "status": disease_info.get("status"),
                "status_ur": disease_info.get("status_ur"),
                "severity": disease_info.get("severity"),
                "severity_ur": disease_info.get("severity_ur"),
                "symptoms": disease_info.get("symptoms"),
                "symptoms_ur": disease_info.get("symptoms_ur"),
                "prevention": disease_info.get("prevention"),
                "prevention_ur": disease_info.get("prevention_ur"),
                "treatment": disease_info.get("treatment"),
                "treatment_ur": disease_info.get("treatment_ur"),
                "weather_advisory": disease_info.get("weather_advisory"),
                "weather_advisory_ur": disease_info.get("weather_advisory_ur"),
                "top_predictions": top_predictions,
                "leaf_metrics": metrics,
                "model_architecture": "RandomForest Classifier (Botanical Feature Extraction - 36 dimensions)",
                "expert_disclaimer": "Diagnostic assistance only. Always consult a local agricultural extension officer before chemical treatment."
            }

        except Exception as e:
            logger.error(f"Inference execution error: {e}", exc_info=True)
            return {
                "success": False,
                "error": "Inference Error",
                "message": f"An error occurred during model prediction: {str(e)}"
            }

# Singleton instance
inference_service = PlantDiseaseInferenceService()
