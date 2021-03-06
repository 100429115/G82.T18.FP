"""Module AccessManager with AccessManager Class """

from secure_all.data.access_key import AccessKey
from secure_all.data.access_request import AccessRequest


from secure_all.storage.last_access_store import LastAccessJsonStore
from secure_all.storage.revoke_key_store import RevokeKeyJsonStore


class AccessManager:
    """AccessManager class, manages the access to a building implementing singleton """
    #pylint: disable=too-many-arguments,no-self-use,invalid-name, too-few-public-methods
    class __AccessManager:
        """Class for providing the methods for managing the access to a building"""

        def request_access_code(self, id_card, name_surname, access_type, email_address, days):
            """ this method give access to the building"""
            my_request = AccessRequest(id_card, name_surname, access_type, email_address, days)
            code = my_request.access_code
            my_request.store_request()
            return code

        def get_access_key(self, keyfile):
            """Returns the access key for the access code & dni received in a json file"""
            my_key = AccessKey.create_key_from_file(keyfile)
            my_key.store_keys()
            return my_key.key

        def open_door(self, key):
            """Opens the door if the key is valid an it is not expired"""
            my_key = AccessKey.create_key_from_id(key)
            if my_key.is_valid():
                last_access = LastAccessJsonStore()
                last_access.store_time_mark(key)
            return my_key.is_valid()

        def revoke_key(self, filepath):
            """Devuelve el correo electrónico o un AccessManagementException"""
            labels = AccessKey.obtain_revoke_labels(filepath)
            my_key = AccessKey.create_key_from_id(labels[0])
            if my_key.is_valid():
                existencia = RevokeKeyJsonStore().find_item(labels[0])
                RevokeKeyJsonStore().revoke_key_store(labels, existencia)
            return str(my_key.notification_emails)

    __instance = None

    def __new__(cls):
        if not AccessManager.__instance:
            AccessManager.__instance = AccessManager.__AccessManager()
        return AccessManager.__instance

    def __getattr__(self, nombre):
        return getattr(self.__instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.__instance, nombre, valor)
