class Simbolo:
    def __init__(self, token: str, lexema: str, palabra_reservada: bool = False):
        self.token = token
        self.lexema = lexema
        self.palabra_reservada = palabra_reservada

    def __str__(self):
        return f"Token: {self.token}, Lexema: {self.lexema}, Reservada: {self.palabra_reservada}"

    def __eq__(self, other):
        if not isinstance(other, Simbolo):
            return False
        return (self.token == other.token and 
                self.lexema == other.lexema and 
                self.palabra_reservada == other.palabra_reservada)