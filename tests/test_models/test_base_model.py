#!/usr/bin/python3
'''
Comprehensive tests for the BaseModel class.
'''

import unittest
import os
import models
from datetime import datetime
from time import sleep
from models.base_model import BaseModel
import uuid
import json


class TestBaseModelInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base_model1 = BaseModel()
        base_model2 = BaseModel()
        self.assertNotEqual(base_model1.id, base_model2.id)

    def test_two_models_different_created_at(self):
        base_model1 = BaseModel()
        sleep(0.05)
        base_model2 = BaseModel()
        self.assertLess(base_model1.created_at, base_model2.created_at)

    def test_two_models_different_updated_at(self):
        base_model1 = BaseModel()
        sleep(0.05)
        base_model2 = BaseModel()
        self.assertLess(base_model1.updated_at, base_model2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = dt
        base_modelstr = base_model.__str__()
        self.assertIn("[BaseModel] (123456)", base_modelstr)
        self.assertIn("'id': '123456'", base_modelstr)
        self.assertIn("'created_at': " + dt_repr, base_modelstr)
        self.assertIn("'updated_at': " + dt_repr, base_modelstr)

    def test_args_unused(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        base_model = BaseModel(id="6789", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base_model.id, "6789")
        self.assertEqual(base_model.created_at, dt)
        self.assertEqual(base_model.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        base_model = BaseModel("12", id="6789", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(base_model.id, "6789")
        self.assertEqual(base_model.created_at, dt)
        self.assertEqual(base_model.updated_at, dt)

    def test_id_is_uuid4(self):
        """Test that the id follows uuid4 format."""
        base_model = BaseModel()
        uuid_obj = uuid.UUID(base_model.id)
        self.assertEqual(uuid_obj.version, 4)

    def test_invalid_datetime_in_kwargs(self):
        """Test that BaseModel handles invalid datetime strings in kwargs."""
        invalid_datetime = "invalid-datetime"
        model_dict = BaseModel().to_dict()
        model_dict["created_at"] = invalid_datetime
        model_dict["updated_at"] = invalid_datetime
        new_model = BaseModel(**model_dict)
        self.assertNotEqual(new_model.created_at, invalid_datetime)
        self.assertNotEqual(new_model.updated_at, invalid_datetime)
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)


class TestBaseModelSave(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        self.assertLess(first_updated_at, base_model.updated_at)

    def test_two_saves(self):
        base_model = BaseModel()
        sleep(0.05)
        first_updated_at = base_model.updated_at
        base_model.save()
        second_updated_at = base_model.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_model.save()
        self.assertLess(second_updated_at, base_model.updated_at)

    def test_save_with_arg(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.save(None)

    def test_save_updates_file(self):
        base_model = BaseModel()
        base_model.save()
        base_modelid = "BaseModel." + base_model.id
        with open("file.json", "r") as f:
            self.assertIn(base_modelid, f.read())

    def test_save_creates_file(self):
        """Test if save method creates the file.json file."""
        base_model = BaseModel()
        base_model.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """Test if save method properly writes JSON content to file."""
        base_model = BaseModel()
        base_model.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertIn(f"BaseModel.{base_model.id}", content)

    def test_save_existing_file(self):
        """Test that save method updates an existing file.json file."""
        base_model = BaseModel()
        base_model.save()
        old_updated_at = base_model.updated_at
        base_model.name = "Updated Name"
        base_model.save()
        with open("file.json", "r") as f:
            content = json.load(f)
        self.assertIn(f"BaseModel.{base_model.id}", content)
        self.assertEqual(content[f"BaseModel.{base_model.id}"]["name"], "Updated Name")
        self.assertGreater(base_model.updated_at, old_updated_at)


class TestBaseModelToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        base_model = BaseModel()
        self.assertTrue(dict, type(base_model.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        base_model = BaseModel()
        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base_model = BaseModel()
        base_model.name = "Jhon"
        base_model.my_age = 98
        self.assertIn("name", base_model.to_dict())
        self.assertIn("my_age", base_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        self.assertEqual(str, type(base_model_dict["created_at"]))
        self.assertEqual(str, type(base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(base_model.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        base_model = BaseModel()
        self.assertNotEqual(base_model.to_dict(), base_model.__dict__)

    def test_to_dict_with_arg(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.to_dict(None)

    def test_to_dict_contains_all_keys(self):
        """
        Test that to_dict contains all keys in the __dict__ of the instance.
        """
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        for key in base_model.__dict__:
            self.assertIn(key, base_model_dict)

    def test_to_dict_with_additional_attributes(self):
        """Test that to_dict method includes additional attributes."""
        base_model = BaseModel()
        base_model.name = "Jhon Wick"
        base_model.age = 52
        model_dict = base_model.to_dict()
        self.assertIn("name", model_dict)
        self.assertIn("age", model_dict)
        self.assertEqual(model_dict["name"], "Jhon Wick")
        self.assertEqual(model_dict["age"], 52)


if __name__ == '__main__':
    unittest.main()
