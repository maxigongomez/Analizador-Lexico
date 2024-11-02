class Simbolo:
    def __init__(self, token: str, lexema: str, palabra_reservada: bool = False, linea: int = 0, columna: int = 0):
        self.token = token
        self.lexema = lexema
        self.palabra_reservada = palabra_reservada
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f'({self.token}, "{self.lexema}", línea {self.linea}, columna {self.columna})'

    def to_file_string(self):
        return f'({self.token}, "{self.lexema}", línea {self.linea}, columna {self.columna})'