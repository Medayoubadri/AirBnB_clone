#!/usr/bin/python3

"""
Unit tests for the City class.
"""

import unittest
import os
import models
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)

    def test_name_is_public_class_attribute(self):
        city = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_two_cities_unique_ids(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_two_cities_different_created_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_two_cities_different_updated_at(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        citystr = city.__str__()
        self.assertIn("[City] (123456)", citystr)
        self.assertIn("'id': '123456'", citystr)
        self.assertIn("'created_at': " + dt_repr, citystr)
        self.assertIn("'updated_at': " + dt_repr, citystr)

    def test_args_unused(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, dt)
        self.assertEqual(city.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_public_attributes(self):
        """Test that City class has expected public attributes."""
        city = City()
        city.name = "Gotham"
        city.state_id = "nyc-001"
        self.assertIsInstance(city.name, str)
        self.assertEqual(city.name, "Gotham")
        self.assertIsInstance(city.state_id, str)
        self.assertEqual(city.state_id, "nyc-001")

    def test_additional_attributes(self):
        """
        Test adding new attributes to a City instance.
        Gotham could use more heroes.
        """
        city = City()
        city.mayor = "Bruce Wayne"
        self.assertEqual(city.mayor, "Bruce Wayne")


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_two_saves(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        city = City()
        city.save()
        cityid = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(cityid, f.read())

    def test_save_creates_file(self):
        """Test that save() creates file.json."""
        city = City()
        city.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_save_file_content(self):
        """
        Test that save() writes correct data to file.json.
        Gotham needs order, and so does this test.
        """
        city = City()
        city.name = "Gotham"
        city.save()
        with open("file.json", "r", encoding="utf-8") as f:
            data = f.read()
            self.assertIn("City." + city.id, data)
            self.assertIn("Gotham", data)


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city = City()
        city.middle_name = "Holberton"
        city.my_number = 98
        self.assertEqual("Holberton", city.middle_name)
        self.assertIn("my_number", city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)

    def test_to_dict_includes_all_attributes(self):
        """Test that to_dict() includes all City attributes."""
        city = City()
        city.name = "Gotham"
        city.state_id = "nyc-001"
        city_dict = city.to_dict()
        self.assertIn("name", city_dict)
        self.assertIn("state_id", city_dict)
        self.assertEqual(city_dict["name"], "Gotham")
        self.assertEqual(city_dict["state_id"], "nyc-001")

    def test_to_dict_additional_attributes(self):
        """
        Test that to_dict() includes dynamically added attributes.
        Gotham's secrets don't stay hidden.
        """
        city = City()
        city.hero = "Batman"
        city_dict = city.to_dict()
        self.assertIn("hero", city_dict)
        self.assertEqual(city_dict["hero"], "Batman")


if __name__ == "__main__":
    unittest.main()