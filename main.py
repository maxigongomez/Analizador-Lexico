import os
import sys
import tkinter as tk
from src.modelo.tabla_simbolos import TablaSimbolos
from src.controlador.analizador_lexico import AnalizadorLexico
from src.vista.index_compilador import IndexCompilador

def main():
    root = tk.Tk()
    tabla_simbolos = TablaSimbolos()
    analizador = AnalizadorLexico(tabla_simbolos)
    app = IndexCompilador(root, analizador)
    root.mainloop()

if __name__ == "__main__":
    main()