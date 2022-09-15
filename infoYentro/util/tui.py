'''
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import os

# Librerias de terceros.
import numpy as np
import pandas as pd

# Librerias propias.
from util.constantes import Tipo_Operacion


# Toma por parte del usuario el tipo de operación.
def get_tipo_operacion() -> 'Tipo_Operacion':
    seleccion = None

    while not seleccion:
        os.system('clear')
        print('Seleccionar un tipo de proceso:')
        print('\t1.- Cuantificable.')
        print('\t2.- Transmición de datos.')
        print('\t3.- Transicion de estados.')
        seleccion = input('Seleccionar el numero |---> ')

        if seleccion == '1':
            operacion = Tipo_Operacion.CUANTIFICABLE
        elif seleccion == '2':
            operacion = Tipo_Operacion.TRANSMISION_DATOS
        elif seleccion == '3':
            operacion = Tipo_Operacion.TRANSICION_ESTADOS
        else:
            seleccion = None

    return operacion


# Verifica que se realizo una seleccion correcta en la creacion de
# instancias.
def verificar_seleccion(
    seleccion: str,
    datos: 'list[float]'
) -> 'tuple[str, str | None]':
    alerta = ''
    # Verifica que se realizara una seleccion.
    if seleccion != '':
        if seleccion[0] == 'f':
            # Se indica que el programa saldra del ingreso de datos.
            pass

        elif seleccion[0] == 'd':
            # Elimina un dato en un index dado.
            index = seleccion.split('d')[-1]

            if '.' in index:
                # El index debe ser un entero.
                alerta = 'El index debe ser un entero, no un flotante '
            else:
                index = int(index)
                if index < 0 or index >= len(datos):
                    #  El index debe ser menor que la cantida de
                    # datos total y mayor que 0.
                    alerta = 'El index debe ser mayor que 0 y menor que {}'
                    alerta = alerta.format(len(datos))
                else:
                    dato_eliminado = datos.pop(index)
                    alerta = 'El elemento {} con index {} fue eliminado '
                    alerta = alerta.format(dato_eliminado, index)

            seleccion = None

        elif seleccion[0] == 'a':
            # Agrega un dato en un index dado.
            dato = float(seleccion.split('d')[-1])
            index = seleccion.split('d')[0][1:]

            if '.' in index:
                # El index debe ser un entero.
                alerta = 'El index debe ser un entero, no un flotante '
            else:
                index = int(index)
                if index < 0 or index >= len(datos):
                    #  El index debe ser menor que la cantida de
                    # datos total y mayor que 0.
                    alerta = 'El index debe ser mayor que 0 y menor que {}'
                    alerta = alerta.format(len(datos))
                else:
                    # Si el dato es valido para procesar,
                    # se agrega a los datos.
                    if dato != 0 and dato != -1:
                        datos.insert(index, dato)
                        alerta = 'El elemento {} con index {} fue agregado'
                        alerta = alerta.format(dato, index)
                    else:
                        alerta = 'Solo agregar datos diferentes de -1 y 0'

            seleccion = None

        elif seleccion[0] == 'm':
            # Modifica un dato en un index dado.
            dato = float(seleccion.split('d')[-1])
            index = seleccion.split('d')[0][1:]

            if '.' in index:
                # El index debe ser un entero.
                alerta = 'El index debe ser un entero, no un flotante '
            else:
                index = int(index)
                if index < 0 or index >= len(datos):
                    #  El index debe ser menor que la cantida de
                    # datos total y mayor que 0.
                    alerta = 'El index debe ser mayor que 0 y menor que {}'
                    alerta = alerta.format(len(datos))
                else:
                    # Si el dato es valido para procesar,
                    # se agrega a los datos.
                    if dato != 0 and dato != -1:
                        dato_anterior = datos[index]
                        datos[index] = dato
                        alerta = 'El elemento {} con index {}'
                        alerta += ' fue modificado a {}'
                        alerta = alerta.format(dato_anterior, index, dato)
                    else:
                        alerta = 'Solo agregar datos diferentes de -1 y 0'

            seleccion = None

        else:
            # Se ingresa un dato como tal y se convierte en float.
            dato = float(seleccion)

            # Si el dato es valido para procesar, se agrega a los datos.
            if dato != 0 and dato != -1:
                datos.append(dato)
            else:
                alerta = 'Solo agregar datos diferentes de -1 y 0'

            seleccion = None
    else:
        alerta = 'Reaiza una seleccion'

    return alerta, seleccion


# Ingreso de datos directo del usuario.
def data_input() ->  'tuple[pd.Series, Tipo_Operacion]':
    # Obtiene el tipo de operacion que ingresa el usuario.
    operacion = get_tipo_operacion()

    alerta = ''
    datos = []
    seleccion = None
    while not seleccion:
        os.system('clear')

        mensaje = '''
            Ingresa un numero para agregarlo
            {}
            {}
            {}
            f.- Finaliza el ingreso de datos
            d + index.- Elimina el dato en el index dado Ej: d0
            a + index + d + dato.- Agrega el dato en el index dado Ej: a0d10
            m + index + d + dato.- Modifica el dato en el index dado Ej: m0d10
        '''.format('-'*len(str(datos)), datos, '-'*len(str(datos)))

        print(mensaje)

        seleccion = input('\n{}|---> '.format(alerta))
        seleccion = seleccion.lower()
        alerta = ''

        alerta, seleccion = verificar_seleccion(seleccion, datos)

    variables = {}
    i = 0
    for dato in datos:
        variables['f{}'.format(i)] = dato
        i += 1

    return pd.Series(variables), operacion