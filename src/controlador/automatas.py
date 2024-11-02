class Automatas:
    @staticmethod
    def isIdentificador(cadena: str) -> bool:
        if not cadena:
            return False
        if not cadena[0].isalpha():
            return False
        return all(c.isalnum() or c == '_' for c in cadena[1:])

    @staticmethod
    def isNumero(cadena: str) -> bool:
        if not cadena:
            return False
        if cadena[0] == '-':
            if len(cadena) == 1:
                return False
            return cadena[1:].isdigit()
        return cadena.isdigit()

    @staticmethod
    def isReal(cadena: str) -> bool:
        try:
            if not cadena or cadena == '.':
                return False
            float(cadena)
            return '.' in cadena
        except ValueError:
            return False