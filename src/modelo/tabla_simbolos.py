import json
from .simbolo import Simbolo
from typing import Dict, List, Optional

class TablaSimbolos:
    def __init__(self):
        self.simbolos: Dict[str, Simbolo] = {}

    def agregar_simbolo(self, simbolo: Simbolo) -> None:
        """Agrega un símbolo a la tabla"""
        self.simbolos[simbolo.lexema] = simbolo

    def buscar_simbolo(self, lexema: str) -> Optional[Simbolo]:
        """Busca un símbolo por su lexema"""
        return self.simbolos.get(lexema)

    def obtener_todos_simbolos(self) -> List[Simbolo]:
        """Retorna una lista con todos los símbolos"""
        return list(self.simbolos.values())

    def cargar_simbolos_iniciales(self, ruta_archivo: str) -> None:
        """Carga los símbolos iniciales desde un archivo JSON"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                for item in datos['simbolos']:
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