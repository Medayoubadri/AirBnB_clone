#!/usr/bin/python3

'''
Unit tests for the FileStorage class.
'''

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorageInstantiation(unittest.TestCase):
    """Tests for instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        """Test FileStorage instantiation without arguments."""
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        """Test FileStorage instantiation with argument."""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initialize(self):
        """Test that storage is an instance of FileStorage."""
        from models import storage
        self.assertEqual(type(storage), FileStorage)


class TestFileStorageAll(unittest.TestCase):
    """Tests for all() method of the FileStorage class."""

    @classmethod
    def setUp(self):
        """Set up for the tests."""
        self.storage = FileStorage()

    def test_all_returns_dict(self):
        """Test that all() returns the __objects dictionary."""
        self.assertEqual(dict, type(self.storage.all()))

    def test_all_returns_with_arg(self):
        """Test all() with arguments."""
        with self.assertRaises(TypeError):
            self.storage.all(None)


class TestFileStorageNew(unittest.TestCase):
    """Tests for new() method of the FileStorage class."""

    @classmethod
    def setUp(self):
        """Set up for the tests."""
        self.storage = FileStorage()

    def test_new_adds_instance(self):
        """Test that new() adds an instance to __objects."""
        base_model = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        self.storage.new(base_model)
        self.storage.new(user)
        self.storage.new(state)
        self.storage.new(place)
        self.storage.new(city)
        self.storage.new(amenity)
        self.storage.new(review)
        self.assertIn("BaseModel." + base_model.id, self.storage.all().keys())
        self.assertIn(base_model, self.storage.all().values())
        self.assertIn("User." + user.id, self.storage.all().keys())
        self.assertIn(user, self.storage.all().values())
        self.assertIn("State." + state.id, self.storage.all().keys())
        self.assertIn(state, self.storage.all().values())
        self.assertIn("Place." + place.id, self.storage.all().keys())
        self.assertIn(place, self.storage.all().values())
        self.assertIn("City." + city.id, self.storage.all().keys())
        self.assertIn(city, self.storage.all().values())
        self.assertIn("Amenity." + amenity.id, self.storage.all().keys())
        self.assertIn(amenity, self.storage.all().values())
        self.assertIn("Review." + review.id, self.storage.all().keys())
        self.assertIn(review, self.storage.all().values())

    def test_new_with_args(self):
        """Test new() with arguments."""
        with self.assertRaises(TypeError):
            self.storage.new(BaseModel(), 1)


class TestFileStorageSave(unittest.TestCase):
    """Tests for save() method of the FileStorage class."""

    @classmethod
    def setUp(self):
        """Set up for the tests."""
        self.storage = FileStorage()

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_content(self):
        """Test that save writes correct data to file.json."""
        base_model = BaseModel()
        base_model.name = "Jhon Wick"
        base_model.age = 52
        self.storage.new(base_model)
        self.storage.save()
        with open("file.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "Jhon Wick")
        self.assertEqual(data[key]["age"], 52)

    def test_save_with_arg(self):
        """Test save() with argument."""
        with self.assertRaises(TypeError):
            self.storage.save(None)


class TestFileStorageReload(unittest.TestCase):
    """Tests for reload() method of the FileStorage class."""

    @classmethod
    def setUp(self):
        """Set up for the tests."""
        self.storage = FileStorage()

    def tearDown(self):
        """Clean up any created files after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_reload(self):
        """Test that reload correctly loads objects from file.json."""
        base_model = BaseModel()
        base_model.name = "Jhon Wick"
        base_model.age = 52
        self.storage.new(base_model)
        self.storage.save()
        self.storage.reload()
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        reloaded_model = self.storage.all()[key]
        self.assertEqual(reloaded_model.id, base_model.id)
        self.assertEqual(reloaded_model.name, "Jhon Wick")
        self.assertEqual(reloaded_model.age, 52)

    def test_reload_with_no_file(self):
        """Test that reload does not throw an error if file.json is missing."""
        if os.path.exists("file.json"):
            os.remove("file.json")
        try:
            self.storage.reload()
        except Exception as e:
            self.fail(f"reload() raised {type(e)} unexpectedly!")

    def test_reload_invalid_json(self):
        """Test that reload handles an invalid JSON file gracefully."""
        with open("file.json", "w", encoding="utf-8") as file:
            file.write("{ invalid json }")
        try:
            self.storage.reload()
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

    def test_reload_with_arg(self):
        """Test reload() with argument."""
        with self.assertRaises(TypeError):
            self.storage.reload(None)


if __name__ == '__main__':
    unittest.main()
