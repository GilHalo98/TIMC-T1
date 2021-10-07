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

            # Se genera un nuevo nodo conteniendo el nuevo omega.
            self.topologia[nuevo_id] = Nodo(
                nuevo_id,
                frecuencias[nuevo_id],
                hijo_izquierda=frontera[1],
                hijo_derecha=frontera[0]
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

    # Grafica el arbol de hunffman.
    def graficar(self, archivo_salida):
        grafico = Graph(
            comment='Test',
            format='svg',
        )

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
                    '{}\n{}'.format(nodo.id_nodo, float(nodo.contenido))
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
                # Si el nodo es una hoja, se agrega tambien su caracter.
                grafico.node(
                    str(nodo.id_nodo),
                    '{}\n{}\n{}'.format(
                        nodo.id_nodo,
                        self.diccionario[nodo.id_nodo],
                        float(nodo.contenido),
                    )
                )

        # Por ultimo renderiza el grafo en un archivo svg.
        grafico.render(filename=archivo_salida)
