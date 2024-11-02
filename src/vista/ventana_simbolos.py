import tkinter as tk
from tkinter import ttk
from typing import List
from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos

class VentanaSimbolos(tk.Toplevel):
    def __init__(self, parent, tabla_simbolos):
        super().__init__(parent)
        self.title("Tabla de Símbolos")
        self.geometry("800x600")
        self.configure(bg='#1e1f29')
        
        self.tree = ttk.Treeview(self, columns=("Token", "Lexema", "Tipo"),
                                show="headings",
                                style="Treeview")
        
        self.tree.heading("Token", text="Token")
        self.tree.heading("Lexema", text="Lexema")
        self.tree.heading("Tipo", text="Tipo")
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        self.cargar_simbolos(tabla_simbolos)
        
    def cargar_simbolos(self, tabla_simbolos):
        for simbolo in tabla_simbolos.obtener_todos_simbolos():
            tipo = "Reservada" if simbolo.palabra_reservada else "Identificador"
            self.tree.insert("", "end", values=(simbolo.token, 
                                              simbolo.lexema,
                                              tipo))