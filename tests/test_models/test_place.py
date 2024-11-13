#!/usr/bin/python3

"""
Unit tests for the Place class.
"""

import unittest
from models.place import Place
from models.base_model import BaseModel

class TestPlace(unittest.TestCase):
    """Tests for the Place class."""

    def setUp(self):
        """Sets up a Place instance before each test."""
        self.place = Place()
        self.place.city_id = "1234"
        self.place.user_id = "5678"
        self.place.name = "Beach House"
        self.place.description = "A beautiful beach house."
        self.place.number_rooms = 3
        self.place.number_bathrooms = 2
        self.place.max_guest = 6
        self.place.price_by_night = 150

    def test_inheritance(self):
        """Test that Place class inherits from BaseModel."""
        self.assertIsInstance(self.place, BaseModel)

    def test_attributes(self):
        """Test that Place has the correct attributes."""
        self.assertEqual(self.place.city_id, "1234")
        self.assertEqual(self.place.user_id, "5678")
        self.assertEqual(self.place.name, "Beach House")
        self.assertEqual(self.place.description, "A beautiful beach house.")
        self.assertEqual(self.place.number_rooms, 3)
        self.assertEqual(self.place.number_bathrooms, 2)
        self.assertEqual(self.place.max_guest, 6)
        self.assertEqual(self.place.price_by_night, 150)

    def test_str_method(self):
        """Test the __str__ method for correct output format."""
        expected_output = f"[Place] ({self.place.id}) {self.place.__dict__}"
        self.assertEqual(str(self.place), expected_output)

    def test_to_dict_method(self):
        """Test to_dict method includes Place attributes."""
        place_dict = self.place.to_dict()
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertEqual(place_dict["name"], "Beach House")

if __name__ == "__main__":
    unittest.main()
