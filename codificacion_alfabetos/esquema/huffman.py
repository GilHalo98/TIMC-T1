"""
    Arbol de Hunffman, es un arbol binario modificado.
"""

# Librerias estandar.
import pathlib

# Librerias Propias
from util.funciones import Ie, He
from util.constantes import Tipo_Operacion
from estructuras_datos.nodo import Nodo_Binario
from estructuras_datos.recoridos_arbol import DFS
from util.graficador import graficar_arbol_binario
from estructuras_datos.arbol_binario import Arbol_Binario

# Librerias de terceros.
import numpy
import pandas


class Arbol_Huffman(object):

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

    def codificar(self, texto: str) -> str:
        # Codifica un texto dado con el esquema.
        texto_codificado = ''

        for caracter in texto:
            codigo = self.tabla_codificacion[caracter]
            texto_codificado += codigo

        return texto_codificado

    def decodificar(self, texto_codificado: str) -> str:
        # Decodifica un texto codificado con el esquema.
        texto = ''

        # Puntero auxiliar.
        puntero = self.arbol.raiz

        # Por cada simbolo en el texto codificado.
        for simbolo_bit in texto_codificado:
            # Recuperamos el bit.
            bit = int(simbolo_bit)

            # Instanciamos el nodo del puntero.
            nodo: Nodo_Binario = self.arbol[puntero]

            # Instanciamos un puntero auxiliar.
            puntero_aux = None

            #  Si el bit es 1, nos movemos a la derecha, sino, nos
            # movemos a la izquierda.
            if bit == 1:
                puntero_aux = nodo.hijo_derecha

            else:
                puntero_aux = nodo.hijo_izquierda

            # Si el nodo hijo es una hoja, entonces retornamos el
            # simbolo decodificado y reseteamos el puntero a la raiz
            # del arbol.
            if self.arbol[puntero_aux].es_hoja():
                texto += self.arbol[puntero_aux].propiedades['simbolo']
                puntero = self.arbol.raiz

            # Sino, movemos el puntero.
            else:
                puntero = puntero_aux

        return texto

    def deltas_nodos(self) -> 'pandas.Series':
        # Retorna una serie con los deltas de los nodos, o la diferencia
        # entre ramas de la frecuencia de los nodos.
        deltas = pandas.Series()

        # Por cada nodo en el arbol.
        for id_nodo in self.arbol:
            # Instanciamos el nodo.
            nodo: Nodo_Binario = self.arbol[id_nodo]

            # Si no es una hoja.
            if not nodo.es_hoja():
                # Se calcula el delta de las frecuencias de sus ramas.
                delta = (
                    self.arbol[nodo.hijo_derecha].propiedades['valor']
                    - self.arbol[nodo.hijo_izquierda].propiedades['valor']
                )

                # Unicamente deltas mayores a 0 son tomadas en cuenta.
                if delta > 0:
                    deltas[id_nodo] = delta

        return deltas

    def longitud_promedio_salida(self) -> float:
        Ls = 0

        # Por cada simbolo en el alfabeto.
        for simbolo in self.tabla_codificacion.index:
            # Buscamos su codigo.
            codigo = self.tabla_codificacion[simbolo]
            id = self.alfabeto[simbolo]

            # Calculamos la longitud promedio de salida,
            # longitud del codigo * frecuencia de simbolo.
            Ls += len(codigo) * self.frecuencias[id]

        # Las unidades son equivalentes al tipo de operacion.
        return Ls

    def radio_comprecion(self, Le: float) -> float:
        # Calcula el radio de comprecion del esquema.
        Ls = self.longitud_promedio_salida()

        return Le / Ls

    def generar_reporte(self, dir_archivo: str) -> None:
        # Genera un archivo reporte del esquema.

        # Graficamos el arbol de huffman.
        graficar_arbol_binario(self.arbol, dir_archivo)

        # Instanciamos el directorio del archivo.
        directorio = pathlib.Path(dir_archivo + '.txt')

        # Creamos el archivo del reporte.
        with open(directorio, 'w+', encoding='utf-8') as objeto_archivo:

            # Se calcula la informacion mutua de la entrada.
            inf_mutua_entrada = Ie(
                self.org_frecuencias,
                Tipo_Operacion.TRANSMISION_DATOS
            )

            # Se calcula la entropia de entrada.
            entropia_entrada = He(
                self.org_frecuencias,
                inf_mutua_entrada
            )

            # Creamos un dataframe que mantenga el reporte
            # de los datos de entrada.
            reporte_entrada = pandas.DataFrame(
                {
                    'Simbolo': [
                        simbolo for simbolo in self.alfabeto.index
                    ],
                    'Frecuencia': [
                        round(Fi, 2) for Fi in self.org_frecuencias
                    ],
                    'Conteo': [int(
                        self.longitud_texto * frecuencia
                    ) for frecuencia in self.org_frecuencias],
                    'Información (Bits/Simbolo)': [
                        'I(i) = -log2({}) = {}'.format(
                            round(Fi, 2),
                            round(Ii, 2)
                        ) for Fi, Ii in zip(
                            self.org_frecuencias,
                            inf_mutua_entrada
                        )
                    ],
                    'Entropia (Bits/Simbolo)': [
                        'E(i) = {} * {} = {}'.format(
                            round(Fi, 2),
                            round(Ii, 2),
                            round(Hi, 2),
                        ) for Fi, Ii, Hi  in zip(
                            self.org_frecuencias,
                            inf_mutua_entrada,
                            entropia_entrada
                        )
                    ],
                },
                index=self.org_frecuencias.index
            )
            # Escribimos el reporte de entrada.
            objeto_archivo.write('\nReporte de entrada\n')
            objeto_archivo.write(reporte_entrada.to_string())

            # Entropia de la entrada.
            objeto_archivo.write(
                '\nEntropia de entrada: {0:.2f} Bits/Simbolo\n'.format(
                    sum(entropia_entrada)
                )
            )

            # Se genera el reporte de salida.
            reporte_salida = pandas.DataFrame(
                {
                    'Simbolo': [
                        simbolo for simbolo  in self.alfabeto.index
                    ],
                    'Codificacion': [
                        self.tabla_codificacion[simbolo] for simbolo in self.alfabeto.index
                    ],
                    'Longitud': [
                        len(self.tabla_codificacion[simbolo]) for simbolo in self.alfabeto.index
                    ],
                    'Longitud salida': [
                        'LS(i) = {} * {} = {}'.format(
                            len(self.tabla_codificacion[simbolo]),
                            round(Fi, 2),
                            round(len(self.tabla_codificacion[simbolo]) * Fi, 2)
                        ) for simbolo, Fi in zip(
                            self.alfabeto.index,
                            self.org_frecuencias
                        )
                    ],
                },
                index=self.org_frecuencias.index
            )

            # Escribimos el reporte de salida.
            objeto_archivo.write('\nReporte de salida\n')
            objeto_archivo.write(reporte_salida.to_string())

            # Longitud promedio de salida.
            objeto_archivo.write(
                '\nLongitud promedio de salida {0:.2f} Bits/Simbolo'.format(
                    self.longitud_promedio_salida()
                )
            )

            # Radio de comprecion.
            radio_comprecion = self.radio_comprecion(8)
            objeto_archivo.write(
                '\nRadio de comprecion {0:.2f}'.format(
                    radio_comprecion
                )
            )

            # Eficiencia del esquema.
            eficiencia = 1 / radio_comprecion
            objeto_archivo.write(
                '\nEficiencia del esquema {0:.2f}%\n'.format(
                    eficiencia * 100
                )
            )

            # Calculamos los deltas de los nodos.
            deltas = self.deltas_nodos()

            # Calculamos la informacion mutua de los deltas.
            inf_mutua_deltas = Ie(deltas, Tipo_Operacion.TRANSMISION_DATOS)
            entropia_deltas = He(deltas, inf_mutua_deltas)

            # Creamos un dataframe del esquema.
            reporte_esquema = pandas.DataFrame(
                {
                    'Delta': [round(Fi, 2) for Fi in deltas],
                    'Información (Bits/Simbolo)': [
                        'I(i) = -log2({}) = {}'.format(
                            round(Fi, 2),
                            round(Ii, 2)
                        ) for Fi, Ii in zip(
                            deltas,
                            inf_mutua_deltas
                        )
                    ],
                    'Entropia (Bits/Simbolo)': [
                        'E(i) = {} * {} = {}'.format(
                            round(Fi, 2),
                            round(Ii, 2),
                            round(Hi, 2),
                        ) for Fi, Ii, Hi  in zip(
                            deltas,
                            inf_mutua_deltas,
                            entropia_deltas
                        )
                    ],
                },
                index=deltas.index
            )

            # Escribimos el reporte del  esquema.
            objeto_archivo.write('\nReporte del esquema\n')
            objeto_archivo.write(reporte_esquema.to_string())

            # Escribimos la entropia del esquema.
            objeto_archivo.write(
                '\nEntropia del esquema: {0:.2f} Bits/Simbolo\n'.format(
                    sum(entropia_deltas)
                )
            )


class Huffman_Jerarquico(Arbol_Huffman):

    def __init__(
        self,
        alfabeto: 'pandas.DataFrame',
        frecuencias: 'pandas.DataFrame',
        longitud_texto: int
    ) -> None:
        # Inicializamos la clase padre.
        Arbol_Huffman.__init__(
            self,
            alfabeto,
            frecuencias,
            longitud_texto
        )

    def __construir_arbol_binario(self) -> None:
        # Se construye el arbol binario desde la parte inferior, o
        # los nodos hasta la raiz.
        # Limpiamos el arbol binario.
        self.arbol.flush()

        # Limpiamos tambien la tabla de codificacion.
        self.tabla_codificacion = pandas.Series()

        # Limpiamos la tabla de frecuencias sigma.
        self.frecuencias_sigma = pandas.Series()

        # Instanciamos un zip con el simbolo y el id del simbolo.
        simbolo_id = zip(
            self.alfabeto.index,
            self.alfabeto
        )

        # Agregamos las hojas al arbol binario.
        for simbolo, id_hoja in simbolo_id:
            self.arbol[id_hoja] = Nodo_Binario(
                id_hoja,
                valor=self.frecuencias[id_hoja],
                simbolo=simbolo
            )

        # Primero creamos una copia auxiliar de las frecuencias.
        frecuencias_aux = self.frecuencias.copy()

        # Organizamos las frecuencias de manera decendente.
        frecuencias_aux.sort_values(ascending=True, inplace=True)

        # Ahora construimos el arbol desde las hojas hasta la raiz.
        s = 0
        while not frecuencias_aux.empty:
            # Extraemos los simbolos con menor frecuencia.
            simbolo_a = frecuencias_aux.index[0]
            simbolo_b = frecuencias_aux.index[1]

            # Calculamos su sigma, una suma de las frecuencias de ambos
            # simbolos.
            id_sigma = 'N{}'.format(s)
            sigma = frecuencias_aux[simbolo_a] + frecuencias_aux[simbolo_b]

            # Se agrega el sigma a una tabla de frecuencias de sigma.
            self.frecuencias_sigma[id_sigma] = sigma
            self.frecuencias[id_sigma] = sigma

            # Se agrega el sigma como una frecuencia en la
            # tabla de frecuencias auxiliar.
            frecuencias_aux[id_sigma] = sigma

            # Agregamos el nodo del sigma con correspondencia a su
            # frecuencia calculada.
            if self.frecuencias[simbolo_a] > self.frecuencias[simbolo_b]:
                id_der = simbolo_a
                id_izq = simbolo_b

            else:
                id_der = simbolo_b
                id_izq = simbolo_a

            # Actualizamos la conexion del padre de los hijos del nodo
            # sigma.
            self.arbol[id_izq].padre = id_sigma
            self.arbol[id_der].padre = id_sigma

            # Agregamos el nodo sigma al arbol.
            self.arbol[id_sigma] = Nodo_Binario(
                id_sigma,
                hijo_izquierda=id_izq,
                hijo_derecha=id_der,
                valor=sigma
            )

            # Eliminamos las frecuencias seleccionadas de la tabla de
            # frecuencias auxiliar.
            frecuencias_aux.pop(simbolo_a)
            frecuencias_aux.pop(simbolo_b)

            # Si existe un unico elemento, eso quiere decir que
            # encontramos la raiz.
            if len(frecuencias_aux) <= 1:
                break

            # Organizamos las frecuencias de manera decendente.
            frecuencias_aux.sort_values(ascending=True, inplace=True)

            # Aumentamos el conteo de sigmas.
            s += 1

        # El ultimo sigma calculado es la raiz del arbol.
        self.arbol.raiz = id_sigma

        # Se cuentan el total de nodos en el arbol.
        self.arbol.total_nodos = len(self.arbol)

        # Restablecemos las frecuencias originales.
        self.frecuencias = self.org_frecuencias.copy()

    def generar_tabla_codigos(self) -> None:
        # Se genera la tabla de codificacion del esquema.

        # Generamos el arbol binario.
        self.__construir_arbol_binario()

        # indicamos el recorrido a usar para crear la tabla, en este 
        # se usara DFS.
        recorridos = DFS(self.arbol)

        # Por cada recorrido.
        for recorrido in recorridos:
            # Obtenemos el nodo que retorna el recorrido.
            id_nodo = recorrido[-1]

            # Nodo actual
            nodo: Nodo_Binario = self.arbol[id_nodo]

            # Si el nodo es una hoja o un simbolo.
            if nodo.es_hoja():
                # Codigo del simbolo.
                codigo = ''

                # Por cada conexion en el recorrido y sus nodos
                i = 0
                for _ in recorrido[:-1]:
                    # Recupera el costo de moverse de i a i + 1.
                    costo = self.arbol[recorrido[i]].costo_hacia(
                        recorrido[i + 1]
                    )

                    # Concatenalo al codigo.
                    codigo += str(costo)
                    i += 1

                # Agrega el codigo a la tabla de codificacion.
                self.tabla_codificacion[
                    nodo.propiedades['simbolo']
                ] = codigo


class Huffman_Balanceado(Arbol_Huffman):

    def __init__(
        self,
        alfabeto: 'pandas.DataFrame',
        frecuencias: 'pandas.DataFrame',
        longitud_texto: int
    ) -> None:
        # Inicializamos la clase padre.
        Arbol_Huffman.__init__(
            self,
            alfabeto,
            frecuencias,
            longitud_texto
        )

        # Conteo de Id de los nodos.
        self.conteo = 0

    def __particion_alfabeto(
        self,
        id_padre: 'str | int',
        frecuencias: pandas.Series,
        frecuencia_nivel: int = 1,
        nivel: int = 0,
    ) -> None:
        # Agregamos la frecuencia acumulada del nodo.
        self.frecuencias_sigma[id_padre] = sum(frecuencias)

        if len(frecuencias) == 2:
            # Si existen unicamente dos elementos en la frecuencia
            # separa los elementos en dos grupos distintos y recursa.
            grupo_a = pandas.Series(
                frecuencias[frecuencias.index[0]],
                index=[frecuencias.index[0]]
            )

            grupo_b = pandas.Series(
                frecuencias[frecuencias.index[1]],
                index=[frecuencias.index[1]]
            )

        else:
            # Organizamos las frecuencias de manera decendente.
            frecuencias.sort_values(ascending=False, inplace=True)

            # Creamos una serie grupo A.
            grupo_a = pandas.Series()

            # Por cada frecuencia.
            for id in frecuencias.index:
                Fi = frecuencias[id]

                # Si la frecuencia acumulada es menor que la frecuencia
                # maxima del nivel.
                if sum(grupo_a) + Fi < frecuencia_nivel:
                    # Agregala al grupo.
                    grupo_a[id] = Fi

            # Excluimos los elementos que pertenecen al grupo A y creamos
            # otro grupo, grupo B
            grupo_b = frecuencias.drop(grupo_a.index)

            # Si el grupo A esta vacio, asigna una
            # frecuencia y descartala del grupo B.
            if len(grupo_a) == 0:
                grupo_a = grupo_b.drop(grupo_b.index[0])
                grupo_b = grupo_b.drop(grupo_a.index)

            # Si el grupo B esta vacio, asigna una
            # frecuencia y descartala del grupo A.
            if len(grupo_b) == 0:
                grupo_b = grupo_a.drop(grupo_a.index[0])
                grupo_b = grupo_b.drop(grupo_b.index)

        # Asignamos el id al nodo.
        self.conteo += 1 if len(grupo_b) > 1 else 0
        id_nodo_b = 'N{}'.format(self.conteo)

        # Asignamos el id al nodo.
        self.conteo += 1 if len(grupo_a) > 1 else 0
        id_nodo_a = 'N{}'.format(self.conteo)

        # Asigna la direccion de los grupos.
        if len(grupo_a) > len(grupo_b):
            id_hijo_izq = id_nodo_b
            grupo_izq= grupo_b

            id_hijo_der = id_nodo_a
            grupo_der= grupo_a

        else:
            id_hijo_izq = id_nodo_a
            grupo_izq= grupo_a

            id_hijo_der = id_nodo_b
            grupo_der= grupo_b

        if len(grupo_izq) > 1:
            # Recursa la particion del grupo A.
            self.__particion_alfabeto(
                id_hijo_izq,
                grupo_izq,
                frecuencia_nivel / 2,
                nivel + 1
            )

        else:
            # Si la cantidad de los elementos es menor o igual a 1
            # entonces asigna el hijo y su direccion.
            if len(grupo_izq) > len(grupo_der):
                id_hijo_der = grupo_izq.index[0]

            else:
                id_hijo_izq = grupo_izq.index[0]

        if len(grupo_der) > 1:
            # Recursa la particion del grupo B.
            self.__particion_alfabeto(
                id_hijo_der,
                grupo_der,
                frecuencia_nivel / 2,
                nivel + 1
            )

        else:
            # Si la cantidad de los elementos es menor o igual a 1
            # entonces asigna el hijo y su direccion.
            if len(grupo_izq) > len(grupo_der):
                id_hijo_izq = grupo_der.index[0]

            else:
                id_hijo_der = grupo_der.index[0]

        # Agregamos el nodo al arbol binario.
        self.arbol[id_padre] = Nodo_Binario(
            id_padre,
            valor=sum(frecuencias),
            hijo_izquierda=id_hijo_izq,
            hijo_derecha=id_hijo_der,
        )

    def __construir_arbol_binario(self) -> None:
        '''
            Se construye el arbol de huffman balanceado,
            este arbol se construye desde la raiz hacia las hojas.
        '''

        # Se construye el arbol binario desde la parte inferior, o
        # los nodos hasta la raiz.
        # Limpiamos el arbol binario.
        self.arbol.flush()

        # Limpiamos tambien la tabla de codificacion.
        self.tabla_codificacion = pandas.Series()

        # Limpiamos la tabla de frecuencias sigma.
        self.frecuencias_sigma = pandas.Series()

        # Instanciamos un zip con el simbolo y el id del simbolo.
        simbolo_id = zip(
            self.alfabeto.index,
            self.alfabeto
        )

        # Agregamos las hojas al arbol binario.
        for simbolo, id_hoja in simbolo_id:
            self.arbol[id_hoja] = Nodo_Binario(
                id_hoja,
                valor=self.frecuencias[id_hoja],
                simbolo=simbolo
            )

        # Primero creamos una copia auxiliar de las frecuencias.
        frecuencias_aux = self.frecuencias.copy()

        # Id del nodo raiz.
        id_raiz = 'N{}'.format(self.conteo)

        # Agregamos la frecuencia acumulada de nodo raiz.
        self.frecuencias_sigma[id_raiz] = sum(frecuencias_aux)

        # Realizamo la particion de las frecuencias para poder asignar
        # los nodos.
        self.__particion_alfabeto(
            id_raiz,
            frecuencias_aux,
            0.5,
            1
        )

        # Establecemos los valores del arbol.
        self.arbol.raiz = id_raiz
        self.arbol.total_nodos = len(self.arbol)

    def generar_tabla_codigos(self) -> None:
        # Se genera la tabla de codificacion del esquema.

        # Generamos el arbol binario.
        self.__construir_arbol_binario()

        # indicamos el recorrido a usar para crear la tabla, en este 
        # se usara DFS.
        recorridos = DFS(self.arbol)

        # Por cada recorrido.
        for recorrido in recorridos:
            # Obtenemos el nodo que retorna el recorrido.
            id_nodo = recorrido[-1]

            # Nodo actual
            nodo: Nodo_Binario = self.arbol[id_nodo]

            # Si el nodo es una hoja o un simbolo.
            if nodo.es_hoja():
                # Codigo del simbolo.
                codigo = ''

                # Por cada conexion en el recorrido y sus nodos
                i = 0
                for _ in recorrido[:-1]:
                    # Recupera el costo de moverse de i a i + 1.
                    costo = self.arbol[recorrido[i]].costo_hacia(
                        recorrido[i + 1]
                    )

                    # Concatenalo al codigo.
                    codigo += str(costo)
                    i += 1

                # Agrega el codigo a la tabla de codificacion.
                self.tabla_codificacion[
                    nodo.propiedades['simbolo']
                ] = codigo
