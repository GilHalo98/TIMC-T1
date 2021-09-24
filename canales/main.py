'''
    Canales.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system

# Librerias de tercer
# import numpy as np

# Propias.
from grafo.arbol_combinaciones import Arbol_Combinaciones


# Funcion main.
def main():
    system('clear')
    # A = ['#', '$', '%', '!', '"']
    B = ['!', '##', '$$', '"""', '%%%%']
    arbol = Arbol_Combinaciones()
    arbol.generar_combinaciones(B, 5)
    for nodo in arbol.topologia.values():
        print(nodo)
    print()

    combinaciones = arbol.dfs()
    for combinacion in combinaciones:
        print(combinacion)


if __name__ == "__main__":
    main(*sys.argv[1:])
