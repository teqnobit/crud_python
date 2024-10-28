import os
import time
from classes.validations import Validations
from classes.dbcontacts import DBContacts
from classes.contacts import Contact
from prettytable import PrettyTable

validator = Validations()
db = DBContacts()

def print_options():
    print("AGENDA DE CONTACTOS")
    print("*" * 50)
    print("--Menu--")
    print("[C]rear contacto")
    print("[L]istado de contactos")
    print("[M]odificar contacto")
    print("[E]liminar contacto")
    print("[B]uscar contacto")
    print("[S]alir")

def run():
    print_options()

    command = input("Selecciona una opcion: ")
    command = command.upper()

    if command == "C":
        create_contact()
    elif command == "L":
        list_contacts()
    elif command == "M":
        pass
    elif command == "E":
        pass
    elif command == "B":
        pass
    elif command == "S":
        print("GoodBye :)")
        os._exit(1)
    else:
        print("Comando invalido")
        time.sleep(1)
    run()

def create_contact():
    print("CREACION DE CONTACTO")
    print("*" * 50)
    name = check_contact_name("Introduce el nombre:", "name")
    surname = check_contact_name("Introduce el apellido:", "surname")
    email = check_contact_name("Introduce el email:", "email")
    phone = check_contact_name("Introduce el telefono (solo 10 digitos sin espacios ni guiones):", "phone")
    birthday = check_contact_name("Introduce la fecha de nacimiento (YYYY-MM-DD):", "birthday")

    contact = Contact(None, name, surname, email, phone, birthday)
    if db.save_contacts(contact):
        print("Contacto ingresado exitosamente")
    else:
        print("Error al guardar el contacto")

### Se puede simplificar, mirar mas abajo
""" Funciones check_contact
def check_name():
    print("Introduce el nombre del usuario:")
    name = input()
    try:
        validator.validateName(name)
        return name
    except ValueError as err:
        print(err)
        check_name()
    
def check_surname():
    print("Introduce el apellido del usuario:")
    surname = input()
    try:
        validator.validateSurname(surname)
        return surname
    except ValueError as err:
        print(err)
        check_surname()
    
def check_email():
    print("Introduce el email del usuario:")
    email = input()
    try:
        validator.validateEmail(email)
        return email
    except ValueError as err:
        print(err)
        check_email()
    
def check_phone():
    print("Introduce el telefono del usuario (solo 10 digitos sin espacios ni guiones):")
    phone = input()
    try:
        validator.validatePhone(phone)
        return phone
    except ValueError as err:
        print(err)
        check_phone()
    
def check_birthday():
    print("Introduce la fecha de nacimiento del usuario (YYYY-MM-DD):")
    birthday = input()
    try:
        validator.validateBirthday(birthday)
        return birthday
    except ValueError as err:
        print(err)
        check_birthday()
"""
### Las instrucciones anteriores se pueden simplificar con la siguiente
def check_contact_name(message, data_name):
    print(message)
    input_data = input()
    try:
        getattr(validator, f"validate{data_name.capitalize()}")(input_data)
        # getattr es metodo que se utiliza par invocar metodos de forma dinamica; recibe almenos dos parametros
        # el primero es el metodo que se desea ejecutar
        # el segundo es el nombre del metodo que se desea ejecutar
        # al final se agrega entre parentesis la informacion que espera recibir los parametros del metodo nombrado
        return input_data
    except ValueError as err:
        print(err)
        check_contact_name(message, data_name)
    
def list_contacts():
    list_contacts = db.list_contacts()

    if not list_contacts:
        print("Aun no hay contactos registrados")

    table = PrettyTable(db.get_schema().keys())
    for contact in list_contacts:
        table.add_row([
            contact.id_contact,
            contact.name,
            contact.surname,
            contact.email,
            contact.phone,
            contact.birthday
        ])

    print(table)
    print("Pulsa intro para salir")
    command = input()

if __name__ == "__main__":
    run()

    