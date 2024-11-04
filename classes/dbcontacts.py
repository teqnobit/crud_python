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
    
    def list_contacts(self):
        list_contacts = self.get_all()
        return self._create_object_contacts(list_contacts)
        
        """ Se remplazo por el metodo _create_object_contacts
        object_contacts = []
        # Convertimos los datos objetos de tipo Contact
        for contact in list_contacts:
            c = Contact(
                contact["ID"], 
                contact["NAME"], 
                contact["SURNAME"], 
                contact["EMAIL"],
                contact["PHONE"],
                contact["BIRTHDAY"]
            )
            object_contacts.append(c)

        return object_contacts
        """
    
    def search_users(self, filters):
        if 'NAME' not in filters and 'SURNAME' not in filters and 'EMAIL' not in filters:
            raise ValueError("Debes enviar al menos un filtro")
        
        list_contacts = self.get_by_filter(filters)
        return self._create_object_contacts(list_contacts)
    
    def _create_object_contacts(self, list_contacts):
        if not list_contacts:
            return None
        
        object_contacts = []
        # convertirmos los datos a objetos de tipo Contact
        for contact in list_contacts:
            c = Contact(
                contact["ID"], 
                contact["NAME"],
                contact["SURNAME"],
                contact["EMAIL"],
                contact["PHONE"],
                contact["BIRTHDAY"]
            )
            object_contacts.append(c)

        return object_contacts
    
    def update_contact(self, id_object, data):
        if not id_object:
            raise ValueError("Es necesario proporcionar un id de usuario")
        if not data:
            raise ValueError("Es necesario enviar almenos un parametro a actualizar")
        self.update(id_object, data)

    def delete_contact(self, id_object):
        if not id_object:
            raise ValueError("Es necesario proporcionar un id")
        self.delete(id_object)

    def get_schema(self):
        return SCHEMA