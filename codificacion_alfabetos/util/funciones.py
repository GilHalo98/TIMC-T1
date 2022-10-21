# Librerias estandar.
import fractions

# Librerias de terceros.
import numpy
import pandas

# Dependencias.
from .constantes import Tipo_Operacion
from .tipos_datos import Notacion_Binaria


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


def Fa(frecuencias: pandas.Series) -> pandas.Series:
    '''
        Calcula la frecuencia acumulada de las frecuencias pasadas.
    '''
    # Creamos una serie que contenga las frecuencias acumuladas.
    frecuencias_acumuladas = pandas.Series(
        [fractions.Fraction(0.0) for _ in frecuencias],
        index=frecuencias.index
    )

    # La frecuencia acumulada actual.
    frecuencia_acumulada = fractions.Fraction(0.0)

    # Por cada frecuencia en las frecuencias.
    for id in frecuencias.index:
        # Se guarda en las frecuencias acumuladas.
        frecuencias_acumuladas[id] = frecuencia_acumulada

        # Se acumula la frecuencia.
        frecuencia_acumulada += frecuencias[id]

    return frecuencias_acumuladas


def expancion_binaria(
    fraccion: 'float | fractions.Fraction'
) -> str:
    '''
        Retorna la expancion binaria de una fraccion.
    '''
    # Expancion binaria.
    codigo = ''

    # Expancion actual.
    expancion = fraccion * 2

    # Memoizacion de la expancion binaria.
    memoizacion = []

    # La expancion binara es realzia hasta que se encuentre la expancion
    # actual en la memoización.
    while expancion not in memoizacion:
        memoizacion.append(expancion)

        if expancion < 1:
            expancion *= 2
            codigo += '0'

        else:
            expancion = (expancion - 1) * 2
            codigo += '1'

    # Obtenemos el inicio del periodo la notacion.
    inicio_periodo = memoizacion.index(expancion)

    # Obtenemos el periodo de la notacion.
    periodo = (
        len(memoizacion) - inicio_periodo
    ) if fraccion > 1 else numpy.inf

    return Notacion_Binaria(codigo, periodo, inicio_periodo)