#!/usr/bin/python3

'''
Unit tests for the FileStorage class.
'''

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
import os
import json
from models import storage


class TestFileStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up for all tests"""
        cls.storage = FileStorage()
        cls.model = BaseModel()
        cls.model.name = "Test Model"
        cls.model.number = 42
        cls.storage.new(cls.model)

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        """Test that all returns the __objects dictionary."""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_adds_instance(self):
        """Test that new() adds an instance to __objects."""
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, self.storage.all())

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_content(self):
        """Test that save writes correct data to file.json."""
        self.storage.save()
        with open("file.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "Test Model")
        self.assertEqual(data[key]["number"], 42)

    def test_reload(self):
        """Test that reload correctly loads objects from file.json."""
        self.storage.save()
        self.storage.reload()
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, self.storage.all())
        reloaded_model = self.storage.all()[key]
        self.assertEqual(reloaded_model.id, self.model.id)
        self.assertEqual(reloaded_model.name, "Test Model")
        self.assertEqual(reloaded_model.number, 42)

    def test_reload_with_no_file(self):
        """
        Test that reload does not throw an error if file.json is missing.
        """
        if os.path.exists("file.json"):
            os.remove("file.json")
        try:
            self.storage.reload()  # Should not raise an exception
        except Exception as e:
            self.fail(f"reload() raised {type(e)} unexpectedly!")

    def test_reload_invalid_json(self):
        """Test that reload handles an invalid JSON file gracefully."""
        with open("file.json", "w", encoding="utf-8") as file:
            file.write("{ invalid json }")
        try:
            self.storage.reload()  # Should not raise an exception
        except Exception as e:
            self.fail(f"reload() raised {type(e)} unexpectedly!")

    def test_reload_different_class(self):
        """Test that reload can handle different classes correctly."""
        user = User()
        user.name = "John Doe"
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        user_key = f"User.{user.id}"
        self.assertIn(user_key, self.storage.all())
        reloaded_user = self.storage.all()[user_key]
        self.assertEqual(reloaded_user.name, "John Doe")


if __name__ == '__main__':
    unittest.main()
