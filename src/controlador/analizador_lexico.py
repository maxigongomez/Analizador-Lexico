from typing import List
from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos
from .automatas import Automatas

class AnalizadorLexico:
    def __init__(self, tabla_simbolos: TablaSimbolos):
        self.tabla_simbolos = tabla_simbolos
        self.automatas = Automatas()
        self.buffer = ""
        self.linea_actual = 1
        self.columna_actual = 1
        self.special_chars = "+-*/(){};,="

    def analizar_linea(self, texto: str) -> List[Simbolo]:
        tokens = []
        self.buffer = ""
        i = 0
        
        while i < len(texto):
            char = texto[i]
            
            if char.isspace():
                if self.buffer:
                    tokens.extend(self._analizar_buffer())
                i += 1
                self.columna_actual += 1
                continue

            if char == '/' and i + 1 < len(texto) and texto[i + 1] == '/':
                if self.buffer:
                    tokens.extend(self._analizar_buffer())
                comentario = "//"
                i += 2
                while i < len(texto):
                    comentario += texto[i]
                    i += 1
                tokens.append(Simbolo("COMENTARIO", comentario, False))
                continue

            if char == "'":
                i = self._procesar_caracter(tokens, texto, i)
                continue

            if char == '-' and i + 1 < len(texto) and texto[i + 1].isdigit():
                i = self._procesar_numero_negativo(tokens, texto, i)
                continue

            if char in self.special_chars:
                if self.buffer:
                    tokens.extend(self._analizar_buffer())
                tokens.extend(self._analizar_lexema(char))
                i += 1
                self.columna_actual += 1
                continue

            if char == '"':
                i = self._procesar_cadena(tokens, texto, i)
                continue

            self.buffer += char
            i += 1
            self.columna_actual += 1
            
        if self.buffer:
            tokens.extend(self._analizar_buffer())
            
        return tokens

    def _procesar_caracter(self, tokens: List[Simbolo], texto: str, i: int) -> int:
        if self.buffer:
            tokens.extend(self._analizar_buffer())
        
        contenido = "'"
        i += 1
        
        if i < len(texto):
            if texto[i] == '\\':
                contenido += texto[i]
                i += 1
                if i < len(texto):
                    contenido += texto[i]
                    i += 1
            else:
                contenido += texto[i]
                i += 1

            if i < len(texto) and texto[i] == "'":
                contenido += texto[i]
                tokens.append(Simbolo("CARACTER", contenido, False))
                i += 1
            else:
                tokens.append(Simbolo("ERROR", "Caracter no cerrado", False))
        else:
            tokens.append(Simbolo("ERROR", "Caracter no cerrado", False))
        
        return i

    def _procesar_numero_negativo(self, tokens: List[Simbolo], texto: str, i: int) -> int:
        if self.buffer:
            tokens.extend(self._analizar_buffer())
        
        num_buffer = "-"
        i += 1
        
        while i < len(texto) and (texto[i].isdigit() or texto[i] == '.'):
            num_buffer += texto[i]
            i += 1
            
        if self.automatas.isReal(num_buffer):
            tokens.append(Simbolo("REAL", num_buffer, False))
        elif self.automatas.isNumero(num_buffer):
            tokens.append(Simbolo("ENTERO", num_buffer, False))
            
        return i

    def _procesar_cadena(self, tokens: List[Simbolo], texto: str, i: int) -> int:
        if self.buffer:
            tokens.extend(self._analizar_buffer())
            
        inicio_columna = self.columna_actual
        contenido = '"'
        i += 1
        self.columna_actual += 1
        
        while i < len(texto) and texto[i] != '"':
            contenido += texto[i]
            i += 1
            self.columna_actual += 1
            
        if i < len(texto):
            contenido += texto[i]
            tokens.append(Simbolo("CADENA", contenido, False))
            i += 1
            self.columna_actual += 1
        else:
            tokens.append(Simbolo("ERROR", f"Cadena no cerrada en línea {self.linea_actual}, columna {inicio_columna}", False))
            
        return i

    def _analizar_buffer(self) -> List[Simbolo]:
        tokens = self._analizar_lexema(self.buffer)
        self.buffer = ""
        return tokens

    def _analizar_lexema(self, lexema: str) -> List[Simbolo]:
        simbolo = self.tabla_simbolos.buscar_simbolo(lexema)
        if simbolo:
            return [simbolo]

        if self.automatas.isIdentificador(lexema):
            nuevo_simbolo = Simbolo("ID", lexema, False)
            self.tabla_simbolos.agregar_simbolo(nuevo_simbolo)
            return [nuevo_simbolo]
        
        if self.automatas.isReal(lexema):
            return [Simbolo("REAL", lexema, False)]
        
        if self.automatas.isNumero(lexema):
            return [Simbolo("ENTERO", lexema, False)]

        if lexema.isalnum():
            return [Simbolo("ERROR", f"Token inválido '{lexema}'", False)]

        return [Simbolo("ERROR", f"Token no reconocido '{lexema}' en línea {self.linea_actual}, columna {self.columna_actual}", False)]