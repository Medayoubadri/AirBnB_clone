#!/usr/bin/python3
"""Test module for console.py"""

import unittest
from unittest.mock import patch
from io import StringIO
import os
import sys
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class TestHBNBCommand(unittest.TestCase):
    """Tests the HBNBCommand console."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        del cls.console

    def setUp(self):
        """Redirect stdout to capture console outputs"""
        self.held_stdout = StringIO()
        self.patcher = patch('sys.stdout', new=self.held_stdout)
        self.patcher.start()
        if os.path.isfile("file.json"):
            os.rename("file.json", "file.json.bak")

    def tearDown(self):
        """Reset stdout and clean up test environment"""
        self.patcher.stop()
        self.held_stdout.close()
        FileStorage._FileStorage__objects = {}
        storage.save()
        if os.path.isfile("file.json"):
            os.remove("file.json")
        if os.path.isfile("file.json.bak"):
            os.rename("file.json.bak", "file.json")

    def test_do_quit(self):
        """Test the quit command"""
        self.assertTrue(self.console.onecmd("quit"))

    def test_do_EOF(self):
        """Test the EOF command"""
        self.assertTrue(self.console.onecmd("EOF"))

    def test_emptyline(self):
        """Test that empty line does nothing"""
        self.assertFalse(self.console.onecmd(""))

    def test_create_missing_class(self):
        """Test create with no class name"""
        self.console.onecmd("create")
        self.assertEqual(
            "** class name missing **\n", self.held_stdout.getvalue()
            )

    def test_create_invalid_class(self):
        """Test create with invalid class name"""
        self.console.onecmd("create MyModel")
        self.assertEqual(
            "** class doesn't exist **\n", self.held_stdout.getvalue()
            )

    def test_create_valid_class(self):
        """Test create with valid class name"""
        self.console.onecmd("create BaseModel")
        output = self.held_stdout.getvalue().strip()
        self.assertTrue(len(output) > 0)
        key = f"BaseModel.{output}"
        self.assertIn(key, storage.all())

    def test_show_missing_class(self):
        """Test show command with missing class"""
        self.console.onecmd("show")
        self.assertEqual(
            "** class name missing **\n", self.held_stdout.getvalue()
            )

    def test_show_invalid_class(self):
        """Test show command with invalid class"""
        self.console.onecmd("show MyModel")
        self.assertEqual(
            "** class doesn't exist **\n", self.held_stdout.getvalue()
            )

    def test_show_missing_id(self):
        """Test show command with missing ID"""
        self.console.onecmd("show BaseModel")
        self.assertEqual(
            "** instance id missing **\n", self.held_stdout.getvalue()
            )

    def test_show_no_instance_found(self):
        """Test show command with non-existent instance"""
        self.console.onecmd("show BaseModel 1234")
        self.assertEqual(
            "** no instance found **\n", self.held_stdout.getvalue()
            )

    def test_show_valid_instance(self):
        """Test show command with valid class and ID"""
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f"show User {user_id}")
        output = self.held_stdout.getvalue()
        self.assertIn(user_id, output)

    def test_destroy_missing_class(self):
        """Test destroy command with missing class"""
        self.console.onecmd("destroy")
        self.assertEqual(
            "** class name missing **\n", self.held_stdout.getvalue()
            )

    def test_destroy_invalid_class(self):
        """Test destroy command with invalid class"""
        self.console.onecmd("destroy MyModel")
        self.assertEqual(
            "** class doesn't exist **\n", self.held_stdout.getvalue()
            )

    def test_destroy_missing_id(self):
        """Test destroy command with missing ID"""
        self.console.onecmd("destroy User")
        self.assertEqual(
            "** instance id missing **\n", self.held_stdout.getvalue()
            )

    def test_destroy_no_instance_found(self):
        """Test destroy command with non-existent instance"""
        self.console.onecmd("destroy User 1234")
        self.assertEqual(
            "** no instance found **\n", self.held_stdout.getvalue()
            )

    def test_destroy_valid_instance(self):
        """Test destroy command with valid class and ID"""
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f"destroy User {user_id}")
        self.assertEqual("", self.held_stdout.getvalue())
        self.assertNotIn(f"User.{user_id}", storage.all())

    def test_all_no_class(self):
        """Test all command without class name"""
        self.console.onecmd("create BaseModel")
        base_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd("all")
        output = self.held_stdout.getvalue()
        self.assertIn(f"[BaseModel] ({base_id})", output)
        self.assertIn(f"[User] ({user_id})", output)

    def test_all_with_class(self):
        """Test all command with class name"""
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd("all User")
        output = self.held_stdout.getvalue()
        self.assertIn(f"[User] ({user_id})", output)

    def test_all_invalid_class(self):
        """Test all command with invalid class"""
        self.console.onecmd("all MyModel")
        self.assertEqual(
            "** class doesn't exist **\n", self.held_stdout.getvalue()
            )

    def test_update_missing_class(self):
        """Test update command with missing class"""
        self.console.onecmd("update")
        self.assertEqual(
            "** class name missing **\n", self.held_stdout.getvalue()
            )

    def test_update_invalid_class(self):
        """Test update command with invalid class"""
        self.console.onecmd("update MyModel")
        self.assertEqual(
            "** class doesn't exist **\n", self.held_stdout.getvalue()
            )

    def test_update_missing_id(self):
        """Test update command with missing ID"""
        self.console.onecmd("update User")
        self.assertEqual(
            "** instance id missing **\n", self.held_stdout.getvalue()
            )

    def test_update_no_instance_found(self):
        """Test update command with non-existent instance"""
        self.console.onecmd("update User 1234")
        self.assertEqual(
            "** no instance found **\n", self.held_stdout.getvalue()
            )

    def test_update_missing_attribute_name(self):
        """Test update command with missing attribute name"""
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f"update User {user_id}")
        self.assertEqual(
            "** attribute name missing **\n", self.held_stdout.getvalue()
            )

    def test_update_missing_value(self):
        """Test update command with missing value"""
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f"update User {user_id} name")
        self.assertEqual("** value missing **\n", self.held_stdout.getvalue())

    def test_update_valid_instance(self):
        """Test update command with valid data"""
        self.console.onecmd("create User")
        user_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f'update User {user_id} name "Alice"')
        self.assertEqual("", self.held_stdout.getvalue())
        key = f"User.{user_id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "Alice")

    def test_count(self):
        """Test count method for User class"""
        self.console.onecmd("create User")
        self.console.onecmd("create User")
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd("User.count()")
        self.assertEqual("2\n", self.held_stdout.getvalue())

    def test_default_all(self):
        """Test default all method"""
        self.console.onecmd("create State")
        state_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd("State.all()")
        output = self.held_stdout.getvalue()
        self.assertIn(f"[State] ({state_id})", output)

    def test_default_show(self):
        """Test default show method"""
        self.console.onecmd("create City")
        city_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f'City.show("{city_id}")')
        output = self.held_stdout.getvalue()
        self.assertIn(f"[City] ({city_id})", output)

    def test_default_destroy(self):
        """Test default destroy method"""
        self.console.onecmd("create Place")
        place_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        self.console.onecmd(f'Place.destroy("{place_id}")')
        self.assertEqual("", self.held_stdout.getvalue())
        self.assertNotIn(f"Place.{place_id}", storage.all())

    def test_default_update_with_dict(self):
        """Test default update method with dictionary"""
        self.console.onecmd("create Amenity")
        amenity_id = self.held_stdout.getvalue().strip()
        self.held_stdout.truncate(0)
        self.held_stdout.seek(0)
        update_dict = {"name": "Pool", "rating": 5}
        self.console.onecmd(f'Amenity.update("{amenity_id}", {update_dict})')
        self.assertEqual("", self.held_stdout.getvalue())
        key = f"Amenity.{amenity_id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].name, "Pool")
        self.assertEqual(storage.all()[key].rating, 5)

    def test_invalid_syntax(self):
        """Test invalid command syntax"""
        self.console.onecmd("MyModel.create()")
        self.assertEqual(
            "** class doesn't exist **\n", self.held_stdout.getvalue()
            )



if __name__ == "__main__":
    unittest.main()
