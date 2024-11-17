#!/usr/bin/python3

"""
Unit tests for the Amenity class.
"""

import unittest
import os
import json
from time import sleep
from datetime import datetime
from models.amenity import Amenity
from models import storage


class TestAmenityCreation(unittest.TestCase):
    """Unittests for testing creation of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "temp.json")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp.json", "file.json")
        except IOError:
            pass

    def test_amenity_instantiation(self):
        """Test instantiation of Amenity class."""
        self.assertEqual(Amenity, type(Amenity()))

    def test_amenity_in_storage(self):
        """Test if new instance is stored in storage."""
        self.assertIn(Amenity(), storage.all().values())

    def test_id_is_string(self):
        """Test that id is a string."""
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_datetime(self):
        """Test that created_at is a datetime object."""
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_datetime(self):
        """Test that updated_at is a datetime object."""
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_amenity_name_attribute(self):
        """Test that Amenity has name attribute."""
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_unique_amenity_ids(self):
        """Test that two amenities have different ids."""
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_different_created_at(self):
        """Test that two amenities have different created_at times."""
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_different_updated_at(self):
        """Test that two amenities have different updated_at times."""
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_string_representation(self):
        """Test the string representation of Amenity."""
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123abc"
        am.created_at = am.updated_at = dt
        amstr = str(am)
        self.assertIn("[Amenity] (123abc)", amstr)
        self.assertIn("'id': '123abc'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_unused_args(self):
        """Test that unused args don't add attributes."""
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation with kwargs."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="123abc", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "123abc")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that None kwargs raise a TypeError."""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenitySave(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    def setUp(self):
        """Set up for the tests."""
        self.amenity = Amenity()

    def test_single_save(self):
        """Test that save updates updated_at attribute."""
        first_updated_at = self.amenity.updated_at
        sleep(0.05)
        self.amenity.save()
        self.assertLess(first_updated_at, self.amenity.updated_at)

    def test_multiple_saves(self):
        """Test multiple saves update updated_at attribute."""
        first_updated_at = self.amenity.updated_at
        sleep(0.05)
        self.amenity.save()
        second_updated_at = self.amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        self.amenity.save()
        self.assertLess(second_updated_at, self.amenity.updated_at)

    def test_save_with_arg(self):
        """Test save method with arguments."""
        with self.assertRaises(TypeError):
            self.amenity.save(None)

    def test_save_updates_file(self):
        """Test that save method updates file."""
        self.amenity.save()
        amid = "Amenity." + self.amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def setUp(self):
        """Set up for the tests."""
        self.amenity = Amenity()

    def test_to_dict_type(self):
        """Test that to_dict returns a dictionary."""
        self.assertTrue(dict, type(self.amenity.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that to_dict contains the correct keys."""
        am_dict = self.amenity.to_dict()
        self.assertIn("id", am_dict)
        self.assertIn("created_at", am_dict)
        self.assertIn("updated_at", am_dict)
        self.assertIn("__class__", am_dict)

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict includes added attributes."""
        self.amenity.middle_name = "Test"
        self.amenity.my_number = 98
        self.assertEqual("Test", self.amenity.middle_name)
        self.assertIn("my_number", self.amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that to_dict datetime attributes are strings."""
        am_dict = self.amenity.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the output of to_dict method."""
        dt = datetime.today()
        self.amenity.id = "123abc"
        self.amenity.created_at = self.amenity.updated_at = dt
        expected_dict = {
            'id': '123abc',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.amenity.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that to_dict is different from __dict__."""
        self.assertNotEqual(self.amenity.to_dict(), self.amenity.__dict__)

    def test_to_dict_with_arg(self):
        """Test to_dict with argument."""
        with self.assertRaises(TypeError):
            self.amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
