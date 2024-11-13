#!/usr/bin/python3
'''
Defines the City class and its relationships.
'''

from models.base_model import BaseModel

class City(BaseModel):
    """
    City class inherits from BaseModel.
    Public attributes:
        - state_id: empty string, refers to State.id
        - name: empty string
    """
    state_id = ""
    name = ""
