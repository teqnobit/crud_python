class Contact:

    ## Constructor
    def __init__(self, id_contact, name, surname, email, phone, birthday):
        self._id_contact = id_contact
        self._name = name
        self._surname = surname
        self._email = email
        self._phone = phone
        self._birthday = birthday

    ## Getters y Setters
    @property # @property convierte una funciona en una funcion de solo lectura (getter)
    def id_contact(self):
        return self._id_contact

    @id_contact.setter
    def id_contact(self, id_contact):
        self._id_contact = id_contact

    @property 
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def surname(self):
        return self._surname
    
    @surname.setter
    def surname(self, surname):
        self._surname = surname

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def birthday(self):
        return self._birthday
    
    @birthday.setter
    def birthday(self, birthday):
        self._birthday = birthday

