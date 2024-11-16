#!/usr/bin/python3

"""
Unit tests for the City class.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.city import City
from models import storage


class TestCity(unittest.TestCase):
    """Comprehensive tests for the City class."""

    def setUp(self):
        """Sets up a City instance before each test."""
        self.city = City()
        self.city.name = "Gotham"
        self.city.state_id = "nyc-001"

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    # Section 1: Tests for Instantiation
    def test_instance_creation(self):
        """Test creating a new City instance without arguments."""
        self.assertIsInstance(self.city, City)
        self.assertIn(self.city, storage.all().values())

    def test_unique_id_per_instance(self):
        """Test that each City instance has a unique id."""
        city2 = City()
        self.assertNotEqual(self.city.id, city2.id)

    def test_id_is_string(self):
        """Test that id attribute is a string."""
        self.assertIsInstance(self.city.id, str)

    def test_datetime_attributes(self):
        """Test that created_at and updated_at are datetime objects."""
        self.assertIsInstance(self.city.created_at, datetime)
        self.assertIsInstance(self.city.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """
        Test different created_at times for distinct instances.
        Not even time can make Gotham safer.
        """
        city2 = City()
        sleep(0.01)
        city3 = City()
        self.assertLess(city2.created_at, city3.created_at)

    def test_public_attributes(self):
        """Test that City class has expected public attributes."""
        self.assertIsInstance(self.city.name, str)
        self.assertEqual(self.city.name, "Gotham")
        self.assertIsInstance(self.city.state_id, str)
        self.assertEqual(self.city.state_id, "nyc-001")

    def test_additional_attributes(self):
        """
        Test adding new attributes to a City instance.
        Gotham could use more heroes.
        """
        self.city.mayor = "Bruce Wayne"
        self.assertEqual(self.city.mayor, "Bruce Wayne")

    # Section 2: Tests for save Method
    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.city.updated_at
        sleep(0.01)
        self.city.save()
        self.assertGreater(self.city.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        self.city.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """
        Test that save() writes correct data to file.json.
        Gotham needs order, and so does this test.
        """
        self.city.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = f"City.{self.city.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "Gotham")

    def test_save_with_invalid_argument(self):
        """
        Test save() with an invalid argument raises a TypeError.
        Only vigilantes, no free riders.
        """
        with self.assertRaises(TypeError):
            self.city.save(None)

    # Section 3: Tests for to_dict Method
    def test_to_dict_includes_all_attributes(self):
        """Test that to_dict() includes all City attributes."""
        city_dict = self.city.to_dict()
        self.assertIn("id", city_dict)
        self.assertIn("created_at", city_dict)
        self.assertIn("updated_at", city_dict)
        self.assertIn("name", city_dict)
        self.assertIn("state_id", city_dict)
        self.assertEqual(city_dict["name"], "Gotham")

    def test_to_dict_datetime_format(self):
        """Test that to_dict() converts datetime attributes to ISO format."""
        city_dict = self.city.to_dict()
        self.assertIsInstance(city_dict["created_at"], str)
        self.assertIsInstance(city_dict["updated_at"], str)
        self.assertEqual(
            city_dict["created_at"], self.city.created_at.isoformat())
        self.assertEqual(
            city_dict["updated_at"], self.city.updated_at.isoformat())

    def test_to_dict_additional_attributes(self):
        """
        Test that to_dict() includes dynamically added attributes.
        Gotham’s secrets don’t stay hidden.
        """
        self.city.hero = "Batman"
        city_dict = self.city.to_dict()
        self.assertIn("hero", city_dict)
        self.assertEqual(city_dict["hero"], "Batman")

    def test_to_dict_with_invalid_argument(self):
        """
        Test that to_dict() with invalid arguments raises TypeError.
        Even Gotham has rules.
        """
        with self.assertRaises(TypeError):
            self.city.to_dict(None)

    def test_to_dict_output(self):
        """
        Test that to_dict() output matches expected dictionary.
        The city, just as Batman left it.
        """
        self.city.id = "123456"
        self.city.created_at = datetime(2024, 1, 1, 12, 0, 0)
        self.city.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        expected_dict = {
            "id": "123456",
            "__class__": "City",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00",
            "name": "Gotham",
            "state_id": "nyc-001",
            "mayor": "Bruce Wayne"
        }
        self.city.mayor = "Bruce Wayne"
        self.assertEqual(self.city.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
