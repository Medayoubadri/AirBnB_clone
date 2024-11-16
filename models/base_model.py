#!/usr/bin/python3

'''
BaseModel defines all common attributes/methods for other classes.
'''

import uuid
from datetime import datetime


class BaseModel:
    """BaseModel defines all common attributes/methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    try:
                        setattr(self, key, datetime.fromisoformat(value))
                    except ValueError:
                        setattr(self, key, datetime.now())
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.save()

            from models import storage
            storage.new(self)

    def __str__(self):
        """Returns a string representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates `updated_at` and saves the instance to storage."""
        self.updated_at = datetime.now()

        from models import storage
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance."""
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
