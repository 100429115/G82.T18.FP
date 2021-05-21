"""Module for revoke key tests"""
import unittest
import csv
from secure_all import AccessManager, AccessManagementException, \
    JSON_FILES_PATH, RequestJsonStore, AccessKey
from secure_all.storage.revoke_key_store import RevokeKeyJsonStore
from secure_all.storage.keys_json_store import KeysJsonStore


class TestAccessManager(unittest.TestCase):
    """Test class for testing revoke_key"""

    @classmethod
    def setUpClass(cls) -> None:
        """Removing the Stores and creating required AccessRequest for testing"""
        # pylint: disable=no-member

        requests_store = RequestJsonStore()
        requests_store.empty_store()
        keys_store = KeysJsonStore()
        keys_store.empty_store()

        my_manager = AccessManager()
        # Valores a usar para la clave estandar
        my_manager.request_access_code("05270358T", "Pedro Martin",
                                       "Resident", "uc3m@gmail.com", 0)
        # introduce a key valid and expiration date = 0 , resident
        my_manager.get_access_key(JSON_FILES_PATH + "key_ok3_resident.json")

        # Valores a usar para la clave expirada
        my_manager.request_access_code("68026939T", "Juan Perez",
                                       "Guest", "expired@gmail.com", 2)
        # expected result 383a8eb306459919ef0dc819405f16a6
        # We generate the AccessKey for this AccessRequest
        my_key_expirated = AccessKey.create_key_from_file(JSON_FILES_PATH +
                                                          "key_ok_testing_expired.json")
        # We manipulate the expiration date to obtain an expired AccessKey
        my_key_expirated.expiration_date = 0
        my_key_expirated.store_keys()

    print("one")

    def test_invalid_format_key(self):
        """Testing not format key"""
        with self.assertRaises(AccessManagementException) as c_m:
            my_manager = AccessManager()
            my_manager.revoke_key(JSON_FILES_PATH + "clase_eq_key_nostr.json")
        self.assertEqual(c_m.exception.message, "key invalid")

    print("two")

    def test_invalid_format_revocation(self):
        """Testing not format revocation"""
        with self.assertRaises(AccessManagementException) as c_m:
            my_manager = AccessManager()
            my_manager.revoke_key(JSON_FILES_PATH + "clase_eq_revo_notstr.json")
        self.assertEqual(c_m.exception.message, "revocation is not valid")

    print("three")

    def test_invalid_format_reason(self):
        """Testing not format reason"""
        with self.assertRaises(AccessManagementException) as c_m:
            my_manager = AccessManager()
            my_manager.revoke_key(JSON_FILES_PATH + "clase_eq_reason_nostr.json")
        self.assertEqual(c_m.exception.message, "reason is not valid")

    print("Four")

    # Como no se ha vaciado todavía, permanece
    # key= "de000a04f3a9b1d15b07e38b166f00f3fb1bf46533f32ac37156faf43e47f722",
    def test_already_revoked_key(self):
        """Testing a key that is already revoked"""
        with self.assertRaises(AccessManagementException) as c_m:
            my_manager = AccessManager()
            my_manager.revoke_key(JSON_FILES_PATH + "graf_key_revoke.json")
        self.assertEqual(c_m.exception.message, "key already found in RevokeKeyJson")

    print("five")

    def test_expired_key(self):
        """Testing that the key is expired"""
        with self.assertRaises(AccessManagementException) as c_m:
            my_manager = AccessManager()
            my_manager.revoke_key(JSON_FILES_PATH + "graf_key_expired.json")
        self.assertEqual(c_m.exception.message, "key is not found or is expired")

    print("Finished init")

    def test_parametrized_cases_tests(self):
        """Parametrized cases read from testingCases_RF4.csv"""
        my_cases = JSON_FILES_PATH + "testingCases_RF4.csv"
        with open(my_cases, newline='', encoding='utf-8') as csvfile:
            param_test_cases = csv.DictReader(csvfile, delimiter=';')
            my_code = AccessManager()
            for row in param_test_cases:
                revoke_store = RevokeKeyJsonStore()
                revoke_store.empty_store()
                print("Param:" + row['ID TEST'] + row["VALID INVALID"])
                if row["VALID INVALID"] == "VALID":
                    valor = my_code.revoke_key(JSON_FILES_PATH + row['FILE'])
                    self.assertEqual(row['EXPECTED RESULT'], valor)

                else:
                    with self.assertRaises(AccessManagementException) as c_m:
                        valor = my_code.revoke_key(JSON_FILES_PATH + row['FILE'])
                    self.assertEqual(c_m.exception.message, row['EXPECTED RESULT'])


if __name__ == '__main__':
    unittest.main()
