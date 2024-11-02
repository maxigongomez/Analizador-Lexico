# Analizador Léxico

Un analizador léxico en Python que identifica y clasifica tokens en código fuente, implementado con una interfaz gráfica moderna.

## Características

- Interfaz gráfica moderna con tema oscuro
- Resaltado de sintaxis en tiempo real
- Análisis token por token con información detallada
- Soporte para múltiples tipos de tokens
- Detección y marcado de errores léxicos
- Pruebas unitarias con cobertura superior al 65%

## Estructura del Proyecto

```
analizador_lexico/
├── src/
│   ├── controlador/
│   │   ├── analizador_lexico.py
│   │   └── automatas.py        
│   ├── modelo/
│   │   ├── simbolo.py          
│   │   └── tabla_simbolos.py   
│   ├── vista/
│   │   ├── index_compilador.py 
│   │   └── ventana_simbolos.py 
│   └── utils/
│       └── file_handler.py        
├── tests/
│   ├── test_analizador.py
│   ├── test_automatas.py
│   ├── test_integration.py
│   └── test_performance.py
├── recursos/
│   ├── programa_prueba.txt
│   └── tabla_simbolos_inicial.json
└── main.py
```

## Requisitos

- Python 3.7 o superior
- Tkinter (incluido con Python)
- Dependencias en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/analizador-lexico.git
cd analizador-lexico
```

2. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Ejecutar el programa:
```bash
python main.py
```

2. Funcionalidades disponibles:
   - Cargar archivos fuente (.txt)
   - Analizar código
   - Ver tabla de símbolos
   - Examinar tokens identificados

## Ejemplo de Código Soportado

```python
programa sumar() {
    int a, b, c;
    leer a;
    leer b;
    c = a + b;
    imprimir("la suma es: ", c);
    terminar;
}
```

## Funcionalidades Soportadas

- Palabras reservadas (programa, int, if, while, etc.)
- Identificadores (nombres de variables y funciones)
- Números enteros y reales (incluyendo negativos)
- Operadores aritméticos y de asignación
- Delimitadores y símbolos especiales
- Cadenas de texto y caracteres
- Comentarios de línea
- Detección de errores léxicos