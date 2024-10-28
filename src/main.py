import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from src.modelo.tabla_simbolos import TablaSimbolos
from src.controlador.analizador_lexico import AnalizadorLexico
from src.vista.index_compilador import IndexCompilador

def main():
    tabla_simbolos = TablaSimbolos()
    ruta_simbolos = os.path.join('recursos', 'tabla_simbolos_inicial.json')
    tabla_simbolos.cargar_simbolos_iniciales(ruta_simbolos)
    
    analizador = AnalizadorLexico(tabla_simbolos)
    
    root = tk.Tk()
    app = IndexCompilador(root, analizador)
    app.run()

if __name__ == "__main__":
    main()