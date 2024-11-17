#!/usr/bin/python3
"""Test module for console.py"""

import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage


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
        """Prepare test environment"""
        if os.path.isfile("file.json"):
            os.rename("file.json", "file.json.bak")

    def tearDown(self):
        """Reset environment"""
        FileStorage._FileStorage__objects = {}
        storage.save()
        if os.path.isfile("file.json"):
            os.remove("file.json")
        if os.path.isfile("file.json.bak"):
            os.rename("file.json.bak", "file.json")

    def test_do_quit(self):
        """Test the quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))

    def test_do_EOF(self):
        """Test the EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))

    def test_emptyline(self):
        """Test that empty line does nothing"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd(""))

    def test_create_missing_class(self):
        """Test create with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_create_invalid_class(self):
        """Test create with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_create_valid_class(self):
        """Test create with valid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()
            self.assertTrue(len(obj_id) > 0)
            key = f"BaseModel.{obj_id}"
            self.assertIn(key, storage.all())

    def test_show_missing_class(self):
        """Test show command with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_show_invalid_class(self):
        """Test show command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_show_missing_id(self):
        """Test show command with missing ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())

    def test_show_no_instance_found(self):
        """Test show command with non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel 1234")
            self.assertEqual("** no instance found **\n", f.getvalue())

    def test_show_valid_instance(self):
        """Test show command with valid class and ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"show User {user_id}")
            output = f.getvalue()
            self.assertIn(user_id, output)

    def test_destroy_missing_class(self):
        """Test destroy command with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_destroy_invalid_class(self):
        """Test destroy command with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_destroy_missing_id(self):
        """Test destroy command with missing ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User")
            self.assertEqual("** instance id missing **\n", f.getvalue())

    def test_destroy_no_instance_found(self):
        """Test destroy command with non-existent instance"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User 1234")
            self.assertEqual("** no instance found **\n", f.getvalue())

    def test_destroy_valid_instance(self):
        """Test destroy command with valid class and ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"destroy User {user_id}")
            self.assertEqual("", f.getvalue())
            self.assertNotIn(f"User.{user_id}", storage.all())

    def test_all_no_class(self):
        """Test all command without class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            base_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue()
            self.assertIn(f"[BaseModel] ({base_id})", output)
            self.assertIn(f"[User] ({user_id})", output)

    def test_all_with_class(self):
        """Test all command with class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            user_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            output = f.getvalue()
            self.assertIn(f"[User] ({user_id})", output)

    def test_count(self):
        """Test count method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            self.console.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count User")
            self.assertEqual("2\n", f.getvalue())

    def test_invalid_dot_notation(self):
        """Test invalid dot notation"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("InvalidClass.invalid_command()")
            self.assertEqual("*** Unknown syntax: InvalidClass.invalid_command()\n", f.getvalue())

    def test_do_update_dot_notation_dict(self):
        """Test update with dot notation"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create City")
            city_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            update_dict = {"population": 500000, "nickname": "Metropolis"}
            self.console.onecmd(f'City.update("{city_id}", {update_dict})')
        key = f"City.{city_id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].population, 500000)
        self.assertEqual(storage.all()[key].nickname, "Metropolis")


if __name__ == "__main__":
    unittest.main()
