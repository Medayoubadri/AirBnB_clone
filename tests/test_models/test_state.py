#!/usr/bin/python3

"""
Unit tests for the State class.
"""

import unittest
from models.state import State
from models.base_model import BaseModel

class TestState(unittest.TestCase):
    """Tests for the State class."""

    def setUp(self):
        """Sets up a State instance before each test."""
        self.state = State()
        self.state.name = "California"

    def test_inheritance(self):
        """Test that State class inherits from BaseModel."""
        self.assertIsInstance(self.state, BaseModel)

    def test_attributes(self):
        """Test that State has the correct attributes."""
        self.assertEqual(self.state.name, "California")

    def test_str_method(self):
        """Test the __str__ method for correct output format."""
        expected_output = f"[State] ({self.state.id}) {self.state.__dict__}"
        self.assertEqual(str(self.state), expected_output)

    def test_to_dict_method(self):
        """Test to_dict method includes State attributes."""
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertEqual(state_dict["name"], "California")

if __name__ == "__main__":
    unittest.main()
