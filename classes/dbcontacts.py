from .contacts import Contact
from .dbcsv import DBbyCSV

SCHEMA = {
    'ID': {
        'type': 'autoincrement',
    },
    'NAME': {
        'type': 'string',
        'min_length': 3,
        'max_length': 40
    },
    'SURNAME': {
        'type': 'string',
        'min_length': 3,
        'max_length': 50
    },
    'EMAIL': {
        'type': 'string',
        'max_length': 254
    },
    'PHONE': {
        'type': 'int'
    },
    'BIRTHDAY': {
        'type': 'date'
    }
}

class DBContacts(DBbyCSV):
    def __init__(self):
        super().__init__(SCHEMA, 'contacts')

    def save_contacts(self, contact):
        data = [contact.name, contact.surname, contact.email, contact.phone, contact.birthday]
        return self.insert(data)