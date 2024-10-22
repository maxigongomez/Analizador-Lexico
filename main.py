from src.modelo.tabla_simbolos import TablaSimbolos
from src.controlador.analizador_lexico import AnalizadorLexico
from src.vista.index_compilador import IndexCompilador
import tkinter as tk

def main():
    # Inicializar la tabla de símbolos
    tabla_simbolos = TablaSimbolos()
    try:
        tabla_simbolos.cargar_simbolos_iniciales('recursos/tabla_simbolos_inicial.json')
    except Exception as e:
        print(f"Error al cargar la tabla de símbolos: {str(e)}")
        return

    # Crear el analizador léxico
    analizador = AnalizadorLexico(tabla_simbolos)

    # Iniciar la interfaz gráfica
    root = tk.Tk()
    app = IndexCompilador(root, analizador)
    root.mainloop()

if __name__ == "__main__":
    main()