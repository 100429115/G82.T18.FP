"""Module link to he json with the time mark and the final key"""

from secure_all.storage.json_store import JsonStore
from secure_all.cfg.access_manager_config import JSON_FILES_PATH

from secure_all.exception.access_management_exception import AccessManagementException


class RevokeKeyJsonStore:
    """Extends JsonStore """
    class __RevokeKeyJsonStore(JsonStore):
        # pylint: disable=invalid-name
        ID_FIELD = "_RevokeKey__key"
        ID_FIELD2 = "_RevokeKey__revocation"
        INVALID_ITEM = "Invalid item to be stored as a key"
        KEY_ALREADY_STORED = "key already found in RevokeKeyJson"

        _FILE_PATH = JSON_FILES_PATH + "storeRevokeKeys.json"
        _ID_FIELD = ID_FIELD
        _ID_FIELD2 = ID_FIELD2

        def revoke_key_store(self, tupla, valor):
            """Creates the dicc to include en el store de revoked keys"""
            if valor is None:
                data = {self._ID_FIELD: tupla[0], self._ID_FIELD2: tupla[1]}
                super().add_item2(data)
            else:
                raise AccessManagementException(self.KEY_ALREADY_STORED)

    __instance = None

    def __new__(cls):
        if not RevokeKeyJsonStore.__instance:
            RevokeKeyJsonStore.__instance = RevokeKeyJsonStore.__RevokeKeyJsonStore()
        return RevokeKeyJsonStore.__instance

    def __getattr__(self, nombre):
        return getattr(self.__instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.__instance, nombre, valor)
