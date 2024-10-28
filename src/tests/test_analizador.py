import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.controlador.analizador_lexico import AnalizadorLexico
from src.modelo.tabla_simbolos import TablaSimbolos
from src.modelo.simbolo import Simbolo

@pytest.fixture
def setup_analizador():
    """Configuración inicial para las pruebas"""
    tabla = TablaSimbolos()
    tabla.agregar_simbolo(Simbolo("PROGRAMA", "programa", True))
    tabla.agregar_simbolo(Simbolo("INT", "int", True))
    tabla.agregar_simbolo(Simbolo("SUMA", "+", True))
    tabla.agregar_simbolo(Simbolo("RESTA", "-", True))
    tabla.agregar_simbolo(Simbolo("ASIGNACION", "=", True))
    tabla.agregar_simbolo(Simbolo("PUNTO_COMA", ";", True))
    return AnalizadorLexico(tabla)

def test_analizar_identificador(setup_analizador):
    """Prueba el reconocimiento de identificadores"""
    tokens = setup_analizador.analizar_linea("variable")
    assert len(tokens) == 1
    assert tokens[0].token == "ID"
    assert tokens[0].lexema == "variable"
    assert tokens[0].palabra_reservada == False

def test_analizar_numero(setup_analizador):
    """Prueba el reconocimiento de números enteros"""
    tokens = setup_analizador.analizar_linea("123")
    assert len(tokens) == 1
    assert tokens[0].token == "ENTERO"
    assert tokens[0].lexema == "123"

    tokens = setup_analizador.analizar_linea("-123")
    assert len(tokens) == 1
    assert tokens[0].token == "ENTERO"
    assert tokens[0].lexema == "-123"

def test_analizar_real(setup_analizador):
    """Prueba el reconocimiento de números reales"""
    tokens = setup_analizador.analizar_linea("123.45")
    assert len(tokens) == 1
    assert tokens[0].token == "REAL"
    assert tokens[0].lexema == "123.45"

    tokens = setup_analizador.analizar_linea("-123.45")
    assert len(tokens) == 1
    assert tokens[0].token == "REAL"
    assert tokens[0].lexema == "-123.45"

def test_analizar_palabra_reservada(setup_analizador):
    """Prueba el reconocimiento de palabras reservadas"""
    tokens = setup_analizador.analizar_linea("programa")
    assert len(tokens) == 1
    assert tokens[0].token == "PROGRAMA"
    assert tokens[0].palabra_reservada == True

def test_analizar_linea_completa(setup_analizador):
    """Prueba el análisis de una línea completa de código"""
    tokens = setup_analizador.analizar_linea("int x = 10;")
    assert len(tokens) == 5
    assert [t.token for t in tokens] == ["INT", "ID", "ASIGNACION", "ENTERO", "PUNTO_COMA"]

def test_analizar_cadena(setup_analizador):
    """Prueba el reconocimiento de cadenas de texto"""
    tokens = setup_analizador.analizar_linea('"Hola Mundo"')
    assert len(tokens) == 1
    assert tokens[0].token == "CADENA"
    assert tokens[0].lexema == '"Hola Mundo"'

def test_analizar_operaciones(setup_analizador):
    """Prueba el reconocimiento de operaciones aritméticas"""
    tokens = setup_analizador.analizar_linea("a = b + c;")
    assert len(tokens) == 6
    assert [t.token for t in tokens] == ["ID", "ASIGNACION", "ID", "SUMA", "ID", "PUNTO_COMA"]

def test_analizar_errores(setup_analizador):
    """Prueba el manejo de tokens no válidos"""
    tokens = setup_analizador.analizar_linea("@#$")
    assert len(tokens) == 1
    assert tokens[0].token == "ERROR"

def test_analizar_linea_vacia(setup_analizador):
    """Prueba el análisis de una línea vacía"""
    tokens = setup_analizador.analizar_linea("")
    assert len(tokens) == 0

def test_analizar_espacios_multiples(setup_analizador):
    """Prueba el manejo de múltiples espacios en blanco"""
    tokens = setup_analizador.analizar_linea("   a    =    b   ")
    assert len(tokens) == 3
    assert [t.token for t in tokens] == ["ID", "ASIGNACION", "ID"]

def test_analizar_comentarios(setup_analizador):
    """Prueba el reconocimiento de comentarios"""
    tokens = setup_analizador.analizar_linea("// Este es un comentario")
    assert len(tokens) == 1
    assert tokens[0].token == "COMENTARIO"
    assert tokens[0].lexema.startswith("//")

def test_analizar_combinacion_tokens(setup_analizador):
    """Prueba el análisis de una línea con múltiples tipos de tokens"""
    codigo = "int suma = -15.5 + variable_1; // Comentario"
    tokens = setup_analizador.analizar_linea(codigo)
    
    expected_tokens = [
        ("INT", True),
        ("ID", False),
        ("ASIGNACION", True),
        ("REAL", False),
        ("SUMA", True),
        ("ID", False),
        ("PUNTO_COMA", True),
        ("COMENTARIO", False)
    ]
    
    assert len(tokens) == len(expected_tokens)
    for token, (expected_type, expected_reserved) in zip(tokens, expected_tokens):
        assert token.token == expected_type
        assert token.palabra_reservada == expected_reserved

def test_analizar_caracteres_especiales(setup_analizador):
    """Prueba el reconocimiento de caracteres especiales"""
    casos = [
        ("'\\n'", "CARACTER", "'\\n'"),   
        ("'\\t'", "CARACTER", "'\\t'"),   
        ("'\\''", "CARACTER", "'\\''"),   
        ("'a'", "CARACTER", "'a'")        
    ]
    
    for entrada, token_esperado, lexema_esperado in casos:
        tokens = setup_analizador.analizar_linea(entrada)
        assert len(tokens) == 1, f"Error analizando {entrada}, tokens obtenidos: {[t.lexema for t in tokens]}"
        assert tokens[0].token == token_esperado, f"Token incorrecto para {entrada}"
        assert tokens[0].lexema == lexema_esperado, f"Lexema incorrecto para {entrada}"

def test_manejo_errores_complejos(setup_analizador):
    """Prueba casos complejos de error"""
    casos_error = [
        ("123abc", "ERROR"),     
        ("''", "ERROR"),         
        ("'", "ERROR"),          
        ('"texto', "ERROR"),     
        ("@#$", "ERROR")         
    ]
    
    for entrada, token_esperado in casos_error:
        tokens = setup_analizador.analizar_linea(entrada)
        error_encontrado = any(t.token == token_esperado for t in tokens)
        assert error_encontrado, f"No se detectó error en '{entrada}', tokens obtenidos: {[t.token for t in tokens]}"