import tkinter as tk
from tkinter import ttk
from typing import List
from ..modelo.simbolo import Simbolo
from ..modelo.tabla_simbolos import TablaSimbolos

class VentanaSimbolos(tk.Toplevel):
    def __init__(self, parent, tabla_simbolos: TablaSimbolos):
        super().__init__(parent)
        self.title("Tabla de Símbolos")
        self.geometry("800x600")
        self.configure(bg='#1e1f29')
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure("Treeview", 
                           background="#282a36",
                           foreground="white",
                           fieldbackground="#282a36")
        
        self.style.configure("Treeview.Heading",
                           background="#44475a",
                           foreground="white",
                           font=('Segoe UI', 10, 'bold'))
        
        # Crear frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear Treeview con colores personalizados
        self.tree = ttk.Treeview(main_frame, 
                                columns=("Token", "Lexema", "Reservada"), 
                                show="headings",
                                style="Treeview")
        
        # Configurar encabezados
        self.tree.heading("Token", text="Token")
        self.tree.heading("Lexema", text="Lexema")
        self.tree.heading("Reservada", text="Palabra Reservada")
        
        # Configurar columnas
        self.tree.column("Token", width=250)
        self.tree.column("Lexema", width=250)
        self.tree.column("Reservada", width=250)
        
        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar widgets
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar símbolos
        self.cargar_simbolos(tabla_simbolos.obtener_todos_simbolos())
        
        # Centrar la ventana
        self.center_window()
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def cargar_simbolos(self, simbolos: List[Simbolo]):
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insertar símbolos con tags de color
        for simbolo in simbolos:
            tag = 'reservada' if simbolo.palabra_reservada else 'no_reservada'
            self.tree.insert("", "end", 
                           values=(simbolo.token, 
                                 simbolo.lexema,
                                 "Sí" if simbolo.palabra_reservada else "No"),
                           tags=(tag,))

        # Configurar colores para los tags
        self.tree.tag_configure('reservada', foreground='#7B42F5')  # Morado para palabras reservadas
        self.tree.tag_configure('no_reservada', foreground='#4FC1FF')  # Azul para no reservadas