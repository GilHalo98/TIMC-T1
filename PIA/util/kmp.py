# Algoritmo de Knuth-Morres-Pratt.
def huffman_kmp(t, p):
    n = len(t)  # Longitud del texto.
    m = len(p)  # Longitud del patron.

    j = 0  # Index del patron.
    i = 0  # Index del texto.

    # Precomputa el arreglo de lps.
    lps = funcion_prefijo(p, m)

    # Mientras que i se encuentre dentro de p.
    while i < n:
        if p[j] == t[i]:
            # Si el caracter en p[j] es igual que t[i].
            # Verifica el proximo caracter en el patron y el texto.
            i += 1
            j += 1

        if j == m:
            # Si el index en j es igual que la longitud del patron,
            # hay una ocurrencia.
            yield i - j

            # El index j se mueve a la de la ocurrencia.
            j = lps[j - 1]

        elif i < n and p[j] != t[i]:
            # En otro caso, si i es menor que la longitud del texto y
            # el caracter en p[j] es distinto de t[i].
            if j != 0:
                # Si j es distinto de 0.
                # j se mueve a lsp[j - 1]
                j = lps[j - 1]

            else:
                # Sino i aumenta en uno.
                i += 1


# Funcion de prefijo.
def funcion_prefijo(p, m):
    # Se inicializa un arreglo con la longitud de los sufijos en 0.
    lps = [0] * m

    # Se inicializa la longitud del sufijo actual en 0.
    longitud_prefijo = 0

    # Se inicializa el analisis desde el segundo elemento.
    i = 1
    while i < m:
        if p[longitud_prefijo] == p[i]:
            # Si el caracter anterior es igual al actual la longitud del
            # sufijo aumenta en 1.
            longitud_prefijo += 1

            # Se agrega la longitud actual contada en el arreglo de
            # longitudes.
            lps[i] = longitud_prefijo

            # Se mueve una posicion en el patron.
            i += 1

        else:
            # Si los caracteres son distintos.
            if longitud_prefijo != 0:
                # Si la longitud del sufijo es distinta de cero, se compara
                # con el caracter anterior, hasta llegar al primer caracter
                # del sufijo.
                longitud_prefijo = lps[longitud_prefijo - 1]

            else:
                # Si se llega al ultimo caracter del sufijo y no se encuentra
                # un caracter similar, se reinicia el sufijo.
                lps[i] = 0

                # Se mueve al siguiente caracter en el patron.
                i += 1

    return lps


# La funcion de mapeo de indices del patron codificado.
def mapeo_indices(p, cod):
    # Mapeo de inicies en el patron codificado.
    mapeo = []

    # Index de mapeo empieza en -1
    i = -1

    # Por cada caracter en el patron.
    for c in p:

        # Se codifica el patron y se calcula el index en donde termina
        # el codifo de cada caracter.
        i += len(cod[c])

        # Se agrega el index en el mapeo de index.
        mapeo.append(i)

    # Retorna el mapeo.
    return mapeo
