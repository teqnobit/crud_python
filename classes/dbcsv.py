import csv
import re
from tempfile import NamedTemporaryFile
import shutil

class DBbyCSV:
    def __init__(self, schema, filename):
        self._filename = f"./{filename}.csv"
        try:
            # Verificamos si ya existe el archivo
            f = open(self._filename)
            f.close()
        except IOError:
            # Si el archivo no existe crearemos la cabecera
            with open(self._filename, mode="w", encoding="utf-16") as csv_file:
                data_writer = csv.writer(csv_file, delimiter=";", quotechar="\"", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
                data_writer.writerow(schema.keys())

    def insert(self, data):
        id_contact = self.get_last_id() + 1
        line = [id_contact] + data

        with open(self._filename, mode="a", encoding="utf-16") as csv_file:
            data_writer = csv.writer(  # metodo writer permite escribir en el archivo usando el formato de csv
                csv_file, 
                delimiter=";", 
                quotechar="\"", # Cada cadena de texto estara delimitada por comillas dobles (")
                quoting=csv.QUOTE_MINIMAL, # Constante que define CUANDO los datos del csv deben ir encerrados entre comillas de forma automatica
                lineterminator="\n"
            )
            data_writer.writerow(line)

        return True

    def get_last_id(self):
        list_ids = []
        with open(self._filename, mode="r", encoding="utf-16") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            is_header = True
            for row in csv_reader:
                if is_header:
                    is_header = False
                    continue

                if row:
                    list_ids.append(row[0])

        if not list_ids:
            return 0
        
        list_ids.sort(reverse=True)
        return int(list_ids[0])
    
    def get_all(self):
        list_data = []
        list_header = []

        with open(self._filename, mode="r", encoding="utf-16") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    continue

                if row:
                    file = {} # Diccionario de pares headers-valores
                    for key, value in enumerate(row):
                        file[list_header[key]] = value

                    list_data.append(file)

        return list_data
    
    def get_by_filter(self, filters):
        list_data = []
        list_header = []

        with open(self._filename, mode="r", encoding="utf-16") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    continue

                if row:
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value

                    for key_filter, value_filter in filters.items():
                        matches = re.search(rf"{value_filter}", rf"{file[key_filter]}", re.IGNORECASE)
                        if matches:
                            list_data.append(file)
                            break
        #with csv_file
        return list_data
    
    def get_by_id(self, id_object):
        list_header = []
        with open(self._filename, mode="r", encoding="utf-16") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    continue

                if row:
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    if file["ID"] == id_object:
                        return file
        return {}
    
    def update(self, id_object, data):
        return self.modify_file(id_object, data, "update")
    
    def delete(self, id_object):
        return self.modify_file(id_object, {}, "delete")
    
    def modify_file(self, id_object, data, action):
        data_csv = self.get_by_id(id_object)

        if not data_csv:
            raise Exception("No se ha encontrado el usuario con el id solicitado")
        
        for key, value in data.items():
            # Modificamos la busqueda con los datos solicitados
            data_csv[key] = value

        # Nuevo conocimiento #
        tempfile = NamedTemporaryFile(mode="w", delete=False, encoding="utf-16")

        list_header = []
        with open(self._filename, mode="r", encoding="utf-16") as csv_file, tempfile:
            csv_reader = csv.reader(csv_file, delimiter=";")
            data_writer = csv.writer(tempfile, delimiter=";", quotechar="\"", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)

            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    data_writer.writerow(row)
                    continue

                if row and action == "update":
                    file = {}
                    ## Crear el diccionario con los datos de csv
                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    ## Reescribir en el tempfile(file) todo lo del csv menos el id buscado(data_csv)
                    if file["ID"] != data_csv["ID"]:
                        data_writer.writerow(row)
                        continue
                    ## agregar lo que cambia al diccionario
                    for key, value in data_csv.items():
                        file[key] = value

                    ## Reescribir todo el tempfile con el diccionario completo (ya con cambios)
                    data_writer.writerow(file.values())

                elif row and action == "delete":
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    # si es delete simplemente nos saltamos el reinsertar la linea
                    if file["ID"] == data_csv["ID"]:
                        continue
                    data_writer.writerow(file.values())

        # Libreria shutil para realizar comando de consola
        # Le asignamos al archivo temporal el nombre de la db, por lo que:
        #   - tempfile obtiene el nombre de contacts.csv
        #   - contacts.csv (viejo) se sobreescribe por el nuevo
        #   - tempfile deja de ser un arhivo temporal (ya que ahora es otro archivo)
        shutil.move(tempfile.name, self._filename)
        return True