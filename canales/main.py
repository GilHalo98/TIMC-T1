'''
    Canales.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system

# Librerias de tercer

# Propias.
from grafo.arbol_combinaciones import Arbol_Combinaciones


# Funcion main.
def main():
    system('clear')
    # C = ['0', '1', '*']
    # C = ['0000', '1111']
    # C = ['#', '$', '%', '!', '"']
    C = ['!', '##', '$$', '"""', '%%%%']
    C = ['P', 'E', 'R']
    arbol = Arbol_Combinaciones()
    arbol.generar_combinaciones(C, 4)

    print(arbol)

    combinaciones = ''
    for combinacion in arbol.combinaciones():
        combinaciones += combinacion
        combinaciones += '\n'

    print(combinaciones)
    arbol.graficar('prueba')


if __name__ == "__main__":
    main(*sys.argv[1:])
