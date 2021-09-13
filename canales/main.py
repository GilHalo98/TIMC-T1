'''
    Canales.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from itertools import product
from os import system

# Librerias de tercer
# import numpy as np


# Realiza las combinaciones.
def realizar_combinaciones(canal, longitud):
    caracteres = ['']
    combinaciones = []

    for caracter in canal:
        if len(caracter) <= longitud:
            caracteres.append(caracter)

    n_canal = 0
    print(caracteres[1:], longitud)
    for combinacion in product(caracteres, repeat=longitud):
        cadena = ''.join(combinacion)
        if len(cadena) == longitud and cadena not in combinaciones:
            combinaciones.append(cadena)
            n_canal += 1
    print(combinaciones, n_canal)


# Funcion main.
def main():
    system('clear')
    A = ['#', '$', '%', '!', '"']
    B = ['!', '##', '$$', '"""', '%%%%']
    realizar_combinaciones(B, 6)


if __name__ == "__main__":
    main(*sys.argv[1:])
