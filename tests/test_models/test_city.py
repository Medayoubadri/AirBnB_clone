#!/usr/bin/python3

"""
Unit tests for the City class.
"""

import unittest
from models.city import City
from datetime import datetime
from models.base_model import BaseModel

class TestCity(unittest.TestCase):
    """Tests for the City class."""

    def setUp(self):
        """Sets up a City instance before each test."""
        self.city = City()
        self.city.name = "New York"
        self.city.state_id = "1234"

    def test_inheritance(self):
        """Test that City class inherits from BaseModel."""
        self.assertIsInstance(self.city, BaseModel)

    def test_attributes(self):
        """Test that City has the correct attributes."""
        self.assertEqual(self.city.name, "New York")
        self.assertEqual(self.city.state_id, "1234")

    def test_str_method(self):
        """Test the __str__ method for correct output format."""
        expected_output = f"[City] ({self.city.id}) {self.city.__dict__}"
        self.assertEqual(str(self.city), expected_output)

    def test_to_dict_method(self):
        """Test to_dict method includes City attributes."""
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")
        self.assertEqual(city_dict["name"], "New York")
        self.assertEqual(city_dict["state_id"], "1234")

if __name__ == "__main__":
    unittest.main()
