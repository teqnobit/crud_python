import unittest
from classes.contacts import Contact
from classes.dbcontacts import DBContacts

"""
Para ejecutar los tests es importante que la carpeta (modulo) empiece con el nombre "tests", los
archivos empiecen con nombre "test", las clases empiecen con nombre "Test" y las funciones con nombre "test".

Para correr las pruebas, en la consola hay que ejecutar el comando:
    python -m unittest tests/test_dbcontacts.py --verbose
"""

# Para las pruebas unitarias, las clases y funciones deben empesar por test
class TestDBContacts(unittest.TestCase):
    
    # setUp declara funcionalidades antes de que empiece el test
    def setUp(self):
        self.db = DBContacts(True)
        self.db.save_contacts(self._object_contact())

    def _object_contact(self):
        return Contact(None, "Usertest", "User Test", "user@test.com", "1234567890", "2000-01-01")
    
    def _dict_contact(self):
        return {
            "name": "Usertest2",
            "surname": "User Test2",
            "email": "user2@test.com",
            "phone": 9876543210,
            "birthday": "2000-12-12"
        }
    

    def test_save_contact(self):
        result = self.db.save_contacts(self._object_contact())
        self.assertEqual(result, 1)

    def test_update_contact(self):
        contact = self._dict_contact()
        last_id = self.db.get_last_id()

        result = self.db.update_contact(last_id, contact)
        self.assertNotEqual(result, 0)  # update_contact cuando no modifica ninguna celda regresa 0 (por el cursor.rowcount)

        ddbb_contact = self.db.get_by_id(last_id)

        # Verificamos que todas las modificaciones se hayan ejecutado correctamente
        self.assertEqual(contact["name"], ddbb_contact["name"])
        self.assertEqual(contact["surname"], ddbb_contact["surname"])
        self.assertEqual(contact["email"], ddbb_contact["email"])
        self.assertEqual(contact["phone"], ddbb_contact["phone"])
        self.assertEqual(contact["birthday"], ddbb_contact["birthday"].strftime("%Y-%m-%d"))

    def test_get_contact(self):
        last_id = self.db.get_last_id()

        contact = self.db.get_by_id(last_id)
        self.assertNotEqual(contact, {})

        my_contact = self._object_contact()
        self.assertEqual(contact["name"], my_contact.name)
        self.assertEqual(contact["surname"], my_contact.surname)
        self.assertEqual(contact["email"], my_contact.email)
        self.assertEqual(str(contact["phone"]), my_contact.phone)
        self.assertEqual(contact["birthday"].strftime("%Y-%m-%d"), my_contact.birthday)

    def test_search_user(self):
        # last_id = self.db.get_last_id()

        my_contact = self._object_contact()
        filters = {
            "name": my_contact.name,
            "surname": my_contact.surname,
            "email": my_contact.email
        }

        list_contacts = self.db.search_contacts(filters)
        self.assertNotEqual(list_contacts, [])
        for contact in list_contacts:
            self.assertIsInstance(contact, Contact)
            self.assertEqual(contact.name, my_contact.name)
            self.assertEqual(contact.surname, my_contact.surname)
            self.assertEqual(contact.email, my_contact.email)
            self.assertEqual(str(contact.phone), my_contact.phone)
            self.assertEqual(contact.birthday.strftime("%Y-%m-%d"), my_contact.birthday)
            break
    
    def test_list_contacts(self):
        list_contacts = self.db.list_contacts()
        self.assertNotEqual(list_contacts, [])

        for contact in list_contacts:
            self.assertIsInstance(contact, Contact)

    def test_remove_contact(self):
        last_id = self.db.get_last_id()

        self.assertEqual(self.db.delete_contact(last_id), 1)
        contact = self.db.get_by_id(last_id)
        self.assertEqual(contact, {})
        

    if __name__ == "__main__":
        unittest.main()