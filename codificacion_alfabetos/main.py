'''
    Codificación de alfabetos, se utilizan distintos metodos
    para codificar alfabetos.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system
import fractions

# Libreria propia
from grafo.arbol_hunffman import Arbol_Hunffman


# Funcion main.
def main():
    system('clear')

    f = {
        's1': fractions.Fraction(25, 100),
        's2': fractions.Fraction(20, 100),
        's3': fractions.Fraction(20, 100),
        's4': fractions.Fraction(15, 100),
        's5': fractions.Fraction(12, 100),
        's6': fractions.Fraction(8, 100),
    }

    d = {}

    for id, c in zip(f, ['!', '""', '###', '%%%%', '!!', '$$']):
        d[id] = c

    arbol = Arbol_Hunffman()
    arbol.diccionario = d
    arbol.generar_arbol(f)
    arbol.graficar('prueba')


if __name__ == "__main__":
    main(*sys.argv[1:])
