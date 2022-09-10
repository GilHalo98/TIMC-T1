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
def main(archivo_entrada=None):
    system('clear')

    if archivo_entrada is None:
        try:
            req = get('https://loripsum.net/api/10/verylong/plaintext')
            # req = get('https://loripsum.net/api/1/short/plaintext')

            texto = ''
            for r in req:
                texto += r.decode('utf-8')

        except Exception:
            texto = generar_texto_aleatorio(100)

    else:
        objeto_archivo = open(archivo_entrada, 'r')
        texto = objeto_archivo.read()
        objeto_archivo.close()

    print('Texto generado:\n{}'.format(texto))

    frecuencias, diccionario = calcular_frecuencias(texto)

    for id in diccionario:
        c = diccionario[id]
        if c == '\n':
            c = 'NUEVA LINEA'
        elif c == ' ':
            c = 'ESPACIO'
        print(id, c, frecuencias[id])

    arbol = Arbol_Hunffman(diccionario, frecuencias)
    arbol.graficar('prueba')

    print()
    for codigo in arbol.codigos():
        c = diccionario[codigo[0]]
        if c == '\n':
            c = 'NUEVA LINEA'
        elif c == ' ':
            c = 'ESPACIO'
        print(c, codigo[1])

    # Se calcula la longitud promedio de caracter por codificación.
    long_prom = 0
    for id, codigo in zip(diccionario, arbol.codigos()):
        frecuencia = frecuencias[id]
        longitud_codigo = len(str(codigo[1]))

        long_prom += longitud_codigo * frecuencia

    print()
    print("longitud promedio {}".format(float(long_prom)))

    print()
    radio_comprecion = 8 / float(long_prom)
    print('Radio de compreción: {}'.format(radio_comprecion))

    texto_encriptado = arbol.encriptar(texto)
    print('Texto encriptado (NUEVO):\n{}\n'.format(texto_encriptado))

    texto_desencriptado = arbol.desencriptar(texto_encriptado)
    print('Texto desencriptado (NUEVO):\n{}\n'.format(texto_desencriptado))

    # archivo = open('texto_encriptado.txt', 'w')
    # archivo.write(texto_encriptado)
    # archivo.close()

    # archivo = open('texto_desencriptado.txt', 'w')
    # archivo.write(texto_desencriptado)
    # archivo.close()


if __name__ == "__main__":
    main(*sys.argv[1:])
