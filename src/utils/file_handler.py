import os
from typing import List, Dict
from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos

class FileHandler:
    @staticmethod
    def crear_directorio_salida(ruta_entrada: str) -> str:
        directorio = os.path.dirname(ruta_entrada)
        nombre_base = os.path.splitext(os.path.basename(ruta_entrada))[0]
        dir_salida = os.path.join(directorio, f"{nombre_base}_salida")
        
        if not os.path.exists(dir_salida):
            os.makedirs(dir_salida)
        
        return dir_salida

    @staticmethod
    def guardar_tokens(ruta_dir: str, tokens: List[Simbolo]) -> None:
        # Guardar formato de tokens secuencial
        ruta_resultados = os.path.join(ruta_dir, "resultado_analisis.txt")
        contenido_resultados = ""
        
        for token in tokens:
            if token.token == "PALABRA_RESERVADA":
                linea = f'(PALABRA_RESERVADA, "{token.lexema}", línea {token.linea}, columna {token.columna})\n'
            elif token.token == "STRING":
                linea = f'(STRING, "{token.lexema}", línea {token.linea}, columna {token.columna})\n'
            elif token.token == "ID":
                linea = f'(ID, "{token.lexema}", línea {token.linea}, columna {token.columna})\n'
            elif token.token in ["DELIMITADOR", "SIMBOLO_PUNTUACION", "OPERADOR_ARITMETICO", "OPERADOR_ASIGNACION"]:
                linea = f'({token.token}, "{token.lexema}", línea {token.linea}, columna {token.columna})\n'
            else:
                linea = f'({token.token}, "{token.lexema}", línea {token.linea}, columna {token.columna})\n'
            contenido_resultados += linea

        with open(ruta_resultados, 'w', encoding='utf-8') as f:
            f.write(contenido_resultados)

        # Guardar formato de análisis por líneas
        ruta_tokens = os.path.join(ruta_dir, "tokens.txt")
        contenido_tokens = ""
        
        # Agrupar tokens por línea
        tokens_por_linea: Dict[int, List[Simbolo]] = {}
        for token in tokens:
            if token.linea not in tokens_por_linea:
                tokens_por_linea[token.linea] = []
            tokens_por_linea[token.linea].append(token)
        
        # Generar contenido por líneas
        for num_linea in sorted(tokens_por_linea.keys()):
            tokens_linea = tokens_por_linea[num_linea]
            if tokens_linea:
                contenido_tokens += f"Línea {num_linea + 1}:\n"
                for token in tokens_linea:
                    token_str = f"  - {token.token:<15} → {token.lexema:<15}"
                    if token.palabra_reservada:
                        token_str += " (Palabra Reservada)"
                    contenido_tokens += token_str + "\n"
                contenido_tokens += "\n"

        with open(ruta_tokens, 'w', encoding='utf-8') as f:
            f.write(contenido_tokens)

    @staticmethod
    def guardar_tabla_simbolos(ruta_dir: str, tabla: TablaSimbolos) -> None:
        ruta = os.path.join(ruta_dir, "tabla_simbolos.txt")
        contenido = ""
        
        for simbolo in tabla.obtener_todos_simbolos():
            tipo = "Reservada" if simbolo.palabra_reservada else "Identificador"
            contenido += f"{simbolo.token}\t\t{simbolo.lexema}\t\t{tipo}\n"

        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)

    @staticmethod
    def guardar_errores(ruta_dir: str, errores: List[dict]) -> None:
        if not errores:
            return
            
        ruta = os.path.join(ruta_dir, "errores.txt")
        contenido = ""

        for error in errores:
            contenido += f"Línea {error['linea'] + 1}, Columna {error['columna']}: {error['mensaje']}\n"

        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)

    @staticmethod
    def leer_archivo(ruta: str) -> str:
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        except Exception as e:
            raise Exception(f"Error al leer el archivo {ruta}: {str(e)}")