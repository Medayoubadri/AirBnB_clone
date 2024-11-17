#!/usr/bin/python3
"""
Defines unittests for console.py.
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommandPrompting(unittest.TestCase):
    """Unittests for the HBNB command interpreter's prompting behavior."""

    def test_prompt_string(self):
        """Test if the command prompt string is correct."""
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        """Test if empty line input does nothing."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

    def test_whitespace_only_input(self):
        """Test if whitespace-only input behaves like an empty line."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("    "))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommandHelp(unittest.TestCase):
    """
    Unittests for testing help messages of the HBNB command interpreter.
    """

    def test_help(self):
        """
        Test if the general help command displays the correct help message.
        """
        h = (
            "Documented commands (type help <topic>):\n"
            "========================================\n"
            "EOF  all  count  create  destroy  help  quit  show  update"
        )
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_quit(self):
        """Test if the help message for the 'quit' command is correct."""
        h = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(h, output.getvalue().strip())


class TestHBNBCommandExit(unittest.TestCase):
    """
    Unittests for testing exit behavior of the HBNB command interpreter.
    """

    def test_quit_exits(self):
        """Test if the 'quit' command exits the interpreter."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_eof_exits(self):
        """Test if the 'EOF' command exits the interpreter."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandCreate(unittest.TestCase):
    """
    Unittests for testing 'create' command in the HBNB command interpreter.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the environment before each test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Clean up the environment after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        """Test create with no class name."""
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_class(self):
        """Test create with an invalid class name."""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        """Test create with invalid syntax."""
        correct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_create_object(self):
        """Test create for valid classes."""
        classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
        ]
        for cls in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))
                object_id = output.getvalue().strip()
                self.assertGreater(len(object_id), 0)
                test_key = f"{cls}.{object_id}"
                self.assertIn(test_key, storage.all().keys())


class TestHBNBCommandShow(unittest.TestCase):
    """Unittests for testing 'show' command of the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """Set up the environment before each test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Clean up the environment after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def _create_test_object(self, class_name):
        """Helper method to create a test object and return its ID."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            return output.getvalue().strip()

    def test_show_invalid_class(self):
        """Test 'show' with an invalid class name."""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_show_missing_id(self):
        """Test 'show' with a missing ID."""
        correct = "** instance id missing **"
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"show {cls}"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_no_instance_found(self):
        """Test 'show' when no instance is found."""
        correct = "** no instance found **"
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"show {cls} 1"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_show_valid_object_space_notation(self):
        """Test 'show' with valid objects using space notation."""
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            obj_id = self._create_test_object(cls)
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{cls}.{obj_id}"]
                self.assertFalse(HBNBCommand().onecmd(f"show {cls} {obj_id}"))
                self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_valid_object_dot_notation(self):
        """Test 'show' with valid objects using dot notation."""
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            obj_id = self._create_test_object(cls)
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()[f"{cls}.{obj_id}"]
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.show({obj_id})"))
                self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommandDestroy(unittest.TestCase):
    """
    Unittests for testing 'destroy' command of the HBNB command interpreter.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the environment before each test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Clean up the environment after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def _create_test_object(self, class_name):
        """Helper method to create a test object and return its ID."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            return output.getvalue().strip()

    def test_destroy_missing_class(self):
        """Test 'destroy' with no class name."""
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_class(self):
        """Test 'destroy' with an invalid class name."""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_missing_id(self):
        """Test 'destroy' with a missing ID."""
        correct = "** instance id missing **"
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {cls}"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.destroy()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_invalid_id(self):
        """Test 'destroy' with an invalid ID."""
        correct = "** no instance found **"
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {cls} 1"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.destroy(1)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_destroy_valid_object_space_notation(self):
        """Test 'destroy' with valid objects using space notation."""
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            obj_id = self._create_test_object(cls)
            with patch("sys.stdout", new=StringIO()):
                self.assertFalse(
                    HBNBCommand().onecmd(f"destroy {cls} {obj_id}"))
            self.assertNotIn(f"{cls}.{obj_id}", storage.all())

    def test_destroy_valid_object_dot_notation(self):
        """Test 'destroy' with valid objects using dot notation."""
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            obj_id = self._create_test_object(cls)
            with patch("sys.stdout", new=StringIO()):
                self.assertFalse(HBNBCommand().onecmd(
                    f"{cls}.destroy({obj_id})"))
            self.assertNotIn(f"{cls}.{obj_id}", storage.all())


class TestHBNBCommandAll(unittest.TestCase):
    """Unittests for testing 'all' command of the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """Set up the environment before each test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Clean up the environment after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def _create_test_objects(self):
        """Helper method to create objects for all classes."""
        classes = [
            "BaseModel", "User", "State", "City", "Amenity", "Place", "Review"
        ]
        for cls in classes:
            with patch("sys.stdout", new=StringIO()):
                self.assertFalse(HBNBCommand().onecmd(f"create {cls}"))

    def test_all_invalid_class(self):
        """Test 'all' with an invalid class name."""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_all_objects_space_notation(self):
        """Test 'all' with all objects using space notation."""
        self._create_test_objects()
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            output_value = output.getvalue().strip()
            self.assertIn("BaseModel", output_value)
            self.assertIn("User", output_value)
            self.assertIn("State", output_value)
            self.assertIn("Place", output_value)
            self.assertIn("City", output_value)
            self.assertIn("Amenity", output_value)
            self.assertIn("Review", output_value)

    def test_all_objects_dot_notation(self):
        """Test 'all' with objects using dot notation."""
        self._create_test_objects()
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.all()"))
                output_value = output.getvalue().strip()
                self.assertIn(cls, output_value)

    def test_all_single_object_space_notation(self):
        """Test 'all' for a single class using space notation."""
        self._create_test_objects()
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"all {cls}"))
                output_value = output.getvalue().strip()
                self.assertIn(cls, output_value)
                for other_cls in [
                        "BaseModel",
                        "User",
                        "State",
                        "City",
                        "Amenity",
                        "Place",
                        "Review"]:
                    if other_cls != cls:
                        self.assertNotIn(other_cls, output_value)

    def test_all_single_object_dot_notation(self):
        """Test 'all' for a single class using dot notation."""
        self._create_test_objects()
        for cls in [
                "BaseModel",
                "User",
                "State",
                "City",
                "Amenity",
                "Place",
                "Review"]:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.all()"))
                output_value = output.getvalue().strip()
                self.assertIn(cls, output_value)
                for other_cls in [
                        "BaseModel",
                        "User",
                        "State",
                        "City",
                        "Amenity",
                        "Place",
                        "Review"]:
                    if other_cls != cls:
                        self.assertNotIn(other_cls, output_value)


class TestHBNBCommandUpdate(unittest.TestCase):
    """
    Unittests for testing 'update' command of the HBNB command interpreter.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the environment before each test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Clean up the environment after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def _create_object(self, cls_name):
        """Helper method to create an object and return its ID."""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(f"create {cls_name}"))
            return output.getvalue().strip()

    def test_update_invalid_class(self):
        """Test 'update' with an invalid class."""
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_id(self):
        """Test 'update' with a missing ID."""
        correct = "** instance id missing **"
        classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
            ]
        for cls in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"update {cls}"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.update()"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_invalid_id(self):
        """Test 'update' with an invalid ID."""
        correct = "** no instance found **"
        classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
            ]
        for cls in classes:
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"update {cls} 1234"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(f"{cls}.update(1234)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name(self):
        """Test 'update' with a missing attribute name."""
        correct = "** attribute name missing **"
        classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
            ]
        for cls in classes:
            obj_id = self._create_object(cls)
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    HBNBCommand().onecmd(f"update {cls} {obj_id}"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    HBNBCommand().onecmd(f"{cls}.update({obj_id})"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_value(self):
        """Test 'update' with a missing attribute value."""
        correct = "** value missing **"
        classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
            ]
        for cls in classes:
            obj_id = self._create_object(cls)
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    HBNBCommand().onecmd(f"update {cls} {obj_id} attr_name"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(
                    HBNBCommand().onecmd(f"{cls}.update({obj_id}, attr_name)"))
                self.assertEqual(correct, output.getvalue().strip())

    def test_update_valid_string_attr(self):
        """Test 'update' with a valid string attribute."""
        classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
            ]
        for cls in classes:
            obj_id = self._create_object(cls)
            cmd_space = f"update {cls} {obj_id} attr_name 'attr_value'"
            cmd_dot = f"{cls}.update({obj_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(cmd_space))
            self.assertFalse(HBNBCommand().onecmd(cmd_dot))
            obj = storage.all()[f"{cls}.{obj_id}"]
            self.assertEqual(obj.__dict__["attr_name"], "attr_value")

    def test_update_valid_numeric_attr(self):
        """Test 'update' with a valid numeric attribute (int and float)."""
        obj_id = self._create_object("Place")
        cmds = [
            (f"update Place {obj_id} max_guest 98", "max_guest", 98),
            (f"update Place {obj_id} latitude 7.2", "latitude", 7.2),
            (f"Place.update({obj_id}, max_guest, 98)", "max_guest", 98),
            (f"Place.update({obj_id}, latitude, 7.2)", "latitude", 7.2),
        ]
        for cmd, attr, value in cmds:
            self.assertFalse(HBNBCommand().onecmd(cmd))
            obj = storage.all()[f"Place.{obj_id}"]
            self.assertEqual(obj.__dict__[attr], value)

    def test_update_valid_dict_attr(self):
        """Test 'update' with a valid dictionary of attributes."""
        obj_id = self._create_object("BaseModel")
        dict_str = (
            "{"
            "'attr_name': 'attr_value', "
            "'max_guest': 10, "
            "'latitude': 3.14"
            "}"
        )
        cmd_space = f"update BaseModel {obj_id} {dict_str}"
        cmd_dot = f"BaseModel.update({obj_id}, {dict_str})"
        self.assertFalse(HBNBCommand().onecmd(cmd_space))
        self.assertFalse(HBNBCommand().onecmd(cmd_dot))
        obj = storage.all()[f"BaseModel.{obj_id}"]
        self.assertEqual(obj.__dict__["attr_name"], "attr_value")
        self.assertEqual(obj.__dict__["max_guest"], 10)
        self.assertEqual(obj.__dict__["latitude"], 3.14)


class TestHBNBCommandCount(unittest.TestCase):
    """
    Unittests for testing 'count' command of the HBNB command interpreter.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the environment before each test."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Clean up the environment after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def _create_test_object(self, class_name):
        """Helper method to create a test object."""
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd(f"create {class_name}")

    def _get_count_output(self, class_name):
        """Helper method to get the output of the count command."""
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd(f"{class_name}.count()")
            return output.getvalue().strip()

    def test_count_objects(self):
        """Test 'count' command for each class."""
        classes = [
            "BaseModel", "User", "State", "City", "Amenity", "Place", "Review"
        ]
        for cls in classes:
            self._create_test_object(cls)
            count_output = self._get_count_output(cls)
            self.assertEqual("5", count_output)


if __name__ == "__main__":
    unittest.main()
