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
import random

# Libreria propia
from grafo.arbol_hunffman import Arbol_Hunffman


# Genera un texto aleatorio, con una longitud N.
def generar_texto_aleatorio(longitud):
    texto = ''

    caracteres = [c for c in 'abcdefghijklmnopqrstuvwxyz']

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

    texto = generar_texto_aleatorio(100)
    texto = 'bvxeoxxfiifrudwjsbmeburkquieftbfdceyeuwcmnfumgvoruyrosynfisjmuxbioxyxxvrtqyqoohwgbeswjxliirotfvwpul'
    print('Texto generado: {}\n'.format(texto))

    frecuencias, diccionario = calcular_frecuencias(texto)

    for id in diccionario:
        print(id, diccionario[id], frecuencias[id])

    arbol = Arbol_Hunffman()
    arbol.diccionario = diccionario
    arbol.generar_arbol(frecuencias)
    arbol.graficar('prueba')

    print()
    for codigo in arbol.codigos():
        print(diccionario[codigo[0]], codigo[1])

    texto_encriptado = arbol.encriptar(texto)

    print()
    print(texto_encriptado)


if __name__ == "__main__":
    main(*sys.argv[1:])
