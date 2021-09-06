'''
    Entropia e información mutua.

    Parametros:
        - Intancia a procesar.
        - Tipo de operacion, usado unicamente al cargar csv.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import pickle
from os import system

# Librerias de tercer
import numpy as np

# Librerias propias.
from util.funciones import entropia, informacion_mutua
from util.constantes import Tipo_Operacion


# Ingreso de datos directo del usuario.
def data_input():
    seleccion = None

    while not seleccion:
        system('clear')
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

    datos = []
    seleccion = None
    while not seleccion:
        system('clear')
        print('Ingresa un numero para agregarlo')
        print('-'*len(str(datos)))
        print(datos)
        print('-'*len(str(datos)))
        print('f.- Finaliza el ingreso de datos')
        print('d + index.- Elimina el dato en el index dado Ej: d0')
        seleccion = input('|---> ')

        if 'd' in seleccion:
            try:
                i = int(seleccion.split('d')[-1])

                if i > len(datos) or i < 0:
                    raise Exception(
                        'El index {} no es valido'.format(i)
                    )

                datos.pop(int(i))
                seleccion = None
            except:
                raise Exception(
                    'El formato {} no es valido'.format(seleccion)
                )
        else:
            try:
                datos.append(float(seleccion))
                seleccion = None
            except:
                pass

    return np.array(datos, dtype=float), operacion


# Funcion main.
def main(instancia=None, operacion=''):
    if instancia:
        extencion = instancia.split('.')[1]

        if extencion == 'csv':
            # Si se Carga desde un csv.
            datos = np.genfromtxt(instancia, delimiter=',')

            # Removemos los nan.
            datos = datos[np.logical_not(np.isnan(datos))]

            # Se verifica el tipo de operacion.
            if operacion == 'cuantificable':
                 tipo_operacion = Tipo_Operacion.CUANTIFICABLE
            elif operacion == 'datos':
                 tipo_operacion = Tipo_Operacion.TRANSMISION_DATOS
            elif operacion == 'estados':
                 tipo_operacion = Tipo_Operacion.TRANSICION_ESTADOS
            else:
                raise Exception(
                    'El tipo de operación {} no es valido'.format(
                        operacion
                    )
                )

        elif extencion == 'fime':
            # Se abre el fichero si se carga desde un fim.
            fichero = open(instancia, "rb")

            # Se carga el archivo serializado.
            informacion = pickle.load(fichero)

            datos = informacion['datos']
            tipo_operacion = informacion['tipo operacion']
        else:
            raise Exception('Extención de archivo {} no soportada'.format(
                    extencion
                )
            )

    else:
        datos, tipo_operacion = data_input()

    cantidad_datos = 1
    for i in datos.shape:
        cantidad_datos *= i

    unidades = ''
    tipo = ''
    if tipo_operacion is Tipo_Operacion.CUANTIFICABLE:
        unidades = 'Hartleys / Símbolo'
        tipo = 'Cuantificable'
    elif tipo_operacion is Tipo_Operacion.TRANSMISION_DATOS:
        unidades = 'Bits / Símbolo'
        tipo = 'Transmisión de datos'
    elif tipo_operacion is Tipo_Operacion.TRANSICION_ESTADOS:
        unidades = 'Nats / Símbolo'
        tipo = 'Transicion de estados'

    print('---> Datos cargados: {}'.format(cantidad_datos))
    print('---> Tipo de problema: {}\n'.format(tipo))

    sumatoria_he, he, sumatoria_ie, ie = entropia(
        datos,
        tipo_operacion,
        len(datos.shape) > 1
    )

    print('\n---> Ie: {}\n---> sum Ie: {} {}'.format(
            ie,
            sumatoria_ie, unidades
        )
    )
    print('\n---> He: {}\n---> sum He: {} {}'.format(
            he,
            sumatoria_he, unidades
        )
    )


if __name__ == "__main__":
    main(*sys.argv[1:])
