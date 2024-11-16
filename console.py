#!/usr/bin/python3
"""
Console module for HBNB project
"""
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
import ast


class HBNBCommand(cmd.Cmd):
    """HBNB console class"""
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

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
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
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]
        try:
            attr_value = eval(attr_value)
        except Exception:
            pass
        setattr(obj, attr_name, attr_value)
        obj.save()

    def dic_parser(self, arg):
        """
        Parse the cmd string and return class name, method name, and arguments
        """
        parts = arg.split('.', 1)
        if len(parts) != 2:
            return None, None, None
        class_name, method_with_args = parts
        if '(' not in method_with_args or not method_with_args.endswith(')'):
            return None, None, None
        method_name, args_str = method_with_args.split('(', 1)
        args_str = args_str[:-1]
        return class_name, method_name, args_str

    def do_count(self, class_name):
        """Counts the number of instances of a class"""
        count = sum(
            1 for key in storage.all() if key.startswith(f"{class_name}.")
        )
        print(count)

    def handle_update(self, class_name, args_str):
        """Handles the update command from default method"""
        match = re.match(r'\s*"([^"]+)"\s*,\s*(\{.*\})\s*', args_str)
        if match:
            instance_id = match.group(1)
            dict_str = match.group(2)
            try:
                update_dict = ast.literal_eval(dict_str)
                if isinstance(update_dict, dict):
                    for key, value in update_dict.items():
                        self.do_update(
                            f"{class_name} {instance_id} {key} {value}"
                        )
                else:
                    print("** invalid dictionary format **")
            except Exception as e:
                print("** invalid dictionary format **")
        else:
            args = args_str.split(',')
            if len(args) >= 3:
                instance_id = args[0].strip().strip('"')
                attr_name = args[1].strip().strip('"')
                attr_value = args[2].strip().strip('"')
                self.do_update(
                    f"{class_name} {instance_id} {attr_name} {attr_value}"
                )
            else:
                print("** attribute name missing **")

    def default(self, arg):
        """Handle class-specific commands"""
        class_name, method_name, args_str = self.dic_parser(arg)
        if class_name is None:
            print(f"*** Unknown syntax: {arg}")
            return

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        method_dispatch = {
            'all': self.do_all,
            'count': self.do_count,
            'show': self.do_show,
            'destroy': self.do_destroy,
        }

        if method_name in method_dispatch:
            method = method_dispatch[method_name]
            if method_name == 'count':
                method(class_name)
            else:
                args = f"{class_name} {args_str.strip('\"')}"
                method(args)
        elif method_name == 'update':
            self.handle_update(class_name, args_str)
        else:
            print(f"*** Unknown syntax: {arg}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
