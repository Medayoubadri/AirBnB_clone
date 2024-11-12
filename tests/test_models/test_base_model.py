import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid
import os
import models

class TestBaseModel(unittest.TestCase):
    
    def setUp(self):
        """Sets up a new instance of BaseModel before each test."""
        self.model = BaseModel()
    
    def test_id_is_unique(self):
        """Test that id is a unique string for each instance."""
        model2 = BaseModel()
        self.assertNotEqual(self.model.id, model2.id)
        self.assertIsInstance(self.model.id, str)
    
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
        self.assertIsInstance(self.model.updated_at, datetime)
        self.assertGreater(self.model.updated_at, old_updated_at)
    
    def test_to_dict_method(self):
        """Test that to_dict() method creates a dictionary with correct attributes."""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], self.model.id)
        self.assertEqual(model_dict["created_at"], self.model.created_at.isoformat())
        self.assertEqual(model_dict["updated_at"], self.model.updated_at.isoformat())
    
    def test_kwargs_initialization(self):
        """Test that an instance can be created from a dictionary of attributes."""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(new_model.id, self.model.id)
        self.assertEqual(new_model.created_at, self.model.created_at)
        self.assertEqual(new_model.updated_at, self.model.updated_at)
        self.assertEqual(new_model.__str__(), self.model.__str__())


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        """Initial setup for tests"""
        self.model = BaseModel()
        self.model.save()
    
    def tearDown(self):
        """Cleans up any test files created"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_all_returns_dict(self):
        """Test if all returns a dictionary"""
        self.assertIsInstance(models.storage.all(), dict)

    def test_new_adds_object(self):
        """Test if new method adds an object to __objects"""
        key = f"BaseModel.{self.model.id}"
        self.assertIn(key, models.storage.all())

    def test_save_creates_file(self):
        """Test if save method creates the file.json file"""
        models.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_reload(self):
        """Test if reload loads objects correctly"""
        key = f"BaseModel.{self.model.id}"
        models.storage.save()
        models.storage.reload()
        self.assertIn(key, models.storage.all())

if __name__ == '__main__':
    unittest.main()
