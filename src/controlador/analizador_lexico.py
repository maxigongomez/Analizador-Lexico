from typing import List, Optional, Tuple
from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos
from .automatas import Automatas

class AnalizadorLexico:
    def __init__(self, tabla_simbolos: TablaSimbolos):
        self.tabla_simbolos = tabla_simbolos
        self.automatas = Automatas()
        self.tokens = []
        self.errores = []
        self.linea_actual = 0
        self.caracteres_especiales = {
            'n': '\n',
            't': '\t',
            'r': '\r',
            '"': '"',
            "'": "'",
            '\\': '\\'
        }

    def analizar_codigo(self, contenido: str) -> List[Simbolo]:
        self.tokens = []
        self.errores = []
        self.linea_actual = 0
        
        lineas = contenido.split('\n')
        for linea in lineas:
            self.analizar_linea(linea.strip())
            self.linea_actual += 1
            
        return self.tokens

    def analizar_linea(self, linea: str) -> None:
        i = 0
        columna = 1 
        while i < len(linea):
            char = linea[i]

            if char.isspace():
                i += 1
                columna += 1
                continue

            if i < len(linea) - 1 and linea[i:i+2] == "//":
                break

            if char == '"':
                inicio_columna = columna
                self.tokens.append(Simbolo("DELIMITADOR", '"', True, self.linea_actual, inicio_columna))
                resultado = self._procesar_contenido_cadena(linea[i+1:])
                if resultado:
                    contenido, longitud = resultado
                    self.tokens.append(Simbolo("STRING", contenido, False, self.linea_actual, columna + 1))
                    i += longitud + 1
                    columna += longitud + 1
                    if i < len(linea) and linea[i] == '"':
                        self.tokens.append(Simbolo("DELIMITADOR", '"', True, self.linea_actual, columna))
                        i += 1
                        columna += 1
                    else:
                        self._agregar_error("Error léxico: cadena con comillas dobles no cerrada", columna)
                else:
                    self._agregar_error("Error léxico: cadena no válida", columna)
                    i += 1
                    columna += 1
                continue

            elif char == "'":
                inicio_columna = columna
                self.tokens.append(Simbolo("DELIMITADOR", "'", True, self.linea_actual, inicio_columna))
                
                if i + 1 < len(linea):
                    if linea[i+1] == '\\' and i + 2 < len(linea):
                        char_content = linea[i+1:i+3]
                        i += 3
                        columna += 3
                    else:
                        char_content = linea[i+1]
                        i += 2
                        columna += 2

                    self.tokens.append(Simbolo("CHAR", char_content, False, self.linea_actual, inicio_columna + 1))
                    
                    if i < len(linea) and linea[i] == "'":
                        self.tokens.append(Simbolo("COMILLA_SIMPLE", "'", True, self.linea_actual, columna))
                        i += 1
                        columna += 1
                    else:
                        self._agregar_error("Error léxico: carácter no cerrado", columna)
                else:
                    self._agregar_error("Error léxico: carácter no válido", columna)
                continue

            elif not char.isalnum() and char != '_':
                token = self._procesar_operador(linea[i:])
                if token:
                    token.columna = columna
                    self.tokens.append(token)
                    i += len(token.lexema)
                    columna += len(token.lexema)
                else:
                    self._agregar_error(f"Error léxico: carácter no reconocido '{char}'", columna)
                    i += 1
                    columna += 1
                continue

            palabra = ""
            inicio_columna = columna
            while i < len(linea) and (linea[i].isalnum() or linea[i] == '_'):
                palabra += linea[i]
                i += 1
                columna += 1

            if palabra:
                token = self._analizar_palabra(palabra)
                token.columna = inicio_columna
                self.tokens.append(token)
                continue

            i += 1
            columna += 1

    def _procesar_contenido_cadena(self, texto: str) -> Optional[Tuple[str, int]]:
        contenido = ""
        i = 0
        while i < len(texto):
            if texto[i] == '"':
                return contenido, i
            elif texto[i] == '\\' and i + 1 < len(texto):
                if texto[i+1] in self.caracteres_especiales:
                    contenido += texto[i:i+2]
                    i += 2
                    continue
            contenido += texto[i]
            i += 1
        return None

    def _procesar_operador(self, texto: str) -> Optional[Simbolo]:
        if len(texto) >= 2:
            op = texto[:2]
            simbolo = self.tabla_simbolos.buscar_simbolo(op)
            if simbolo:
                return Simbolo(simbolo.token, op, True, self.linea_actual)

        op = texto[0]
        simbolo = self.tabla_simbolos.buscar_simbolo(op)
        if simbolo:
            return Simbolo(simbolo.token, op, True, self.linea_actual)
        
        return None

    def _analizar_palabra(self, palabra: str) -> Simbolo:
        simbolo = self.tabla_simbolos.buscar_simbolo(palabra)
        if simbolo:
            return Simbolo(simbolo.token, palabra, True, self.linea_actual)

        if self.automatas.isReal(palabra):
            return Simbolo("REAL", palabra, False, self.linea_actual)
        if self.automatas.isNumero(palabra):
            return Simbolo("ENTERO", palabra, False, self.linea_actual)

        if self.automatas.isIdentificador(palabra):
            return Simbolo("ID", palabra, False, self.linea_actual)

        return Simbolo("ERROR", palabra, False, self.linea_actual)

    def _agregar_error(self, mensaje: str, columna: int) -> None:
        self.errores.append({
            'linea': self.linea_actual,
            'columna': columna,
            'mensaje': mensaje,
            'tipo': 'LEXICO'
        })

    def obtener_errores(self) -> List[dict]:
        return self.errores