'''
    Algoritmo de acoplamientos.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
from os import system

# Librerias de tercer
import numpy as np


# Algoritmo Boyer-Moore.
def boyer_moore(t, p):
    # print('Buscando {} en {}'.format(p, t))
    n = len(t)
    m = len(p)

    i = m - 1
    j = m - 1

    while True:
        # log = 'Comparando P[{}] = {} con T[{}] = {}\n'.format(j, p[j], i, t[i])
        # Compara el caracter en P[j] con el de T[i]
        if p[j] == t[i]:
            if j == 0:
                # Se comprueba la comparacion del ultimo caracter del
                # patron, el patron se encuentra en el texto.
                # log += '---> Ocurrencia encontrada en {} '.format(i)
                yield i
                i += (m * 2) - 1
                # log += ' saltando a T[{}]\n'.format(i)
                j = m - 1
            else:
                # Mueve la comparacion al siguiente caracter.
                # log += 'Caracteres similares, pasando al siguiente caracter en P\n'
                i -= 1
                j -= 1
        else:
            # log += 'Caracteres distintos'
            # La comparacion fallo, se salta m caracteres a la derecha
            # en T.
            ocurrencia_izquierda = last(t[i], p, m)
            # if ocurrencia_izquierda < 0:
            # log += ' {} no existe en el patron '.format(t[i])

            i += m - min(j, 1 + ocurrencia_izquierda)
            # log += ' saltando a T[{}]\n'.format(i)

            # Se reinicia la comparacion desde P[m - 1]
            j = m - 1

        # print(log + '\n----------------------------------------------\n')

        if i > n - 1:
            break


# Retorna el primer index encontrado del elemento x, desde
# la derecha hacia la izquierda en el patron.
def last(c, p, m):
    i = m - 1
    while i >= 0:
        if p[i] == c:
            break
        i -= 1
    return i


# Retorna el minimo entre dos datos.
def min(a, b):
    return a if a < b else b


# Funcion main.
def main():
    system('clear')
    texto = 'bacbabababacaab'
    patron = 'ababaca'

    for id_ocurrencia in boyer_moore(texto, patron):
        print(id_ocurrencia)


if __name__ == "__main__":
    main(*sys.argv[1:])
