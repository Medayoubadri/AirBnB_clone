#!/usr/bin/python3

'''
Comprehensive tests for the BaseModel class.
'''

import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid
import os
import models
import json


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""
    def setUp(self):
        """Sets up a new instance of BaseModel before each test."""
        self.model = BaseModel()

    def tearDown(self):
        """Cleans up created instances and files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_id_is_unique(self):
        """Test that each instance has a unique id."""
        model2 = BaseModel()
        self.assertNotEqual(self.model.id, model2.id)
        self.assertIsInstance(self.model.id, str)

    def test_id_is_uuid4(self):
        """Test that the id follows uuid4 format."""
        uuid_obj = uuid.UUID(self.model.id)
        self.assertEqual(uuid_obj.version, 4)

    def test_created_at_is_datetime(self):
        """Test that created_at is initialized and is a datetime object."""
        self.assertIsInstance(self.model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test that updated_at is initialized and is a datetime object."""
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str_method(self):
        """Test the __str__ method outputs the correct format."""
        expected_str = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected_str)

    def test_save_method_updates_updated_at(self):
        """Test that save() updates the updated_at attribute."""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)
        self.assertGreater(self.model.updated_at, old_updated_at)

    def test_to_dict_method(self):
        """Test that to_dict() creates a dictionary with correct attributes."""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], self.model.id)
        self.assertEqual(
            model_dict["created_at"], self.model.created_at.isoformat())
        self.assertEqual(
            model_dict["updated_at"], self.model.updated_at.isoformat())

    def test_to_dict_contains_all_keys(self):
        """
        Test that to_dict contains all keys in the __dict__ of the instance.
        """
        model_dict = self.model.to_dict()
        for key in self.model.__dict__:
            self.assertIn(key, model_dict)

    def test_kwargs_initialization(self):
        """
        Test that an instance can be created from a dictionary of attributes.
        """
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.id, self.model.id)
        self.assertEqual(new_model.created_at, self.model.created_at)
        self.assertEqual(new_model.updated_at, self.model.updated_at)
        self.assertEqual(new_model.__str__(), self.model.__str__())

    def test_save_creates_file(self):
        """Test if save method creates the file.json file."""
        self.model.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """Test if save method properly writes JSON content to file."""
        self.model.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertIn(f"BaseModel.{self.model.id}", content)

    def test_reload_retains_saved_data(self):
        """Test that reload properly restores saved data from file.json."""
        self.model.save()
        models.storage.reload()
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, models.storage.all())

    def test_to_dict_has_correct_types(self):
        """
        Test that to_dict method outputs ISO format strings for datetimes.
        """
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)
        self.assertEqual(model_dict["__class__"], "BaseModel")

    def test_save_and_reload_consistency(self):
        """Test that saving and reloading retains the same attribute values."""
        self.model.name = "Test Name"
        self.model.save()
        models.storage.reload()
        reloaded_instance = models.storage.all().get(
            f"BaseModel.{self.model.id}"
            )
        self.assertEqual(reloaded_instance.name, "Test Name")


if __name__ == '__main__':
    unittest.main()
