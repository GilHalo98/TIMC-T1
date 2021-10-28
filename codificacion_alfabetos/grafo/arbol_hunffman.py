"""
    Arbol de Hunffman, es un arbol binario modificado.
"""


# Dependencias.
from grafo.nodo import Nodo

# Librerias de terceros.
from graphviz import Graph


class Arbol_Hunffman(object):
    """
        Arbol binario extendido para usarse como un arbol de Hunffman.

        Falta agregar longitud media de salida, que es la frecuencia de salida
        por la longitud del caracter. en este caso es:
            por cada codificacion de cada caracter, se hace una sumatoria de
            su frecuencia y la longitud de la codifiacion.

        El radio de comprecion es calculado como la divicion entre la longitud
        media de entrada sobre la longitud media de salida.
    """

    # Constructor de clase.
    def __init__(self, diccionario, frecuencias):
        # Almacena la id de la raiz, por default es 0
        self.id_raiz = None

        # La topologia del arbol es descrita por un diccionario.
        # Los diccionarios estan compuestos por id: Nodo
        self.topologia = {}

        # Mantiene los id de los nodos que se agregan unicos.
        self.__id = 0

        # Total de nodos en el arbol.
        self.total_nodos = 0

        # Diccionario de caracteres.
        self.diccionario = diccionario

        # Diccionario de codigos para encriptar.
        self.diccionario_codigos = {}

        # Longitud media de salida.
        self.longitud_media_salia = 0

        # Frecuencias de los caracteres.
        self.frecuencias = frecuencias

        # Longitud media de salida.
        self.longitud_media_salida = 0

        # Longitud media de entrada.
        self.longitud_media_entrada = 0

        # Radio del comprecion del arbol.
        self.radio_comprecion = 0

        # Genera el arbol canonico de Huffman.
        self.__generar_arbol()

    # Retorna la codificacion hasta un caracter, esto se hace con el costo
    # de las aristas, dada una ruta a seguir.
    def __get_codificacion(self, ruta):
        codigo = ''

        for i in range(len(ruta) - 1):
            if self.topologia[ruta[i]].hijo_izquierda == ruta[i + 1]:
                codigo += '0'
            else:
                codigo += '1'

        return codigo

    # Crea el arbol binario desde un diccionario.
    def __generar_arbol(self):
        # Agregamos las hojas del arbol.
        for id in self.frecuencias:
            self.topologia[id] = Nodo(
                id,
                self.frecuencias[id]
            )

            # Aumenta la cantidad de nodos en 1.
            self.total_nodos += 1

        # Para poder generar el arbol como tal se usa una frontera, pero
        # esta contiene los nodos hojas ya que tecnicamente el arbol de
        # hunffman se contruye de las hojas a la raiz.
        frontera = list(self.frecuencias.keys()).copy()

        # Mientras que exitan mas de dos nodos por expandir en la
        # frontera.
        while len(frontera) > 1:
            # Un proceso unico en los arboles de hunffman es que el
            # orden en que se realizan las operaciones es de manera
            # decendente, por eso se ordena de manera decendente la
            # frontera.
            frontera = sorted(frontera, key=self.frecuencias.__getitem__)

            # Se asigna un id al valor omega calculado.
            nuevo_id = 'q' + str(self.__id)

            # Se almacena el nuevo valor omega en las frecuencias.
            self.frecuencias[nuevo_id] = (
                self.frecuencias[frontera[0]]
                + self.frecuencias[frontera[1]]
            )

            # Dependiendo del valor de la frecuencia del hijo se
            # selecciona la direccion de conexion.
            if frontera[1] <= frontera[0]:
                # Si el valor del hijo A es menor que B entonces se
                # conecta A sobre la izquierda.
                hi = frontera[1]
                hd = frontera[0]

            else:
                # Si B es mayor que A, entonces B se conecta a la izquierda.
                hi = frontera[0]
                hd = frontera[1]

            # Se genera un nuevo nodo conteniendo el nuevo omega.
            self.topologia[nuevo_id] = Nodo(
                nuevo_id,
                self.frecuencias[nuevo_id],
                hijo_izquierda=hi,
                hijo_derecha=hd
            )

            # Aumenta la cantidad de nodos en 1.
            self.total_nodos += 1

            # Se actualiza el padre de los nodos usados.
            self.topologia[frontera[0]].padre = nuevo_id
            self.topologia[frontera[1]].padre = nuevo_id

            # Se eliminan los nodos expandidos de la frontera
            frontera = frontera[2:]

            # Se agrega el nuevo nodo encontrado
            frontera.insert(0, nuevo_id)

            # Aumenta el id en uno.
            self.__id += 1

        # Por ultimo, la raiz es el ultimo nodo generado.
        self.id_raiz = nuevo_id

        # Lo ultimo que queda es generar los codigos del encriptado.
        for id_caracter, codigo in self.codigos():
            self.diccionario_codigos[
                self.diccionario[id_caracter]
            ] = codigo

        # Ahora se calcula la frecuencia media de entrada, salida y el
        # radio del comprecion de arbol canonico.

        # Primer calculamos la frecuencia de entrada.
        for id in self.frecuencias:
            frecuencia = self.frecuencias[id]
            if id in self.diccionario:
                caracter = self.diccionario[id]
                codigo = self.diccionario_codigos[caracter]
                self.longitud_media_salida += len(codigo) * float(frecuencia)
                # print(caracter, codigo, frecuencia)

    # Grafica el arbol de hunffman.
    def graficar(self, archivo_salida):
        codificacion = {}
        for id, codigo in self.codigos():
            codificacion[id] = codigo

        grafico = Graph(
            comment='Test',
            format='svg',
        )
        grafico.node_attr['shape'] = 'circle'

        # Lista todos los id de nodos en el arbol.
        nodos = list(self.topologia.values())

        # Invierte el orden de estos, con esto empezamos desde la raiz.
        nodos.reverse()

        # Por cada nodo en el arbol.
        for nodo in nodos:
            # Si el nodo no es una hoja, se agrega el vertice de los hijos.
            if not nodo.es_hoja():
                # Se agrega el nodo en el grafico.
                grafico.node(
                    str(nodo.id_nodo),
                    str('{}'.format(nodo.contenido))
                )

                # Hijo de la izquierda.
                grafico.edge(
                    str(nodo.id_nodo),
                    str(nodo.hijo_izquierda),
                    str(nodo.costo_izquierda)
                )

                # Hijo de la derecha.
                grafico.edge(
                    str(nodo.id_nodo),
                    str(nodo.hijo_derecha),
                    str(nodo.costo_derecha)
                )

            else:
                # Caracter en cuestion.
                c = self.diccionario[nodo.id_nodo]

                # Casos para  caracteres especiales.
                if c == '\n':
                    # Salto de linea.
                    c = 'NUEVA LINEA'

                elif c == ' ':
                    # Espacio.
                    c = 'ESPACIO'

                # Grafico de nodo hoja.
                contenido = '{{'
                contenido += c
                contenido += ' | '
                contenido += str('{}'.format(nodo.contenido))
                contenido += ' } | '
                contenido += codificacion[nodo.id_nodo] + ' }'

                # Si el nodo es una hoja, se agrega tambien su caracter.
                grafico.node(
                    str(nodo.id_nodo),
                    label=contenido,
                    shape='Mrecord'
                )

        # Por ultimo renderiza el grafo en un archivo svg.
        grafico.render(filename=archivo_salida)

    # Utiliza DFS para retornar la codificacion de los caracteres.
    def codigos(self):
        # Almacena la ruta en donde se encuentra, con esto podemos
        # saber la codificacion del caracter.
        ruta = []

        # Lista de nodos visitados.
        visitados = []

        # Cantida de nodos visitados, controla el ciclo.
        total_visitados = 0

        # Nodo donde se comienza el DFS
        id_nodo = self.id_raiz

        # Mientas que queden nodos por visitar.
        while total_visitados < self.total_nodos:

            # Se agrega el nodo a la ruta.
            ruta.append(id_nodo)

            # Si el nodo no esta marcado como visitado, se agrega.
            if id_nodo not in visitados:
                visitados.append(id_nodo)
                total_visitados += 1

            # En este punto, si el nodo es una hoja, retorna la codificacion
            # del caracter, para esto se usa la ruta y el peso de las aristas.
            if self.topologia[id_nodo].es_hoja():
                # Se usan generadores para que no genere tanta memoria.
                yield id_nodo, self.__get_codificacion(ruta)

                # Regresamos una posicion en la ruta.
                id_nodo = ruta.pop()
                id_nodo = ruta.pop()

            # Si no es una hoja.
            else:
                if self.topologia[id_nodo].hijo_izquierda not in visitados:
                    # Si el hijo en izquierda no esta visitado, el puntero
                    # se mueve a dicho hijo.
                    id_nodo = self.topologia[id_nodo].hijo_izquierda

                elif self.topologia[id_nodo].hijo_derecha not in visitados:
                    # Si el hijo sobre la izquierda ya esta visitado, selecciona
                    # el de la derecha si no esta visitado.
                    id_nodo = self.topologia[id_nodo].hijo_derecha

                else:
                    # Si los dos ya han sido visitados, entonces
                    # retorna un nodo.
                    id_nodo = ruta.pop()
                    id_nodo = ruta.pop()

    # Encripta un texto dado con el arbol de Huffman.
    def encriptar(self, texto):
        # Texto encriptado en binario.
        texto_encriptado = ''

        # Conteo de bits del byte.
        conteo_bit = 0

        # Representacion binaria de byte.
        byte = ''

        # Por cada caracter en el texto.
        for c in texto:

            # Por cada bit en la codificacion del caracter.
            for bit in self.diccionario_codigos[c]:

                # Si conteo del byte es 8.
                if conteo_bit == 8:
                    # Se agrega el byte al texto encriptado.
                    texto_encriptado += byte

                    # Se agrega el siguiente bit al byte.
                    byte = bit

                    # El conteo se resetea a 1.
                    conteo_bit = 1

                # En caso anterior.
                else:
                    # Se agrega el bit al byte.
                    byte += bit

                    # Aumenta el conteo del byte.
                    conteo_bit += 1

        # Si el ultimo byte no esta completo, no tiene 8 bits,
        # se agrega.
        if len(byte) > 0:
            texto_encriptado += byte

        return texto_encriptado

    # Desencripta un texto dado con el arbol de Huffman.
    def desencriptar(self, texto_encriptado):
        # El nodo actual en el que se encuentra el puntero.
        nodo_acutal = self.id_raiz

        # El texto desencriptado.
        texto = ''

        # Longitud del texto encriptado.
        n = len(texto_encriptado)

        i = 0
        while i < n:
            # Por cada bit en el texto encriptado.
            if self.topologia[nodo_acutal].es_hoja():
                # Si el nodo acual es una hoja, entonces encontramos un
                # caracter, el caracter se agrega al texto desencriptado.
                texto += self.diccionario[nodo_acutal]

                # Se retorna el puntero a la raiz del arbol canonico.
                nodo_acutal = self.id_raiz

            else:
                if texto_encriptado[i] == '1':
                    # Si el bit actual es 1 se pasa al nodo derecho.
                    nodo_acutal = self.topologia[nodo_acutal].hijo_derecha

                else:
                    # Si el bit es 0 se pasa al nodo izquierdo.
                    nodo_acutal = self.topologia[nodo_acutal].hijo_izquierda

                # Se mueve al siguiente bit.
                i += 1

        # Se agrega el ultimo caracter desencriptado.
        texto += self.diccionario[nodo_acutal]

        return texto
