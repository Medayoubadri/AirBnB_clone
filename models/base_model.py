import uuid
from datetime import datetime

class BaseModel:
    """
    BaseModel defines all common attributes/methods for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.
        - If kwargs is provided, use it to set attributes.
        - Otherwise, generate a new instance with unique id and timestamps.
        """
        if kwargs:
            # Initialize attributes from kwargs dictionary
            for key, value in kwargs.items():
                # Convert created_at and updated_at from string to datetime
                if key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            # If no kwargs, initialize new instance with unique id and timestamps
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance
        in the format [<class name>] (<self.id>) <self.__dict__>
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the updated_at attribute to the current datetime.
        This simulates 'saving' an instance.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Converts the instance to a dictionary, including:
        - instance attributes
        - __class__ key (class name)
        - ISO-formatted strings for datetime attributes
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
