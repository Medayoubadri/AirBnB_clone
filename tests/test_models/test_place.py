#!/usr/bin/python3

"""
Unit tests for the Place class with structured and comprehensive coverage.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.place import Place
from models import storage

class TestPlace(unittest.TestCase):
    """Comprehensive tests for the Place class."""

    def setUp(self):
        """Sets up a Place instance before each test."""
        self.place = Place()
        self.place.city_id = "1234"
        self.place.user_id = "5678"
        self.place.name = "YO MAMA's BEACH HOUSE"
        self.place.description = "A Big house just like Yo mama. It's too expensive for you anyway."
        self.place.number_rooms = 3
        self.place.number_bathrooms = 2
        self.place.max_guest = 6
        self.place.price_by_night = 150
        self.place.latitude = 36.7783
        self.place.longitude = -119.4179

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    # Section 1: Tests for Instantiation
    def test_instance_creation(self):
        """Test creating a new Place instance without arguments."""
        self.assertIsInstance(self.place, Place)
        self.assertIn(self.place, storage.all().values())

    def test_unique_id_per_instance(self):
        """Test that each Place instance has a unique id."""
        place2 = Place()
        self.assertNotEqual(self.place.id, place2.id)

    def test_id_is_string(self):
        """Test that id attribute is a string."""
        self.assertIsInstance(self.place.id, str)

    def test_datetime_attributes(self):
        """Test that created_at and updated_at are datetime objects."""
        self.assertIsInstance(self.place.created_at, datetime)
        self.assertIsInstance(self.place.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """Test different created_at times for distinct instances."""
        place2 = Place()
        sleep(0.01)
        place3 = Place()
        self.assertLess(place2.created_at, place3.created_at)

    def test_public_attributes(self):
        """Test that Place class has expected public attributes."""
        self.assertIsInstance(self.place.city_id, str)
        self.assertIsInstance(self.place.user_id, str)
        self.assertIsInstance(self.place.name, str)
        self.assertIsInstance(self.place.description, str)
        self.assertIsInstance(self.place.number_rooms, int)
        self.assertIsInstance(self.place.number_bathrooms, int)
        self.assertIsInstance(self.place.max_guest, int)
        self.assertIsInstance(self.place.price_by_night, int)
        self.assertIsInstance(self.place.latitude, float)
        self.assertIsInstance(self.place.longitude, float)

    def test_additional_attributes(self):
        """Test adding new attributes to an instance dynamically."""
        self.place.amenity_ids = ["toilet", "wifi"]
        self.assertEqual(self.place.amenity_ids, ["toilet", "wifi"])

    # Section 2: Tests for save Method
    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.place.updated_at
        sleep(0.01)
        self.place.save()
        self.assertGreater(self.place.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        self.place.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """Test that save() writes correct data to file.json."""
        self.place.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = f"Place.{self.place.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "YO MAMA's BEACH HOUSE")

    def test_save_with_invalid_argument(self):
        """Test save() with an invalid argument raises a TypeError."""
        with self.assertRaises(TypeError):
            self.place.save(None)

    # Section 3: Tests for to_dict Method
    def test_to_dict_includes_all_attributes(self):
        """Test that to_dict() includes all Place attributes."""
        place_dict = self.place.to_dict()
        self.assertIn("id", place_dict)
        self.assertIn("created_at", place_dict)
        self.assertIn("updated_at", place_dict)
        self.assertIn("city_id", place_dict)
        self.assertEqual(place_dict["city_id"], "1234")

    def test_to_dict_datetime_format(self):
        """Test that to_dict() converts datetime attributes to ISO format."""
        place_dict = self.place.to_dict()
        self.assertIsInstance(place_dict["created_at"], str)
        self.assertIsInstance(place_dict["updated_at"], str)
        self.assertEqual(place_dict["created_at"], self.place.created_at.isoformat())
        self.assertEqual(place_dict["updated_at"], self.place.updated_at.isoformat())

    def test_to_dict_additional_attributes(self):
        """Test that to_dict() includes dynamically added attributes."""
        self.place.amenity_ids = ["toilet", "wifi"]
        place_dict = self.place.to_dict()
        self.assertIn("amenity_ids", place_dict)
        self.assertEqual(place_dict["amenity_ids"], ["toilet", "wifi"])

    def test_to_dict_with_invalid_argument(self):
        """Test that to_dict() with invalid arguments raises TypeError."""
        with self.assertRaises(TypeError):
            self.place.to_dict(None)

    def test_to_dict_output(self):
        """Test that to_dict() output matches expected dictionary."""
        self.place.id = "123456"
        self.place.created_at = datetime(2024, 1, 1, 12, 0, 0)
        self.place.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        expected_dict = {
            "id": "123456",
            "__class__": "Place",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00",
            "city_id": "1234",
            "user_id": "5678",
            "name": "YO MAMA's BEACH HOUSE",
            "description": "A Big house just like Yo mama. It's too expensive for you anyway.",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 150,
            "latitude": 36.7783,
            "longitude": -119.4179
        }
        self.assertEqual(self.place.to_dict(), expected_dict)

if __name__ == "__main__":
    unittest.main()
