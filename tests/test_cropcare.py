"""
CropCare AI - Automated Test Suite
Unit and integration tests for REST API, ML inference, and database persistence.
"""

import os
import sys
import unittest
import json

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app
import database as db

class CropCareTestCase(unittest.TestCase):
    """Test suite for CropCare AI API and services."""

    def setUp(self):
        """Set up test client with a test configuration."""
        self.app = create_app({
            "TESTING": True,
            "DATABASE_PATH": ":memory:"  # In-memory database for isolation
        })
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        """Verify that the health check endpoint returns 200 and healthy status."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["model"]["is_loaded"])
        self.assertEqual(data["model"]["classes_count"], 16)

    def test_index_view(self):
        """Verify that the main dashboard HTML view renders properly."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CropCare AI", response.data)

    def test_model_status(self):
        """Verify ML model metadata diagnostics."""
        response = self.client.get("/api/model-status")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["is_loaded"])
        self.assertIsNone(data["load_error"])
        self.assertEqual(len(data["classes"]), 16)

    def test_stats_endpoint(self):
        """Verify aggregated statistics endpoint."""
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("total_scans", data["stats"])
        self.assertIn("total_crops", data["stats"])

    def test_mandi_rates_endpoint(self):
        """Verify AMIS wholesale mandi rates endpoint."""
        response = self.client.get("/api/mandi-rates")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("benchmarks", data)
        self.assertGreater(len(data["benchmarks"]), 0)

    def test_scan_sample(self):
        """Verify demo leaf scan inference on bundled sample image."""
        response = self.client.post("/api/scan-sample", data=json.dumps({
            "sample_name": "tomato_early_blight.jpg"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["crop"], "Tomato")
        self.assertTrue(len(data["disease_name"]) > 0)
        self.assertGreater(data["confidence"], 0.5)

    def test_crops_crud(self):
        """Verify field and crop management endpoints."""
        # 1. Add new crop
        payload = {
            "crop_name": "Wheat",
            "field_name": "Test Demonstration Plot",
            "area_acres": 2.5,
            "variety": "Akbar-2019",
            "sowing_date": "2026-11-01",
            "soil_type": "Loam"
        }
        res_post = self.client.post("/api/crops", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res_post.status_code, 201)
        post_data = res_post.get_json()
        crop_id = post_data["crop_id"]

        # 2. Retrieve crops list
        res_get = self.client.get("/api/crops")
        self.assertEqual(res_get.status_code, 200)
        get_data = res_get.get_json()
        self.assertTrue(any(c["id"] == crop_id for c in get_data["crops"]))

        # 3. Delete the test crop
        res_del = self.client.delete(f"/api/crops/{crop_id}")
        self.assertEqual(res_del.status_code, 200)

if __name__ == "__main__":
    unittest.main()
