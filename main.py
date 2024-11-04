import os
import time
from classes.validations import Validations
from classes.dbcontacts import DBContacts
from classes.contacts import Contact
from prettytable import PrettyTable

validator = Validations()
db = DBContacts()

### Imprimir Menu
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

### Menu de acciones
def run():
    print_options()

    command = input("Selecciona una opcion: ")
    command = command.upper()

    if command == "C":
        create_contact()
    elif command == "L":
        list_contacts()
    elif command == "M":
        update_contact()
    elif command == "E":
        delete_contact()
    elif command == "B":
        search_contact()
    elif command == "S":
        print("GoodBye :)")
        os._exit(1)
    else:
        print("Comando invalido")
        time.sleep(1)
    run()

### Funciones auxiliares
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

# Forma dinamica de ejecutar metodos de nombre similar
def check_contact_name(message, data_name, force = True):
    print(message)
    input_data = input()
    
    if not force and not input_data:
        return # Por si se deja el input vacio (ya que en el update no cambiara todo el registro)

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

# El siguiente bloque de codigo fue remplazo por la funcion anterior
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
    
def list_contacts():
    list_contacts = db.list_contacts()

    if not list_contacts:
        print("Aun no hay contactos registrados")

    _print_table_contacts(list_contacts)
    """ Remplazado por la funcion _print_table_contacts()
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
    print("Pulsa cualquier tecla para continuar")
    command = input()
    """

def search_contact():
    filters = {}

    print("Buscar nombre (dejar vacio para usar otro filtro): ")
    nombre = input()
    if nombre:
        filters["NAME"] = nombre

    print("Buscar apellido (dejar vacio para usar otro filtro): ")
    apellido = input()
    if apellido:
        filters["SURNAME"] = apellido

    print("Buscar email (dejar vacio para usar otro filtro): ")
    correo = input()
    if correo:
        filters["EMAIL"] = correo

    try:
        list_contacts = db.search_users(filters)
        if not list_contacts:
            return print("No hay ningun contacto con esos criterios de busqueda")
        
        _print_table_contacts(list_contacts)
    except ValueError as err:
        print(err)
        time.sleep(1)
        search_contact()

def update_contact():

    list_contacts()

    print("Introduce el id del contacto que desea modificar")
    id_object = input()

    data = {}
    nombre = check_contact_name("Introduce nombre a modificar (deja vacio para no modificar)", "name", False)
    if nombre:
        data["NAME"] = nombre
    apellido = check_contact_name("Introduce apellido a modificar (deja vacio para no modificar)", "surname", False)
    if apellido:
        data["SURNAME"] = apellido
    correo = check_contact_name("Introduce correo a modificar (dejar vacio para no modificar)", "email", False)
    if correo:
        data["EMAIL"] = correo
    telefono = check_contact_name("Introduce telefono a modificar (dejar vacio para no modificar)", "phone", False)
    if telefono:
        data["PHONE"] = telefono
    cumple = check_contact_name("Introduce cumpleaños a modificar YYYY-MM-DD (dejar vacio para no modificar)", "birthday", False)
    if cumple:
        data["BIRTHDAY"] = cumple

    try:
        res = db.update(id_object, data)
        if res:
            print("Contacto actuaizado con exito")
    except Exception as err:
        print(err)
        time.sleep(1)
        update_contact()

def delete_contact():
    list_contacts()

    print("Introduce el id del contacto que desea eliminar: ")
    id_object = input()
    try:
        res = db.delete_contact(id_object)
        if res:
            print("Contacto eliminado con exito")
    except Exception as err:
        print(err)
        time.sleep(1)
        delete_contact()

def _print_table_contacts(list_contacts):
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
    # print("Pulsa cualquier tecla para continuar")
    # command = input()

if __name__ == "__main__":
    run()

    