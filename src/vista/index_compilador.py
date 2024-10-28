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

        # Configurar tags para diferentes tipos de tokens
        self.text_salida.tag_configure('palabra_reservada', foreground='#7B42F5')  # Morado
        self.text_salida.tag_configure('identificador', foreground='#4FC1FF')      # Azul claro
        self.text_salida.tag_configure('operador', foreground='#FF7B72')          # Rojo suave
        self.text_salida.tag_configure('delimitador', foreground='#FFA657')       # Naranja
        self.text_salida.tag_configure('literal', foreground='#9FEF00')          # Verde
        self.text_salida.tag_configure('error', foreground='#F85149', underline=1) # Rojo con subrayado

        # Scrollbars
        for text_widget, col in [(self.text_fuente, 0), (self.text_salida, 1)]:
            scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
            scrollbar.grid(row=1, column=col, sticky='nse')
            text_widget.configure(yscrollcommand=scrollbar.set)

        # Configurar peso de las filas
        text_frame.grid_rowconfigure(1, weight=1)

    def cargar_archivo(self):
        """Carga un archivo de texto en el área de código fuente"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    self.text_fuente.delete('1.0', tk.END)
                    self.text_fuente.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

    def analizar(self):
        """Analiza el contenido del área de código fuente"""
        contenido = self.text_fuente.get('1.0', tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "El área de código fuente está vacía.")
            return

        try:
            self.text_salida.delete('1.0', tk.END)
            resultados = self.analizador_lexico.analizar_linea(contenido)
            
            for token in resultados:
                linea = str(token) + "\n"
                
                # Determinar el color basado en el tipo de token
                if "ERROR" in token.token:
                    self.text_salida.insert(tk.END, linea, 'error')
                else:
                    start_index = self.text_salida.index("end-1c linestart")
                    self.text_salida.insert(tk.END, linea)
                    
                    # Aplicar colores según el tipo de token
                    if token.palabra_reservada:
                        self.text_salida.tag_add('palabra_reservada', 
                                               f"{start_index} linestart", 
                                               f"{start_index} lineend")
                    elif token.token == "ID":
                        self.text_salida.tag_add('identificador', 
                                               f"{start_index} linestart", 
                                               f"{start_index} lineend")
                    elif token.token in ["SUMA", "RESTA", "MULTIPLICACION", "DIVISION", "ASIGNACION"]:
                        self.text_salida.tag_add('operador', 
                                               f"{start_index} linestart", 
                                               f"{start_index} lineend")
                    elif token.token in ["PARENTESIS_IZQ", "PARENTESIS_DER", "LLAVE_IZQ", "LLAVE_DER", 
                                       "COMA", "PUNTO_COMA"]:
                        self.text_salida.tag_add('delimitador', 
                                               f"{start_index} linestart", 
                                               f"{start_index} lineend")
                    elif token.token in ["CADENA", "ENTERO", "REAL"]:
                        self.text_salida.tag_add('literal', 
                                               f"{start_index} linestart", 
                                               f"{start_index} lineend")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis: {str(e)}")

    def mostrar_tabla_simbolos(self):
        """Muestra la ventana de tabla de símbolos"""
        VentanaSimbolos(self.master, self.analizador_lexico.tabla_simbolos)

    def run(self):
        """Inicia la ejecución de la aplicación"""
        self.master.mainloop()