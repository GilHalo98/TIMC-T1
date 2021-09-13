'''
    Entropia e información mutua.

    Parametros:
        - Intancia a procesar.
        - Tipo de operacion, usado unicamente al cargar csv.
        - Si no se ingresa ninguno de estos dos parametros, entrara
            en modo de captura de datos manual.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import pickle
import time
from os import system

# Librerias de tercer
import numpy as np

# Librerias propias.
from util.funciones import entropia
from util.constantes import Tipo_Operacion


# Toma por parte del usuario el tipo de operación.
def get_tipo_operacion():
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

    return operacion


def verificar_seleccion(seleccion, datos):
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
def data_input():
    # Obtiene el tipo de operacion que ingresa el usuario.
    operacion = get_tipo_operacion()

    alerta = ''
    datos = []
    seleccion = None
    while not seleccion:
        system('clear')

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

    return np.array(datos, dtype=float), operacion


# Funcion main.
def main(instancia=None, operacion=''):
    system('clear')
    if instancia:
        extencion = instancia.split('.')[1]
        a = time.perf_counter()

        if extencion == 'csv':
            print('---> Cargando Instancia csv')

            mensaje = '\n---> ¡TODOS LOS DATOS QUE SEAN '
            mensaje += 'nan, 0 y -1 SERAN DESCARTADOS!\n'
            print(mensaje)

            # Si se Carga desde un csv.
            datos = np.genfromtxt(instancia, delimiter=',')

            # Removemos los nan.
            datos = datos[np.logical_not(np.isnan(datos))]

            # Removemos los 0
            datos = datos[datos != 0]

            # Removemos los -1
            datos = datos[datos != -1]

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
            print('---> Cargando Instancia fime')
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

        b = time.perf_counter()

    else:
        datos, tipo_operacion = data_input()
        system('clear')

    print('---> Instancia cargada en {0:.2f}s'.format(b - a))
    print('\n{}\n'.format(datos))

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

    a = time.perf_counter()

    sumatoria_he, he, sumatoria_ie, ie = entropia(
        datos,
        tipo_operacion,
        len(datos.shape) > 1
    )

    b = time.perf_counter()

    print('---> Tiempo en realizar las operaciones: {0:.4f}s'.format(
            b - a
        )
    )

    mensaje = '\n---> Ie: {}'.format(ie)
    mensaje += '\n---> sum Ie: {0:.2f} '.format(sumatoria_ie)
    mensaje += unidades
    print(mensaje)

    mensaje = '\n---> He: {}'.format(he)
    mensaje += '\n---> sum He: {0:.2f} '.format(sumatoria_he)
    mensaje += unidades
    print(mensaje)


if __name__ == "__main__":
    main(*sys.argv[1:])
