'''
    Algoritmo de acoplamientos.
'''


# TODO: Arbol de sufijos y arbol de sufijos comprimido.


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system
from requests import get
from random import choice

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
    req = get('https://loripsum.net/api/1/short/plaintext')

    texto = ''
    for r in req:
        texto += r.decode('utf-8')
    patron = choice(texto.split(' '))

    coincidencias = [id for id in kmp(texto, patron)]

    i = 0
    j = 0
    msg = ''
    encontrado = False
    for c in texto:
        if i in coincidencias:
            msg += ' >'
            encontrado = True

        if encontrado:
            if j < len(patron):
                j += 1
            else:
                msg += '< '
                j = 0
                encontrado = False
        msg += c
        i += 1

    print(msg)


if __name__ == "__main__":
    main(*sys.argv[1:])
