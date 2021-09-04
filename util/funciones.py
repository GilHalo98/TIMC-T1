'''
    Funciones para realizar operaciones varias.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias de terceros.
import numpy as np

# Librerias propias.
from util.constantes import Tipo_Operacion

# Calcula la informaicon mutua de un conjunto
# retorna la sumatoria de esta y el valor por dato.
def informacion_mutua(datos, operacion):
    # Se obtiene cual es el operdor del logaritmo a usar.
    if operacion is Tipo_Operacion.CUANTIFICABLE:
        log = np.log10
    elif operacion is Tipo_Operacion.TANSMISION_DATOS:
        log = np.log2
    elif operacion is Tipo_Operacion.TRANSISION_ESTADOS:
        log = np.log
    else:
        raise Exception('El tipo de operación no es valido')

    # Se crea un nuevo array con los datos calculados.
    ie = np.zeros(shape=datos.shape, dtype=float)

    # Por cada elemento, se calcula el logaritmo de base n.
    i = 0
    while i < datos.shape[0]:
        ie[i] = -log(datos[i])
        i += 1

    return np.sum(ie), ie


# Calcula la entropia de un conjunto
# retorna la sumatoria de esta y el valor por dato.
def entropia(datos, operacion):
    _, ie = informacion_mutua(datos, operacion)

    # Se crea un nuevo array con los datos calculados.
    he = np.zeros(shape=datos.shape, dtype=float)

    # Por cada elemento, se calcula el logaritmo de base n.
    i = 0
    while i < datos.shape[0]:
        im = ie[i]
        pe = datos[i]

        he[i] = pe * im
        i += 1

    return np.sum(he), he
