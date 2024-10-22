import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..controlador.analizador_lexico import AnalizadorLexico
from .ventana_simbolos import VentanaSimbolos

class IndexCompilador:
    def __init__(self, master, analizador_lexico: AnalizadorLexico):
        self.master = master
        self.analizador_lexico = analizador_lexico
        
        # Configuración básica de la ventana
        self.master.title("Analizador Léxico")
        self.master.geometry("1200x800")
        self.master.configure(bg='#1e1f29')
        
        # Configurar el estilo
        self.configurar_estilo()
        self.crear_widgets()

    def configurar_estilo(self):
        style = ttk.Style()
        style.configure('Modern.TButton',
                       padding=8,
                       background='#ffffff',
                       foreground='#1e1f29')
        
        style.configure('Modern.TFrame',
                       background='#1e1f29')
        
        style.configure('Modern.TLabel',
                       background='#1e1f29',
                       foreground='#8b949e',
                       font=('Segoe UI', 10))

    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame para botones
        self.frame_botones = ttk.Frame(main_frame, style='Modern.TFrame')
        self.frame_botones.pack(fill=tk.X, pady=(0, 15))

        # Botones con fondo blanco
        button_config = {
            'bg': '#ffffff',
            'fg': '#1e1f29',
            'relief': 'flat',
            'pady': 5,
            'padx': 15,
            'font': ('Segoe UI', 9),
            'cursor': 'hand2'
        }

        self.btn_cargar = tk.Button(self.frame_botones, text="Cargar Archivo", 
                                  command=self.cargar_archivo, **button_config)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_analizar = tk.Button(self.frame_botones, text="Analizar", 
                                    command=self.analizar, **button_config)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)

        self.btn_tabla_simbolos = tk.Button(self.frame_botones, text="Tabla de Símbolos", 
                                          command=self.mostrar_tabla_simbolos, **button_config)
        self.btn_tabla_simbolos.pack(side=tk.LEFT, padx=5)

        # Frame para los cuadros de texto
        text_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_columnconfigure(1, weight=1)

        # Configuración común para las etiquetas
        label_config = {
            'background': '#1e1f29',
            'foreground': '#8b949e',
            'font': ('Segoe UI', 10)
        }

        # Área de código fuente (lado izquierdo)
        tk.Label(text_frame, text="Código Fuente", **label_config).grid(row=0, column=0, sticky='w', pady=(0, 5))
        self.text_fuente = tk.Text(text_frame, 
                                 bg='#282a36',
                                 fg='#f8f8f2',
                                 insertbackground='white',
                                 selectbackground='#44475a',
                                 selectforeground='#f8f8f2',
                                 font=('Consolas', 11),
                                 relief='flat',
                                 border=0)
        self.text_fuente.grid(row=1, column=0, sticky='nsew', padx=(0, 10))

        # Área de resultados (lado derecho)
        tk.Label(text_frame, text="Resultado del Análisis", **label_config).grid(row=0, column=1, sticky='w', pady=(0, 5))
        self.text_salida = tk.Text(text_frame,
                                 bg='#282a36',
                                 fg='#f8f8f2',
                                 insertbackground='white',
                                 selectbackground='#44475a',
                                 selectforeground='#f8f8f2',
                                 font=('Consolas', 11),
                                 relief='flat',
                                 border=0)
        self.text_salida.grid(row=1, column=1, sticky='nsew')

        # Configurar tags para colorear True/False
        self.text_salida.tag_configure('true', foreground='#50fa7b')  # Verde para True
        self.text_salida.tag_configure('false', foreground='#ff5555')  # Rojo para False

        # Scrollbars
        for text_widget, col in [(self.text_fuente, 0), (self.text_salida, 1)]:
            scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
            scrollbar.grid(row=1, column=col, sticky='nse')
            text_widget.configure(yscrollcommand=scrollbar.set)

        # Configurar peso de las filas
        text_frame.grid_rowconfigure(1, weight=1)

    def cargar_archivo(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    self.text_fuente.delete('1.0', tk.END)
                    self.text_fuente.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def analizar(self):
        contenido = self.text_fuente.get('1.0', tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "El área de texto está vacía.")
            return

        try:
            resultados = self.analizador_lexico.analizar_linea(contenido)
            self.text_salida.delete('1.0', tk.END)
            
            for token in resultados:
                # Convertir el token a string para procesarlo
                token_str = str(token)
                
                # Buscar si contiene "True" o "False"
                if "True" in token_str:
                    before_true = token_str[:token_str.find("True")]
                    self.text_salida.insert(tk.END, before_true)
                    self.text_salida.insert(tk.END, "True", 'true')
                    self.text_salida.insert(tk.END, "\n")
                elif "False" in token_str:
                    before_false = token_str[:token_str.find("False")]
                    self.text_salida.insert(tk.END, before_false)
                    self.text_salida.insert(tk.END, "False", 'false')
                    self.text_salida.insert(tk.END, "\n")
                else:
                    self.text_salida.insert(tk.END, f"{token_str}\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis: {str(e)}")

    def mostrar_tabla_simbolos(self):
        """Muestra la ventana de símbolos con los símbolos actuales"""
        VentanaSimbolos(self.master, self.analizador_lexico.tabla_simbolos)

    def run(self):
        self.master.mainloop()