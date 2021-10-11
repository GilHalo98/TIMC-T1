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
    """

    # Constructor de clase.
    def __init__(self):
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
        self.diccionario = {}

        # Diccionario de codigos para encriptar.
        self.diccionario_codigos = {}

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
    def generar_arbol(self, frecuencias):
        # Agregamos las hojas del arbol.
        for id in frecuencias:
            self.topologia[id] = Nodo(
                id,
                frecuencias[id]
            )

            # Aumenta la cantidad de nodos en 1.
            self.total_nodos += 1

        # Para poder generar el arbol como tal se usa una frontera, pero
        # esta contiene los nodos hojas ya que tecnicamente el arbol de
        # hunffman se contruye de las hojas a la raiz.
        frontera = list(frecuencias.keys()).copy()

        # Mientras que exitan mas de dos nodos por expandir en la
        # frontera.
        while len(frontera) > 1:
            # Un proceso unico en los arboles de hunffman es que el
            # orden en que se realizan las operaciones es de manera
            # decendente, por eso se ordena de manera decendente la
            # frontera.
            frontera = sorted(frontera, key=frecuencias.__getitem__)

            # Se asigna un id al valor omega calculado.
            nuevo_id = 'q' + str(self.__id)

            # Se almacena el nuevo valor omega en las frecuencias.
            frecuencias[nuevo_id] = (
                frecuencias[frontera[0]]
                + frecuencias[frontera[1]]
            )

            if frontera[1] <= frontera[0]:
                hi = frontera[1]
                hd = frontera[0]
            else:
                hi = frontera[0]
                hd = frontera[1]

            # Se genera un nuevo nodo conteniendo el nuevo omega.
            self.topologia[nuevo_id] = Nodo(
                nuevo_id,
                frecuencias[nuevo_id],
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
            self.diccionario_codigos[self.diccionario[id_caracter]] = codigo

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
                    str('{0:.2f}'.format(float(nodo.contenido)))
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
                contenido = '{{'
                contenido += self.diccionario[nodo.id_nodo]
                contenido += ' | '
                contenido += str('{0:.2f}'.format(float(nodo.contenido)))
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
                    id_nodo = self.topologia[id_nodo].hijo_izquierda
                elif self.topologia[id_nodo].hijo_derecha not in visitados:
                    id_nodo = self.topologia[id_nodo].hijo_derecha
                else:
                    # Regresamos una posicion en la ruta.
                    id_nodo = ruta.pop()
                    id_nodo = ruta.pop()

    # Encripta un texto dado con el arbol de Huffman.
    def encriptar(self, texto):
        texto_encriptado = ''
        for c in texto:
            texto_encriptado += self.diccionario_codigos[c]

        return texto_encriptado
