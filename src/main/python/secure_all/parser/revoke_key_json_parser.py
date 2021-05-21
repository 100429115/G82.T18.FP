"""parser for input key files according to RF2"""

from secure_all.parser.json_parser import JsonParser


class RevokeJsonParser(JsonParser):
    """parser for input revoke key files"""
    #pylint: disable=too-few-public-methods
    KEY = "Key"
    REVOCATION = "Revocation"
    REASON = "Reason"
    _key_list = [KEY, REVOCATION, REASON]
