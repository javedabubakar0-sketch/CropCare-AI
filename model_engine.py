"""
CropCare AI - Model Engine Compatibility Layer
Re-exports the modular PlantDiseaseInferenceService from services.inference_service.
Ensures full backward compatibility with any existing imports.
"""

from services.inference_service import (
    PlantDiseaseInferenceService as CropCareModelEngine,
    inference_service as model_engine,
    MODEL_PATH,
    CLASSES_PATH
)

__all__ = ["CropCareModelEngine", "model_engine", "MODEL_PATH", "CLASSES_PATH"]
