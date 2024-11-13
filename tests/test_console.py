#!/usr/bin/python3
'''
Tests for the console module.
'''

import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User

class TestHBNBCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up any state that is needed across all tests."""
        cls.console = HBNBCommand()

    def setUp(self):
        """Clean up storage between tests."""
        storage.reload()
    
    def tearDown(self):
        """Removes file.json after tests to avoid interference between tests."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_create_success(self):
        """Test creating a new instance of BaseModel."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("create BaseModel")
            model_id = out.getvalue().strip()
            key = f"BaseModel.{model_id}"
            self.assertIn(key, storage.all())
    
    def test_create_missing_class(self):
        """Test create command with missing class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **\n", out.getvalue())
    
    def test_create_invalid_class(self):
        """Test create command with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", out.getvalue())
    
    def test_show_success(self):
        """Test showing an instance of BaseModel."""
        model = BaseModel()
        model.save()
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd(f"show BaseModel {model.id}")
            output = out.getvalue().strip()
            self.assertIn(model.id, output)
            self.assertIn("BaseModel", output)
            self.assertIn("created_at", output)
            self.assertIn("updated_at", output)
    
    def test_show_missing_class(self):
        """Test show command with missing class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("show")
            self.assertEqual("** class name missing **\n", out.getvalue())
    
    def test_show_invalid_class(self):
        """Test show command with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **\n", out.getvalue())
    
    def test_show_missing_id(self):
        """Test show command with missing ID."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **\n", out.getvalue())
    
    def test_show_invalid_id(self):
        """Test show command with invalid ID."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("show BaseModel 12345")
            self.assertEqual("** no instance found **\n", out.getvalue())
    
    def test_destroy_success(self):
        """Test destroying an instance of BaseModel."""
        model = BaseModel()
        model.save()
        key = f"BaseModel.{model.id}"
        self.assertIn(key, storage.all())
        with patch("sys.stdout", new=StringIO()):
            self.console.onecmd(f"destroy BaseModel {model.id}")
        self.assertNotIn(key, storage.all())
    
    def test_destroy_missing_class(self):
        """Test destroy command with missing class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("destroy")
            self.assertEqual("** class name missing **\n", out.getvalue())
    
    def test_destroy_invalid_class(self):
        """Test destroy command with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("destroy MyModel")
            self.assertEqual("** class doesn't exist **\n", out.getvalue())
    
    def test_destroy_missing_id(self):
        """Test destroy command with missing ID."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **\n", out.getvalue())
    
    def test_destroy_invalid_id(self):
        """Test destroy command with invalid ID."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual("** no instance found **\n", out.getvalue())
    
    def test_all(self):
        """Test all command to list instances."""
        model = BaseModel()
        model.save()
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("all BaseModel")
            output = out.getvalue().strip()
            self.assertIn("[BaseModel]", output)

    
    def test_update_success(self):
        """Test updating an instance's attribute."""
        model = BaseModel()
        model.save()
        with patch("sys.stdout", new=StringIO()):
            self.console.onecmd(f'update BaseModel {model.id} name "New York"')
        self.assertEqual(model.name, "New York")
    
    def test_update_missing_class(self):
        """Test update command with missing class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("update")
            self.assertEqual("** class name missing **\n", out.getvalue())
    
    def test_update_invalid_class(self):
        """Test update command with invalid class name."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("update MyModel")
            self.assertEqual("** class doesn't exist **\n", out.getvalue())
    
    def test_update_missing_id(self):
        """Test update command with missing ID."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("update BaseModel")
            self.assertEqual("** instance id missing **\n", out.getvalue())
    
    def test_update_invalid_id(self):
        """Test update command with invalid ID."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd("update BaseModel 12345 name \"New York\"")
            self.assertEqual("** no instance found **\n", out.getvalue())

    def test_update_missing_attribute(self):
        """Test update command with missing attribute name."""
        model = BaseModel()
        model.save()
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd(f"update BaseModel {model.id}")
            self.assertEqual("** attribute name missing **\n", out.getvalue())

    def test_update_missing_value(self):
        """Test update command with missing attribute value."""
        model = BaseModel()
        model.save()
        with patch("sys.stdout", new=StringIO()) as out:
            self.console.onecmd(f"update BaseModel {model.id} name")
            self.assertEqual("** value missing **\n", out.getvalue())

if __name__ == "__main__":
    unittest.main()
