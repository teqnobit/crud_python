from .contacts import Contact
# from .dbcsv import DBbyCSV
from .dbpostgresql import DBPostgresql

SCHEMA = {
    'id': {
        'type': 'autoincrement',
    },
    'name': {
        'type': 'string',
        'min_length': 3,
        'max_length': 40
    },
    'surname': {
        'type': 'string',
        'min_length': 3,
        'max_length': 50
    },
    'email': {
        'type': 'string',
        'max_length': 254
    },
    'phone': {
        'type': 'bigint'
    },
    'birthday': {
        'type': 'date'
    }
}

class DBContacts(DBPostgresql):
    def __init__(self, is_test = False):
        table_name = "contacts"
        super().__init__(SCHEMA, table_name, is_test)
        
    def save_contacts(self, contact):
        data = {
            "name":contact.name, 
            "surname":contact.surname, 
            "email":contact.email, 
            "phone":contact.phone, 
            "birthday":contact.birthday
        }
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
    
    def search_contacts(self, filters):
        if not filters:
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
                contact["id"], 
                contact["name"],
                contact["surname"],
                contact["email"],
                contact["phone"],
                contact["birthday"]
            )
            object_contacts.append(c)

        return object_contacts
    
    def update_contact(self, id_object, data):
        if not id_object:
            raise ValueError("Es necesario proporcionar un id de usuario")
        if not data:
            raise ValueError("Es necesario enviar almenos un parametro a actualizar")
        return self.update(id_object, data)

    def delete_contact(self, id_object):
        if not id_object:
            raise ValueError("Es necesario proporcionar un id")
        return self.delete(id_object)

    def get_schema(self):
        return SCHEMA