# Librerias de terceros.
import numpy
import pandas

# Dependencias.
from .constantes import Tipo_Operacion


def Ie(
    frecuencias: 'pandas.Series',
    operacion: 'Tipo_Operacion'
) -> 'pandas.Series':
    # Calcula la informaicon mutua de un conjunto
    # retorna la sumatoria de esta y el valor por dato.

    # Se obtiene cual es el operdor del logaritmo a usar.
    if operacion is Tipo_Operacion.CUANTIFICABLE:
        log = numpy.log10
    elif operacion is Tipo_Operacion.TRANSMISION_DATOS:
        log = numpy.log2
    elif operacion is Tipo_Operacion.TRANSICION_ESTADOS:
        log = numpy.log
    else:
        raise Exception('El tipo de operación no es valido')

    informacion_mutua = -log(frecuencias)

    return informacion_mutua


def He(
    frecuencias: 'pandas.Series',
    informacion_mutua: 'pandas.Series',
) -> 'pandas.Series':
    # Calcula la entropia de un conjunto
    # retorna la sumatoria de esta y el valor por dato.
    entropia = frecuencias * informacion_mutua

    return entropia


def pre_analisis(texto: str) -> 'tuple[pandas.Series]':
    # Realiza un pre-analisis del medio.

    frecuencias = pandas.Series()
    alfabeto = pandas.Series()

    i = 0
    for caracter in texto:
        if caracter not in alfabeto.index:
            id = 'S{}'.format(i)

            alfabeto[caracter] = id

            frecuencias[id] = 1

            i += 1

        else:
            id = alfabeto[caracter]
            frecuencias[id] += 1

    frecuencias /= sum(frecuencias)

    return alfabeto, frecuencias
