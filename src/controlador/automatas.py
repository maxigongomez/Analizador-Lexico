class Automatas:
    @staticmethod
    def isIdentificador(cadena: str) -> bool:
        if not cadena:
            return False
        # Un identificador debe comenzar con letra y puede contener letras, números o _
        if not cadena[0].isalpha():
            return False
        return all(c.isalnum() or c == '_' for c in cadena)

    @staticmethod
    def isNumero(cadena: str) -> bool:
        try:
            int(cadena)
            return True
        except ValueError:
            return False

    @staticmethod
    def isReal(cadena: str) -> bool:
        try:
            float(cadena)
            return '.' in cadena
        except ValueError:
            return False