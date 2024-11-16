#!/usr/bin/python3

"""
Unit tests for the Amenity class.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.amenity import Amenity
from models import storage


class TestAmenity(unittest.TestCase):
    """Thorough and slightly amusing tests for the Amenity class."""

    def setUp(self):
        """Sets up an Amenity instance before each test."""
        self.amenity = Amenity()
        self.amenity.name = "Infinity Pool"

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_instance_creation(self):
        """Test creating a new Amenity instance without arguments."""
        self.assertIsInstance(self.amenity, Amenity)
        self.assertIn(self.amenity, storage.all().values())

    def test_unique_id_per_instance(self):
        """
        Test that each Amenity instance has a unique id.
        Only the chosen can have one.
        """
        amenity2 = Amenity()
        self.assertNotEqual(self.amenity.id, amenity2.id)

    def test_id_is_string(self):
        """Test that id attribute is a string."""
        self.assertIsInstance(self.amenity.id, str)

    def test_datetime_attributes(self):
        """
        Test that created_at and updated_at are datetime objects.
        Time flows even by the pool.
        """
        self.assertIsInstance(self.amenity.created_at, datetime)
        self.assertIsInstance(self.amenity.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """
        Test different created_at times for distinct instances.
        Like every amenity, each is unique.
        """
        amenity2 = Amenity()
        sleep(0.01)
        amenity3 = Amenity()
        self.assertLess(amenity2.created_at, amenity3.created_at)

    def test_name_is_string(self):
        """
        Test that the name attribute in Amenity is a string.
        Nothing less than fancy allowed.
        """
        self.assertEqual(self.amenity.name, "Infinity Pool")
        self.assertIsInstance(self.amenity.name, str)

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.amenity.updated_at
        sleep(0.01)
        self.amenity.save()
        self.assertGreater(self.amenity.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        self.amenity.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """
        Test that save() writes correct data to file.json.
        Infinity Pool better be in there.
        """
        self.amenity.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = f"Amenity.{self.amenity.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "Infinity Pool")

    def test_save_with_invalid_argument(self):
        """
        Test save() with an invalid argument raises a TypeError.
        Sorry, reservations only.
        """
        with self.assertRaises(TypeError):
            self.amenity.save(None)

    def test_to_dict_includes_all_attributes(self):
        """Test that to_dict() includes all Amenity attributes."""
        amenity_dict = self.amenity.to_dict()
        self.assertIn("id", amenity_dict)
        self.assertIn("created_at", amenity_dict)
        self.assertIn("updated_at", amenity_dict)
        self.assertIn("name", amenity_dict)
        self.assertEqual(amenity_dict["name"], "Infinity Pool")

    def test_to_dict_datetime_format(self):
        """Test that to_dict() converts datetime attributes to ISO format."""
        amenity_dict = self.amenity.to_dict()
        self.assertIsInstance(amenity_dict["created_at"], str)
        self.assertIsInstance(amenity_dict["updated_at"], str)
        self.assertEqual(
            amenity_dict["created_at"], self.amenity.created_at.isoformat())
        self.assertEqual(
            amenity_dict["updated_at"], self.amenity.updated_at.isoformat())

    def test_to_dict_additional_attributes(self):
        """
        Test that to_dict() includes dynamically added attributes.
        Everything here is extra, darling.
        """
        self.amenity.access = "VIP Only"
        amenity_dict = self.amenity.to_dict()
        self.assertIn("access", amenity_dict)
        self.assertEqual(amenity_dict["access"], "VIP Only")

    def test_to_dict_with_invalid_argument(self):
        """
        Test that to_dict() with invalid arguments raises TypeError.
        VIP access not granted.
        """
        with self.assertRaises(TypeError):
            self.amenity.to_dict(None)

    def test_to_dict_output(self):
        """
        Test that to_dict() output matches expected dictionary.
        Luxury never looked this good.
        """
        self.amenity.id = "123456"
        self.amenity.created_at = datetime(2024, 1, 1, 12, 0, 0)
        self.amenity.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        expected_dict = {
            "id": "123456",
            "__class__": "Amenity",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00",
            "name": "Infinity Pool",
            "access": "VIP Only"
        }
        self.amenity.access = "VIP Only"
        self.assertEqual(self.amenity.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
