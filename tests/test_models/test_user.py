#!/usr/bin/python3
"""
Unit tests for the User class with a structured and comprehensive approach.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.user import User
from models import storage


class TestUserInstantiation(unittest.TestCase):
    """Tests for instantiation of the User class."""

    def setUp(self):
        """Set up a User instance for testing."""
        self.user = User()
        self.user.email = "agent@mi6.co.uk"
        self.user.password = "shaken_not_stirred"
        self.user.first_name = "James"
        self.user.last_name = "Bond"

    def tearDown(self):
        """Clean up any created files."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_instance_creation(self):
        """Test creating a new User instance without arguments."""
        self.assertIsInstance(self.user, User)
        self.assertIn(self.user, storage.all().values())

    def test_unique_id_per_instance(self):
        """Test that each User instance has a unique id."""
        user2 = User()
        self.assertNotEqual(self.user.id, user2.id)

    def test_id_is_string(self):
        """Test that id attribute is a string."""
        self.assertIsInstance(self.user.id, str)

    def test_datetime_attributes(self):
        """Test that created_at and updated_at are datetime objects."""
        self.assertIsInstance(self.user.created_at, datetime)
        self.assertIsInstance(self.user.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """Test different created_at times for distinct instances."""
        user2 = User()
        sleep(0.01)
        user3 = User()
        self.assertLess(user2.created_at, user3.created_at)

    def test_public_attributes(self):
        """Test that User class has expected public attributes."""
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)

    def test_additional_attributes(self):
        """Test adding new attributes to an instance dynamically."""
        self.user.middle_name = "Danger"
        self.user.age = 42
        self.assertEqual(self.user.middle_name, "Danger")
        self.assertEqual(self.user.age, 42)


class TestUserSave(unittest.TestCase):
    """Tests for the save method of the User class."""

    def setUp(self):
        """Set up a User instance for testing."""
        self.user = User()
        self.user.email = "agent@mi6.co.uk"
        self.user.password = "shaken_not_stirred"

    def tearDown(self):
        """Clean up any created files."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.user.updated_at
        sleep(0.01)
        self.user.save()
        self.assertGreater(self.user.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        self.user.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """Test that save() writes correct data to file.json."""
        self.user.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = f"User.{self.user.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["email"], "agent@mi6.co.uk")

    def test_save_with_invalid_argument(self):
        """Test save() with an invalid argument raises a TypeError."""
        with self.assertRaises(TypeError):
            self.user.save(None)


class TestUserToDict(unittest.TestCase):
    """Tests for the to_dict method of the User class."""

    def setUp(self):
        """Set up a User instance for testing."""
        self.user = User()
        self.user.email = "agent@mi6.co.uk"
        self.user.password = "shaken_not_stirred"

    def test_to_dict_includes_all_attributes(self):
        """Test that to_dict() includes all User attributes."""
        user_dict = self.user.to_dict()
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
        self.assertIn("email", user_dict)
        self.assertEqual(user_dict["email"], "agent@mi6.co.uk")

    def test_to_dict_datetime_format(self):
        """Test that to_dict() converts datetime attributes to ISO format."""
        user_dict = self.user.to_dict()
        self.assertEqual(
            user_dict["created_at"], self.user.created_at.isoformat())
        self.assertEqual(
            user_dict["updated_at"], self.user.updated_at.isoformat())

    def test_to_dict_additional_attributes(self):
        """Test that to_dict() includes dynamically added attributes."""
        self.user.middle_name = "Danger"
        self.user.age = 42
        user_dict = self.user.to_dict()
        self.assertIn("middle_name", user_dict)
        self.assertIn("age", user_dict)
        self.assertEqual(user_dict["middle_name"], "Danger")
        self.assertEqual(user_dict["age"], 42)

    def test_to_dict_with_invalid_argument(self):
        """Test that to_dict() with invalid arguments raises TypeError."""
        with self.assertRaises(TypeError):
            self.user.to_dict(None)

    def test_to_dict_output(self):
        """Test that to_dict() output matches expected dictionary."""
        self.user.id = "007"
        self.user.created_at = datetime(2024, 1, 1, 12, 0, 0)
        self.user.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        expected_dict = {
            "id": "007",
            "__class__": "User",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00",
            "email": "agent@mi6.co.uk",
            "password": "shaken_not_stirred"
        }
        self.assertEqual(self.user.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
