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

    


if __name__ == '__main__':
    HBNBCommand().cmdloop()
