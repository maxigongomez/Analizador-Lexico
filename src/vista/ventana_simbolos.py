import tkinter as tk
from tkinter import ttk
from typing import List
from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos

class VentanaSimbolos(tk.Toplevel):
    def __init__(self, parent, tabla_simbolos: TablaSimbolos):
        super().__init__(parent)
        self.title("Tabla de Símbolos")
        self.geometry("600x400")
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                           background="#282a36",
                           foreground="white",
                           fieldbackground="#282a36")
        self.style.configure("Treeview.Heading",
                           background="#44475a",
                           foreground="white")
        
        # Crear Treeview
        self.tree = ttk.Treeview(self, columns=("Token", "Lexema", "Reservada"), show="headings")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Lexema", text="Lexema")
        self.tree.heading("Reservada", text="Palabra Reservada")
        
        # Configurar columnas
        self.tree.column("Token", width=150)
        self.tree.column("Lexema", width=150)
        self.tree.column("Reservada", width=150)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar símbolos
        self.cargar_simbolos(tabla_simbolos.obtener_todos_simbolos())
        
    def cargar_simbolos(self, simbolos: List[Simbolo]):
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insertar símbolos
        for simbolo in simbolos:
            self.tree.insert("", "end", values=(
                simbolo.token,
                simbolo.lexema,
                "Sí" if simbolo.palabra_reservada else "No"
            ))