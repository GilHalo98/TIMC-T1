"""
    Arbol de Hunffman, es un arbol binario modificado.
"""


# Librerias estandar.
import copy

# Librerias Propias
from estructuras_datos.nodo import Nodo_Binario
from util.graficador import graficar_arbol_binario
from estructuras_datos.arbol_binario import Arbol_Binario
from estructuras_datos.recoridos_arbol import DFS

# Librerias de terceros.
import numpy
import pandas


class Arbol_Huffman(dict):

    def __init__(
        self,
        alfabeto: 'pandas.DataFrame',
        frecuencias: 'pandas.DataFrame'
    ) -> None:
        # Frecuencias originales de entrada del abecedaio.
        self.__org_frecuencias = frecuencias

        # Alfabeto del esquema.
        self.alfabeto = alfabeto

        # Frecuencias del esquema.
        self.frecuencias = frecuencias

        # Tabla de frecuencias de sigmas.
        self.__frecuencias_sigma = pandas.Series()

        # Instanciamos el arbol.
        self.__arbol = Arbol_Binario()

        # Tabla de codificaciones.
        self.tabla_codificacion = pandas.Series()

    def __construir_arbol_binario(self) -> None:
        # Se construye el arbol binario desde la parte inferior, o
        # los nodos hasta la raiz.
        # Limpiamos el arbol binario.
        self.__arbol.flush()

        # Limpiamos tambien la tabla de codificacion.
        self.tabla_codificacion = pandas.Series()

        # Limpiamos la tabla de frecuencias sigma.
        self.__frecuencias_sigma = pandas.Series()

        # Instanciamos un zip con el simbolo y el id del simbolo.
        simbolo_id = zip(
            self.alfabeto.index,
            self.alfabeto
        )

        # Agregamos las hojas al arbol binario.
        for simbolo, id_hoja in simbolo_id:
            self.__arbol[id_hoja] = Nodo_Binario(
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
            self.__frecuencias_sigma[id_sigma] = sigma
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
            self.__arbol[id_izq].padre = id_sigma
            self.__arbol[id_der].padre = id_sigma

            # Agregamos el nodo sigma al arbol.
            self.__arbol[id_sigma] = Nodo_Binario(
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
        self.__arbol.raiz = id_sigma

        # Se cuentan el total de nodos en el arbol.
        self.__arbol.total_nodos = len(self.__arbol)

        # Graficamos el arbol de huffman.
        graficar_arbol_binario(self.__arbol, 'prueba')

        # Restablecemos las frecuencias originales.
        self.frecuencias = self.__org_frecuencias.copy()

    def generar_tabla_codigos(self) -> None:
        # Se genera la tabla de codificacion del esquema.

        # Generamos el arbol binario.
        self.__construir_arbol_binario()

        # indicamos el recorrido a usar para crear la tabla, en este 
        # se usara DFS.
        recorridos = DFS(self.__arbol)

        # Por cada recorrido.
        for recorrido in recorridos:
            # Obtenemos el nodo que retorna el recorrido.
            id_nodo = recorrido[-1]

            # Nodo actual
            nodo: Nodo_Binario = self.__arbol[id_nodo]

            # Si el nodo es una hoja o un simbolo.
            if nodo.es_hoja():
                # Codigo del simbolo.
                codigo = ''

                # Por cada conexion en el recorrido y sus nodos
                i = 0
                for _ in recorrido[:-1]:
                    # Recupera el costo de moverse de i a i + 1.
                    costo = self.__arbol[recorrido[i]].costo_hacia(
                        recorrido[i + 1]
                    )

                    # Concatenalo al codigo.
                    codigo += str(costo)
                    i += 1

                # Agrega el codigo a la tabla de codificacion.
                self.tabla_codificacion[
                    nodo.propiedades['simbolo']
                ] = codigo

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
        puntero = self.__arbol.raiz

        # Por cada simbolo en el texto codificado.
        for simbolo_bit in texto_codificado:
            # Recuperamos el bit.
            bit = int(simbolo_bit)

            # Instanciamos el nodo del puntero.
            nodo: Nodo_Binario = self.__arbol[puntero]

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
            if self.__arbol[puntero_aux].es_hoja():
                texto += self.__arbol[puntero_aux].propiedades['simbolo']
                puntero = self.__arbol.raiz

            # Sino, movemos el puntero.
            else:
                puntero = puntero_aux

        return texto

    def deltas_nodos(self) -> 'pandas.Series':
        # Retorna una serie con los deltas de los nodos, o la diferencia
        # entre ramas de la frecuencia de los nodos.
        deltas = pandas.Series()

        # Por cada nodo en el arbol.
        for id_nodo in self.__arbol:
            # Instanciamos el nodo.
            nodo: Nodo_Binario = self.__arbol[id_nodo]

            # Si no es una hoja.
            if not nodo.es_hoja():
                # Se calcula el delta de las frecuencias de sus ramas.
                delta = (
                    self.__arbol[nodo.hijo_derecha].propiedades['valor']
                    - self.__arbol[nodo.hijo_izquierda].propiedades['valor']
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


class Arbol_Hunffman_Modificado(dict):

    def __init__(
        self,
        alfabeto: 'pandas.DataFrame',
        frecuencias: 'pandas.DataFrame'
    ) -> None:
        # Frecuencias originales de entrada del abecedaio.
        self.__org_frecuencias = frecuencias

        # Alfabeto del esquema.
        self.alfabeto = alfabeto

        # Frecuencias del esquema.
        self.frecuencias = frecuencias

        # Tabla de frecuencias de sigmas.
        self.__frecuencias_sigma = pandas.Series()

        # Instanciamos el arbol.
        self.__arbol = Arbol_Binario()

        # Tabla de codificacion izquierda.
        self.tabla_codificacion_izquierda = pandas.Series()

        # Tabla de codificacion derecha.
        self.tabla_codificacion_derecha = pandas.Series()

    def __construir_arbol_binario(self) -> None:
        # Se construye el arbol binario desde la parte inferior, o
        # los nodos hasta la raiz.
        # Limpiamos el arbol binario.
        self.__arbol.flush()

        # Limpiamos la tabla de frecuencias sigma.
        self.__frecuencias_sigma = pandas.Series()

        # Instanciamos un zip con el simbolo y el id del simbolo.
        simbolo_id = zip(
            self.alfabeto.index,
            self.alfabeto
        )

        # Agregamos las hojas al arbol binario.
        for simbolo, id_hoja in simbolo_id:
            self.__arbol[id_hoja] = Nodo_Binario(
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
            self.__frecuencias_sigma[id_sigma] = sigma
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
            self.__arbol[id_izq].padre = id_sigma
            self.__arbol[id_der].padre = id_sigma

            # Agregamos el nodo sigma al arbol.
            self.__arbol[id_sigma] = Nodo_Binario(
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
        self.__arbol.raiz = id_sigma

        # Modificamos el arbol.
        self.__modificar_arbol()

        # Se cuentan el total de nodos en el arbol.
        self.__arbol.total_nodos = len(self.__arbol)

        # Graficamos el arbol de huffman.
        graficar_arbol_binario(self.__arbol, 'prueba')

        # Restablecemos las frecuencias originales.
        self.frecuencias = self.__org_frecuencias.copy()

    def __modificar_arbol(self) -> None:
        id_aux = self.__arbol[self.__arbol.raiz].hijo_derecha

        sub_arbol = {}
        del self.__arbol[id_aux]

        for id_nodo in self.__arbol:
            if id_nodo != self.__arbol.raiz:
                id_l_nodo = 'L{}'.format(id_nodo)
                
                sub_arbol[
                    id_l_nodo
                ] = copy.deepcopy(self.__arbol[id_nodo])

                sub_arbol[id_l_nodo].id_nodo = id_l_nodo

                if not sub_arbol[id_l_nodo].es_hoja():
                    sub_arbol[id_l_nodo].hijo_izquierda = 'L{}'.format(
                        sub_arbol[id_l_nodo].hijo_izquierda
                    )

                    sub_arbol[id_l_nodo].hijo_derecha = 'L{}'.format(
                        sub_arbol[id_l_nodo].hijo_derecha
                    )

                if sub_arbol[id_l_nodo].padre == self.__arbol.raiz:
                    self.__arbol[self.__arbol.raiz].hijo_derecha = id_l_nodo

                else:
                    sub_arbol[id_l_nodo].padre = 'L{}'.format(
                        sub_arbol[id_l_nodo].padre
                    )

        for id in sub_arbol:
            self.__arbol[id] = sub_arbol[id]

        self.__arbol[self.__arbol['LES'].padre].hijo_izquierda = None
        del self.__arbol['LES']

    def generar_tabla_codigos(self) -> None:
        # Se genera la tabla de codificacion del esquema.

        # Generamos el arbol binario.
        self.__construir_arbol_binario()

        # indicamos el recorrido a usar para crear la tabla, en este 
        # se usara DFS.
        recorridos = DFS(self.__arbol)

        # Por cada recorrido.
        for recorrido in recorridos:
            # Obtenemos el nodo que retorna el recorrido.
            id_nodo = recorrido[-1]

            # Nodo actual
            nodo: Nodo_Binario = self.__arbol[id_nodo]

            # Si el nodo es una hoja o un simbolo.
            if nodo.es_hoja():
                # Codigo del simbolo.
                codigo = ''

                # Index del codigo.
                i = 0

                # bit incial
                bit_inicial = self.__arbol[recorrido[i]].costo_hacia(
                    recorrido[i + 1]
                )

                # Por cada conexion en el recorrido y sus nodos
                for _ in recorrido[:-1]:
                    # Recupera el costo de moverse de i a i + 1.
                    costo = self.__arbol[recorrido[i]].costo_hacia(
                        recorrido[i + 1]
                    )

                    # Concatenalo al codigo.
                    codigo += str(costo)
                    i += 1

                if bit_inicial:
                    # Agrega el codigo a la tabla de codificacion.
                    self.tabla_codificacion_derecha[
                        nodo.propiedades['simbolo']
                    ] = codigo

                else:
                    # Agrega el codigo a la tabla de codificacion.
                    self.tabla_codificacion_izquierda[
                        nodo.propiedades['simbolo']
                    ] = codigo

    def codificar(self, texto: str, secreto: str) -> str:
        '''
            Codifica y embebe un mensaje secreto binario en la
            codificacion, es importante notar que
            len(texto) < len(secreto)
        '''
        # Longitud del mensaje secreto binario.
        long_secreto = len(secreto)

        # Mensaje codificado binario.
        stego = ''

        # Primero embebemos el secreto en la codificacion del cover.
        i = 0
        for i in range(long_secreto):
            # Obtenemos el bit en la posicion i del secreto
            bit = int(secreto[i])

            # Obtenemos el caracter en la posicion i del cover.
            caracter = texto[i]

            # Codigo a agregar en el stego.
            codigo = ''

            # Si el bit es 1, entonces se codifica con el codigo a la
            # derecha.
            if bit == 1:
                codigo = self.tabla_codificacion_derecha[caracter]

            # Si es 0, se codifica con el codigo a la izquierda.
            else:
                codigo = self.tabla_codificacion_izquierda[caracter]

            # Agregamos el codigo al stego
            stego += codigo

        # Una vez terminada la integracion del secreto en el stego, se
        # agrega el codigo para ES.
        codigo = ''
        if 'ES' in self.tabla_codificacion_derecha.index:
            codigo = self.tabla_codificacion_derecha['ES']
        else:
           codigo = self.tabla_codificacion_izquierda['ES']
        stego += codigo

        # Ahora terminamos de codifiar el texto sobrante.
        for caracter in texto[i + 1:]:
            # Codigo a agregar en el stego.
            stego += self.tabla_codificacion_izquierda[caracter]

        return stego

    def decodificar(self, stego: str) -> 'tuple[str]':
        # Decodifica un texto codificado con el esquema.
        texto = ''

        # Secreto decodificado.
        secreto = ''

        # Puntero auxiliar.
        puntero = self.__arbol.raiz

        # Longitud del texto codificado.
        long_texto_cod = len(stego)

        # Indica si se encontro el final del secreto.
        final_secreto = False

        # Primero decodificamos el texto que contiene el secreto.
        i = 0
        primer_bit = stego[i]
        while not final_secreto and i < long_texto_cod:
            # Recuperamos el bit.
            bit = int(stego[i])

            # Recuperamos el nodo actual.
            nodo: Nodo_Binario = self.__arbol[puntero]

            # Si el nodo es una hoja.
            if nodo.es_hoja():
                # Recuperamos el simbolo que represeta.
                simbolo = nodo.propiedades['simbolo']

                # Si no es el simbolo de finalizacion del secreto
                # repetimos el proceso con el siguiente conjunt de bits
                if simbolo != 'ES':
                    # Resetamos puntero a la raiz
                    puntero = self.__arbol.raiz
                    # Agregamos simbolo decodificado al texto
                    texto += simbolo

                    # Agregamos el primer bit al secret.
                    secreto += primer_bit
 
                    # Actualizamos cual es el primer bit.
                    primer_bit = stego[i]

                # Si es el simbolo de finalizacion, terminamos el ciclo.
                else:
                    final_secreto = True

            # Si el nodo no es una hoja, nos seguimos moviendo.
            else:
                #  Si el bit es 1, nos movemos a la derecha, sino, nos
                # movemos a la izquierda.
                if bit == 1:
                    puntero = nodo.hijo_derecha

                else:
                    puntero = nodo.hijo_izquierda

                i += 1

        # Resetamos el puntero a la raiz.
        puntero = self.__arbol.raiz

        # Por cada simbolo restante.
        while i < long_texto_cod:
            # Recuperamos el bit.
            bit = int(stego[i])

            # Recuperamos el nodo actual.
            nodo: Nodo_Binario = self.__arbol[puntero]

            # Si el nodo es una hoja.
            if nodo.es_hoja():
                # Recuperamos el simbolo que represeta.
                simbolo = nodo.propiedades['simbolo']

                # Agregamos el simbolo decodificado al texto.
                texto += simbolo

                # Resetamos el puntero a la raiz.
                puntero = self.__arbol.raiz

            # Si el nodo no es una hoja, nos seguimos moviendo.
            else:
                #  Si el bit es 1, nos movemos a la derecha, sino, nos
                # movemos a la izquierda.
                if bit == 1:
                    puntero = nodo.hijo_derecha

                else:
                    puntero = nodo.hijo_izquierda

                i += 1

        # Agregamos el ultimo simbolo.
        texto += self.__arbol[puntero].propiedades['simbolo']

        return texto, secreto

    def deltas_nodos(self) -> 'pandas.Series':
        # Retorna una serie con los deltas de los nodos, o la diferencia
        # entre ramas de la frecuencia de los nodos.
        deltas = pandas.Series()

        # Por cada nodo en el arbol.
        for id_nodo in self.__arbol:
            # Instanciamos el nodo.
            nodo: Nodo_Binario = self.__arbol[id_nodo]

            # Si no es una hoja.
            if not nodo.es_hoja():
                # Se calcula el delta de las frecuencias de sus ramas.
                delta = (
                    self.__arbol[nodo.hijo_derecha].propiedades['valor']
                    - self.__arbol[nodo.hijo_izquierda].propiedades['valor']
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