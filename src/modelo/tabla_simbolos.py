import json
import os
from .simbolo import Simbolo
from typing import Dict, List, Optional

class TablaSimbolos:
    def __init__(self, ruta_json: str = None):
        self.simbolos: Dict[str, Simbolo] = {}
        
        if ruta_json and os.path.exists(ruta_json):
            self.cargar_desde_archivo(ruta_json)
        else:
            self._inicializar_tabla()

    def _inicializar_tabla(self):
        simbolos_iniciales = [
            ("PALABRA_RESERVADA", "programa", True),
            ("PALABRA_RESERVADA", "int", True),
            ("PALABRA_RESERVADA", "float", True),
            ("PALABRA_RESERVADA", "char", True),
            ("PALABRA_RESERVADA", "leer", True),
            ("PALABRA_RESERVADA", "imprimir", True),
            ("PALABRA_RESERVADA", "terminar", True),
            ("DELIMITADOR", "(", True),
            ("DELIMITADOR", ")", True),
            ("DELIMITADOR", "{", True),
            ("DELIMITADOR", "}", True),
            ("SIMBOLO_PUNTUACION", ",", True),
            ("SIMBOLO_PUNTUACION", ";", True),
            ("OPERADOR_ARITMETICO", "+", True),
            ("OPERADOR_ARITMETICO", "-", True),
            ("OPERADOR_ARITMETICO", "*", True),
            ("OPERADOR_ARITMETICO", "/", True),
            ("OPERADOR_ASIGNACION", "=", True),
            ("DELIMITADOR", "\"", True),
            ("DELIMITADOR", "'", True)
        ]
        
        for token, lexema, es_reservada in simbolos_iniciales:
            self.agregar_simbolo(Simbolo(token, lexema, es_reservada))

    def cargar_desde_archivo(self, ruta_archivo: str):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.simbolos.clear()
                for simbolo in datos['simbolos']:
                    self.agregar_simbolo(Simbolo(
                        simbolo['token'],
                        simbolo['lexema'],
                        simbolo['palabraReservada']
                    ))
        except Exception as e:
            raise Exception(f"Error al cargar tabla de símbolos: {str(e)}")

    def agregar_simbolo(self, simbolo):
        self.simbolos[simbolo.lexema] = simbolo

    def buscar_simbolo(self, lexema):
        return self.simbolos.get(lexema)

    def obtener_todos_simbolos(self):
        return list(self.simbolos.values())