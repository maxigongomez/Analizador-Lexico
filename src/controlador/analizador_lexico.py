from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos
from .automatas import Automatas
from typing import List

class AnalizadorLexico:
    def __init__(self, tabla_simbolos: TablaSimbolos):
        self.tabla_simbolos = tabla_simbolos
        self.automatas = Automatas()
        self.buffer = ""
        self.linea_actual = 1
        self.columna_actual = 1

    def analizar_linea(self, linea: str) -> List[Simbolo]:
        tokens = []
        self.buffer = ""
        i = 0
        
        while i < len(linea):
            char = linea[i]
            
            # Ignorar espacios y tabulaciones
            if char.isspace():
                if self.buffer:
                    tokens.extend(self.analizar_lexema(self.buffer))
                    self.buffer = ""
                i += 1
                continue
                
            # Manejar operadores y símbolos especiales
            if char in "+-*/(){};,=":
                if self.buffer:
                    tokens.extend(self.analizar_lexema(self.buffer))
                    self.buffer = ""
                tokens.extend(self.analizar_lexema(char))
                i += 1
                continue
                
            # Manejar cadenas entre comillas
            if char == '"':
                if self.buffer:
                    tokens.extend(self.analizar_lexema(self.buffer))
                    self.buffer = ""
                temp = char
                i += 1
                while i < len(linea) and linea[i] != '"':
                    temp += linea[i]
                    i += 1
                if i < len(linea):
                    temp += linea[i]
                    tokens.append(Simbolo("CADENA", temp, False))
                i += 1
                continue
                
            self.buffer += char
            i += 1
            
        if self.buffer:
            tokens.extend(self.analizar_lexema(self.buffer))
            
        return tokens

    def analizar_lexema(self, lexema: str) -> List[Simbolo]:
        # Buscar primero en la tabla de símbolos
        simbolo = self.tabla_simbolos.buscar_simbolo(lexema)
        if simbolo:
            return [simbolo]
            
        # Si no está en la tabla, analizar con los autómatas
        if self.automatas.isIdentificador(lexema):
            nuevo_simbolo = Simbolo("ID", lexema, False)
            self.tabla_simbolos.agregar_simbolo(nuevo_simbolo)
            return [nuevo_simbolo]
        elif self.automatas.isReal(lexema):
            return [Simbolo("REAL", lexema, False)]
        elif self.automatas.isNumero(lexema):
            return [Simbolo("ENTERO", lexema, False)]
            
        # Si no se reconoce, marcar como error
        return [Simbolo("ERROR", lexema, False)]