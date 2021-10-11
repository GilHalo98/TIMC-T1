'''
    Codificación de alfabetos, se utilizan distintos metodos
    para codificar alfabetos.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import random
import fractions
from os import system
from requests import get

# Libreria propia
from grafo.arbol_hunffman import Arbol_Hunffman


# Genera un texto aleatorio, con una longitud N.
def generar_texto_aleatorio(longitud):
    texto = ''

    caracteres = [
        c for c in 'abcdefghijklmnñopqrstuvwxyz'
    ]

    for _ in range(longitud):
        texto += random.choice(caracteres)

    return texto


# Calcula las frecuencas de los caracteres dado un texto.
def calcular_frecuencias(texto):
    n = len(texto)
    frecuencias = {}
    diccionario = {}

    id = 0
    for caracter in texto:
        if caracter not in diccionario.values():
            id_c = 'S{}'.format(id)
            diccionario[id_c] = caracter
            frecuencias[id_c] = fractions.Fraction(1, n)
            id += 1
        else:
            id_c = list(diccionario.values()).index(caracter)
            id_c = list(diccionario.keys())[id_c]
            frecuencias[id_c] += fractions.Fraction(1, n)

    return frecuencias, diccionario


# Funcion main.
def main():
    system('clear')

    try:
        req = get('https://loripsum.net/api/10/verylong/plaintext')

        texto = ''
        for r in req:
            texto += r.decode('utf-8')

    except Exception:
        texto = generar_texto_aleatorio(100)

    print('Texto generado:\n{}\n'.format(texto))

    frecuencias, diccionario = calcular_frecuencias(texto)

    for id in diccionario:
        c = diccionario[id]

        if c == '\n':
            c = 'NUEVA LINEA'
        elif c == ' ':
            c = 'ESPACIO'

        print(id, c, frecuencias[id])

    arbol = Arbol_Hunffman()
    arbol.diccionario = diccionario
    arbol.generar_arbol(frecuencias)
    arbol.graficar('prueba')

    print()
    for codigo in arbol.codigos():
        c = diccionario[codigo[0]]

        if c == '\n':
            c = 'NUEVA LINEA'
        elif c == ' ':
            c = 'ESPACIO'

        print(c, codigo[1])

    texto_encriptado = arbol.encriptar(texto)

    print()
    print('Texto encriptado:\n{}\n'.format(texto_encriptado))
    print()

    texto_desencriptado = arbol.desencriptar(texto_encriptado)
    print('Texto desencriptado:\n{}\n'.format(texto_desencriptado))


if __name__ == "__main__":
    main(*sys.argv[1:])
