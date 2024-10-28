import pytest
from pathlib import Path
from src.controlador.analizador_lexico import AnalizadorLexico
from src.modelo.tabla_simbolos import TablaSimbolos
from src.utils.file_handler import FileHandler

def test_analisis_archivo_completo(tmp_path):
    test_file = tmp_path / "test_program.txt"
    test_file.write_text("""
        programa test() {
            int x = 10;
            float y = -20.5;
            if (x > 0) {
                imprimir("x es positivo");
            }
            terminar;
        }
    """)
    
    tabla_simbolos = TablaSimbolos()
    tabla_simbolos.cargar_simbolos_iniciales("recursos/tabla_simbolos_inicial.json")
    analizador = AnalizadorLexico(tabla_simbolos)
    
    contenido = FileHandler.leer_archivo(str(test_file))
    tokens = analizador.analizar_linea(contenido)
    
    assert len(tokens) > 0
    assert any(t.token == "PROGRAMA" for t in tokens)
    assert any(t.token == "INT" for t in tokens)
    assert any(t.token == "FLOAT" for t in tokens)
    assert any(t.token == "ID" for t in tokens)
    assert any(t.token == "REAL" for t in tokens)
    assert any(t.token == "ENTERO" for t in tokens)