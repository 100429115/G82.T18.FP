"""Class for validating the keys"""
from secure_all.data.attributes.attribute import Attribute

class Revocation(Attribute):
    """Class for validating the keys with a regex"""
    #pylint: disable=too-few-public-methods
    def __init__(self, attr_value):
        self._validation_pattern = r'(Temporal|Final)'
        self._error_message = "revocation is not valid"
        self._attr_value = self._validate(attr_value)
