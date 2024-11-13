#!/usr/bin/python3

"""
Unit tests for the User class.
"""

import unittest
from models.user import User
from datetime import datetime
from models.base_model import BaseModel

class TestUser(unittest.TestCase):
    """Tests for the User class."""

    def setUp(self):
        """Sets up a User instance before each test."""
        self.user = User()
        self.user.email = "user@example.com"
        self.user.password = "password123"
        self.user.first_name = "John"
        self.user.last_name = "Doe"

    def test_inheritance(self):
        """Test that User class inherits from BaseModel."""
        self.assertIsInstance(self.user, BaseModel)

    def test_attributes(self):
        """Test that User has the correct attributes."""
        self.assertEqual(self.user.email, "user@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

    def test_str_method(self):
        """Test the __str__ method for correct output format."""
        expected_output = f"[User] ({self.user.id}) {self.user.__dict__}"
        self.assertEqual(str(self.user), expected_output)

    def test_to_dict_method(self):
        """Test to_dict method includes User attributes."""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertEqual(user_dict["email"], "user@example.com")
        self.assertEqual(user_dict["first_name"], "John")
        self.assertEqual(user_dict["last_name"], "Doe")

    def test_updated_at_on_save(self):
        """Test that save method updates updated_at attribute."""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(self.user.updated_at, old_updated_at)
        self.assertGreater(self.user.updated_at, old_updated_at)

    def test_to_dict_output_format(self):
        """Test that to_dict provides correctly formatted ISO datetimes."""
        user_dict = self.user.to_dict()
        self.assertIsInstance(user_dict["created_at"], str)
        self.assertIsInstance(user_dict["updated_at"], str)
        # Ensure dates are in ISO format
        self.assertEqual(user_dict["created_at"], self.user.created_at.isoformat())
        self.assertEqual(user_dict["updated_at"], self.user.updated_at.isoformat())

if __name__ == "__main__":
    unittest.main()
