import json
from .simbolo import Simbolo

class TablaSimbolos:
    def __init__(self):
        self.simbolos = {}

    def agregar_simbolo(self, simbolo):
        self.simbolos[simbolo.lexema] = simbolo

    def buscar_simbolo(self, lexema):
        return self.simbolos.get(lexema)

    def obtener_todos_simbolos(self):
        """Retorna una lista con todos los símbolos"""
        return list(self.simbolos.values())

    def cargar_simbolos_iniciales(self, ruta_archivo: str):
        """Carga los símbolos iniciales desde un archivo JSON"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                for item in datos:
                    simbolo = Simbolo(
                        token=item['token'],
                        lexema=item['lexema'],
                        palabra_reservada=item['palabraReservada']
                    )
                    self.agregar_simbolo(simbolo)
        except FileNotFoundError:
            raise Exception(f"No se encontró el archivo de símbolos: {ruta_archivo}")
        except json.JSONDecodeError:
            raise Exception("Error al decodificar el archivo JSON de símbolos")
        except KeyError as e:
            raise Exception(f"Formato inválido en el archivo de símbolos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al cargar los símbolos: {str(e)}")