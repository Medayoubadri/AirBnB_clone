#!/usr/bin/python3

'''
Defines the User class and its relationships.
'''

from models.base_model import BaseModel

class User(BaseModel):
    """
    User class inherits from BaseModel.
    Public attributes:
        - email: empty string
        - password: empty string
        - first_name: empty string
        - last_name: empty string
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
