import os
from typing import Optional, TextIO

class FileHandler:
    @staticmethod
    def leer_archivo(ruta: str) -> str:
        """
        Lee el contenido de un archivo de texto.
        
        Args:
            ruta: Ruta del archivo a leer
            
        Returns:
            Contenido del archivo como string
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Para otros errores de lectura
        """
        try:
            with open(ruta, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        except Exception as e:
            raise Exception(f"Error al leer el archivo {ruta}: {str(e)}")

    @staticmethod
    def escribir_archivo(ruta: str, contenido: str) -> None:
        """
        Escribe contenido en un archivo de texto.
        
        Args:
            ruta: Ruta donde escribir el archivo
            contenido: Contenido a escribir
            
        Raises:
            Exception: Si hay errores al escribir
        """
        try:
            with open(ruta, 'w', encoding='utf-8') as file:
                file.write(contenido)
        except Exception as e:
            raise Exception(f"Error al escribir el archivo {ruta}: {str(e)}")

    @staticmethod
    def crear_directorio(ruta: str) -> None:
        """
        Crea un directorio si no existe.
        
        Args:
            ruta: Ruta del directorio a crear
            
        Raises:
            Exception: Si hay errores al crear el directorio
        """
        try:
            os.makedirs(ruta, exist_ok=True)
        except Exception as e:
            raise Exception(f"Error al crear el directorio {ruta}: {str(e)}")

    @staticmethod
    def obtener_ruta_salida(ruta_entrada: str, nombre_salida: str = "salida.txt") -> str:
        """
        Genera la ruta para el archivo de salida basado en la ruta de entrada.
        
        Args:
            ruta_entrada: Ruta del archivo de entrada
            nombre_salida: Nombre del archivo de salida
            
        Returns:
            Ruta completa para el archivo de salida
        """
        directorio = os.path.dirname(ruta_entrada)
        return os.path.join(directorio, nombre_salida)