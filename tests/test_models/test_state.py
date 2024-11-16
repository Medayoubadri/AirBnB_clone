#!/usr/bin/python3

"""
Unit tests for the State class.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.state import State
from models import storage


class TestState(unittest.TestCase):
    """Comprehensive and witty tests for the State class."""

    def setUp(self):
        """Sets up a State instance before each test."""
        self.state = State()
        self.state.name = "California"

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    # Section 1: Tests for Instantiation
    def test_instance_creation(self):
        """Test creating a new State instance without arguments."""
        self.assertIsInstance(self.state, State)
        self.assertIn(self.state, storage.all().values())

    def test_unique_id_per_instance(self):
        """Test that each State instance has a unique id."""
        state2 = State()
        self.assertNotEqual(self.state.id, state2.id)

    def test_id_is_string(self):
        """Test that id attribute is a string."""
        self.assertIsInstance(self.state.id, str)

    def test_datetime_attributes(self):
        """Test that created_at and updated_at are datetime objects."""
        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsInstance(self.state.updated_at, datetime)

    def test_different_created_at_for_multiple_instances(self):
        """
        Test different created_at times for distinct instances.
        Time waits for no one.
        """
        state2 = State()
        sleep(0.01)
        state3 = State()
        self.assertLess(state2.created_at, state3.created_at)

    def test_name_is_string(self):
        """Test that the name attribute in State is a string."""
        self.assertEqual(self.state.name, "California")
        self.assertIsInstance(self.state.name, str)

    # Section 2: Tests for save Method
    def test_save_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.state.updated_at
        sleep(0.01)  # Sleep so updated_at has a chance to update
        self.state.save()
        self.assertGreater(self.state.updated_at, old_updated_at)

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        self.state.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """
        Test that save() writes correct data to file.json.
        California dreaming? Nah, just testing.
        """
        self.state.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        key = f"State.{self.state.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "California")

    def test_save_with_invalid_argument(self):
        """
        Test save() with an invalid argument raises a TypeError.
        No freeloaders allowed.
        """
        with self.assertRaises(TypeError):
            self.state.save(None)

    # Section 3: Tests for to_dict Method
    def test_to_dict_includes_all_attributes(self):
        """Test that to_dict() includes all State attributes."""
        state_dict = self.state.to_dict()
        self.assertIn("id", state_dict)
        self.assertIn("created_at", state_dict)
        self.assertIn("updated_at", state_dict)
        self.assertIn("name", state_dict)
        self.assertEqual(state_dict["name"], "California")

    def test_to_dict_datetime_format(self):
        """Test that to_dict() converts datetime attributes to ISO format."""
        state_dict = self.state.to_dict()
        self.assertIsInstance(state_dict["created_at"], str)
        self.assertIsInstance(state_dict["updated_at"], str)
        self.assertEqual(
            state_dict["created_at"], self.state.created_at.isoformat()
            )
        self.assertEqual(
            state_dict["updated_at"], self.state.updated_at.isoformat()
            )

    def test_to_dict_additional_attributes(self):
        """
        Test that to_dict() includes dynamically added attributes.
        California knows how to party.
        """
        self.state.governor = "The Terminator"
        state_dict = self.state.to_dict()
        self.assertIn("governor", state_dict)
        self.assertEqual(state_dict["governor"], "The Terminator")

    def test_to_dict_with_invalid_argument(self):
        """
        Test that to_dict() with invalid arguments raises TypeError.
        No freeloaders allowed in this method either.
        """
        with self.assertRaises(TypeError):
            self.state.to_dict(None)

    def test_to_dict_output(self):
        """
        Test to_dict() output matches expected dictionary.
        Only the Golden State vibes.
        """
        self.state.id = "123456"
        self.state.created_at = datetime(2024, 1, 1, 12, 0, 0)
        self.state.updated_at = datetime(2024, 1, 1, 12, 0, 0)
        expected_dict = {
            "id": "123456",
            "__class__": "State",
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00",
            "name": "California",
            "governor": "Arnold Schwarzenegger (in our dreams)"
        }
        self.state.governor = "Arnold Schwarzenegger (in our dreams)"
        self.assertEqual(self.state.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
