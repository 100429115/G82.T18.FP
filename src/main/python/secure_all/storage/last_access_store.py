"""Module link to he json with the time mark and the final key"""
from datetime import datetime
from secure_all.storage.json_store import JsonStore
from secure_all.cfg.access_manager_config import JSON_FILES_PATH


class LastAccessJsonStore:
    """Extends JsonStore """
    class __LastAccessJsonStore(JsonStore):
        # pylint: disable=invalid-name
        ID_FIELD = "_LastAccessKey__key"
        MARK_TIME = "_LastAccessKey__time"
        INVALID_ITEM = "Invalid item to be stored as a key"
        KEY_ALREADY_STORED = "key already found in storeRequest"

        _FILE_PATH = JSON_FILES_PATH + "storeLastKeys.json"
        _ID_FIELD = ID_FIELD

        def store_time_mark(self, key):
            """Method that obtains the mark time in order to add it to the dicc"""
            justnow = datetime.utcnow()
            dicc = {self._ID_FIELD: key, self.MARK_TIME: str(justnow)}
            super().add_item2(dicc)

    __instance = None

    def __new__(cls):
        if not LastAccessJsonStore.__instance:
            LastAccessJsonStore.__instance = LastAccessJsonStore.__LastAccessJsonStore()
        return LastAccessJsonStore.__instance

    def __getattr__(self, nombre):
        return getattr(self.__instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.__instance, nombre, valor)
