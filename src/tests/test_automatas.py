import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.controlador.automatas import Automatas

def test_identificador_valido():
    assert Automatas.isIdentificador("variable1") == True
    assert Automatas.isIdentificador("_variable") == False
    assert Automatas.isIdentificador("1variable") == False
    assert Automatas.isIdentificador("var_1") == True
    assert Automatas.isIdentificador("") == False

def test_numero_entero():
    assert Automatas.isNumero("123") == True
    assert Automatas.isNumero("-123") == True
    assert Automatas.isNumero("0") == True
    assert Automatas.isNumero("-0") == True
    
    assert Automatas.isNumero("") == False
    assert Automatas.isNumero("abc") == False
    assert Automatas.isNumero("12.34") == False
    assert Automatas.isNumero("-") == False
    assert Automatas.isNumero("12-34") == False
    assert Automatas.isNumero("--123") == False

def test_numero_real():
    assert Automatas.isReal("12.34") == True
    assert Automatas.isReal("-12.34") == True
    assert Automatas.isReal("0.0") == True
    assert Automatas.isReal("-0.0") == True
    assert Automatas.isReal(".5") == True
    
    assert Automatas.isReal("12") == False
    assert Automatas.isReal("abc") == False
    assert Automatas.isReal("") == False
    assert Automatas.isReal(".") == False
    assert Automatas.isReal("12.34.56") == False
    assert Automatas.isReal("--12.34") == False