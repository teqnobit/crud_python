import re 
import datetime

regex_email = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
regex_phone = "^[0-9]{10}$"

class Validations:

    def __init__(self):
        pass

    def validateName(self, name):
        if len(name) < 3 or len(name) > 50:
            raise ValueError(f"El nombre no puede ser menor a 2 caracteres ni mayor a 50, tamaño actual: {len(name)}")
        return True
    
    def validateSurname(self, surname):
        if len(surname) < 3 and len(surname) > 40:
            raise ValueError(f"El apellido no puede ser menor a 2 caracteres ni mayor a 40, tamaño actual: {len(surname)}")
        return True
    
    def validateEmail(self, email):
        if not re.search(regex_email, email):
            raise ValueError("Email no valido")
        return True
    
    def validatePhone(self, phone):
        if not re.search(regex_phone, phone):
            raise ValueError("Telefono no valido, intentelo nuevamente")
        return True
    
    def validateBirthday(self, birthday):
        try:
            datetime.datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Fecha no valida, intente el formato YYYY-MM-DD")
        return True