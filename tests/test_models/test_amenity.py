#!/usr/bin/python3

"""
Unit tests for the Amenity class.
"""

import unittest
from models.amenity import Amenity
from models.base_model import BaseModel

class TestAmenity(unittest.TestCase):
    """Tests for the Amenity class."""

    def setUp(self):
        """Sets up an Amenity instance before each test."""
        self.amenity = Amenity()
        self.amenity.name = "Pool"

    def test_inheritance(self):
        """Test that Amenity class inherits from BaseModel."""
        self.assertIsInstance(self.amenity, BaseModel)

    def test_attributes(self):
        """Test that Amenity has the correct attributes."""
        self.assertEqual(self.amenity.name, "Pool")

    def test_str_method(self):
        """Test the __str__ method for correct output format."""
        expected_output = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str(self.amenity), expected_output)

    def test_to_dict_method(self):
        """Test to_dict method includes Amenity attributes."""
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertEqual(amenity_dict["name"], "Pool")

if __name__ == "__main__":
    unittest.main()
