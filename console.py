#!/usr/bin/python3
"""This module defines the entry point of the command interpreter."""
import cmd
import re
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """HBNB console"""
    prompt = '(hbnb) '
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to end the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id"""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{class_name}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = shlex.split(arg)
        obj_list = []
        if not args:
            for obj in storage.all().values():
                obj_list.append(str(obj))
        elif args[0] in HBNBCommand.classes:
            for key, obj in storage.all().items():
                if key.startswith(args[0]):
                    obj_list.append(str(obj))
        else:
            print("** class doesn't exist **")
            return
        print(obj_list)

    def do_count(self, arg):
        """Counts the number of instances of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for key in storage.all() if key.startswith(f"{arg}."))
        print(count)

    def do_update(self, arg):
        """
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        args = HBNBCommand.args_parser(arg)
        objects = storage.all()

        if not args:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False
        if len(args) < 2:
            print("** instance id missing **")
            return False

        instance_key = f"{args[0]}.{args[1]}"
        if instance_key not in objects:
            print("** no instance found **")
            return False
        if len(args) < 3:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                if not isinstance(eval(args[2]), dict):
                    print("** value missing **")
                    return False
            except (NameError, SyntaxError):
                print("** value missing **")
                return False

        obj = objects[instance_key]

        if len(args) == 4:
            attr_name, attr_value = args[2], args[3]
            if attr_name in obj.__class__.__dict__:
                value_type = type(obj.__class__.__dict__[attr_name])
                obj.__dict__[attr_name] = value_type(attr_value)
            else:
                obj.__dict__[attr_name] = attr_value
        elif isinstance(eval(args[2]), dict):
            updates = eval(args[2])
            for key, value in updates.items():
                if (key in obj.__class__.__dict__ and
                        type(
                            obj.__class__.__dict__[key]
                            ) in {str, int, float}):
                    value_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = value_type(value)
                else:
                    obj.__dict__[key] = value

        storage.save()

    def default(self, arg):
        """
        Handle unrecognized commands and allow for dot notation
        (e.g., ClassName.command(args)).
        """
        match = re.search(r"\.", arg)
        if match:
            class_name, command_with_args = arg[
                :match.start()], arg[match.end():]
            if class_name in HBNBCommand.classes:
                match = re.search(r"\((.*?)\)", command_with_args)
                if match:
                    command = command_with_args[:match.start()]
                    command_args = match.group(1)
                    method = getattr(self, f"do_{command}", None)
                    if method:
                        call_args = f"{class_name} {command_args}".strip()
                        return method(call_args)
        print(f"*** Unknown syntax: {arg}")
        return False

    @staticmethod
    def args_parser(arg):
        """Parse input arguments and handle special characters"""
        curlies = re.search(r"\{(.*?)\}", arg)
        brackets = re.search(r"\[(.*?)\]", arg)

        def split_and_strip(input_str):
            return [item.strip(",") for item in shlex.split(input_str)]

        if curlies:
            lexer = split_and_strip(arg[:curlies.span()[0]])
            lexer.append(curlies.group())
            return lexer
        elif brackets:
            lexer = split_and_strip(arg[:brackets.span()[0]])
            lexer.append(brackets.group())
            return lexer
        return split_and_strip(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
