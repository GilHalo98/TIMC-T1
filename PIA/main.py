'''
    Guia de teoria de V&V.
'''


# !/usr/bin/env python
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system

# Librerias propias
from util.kmp import huffman_kmp, mapeo_indices, funcion_prefijo


# Funcion main.
def main():
    system('cls')

    codificacion = {
        'a': '00',
        'b': '01',
        'c': '100',
        'd': '111',
        'e': '110',
    }

    patron = 'bace'

    I = mapeo_indices(patron, codificacion)

    print(I)


if __name__ == "__main__":
    main(*sys.argv[1:])
