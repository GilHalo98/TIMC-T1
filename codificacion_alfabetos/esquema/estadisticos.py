"""
    Esquemas estadisticos, shannon, shannon-fano, shannon-fano-elias
"""

# Librerias estandar.
import pathlib
import fractions

# Librerias Propias
from util.funciones import Ie, He, Fa, expancion_binaria
from util.constantes import Tipo_Operacion
from estructuras_datos.nodo import Nodo_Binario
from estructuras_datos.recoridos_arbol import DFS
from util.graficador import graficar_arbol_binario
from estructuras_datos.arbol_binario import Arbol_Binario

# Librerias de terceros.
import numpy
import pandas

from util.tipos_datos import Notacion_Binaria


class Shannon(object):

    def __init__(
        self,
        alfabeto: 'pandas.DataFrame',
        frecuencias: 'pandas.DataFrame',
        longitud_texto: int
    ) -> None:
        # Longitud del texto de donde proviene el alfabeto y frecuencias.
        self.longitud_texto = longitud_texto

        # Frecuencias originales de entrada del abecedaio.
        self.org_frecuencias = frecuencias.copy()

        # Alfabeto del esquema.
        self.alfabeto = alfabeto

        # Frecuencias del esquema.
        self.frecuencias = frecuencias

        # Tabla de frecuencias de sigmas.
        self.frecuencias_sigma = pandas.Series()

        # Instanciamos el arbol.
        self.arbol = Arbol_Binario()

        # Tabla de codificaciones.
        self.tabla_codificacion = pandas.Series()

    def __generar_arbol_binario(
        self,
    ) -> None:
        # Funcion lambda que genera un id para los nodos del
        # arbol binario.
        generar_id = lambda conteo : 'N{}'.format(conteo)

        # Id de la raiz del arbol binario.
        id_nodo = generar_id(self.arbol.conteo_id)

        # Primero agregamos la raiz al arbol binario.
        self.arbol[
            id_nodo
        ] = Nodo_Binario(
            id_nodo,
            valor=0
        )

        # Establemos el puntero de la raiz al nodo que se
        # acaba de agregar.
        self.arbol.raiz = id_nodo

        # Por cada simbolo con codigo.
        for id_simbolo, simbolo in zip(self.alfabeto, self.alfabeto.index):
            # Instanciamos el nodo pivote como el nodo en la raiz.
            nodo_pivote: Nodo_Binario = self.arbol[self.arbol.raiz]

            # Instanciamos la codificacion del simbolo.
            B = self.tabla_codificacion[simbolo]

            # Por cada bit en la codificacion a excepcion
            # del último bit.
            for bit in B[:-1]:
                # Convertimos el bit a un valor numerico.
                bit = int(bit)

                # Si el bit es 1, entonces navegamos a la derecha.
                if bit == 1:
                    # Si no hay hijo a la derecha.
                    if nodo_pivote.hijo_derecha is None:
                        # Aumentamos el conteo de id.
                        self.arbol.conteo_id += 1

                        # Generamos un id para el nodo.
                        id_nodo = generar_id(self.arbol.conteo_id)

                        # Agregamos el nodo al arbol.
                        self.arbol[id_nodo] = Nodo_Binario(
                            id_nodo,
                            valor=0
                        )

                        # Indicamos que el nodo agregado es el hijo del
                        # nodo pivote.
                        nodo_pivote.hijo_derecha = id_nodo

                    # Nos desplasamos al nodo hijo.
                    nodo_pivote = self.arbol[nodo_pivote.hijo_derecha]

                # Si el bit es 0, entonces navegamos a la izquierda.
                else:
                    # Si no hay hijo a la izquierda.
                    if nodo_pivote.hijo_izquierda is None:
                        # Aumentamos el conteo de id.
                        self.arbol.conteo_id += 1

                        # Generamos un id para el nodo.
                        id_nodo = generar_id(self.arbol.conteo_id)

                        # Agregamos el nodo al arbol.
                        self.arbol[id_nodo] = Nodo_Binario(
                            id_nodo,
                            valor=0
                        )

                        # Indicamos que el nodo agregado es el hijo del
                        # nodo pivote.
                        nodo_pivote.hijo_izquierda = id_nodo

                    # Nos desplasamos al nodo hijo.
                    nodo_pivote = self.arbol[nodo_pivote.hijo_izquierda]

            # Ultimo bit de la codificación.
            bit = int(B[-1])

            # Se agrega finalmente la hoja al arbol binario.
            self.arbol[id_simbolo] = Nodo_Binario(
                id_simbolo,
                simbolo=simbolo,
                valor=self.org_frecuencias[id_simbolo]
            )

            # Si el bit es 1, entonces conectamos el nodo padre con un
            # hijo a la derecha.
            if bit == 1:
                # Indicamos que el nodo agregado es el hijo del
                # nodo pivote.
                nodo_pivote.hijo_derecha = id_simbolo

            # Si el bit es 0, entonces conectamos el nodo padre con un
            # hijo a la izquierda.
            else:
                # Indicamos que el nodo agregado es el hijo del
                # nodo pivote.
                nodo_pivote.hijo_izquierda = id_simbolo

    def longitud_salida(
        self,
        frecuencias: pandas.Series
    ) -> pandas.Series:
        '''
            Calculamos la longitud promedio de salida de cada simbolo.
        '''

        # Por cada frecuencia, se calcula su longitud promedio de salida.
        longitudes = pandas.Series(
            [
                int(numpy.ceil(-numpy.log2(float(Fi)))) for Fi in frecuencias
            ],
            index=frecuencias.index
        )

        return longitudes

    def obtener_codificacion(
        self,
        notacion_binaria: Notacion_Binaria,
        longitud_salida: int,
    ) -> str:
        '''
            Retorna la codificacion dado una notacion binaria y la
            longitud de salida.
        '''

        # Primero asignamos los bits que no estan en el periodo a
        # la codificacion.
        codificacion = notacion_binaria.bits[
            :notacion_binaria.inicio_periodo
        ]

        # Si hacen falta bits para poder cumplir con la longitud de
        # salida, entonces agegamos los bits en el periodo.
        i = notacion_binaria.inicio_periodo
        while len(codificacion) < longitud_salida:
            if i >= len(notacion_binaria.bits):
                i = notacion_binaria.inicio_periodo
            codificacion += notacion_binaria.bits[i]
            i += 1

        return codificacion

    def generar_tabla_codigos(self) -> None:
        # Primero pasamos las frecuencias a fracciones, esto para
        # evitar errores en las operaciones.
        fracciones = {}
        for id in self.frecuencias.index:
            fracciones[id] = fractions.Fraction(
                int(self.frecuencias[id] * self.longitud_texto),
                self.longitud_texto
            )

        # De las frecuencias, instanciamos una serie de las fracciones.
        frecuencias_aux = pandas.Series(
            list(fracciones.values()),
            index=list(fracciones.keys())
        )

        # Ordenamos las frecuencias de manera acendente.
        frecuencias_aux.sort_values(ascending=False, inplace=True)

        # Calculamos las frecuencias acumuladas.
        frecuencias_acumuladas = Fa(frecuencias_aux)

        # Calculamos la longitud promedio de salida.
        long_prom_salida = self.longitud_salida(frecuencias_aux)

        # Por cada frecuencia acumulada, se realiza la expancion binaria.
        for simbolo, id_simbolo in zip(self.alfabeto.index, self.alfabeto):
            # Realizamos la expancion binaria de la frecuencia acumulda.
            notacion_binaria = expancion_binaria(frecuencias_acumuladas[id_simbolo])

            # Obtenemos la codifiacion para el simbolo relacionado con
            # la frecuencia acumulada.
            self.tabla_codificacion[simbolo] = self.obtener_codificacion(
                notacion_binaria,
                long_prom_salida[id_simbolo]
            )

        # Generamos el arbol binario.
        self.__generar_arbol_binario()
