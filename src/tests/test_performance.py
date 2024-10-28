import pytest
import time
from src.controlador.analizador_lexico import AnalizadorLexico
from src.modelo.tabla_simbolos import TablaSimbolos
from src.modelo.simbolo import Simbolo

@pytest.fixture
def setup_analizador():
    tabla = TablaSimbolos()
    # Agregar símbolos básicos para las pruebas
    simbolos_iniciales = [
        ("PROGRAMA", "programa", True),
        ("INT", "int", True),
        ("FLOAT", "float", True),
        ("SUMA", "+", True),
        ("RESTA", "-", True),
        ("ASIGNACION", "=", True),
        ("PUNTO_COMA", ";", True),
        ("LLAVE_IZQ", "{", True),
        ("LLAVE_DER", "}", True)
    ]
    
    for token, lexema, es_reservada in simbolos_iniciales:
        tabla.agregar_simbolo(Simbolo(token, lexema, es_reservada))
    
    return AnalizadorLexico(tabla)

@pytest.fixture
def large_code():
    lines = [
        "programa test() {",
        "   int resultado = 0;",
    ]
    
    # Generar muchas variables y asignaciones
    for i in range(1000):
        lines.append(f"   int var_{i} = {i};")
        if i % 100 == 0:
            lines.append(f"   // Checkpoint {i}")
    
    lines.extend([
        "   return resultado;",
        "}"
    ])
    
    return "\n".join(lines)

def test_rendimiento_analisis(setup_analizador, large_code):
    start_time = time.time()
    tokens = setup_analizador.analizar_linea(large_code)
    end_time = time.time()
    
    tiempo_transcurrido = end_time - start_time
    
    # El análisis no debería tomar más de 1 segundo
    assert tiempo_transcurrido < 1.0, f"El análisis tomó {tiempo_transcurrido:.2f} segundos"
    
    # Verificar cantidad de tokens
    assert len(tokens) > 3000, f"Se esperaban más de 3000 tokens, se encontraron {len(tokens)}"
    
    # Verificar tipos de tokens encontrados
    tipos_token = {t.token for t in tokens}
    tokens_esperados = {"PROGRAMA", "INT", "ID", "ASIGNACION", "ENTERO", "PUNTO_COMA"}
    assert tokens_esperados.issubset(tipos_token), f"Faltan algunos tipos de token esperados. Encontrados: {tipos_token}"
    
    # Verificar que no hay errores
    errores = [t for t in tokens if t.token == "ERROR"]
    assert len(errores) == 0, f"Se encontraron {len(errores)} errores: {errores}"