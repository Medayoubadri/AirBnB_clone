#!/usr/bin/python3

'''
Defines the Review class and its relationships.
'''

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class inherits from BaseModel.
    Public attributes:
        - place_id: empty string, refers to Place.id
        - user_id: empty string, refers to User.id
        - text: empty string
    """
    place_id = ""
    user_id = ""
    text = ""
