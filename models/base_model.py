import uuid
from datetime import datetime

class BaseModel:
    """
    BaseModel defines all common attributes/methods for other classes.
    """

    def __init__(self):
        """
        Initializes a new instance of BaseModel.
        - id is set to a unique UUID.
        - created_at and updated_at are set to the current datetime.
        """
        self.id = str(uuid.uuid4())  # unique id as a string
        self.created_at = datetime.now()  # creation timestamp
        self.updated_at = datetime.now()  # last update timestamp

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
        my_dict = self.__dict__.copy()  # shallow copy of instance's __dict__
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
