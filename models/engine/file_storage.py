#!/usr/bin/python3
'''
This module contains the FileStorage class, which serializes instances
to a JSON file and deserializes JSON file to instances.
'''
import json
from models.base_model import BaseModel


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        obj_dict = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                obj_dict = json.load(file)
                for key, obj_data in obj_dict.items():
                    if obj_data["__class__"] == "BaseModel":
                        self.__objects[key] = BaseModel(**obj_data)
        except Exception:
            pass
