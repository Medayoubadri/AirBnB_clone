#!/usr/bin/python3
"""
Unit tests for the HBNB command interpreter.
"""
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
import os
import json


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for the HBNBCommand console."""

    def setUp(self):
        """Set up test environment."""
        self.console = HBNBCommand()
        self.storage_file = "file.json"
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
        storage._FileStorage__objects.clear()

    def test_quit(self):
        """Test the quit command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))
            output = f.getvalue()
            self.assertEqual(output, "")

    def test_eof(self):
        """Test the EOF command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))
            output = f.getvalue().strip()
            self.assertEqual(output, "")

    def test_empty_line(self):
        """Test that empty lines do not produce errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("")
            output = f.getvalue()
            self.assertEqual(output, "")

    def test_create_missing_class(self):
        """Test create with no class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_create_invalid_class(self):
        """Test create with invalid class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_create_valid_class(self):
        """Test create with a valid class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            self.assertTrue(len(new_id) > 0)
            self.assertIn(f"BaseModel.{new_id}", storage.all())

    def test_show_missing_class(self):
        """Test show with no class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_show_missing_id(self):
        """Test show with missing instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_show_no_instance_found(self):
        """Test show with nonexistent instance."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel 1234-5678")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_show_valid_instance(self):
        """Test show with a valid instance."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            
            self.console.onecmd(f"show BaseModel {new_id}")
            output = f.getvalue().strip()
            self.assertIn(f"[BaseModel] ({new_id})", output)

    def test_destroy_missing_class(self):
        """Test destroy with no class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_destroy_invalid_class(self):
        """Test destroy with invalid class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy with missing instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_destroy_no_instance_found(self):
        """Test destroy with nonexistent instance."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 1234-5678")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_destroy_valid_instance(self):
        """Test destroy with a valid instance."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            self.assertIn(f"BaseModel.{new_id}", storage.all())
            self.console.onecmd(f"destroy BaseModel {new_id}")
            self.assertNotIn(f"BaseModel.{new_id}", storage.all())

    def test_all_no_class(self):
        """Test all with no class (all instances)."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue().strip()
            self.assertEqual(output, "[]")  # Assuming no instances exist.

    def test_all_invalid_class(self):
        """Test all with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_all_valid_class(self):
        """Test all with a valid class."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("all BaseModel")
            output = f.getvalue().strip()
            self.assertIn("BaseModel", output)

    def test_count_missing_class(self):
        """Test count with no class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_count_invalid_class(self):
        """Test count with an invalid class."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_count_valid_class(self):
        """Test count with a valid class."""
        with patch('sys.stdout', new=StringIO()) as f:
            storage._FileStorage__objects.clear()
            
            self.console.onecmd("create BaseModel")
            self.console.onecmd("create BaseModel")
            self.console.onecmd("create BaseModel")
            
            self.console.onecmd("count BaseModel")
            output = f.getvalue().strip()
            self.assertEqual(output.split()[-1], "3")


    def test_update_missing_class(self):
        """Test update with no class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_update_invalid_class(self):
        """Test update with invalid class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_update_missing_id(self):
        """Test update with missing instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_update_no_instance_found(self):
        """Test update with nonexistent instance."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel 1234-5678")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_update_missing_attribute(self):
        """Test update with missing attribute name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            self.console.onecmd(f"update BaseModel {new_id}")
            self.assertEqual(f.getvalue().strip().split("\n")[-1], "** attribute name missing **")

    def test_update_missing_value(self):
        """Test update with missing value."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            self.console.onecmd(f"update BaseModel {new_id} name")
            self.assertEqual(f.getvalue().strip().split("\n")[-1], "** value missing **")

    def test_update_valid(self):
        """Test update with valid attribute and value."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            self.console.onecmd(f"update BaseModel {new_id} name 'MyName'")
            self.console.onecmd(f"show BaseModel {new_id}")
            output = f.getvalue().strip()
            self.assertIn("'name': 'MyName'", output)

    def test_dot_all(self):
        """Test dot notation for 'all' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            self.console.onecmd("BaseModel.all()")
            output = f.getvalue().strip()
            self.assertIn("BaseModel", output)

    def test_dot_count(self):
        """Test dot notation for 'count' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            storage._FileStorage__objects.clear()

            self.console.onecmd("create BaseModel")
            self.console.onecmd("create BaseModel")
            
            self.console.onecmd("BaseModel.count()")
            output = f.getvalue().strip()
            self.assertEqual(output.split()[-1], "2")

    def test_dot_show(self):
        """Test dot notation for 'show' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            
            self.console.onecmd(f"BaseModel.show({new_id})")
            output = f.getvalue().strip()
            self.assertIn(f"[BaseModel] ({new_id})", output)

    def test_dot_destroy(self):
        """Test dot notation for 'destroy' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            self.console.onecmd(f"BaseModel.destroy({new_id})")
            self.console.onecmd(f"show BaseModel {new_id}")
            output = f.getvalue().strip()
            self.assertEqual(output.split("\n")[-1], "** no instance found **")


if __name__ == "__main__":
    unittest.main()
