# Analizador Léxico

Un analizador léxico en Python que identifica y clasifica tokens en código fuente, implementado con una interfaz gráfica moderna.

## Representación Visual de Tokens

El analizador implementa un esquema de colores para identificar diferentes tipos de tokens:

| Tipo de Token | Color | Ejemplo | Descripción |
|--------------|-------|---------|-------------|
| Palabras Reservadas | `#7B42F5` | `programa`, `int`, `if` | Palabras clave del lenguaje |
| Identificadores | `#4FC1FF` | `contador`, `suma`, `x` | Nombres de variables y funciones |
| Operadores | `#FF7B72` | `+`, `-`, `*`, `=` | Símbolos de operaciones |
| Delimitadores | `#FFA657` | `{`, `}`, `;`, `,` | Símbolos de estructura |
| Literales | `#9FEF00` | `"texto"`, `123`, `3.14` | Valores constantes |
| Errores | `#F85149` | `@`, `$` | Tokens no reconocidos |

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
│   │   ├── analizador_lexico.py   # Lógica principal de análisis
│   │   └── automatas.py           # Autómatas para reconocimiento
│   ├── modelo/
│   │   ├── simbolo.py             # Representación de tokens
│   │   └── tabla_simbolos.py      # Gestión de símbolos
│   ├── vista/
│   │   ├── index_compilador.py    # Interfaz principal
│   │   └── ventana_simbolos.py    # Tabla de símbolos
│   └── utils/
│       └── file_handler.py        # Manejo de archivos
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

## Pruebas

Ejecutar tests:
```bash
# Pruebas básicas
python -m pytest src/tests/

# Pruebas con cobertura
python -m pytest --cov=src --cov-report=html

# Pruebas específicas
python -m pytest src/tests/test_analizador.py -v
```

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