import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid

class TestBaseModel(unittest.TestCase):
    def test_id_is_uuid(self):
        """Test if id is a valid UUID string."""
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        # Try to convert id to UUID
        self.assertEqual(uuid.UUID(model.id).version, 4)

    def test_created_at_is_datetime(self):
        """Test if created_at is a datetime object."""
        model = BaseModel()
        self.assertIsInstance(model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """Test if updated_at is a datetime object."""
        model = BaseModel()
        self.assertIsInstance(model.updated_at, datetime)

    def test_str_representation(self):
        """Test the __str__ method for proper format."""
        model = BaseModel()
        self.assertIn("[BaseModel]", str(model))
        self.assertIn("id", str(model))
        self.assertIn("created_at", str(model))

    def test_to_dict(self):
        """Test if to_dict creates correct dictionary format."""
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertIsInstance(model_dict["created_at"], str)
        self.assertIsInstance(model_dict["updated_at"], str)

    def test_save_method(self):
        """Test if save updates updated_at."""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(model.updated_at, old_updated_at)

    def test_init_from_dict(self):
        """Test initialization of BaseModel from a dictionary."""
        my_model = BaseModel()
        model_dict = my_model.to_dict()
        new_model = BaseModel(**model_dict)

        # Check if new_model's attributes match the original's attributes
        self.assertEqual(new_model.id, my_model.id)
        self.assertEqual(new_model.created_at, my_model.created_at)
        self.assertEqual(new_model.updated_at, my_model.updated_at)
        self.assertEqual(new_model.to_dict(), my_model.to_dict())
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)

if __name__ == "__main__":
    unittest.main()
