'''
    Algoritmo de acoplamientos.
'''


# TODO: Arbol de sufijos y arbol de sufijos comprimido.


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system

# Librerias propias
from algoritmos_acoplamiento import kmp


# Aplica un arbol de sufijos.
def construir_arbol_sufijo(p):
    caracteres = {}

    m = len(p)

    for i in range(m):
        if p[i] not in list(caracteres.keys()):
            caracteres[p[i]] = [i]
        else:
            caracteres[p[i]].append(i)

    print(caracteres)


# Funcion main.
def main():
    system('clear')
    texto = 'bacbabababacaab'
    patron = 'ababaca'

    construir_arbol_sufijo(patron)


if __name__ == "__main__":
    main(*sys.argv[1:])
