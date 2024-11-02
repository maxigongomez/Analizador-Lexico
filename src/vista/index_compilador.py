import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..controlador.analizador_lexico import AnalizadorLexico
from ..utils.file_handler import FileHandler
from .ventana_simbolos import VentanaSimbolos

class IndexCompilador:
    def __init__(self, master, analizador_lexico: AnalizadorLexico):
        self.master = master
        self.analizador_lexico = analizador_lexico
        
        self.master.title("Analizador Léxico")
        self.master.geometry("1200x800")
        self.master.configure(bg='#1e1f29')
        
        self.configurar_estilo()
        self.crear_widgets()

    def configurar_estilo(self):
        style = ttk.Style()
        style.configure('Modern.TButton',
                       padding=10,
                       background='#ffffff',
                       foreground='#1e1f29')
        
        style.configure('Modern.TFrame',
                       background='#1e1f29')
        
        style.configure('Modern.TLabel',
                       background='#1e1f29',
                       foreground='#8b949e',
                       font=('Segoe UI', 10))

    def crear_widgets(self):
        main_frame = ttk.Frame(self.master, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        button_frame.pack(fill=tk.X, pady=(0, 15))

        button_config = {
            'bg': '#ffffff',
            'fg': '#1e1f29',
            'relief': 'flat',
            'pady': 5,
            'padx': 15,
            'font': ('Segoe UI', 9),
            'cursor': 'hand2'
        }

        self.btn_cargar = tk.Button(button_frame, 
                                  text="Cargar Archivo", 
                                  command=self.cargar_archivo,
                                  **button_config)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_analizar = tk.Button(button_frame,
                                    text="Analizar",
                                    command=self.analizar_codigo,
                                    **button_config)
        self.btn_analizar.pack(side=tk.LEFT, padx=5)

        self.btn_tabla_simbolos = tk.Button(button_frame,
                                          text="Tabla de Símbolos",
                                          command=self.mostrar_tabla_simbolos,
                                          **button_config)
        self.btn_tabla_simbolos.pack(side=tk.LEFT, padx=5)

        text_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        text_frame.pack(fill=tk.BOTH, expand=True)

        fuente_frame = ttk.Frame(text_frame, style='Modern.TFrame')
        fuente_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(fuente_frame, 
                 text="Código Fuente",
                 style='Modern.TLabel').pack(anchor='w', pady=(0, 5))
                 
        self.text_entrada = tk.Text(fuente_frame,
                                  bg='#282a36',
                                  fg='#f8f8f2',
                                  insertbackground='white',
                                  selectbackground='#44475a',
                                  selectforeground='#f8f8f2',
                                  font=('Consolas', 11),
                                  relief='flat',
                                  padx=10,
                                  pady=10)
        self.text_entrada.pack(fill=tk.BOTH, expand=True)

        salida_frame = ttk.Frame(text_frame, style='Modern.TFrame')
        salida_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(salida_frame, 
                 text="Resultado del Análisis",
                 style='Modern.TLabel').pack(anchor='w', pady=(0, 5))
                 
        self.text_salida = tk.Text(salida_frame,
                                 bg='#282a36',
                                 fg='#f8f8f2',
                                 insertbackground='white',
                                 selectbackground='#44475a',
                                 selectforeground='#f8f8f2',
                                 font=('Consolas', 11),
                                 relief='flat',
                                 padx=10,
                                 pady=10)
        self.text_salida.pack(fill=tk.BOTH, expand=True)

    def cargar_archivo(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            if file_path:
                contenido = FileHandler.leer_archivo(file_path)
                self.text_entrada.delete('1.0', tk.END)
                self.text_entrada.insert(tk.END, contenido)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

    def analizar_codigo(self):
        try:
            contenido = self.text_entrada.get('1.0', tk.END).strip()
            if not contenido:
                messagebox.showwarning("Advertencia", "No hay código para analizar.")
                return

            dir_salida = FileHandler.crear_directorio_salida("resultado_analisis")
            tokens = self.analizador_lexico.analizar_codigo(contenido)
            errores = self.analizador_lexico.obtener_errores()

            self.text_salida.delete('1.0', tk.END)
            
            self.text_salida.insert(tk.END, "ANÁLISIS LÉXICO\n")
            self.text_salida.insert(tk.END, "-" * 50 + "\n\n")
            
            for token in tokens:
                self.text_salida.insert(tk.END, f"{token}\n")

            if errores:
                self.text_salida.insert(tk.END, "\nERRORES ENCONTRADOS\n")
                self.text_salida.insert(tk.END, "-" * 50 + "\n\n")
                for error in errores:
                    self.text_salida.insert(tk.END, 
                                          f"Línea {error['linea']}: {error['mensaje']}\n")

            FileHandler.guardar_tokens(dir_salida, tokens)
            FileHandler.guardar_tabla_simbolos(dir_salida, self.analizador_lexico.tabla_simbolos)
            FileHandler.guardar_errores(dir_salida, errores)

            messagebox.showinfo("Éxito", 
                              f"Análisis completado. Archivos generados en: {dir_salida}")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis: {str(e)}")

    def mostrar_tabla_simbolos(self):
        VentanaSimbolos(self.master, self.analizador_lexico.tabla_simbolos)