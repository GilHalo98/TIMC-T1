import pandas
import numpy



def main() -> None:
    alfabeto = ['a', 'b', 'c', 'd']

    prob_transmicion = pandas.DataFrame(
        {
            'a': [.950, .016, .016, .016],
            'b': [.016, .950, .016, .016],
            'c': [.016, .016, .950, .016],
            'd': [.016, .016, .016, .950]
        },
        index = alfabeto
    )

    print('Matriz de probabilidad de transmicion')
    print(prob_transmicion.to_string())

    frecuencias_entrada = pandas.Series(
        [.19, .38, .25, .18],
        index=alfabeto
    )

    print('\nFrecuencias de entrada')
    print(frecuencias_entrada.to_string())

    matriz_salida = pandas.DataFrame(
        {
            'a': prob_transmicion['a'] * frecuencias_entrada['a'],
            'b': prob_transmicion['b'] * frecuencias_entrada['b'],
            'c': prob_transmicion['c'] * frecuencias_entrada['c'],
            'd': prob_transmicion['d'] * frecuencias_entrada['d'],
        },
        index=alfabeto
    )

    print('\nMatriz de salida')
    print(matriz_salida.to_string())

    frecuencias_salida = pandas.Series(
        [
            sum(matriz_salida[index]) for index in alfabeto
        ],
        index=alfabeto
    )

    print('\nFrecuencias de salida')
    print(frecuencias_salida.to_string())

    # Por cada elemento en las frecuencias de entrada.
    ecuacion = ''
    capacidad = 0
    for i in alfabeto:
        Pi = frecuencias_entrada[i]

        ecuacion += '{} * [\n\t'.format(Pi)

        sum_a = 0
        for j in alfabeto:
            Qij = prob_transmicion[j][i]
            ecuacion += '{} log ({} / ('.format(Qij, Qij)

            sum_b = 0
            for k in alfabeto:
                Pk = frecuencias_entrada[k]
                Qjk = prob_transmicion[k][j]

                ecuacion += '{} * {} + '.format(Pk, Qjk)

                sum_b += Pk * Qjk

            sum_a += Qij * numpy.log10(Qij / sum_b)

            ecuacion += ') = {}) = {}\n\t+ '.format(sum_b, sum_a)

        ecuacion += '] = {}\n+ '.format(Pi * sum_a)
        capacidad += Pi * sum_a

    print(ecuacion)
    print(str(capacidad) + ' bits / simbolo')


if __name__ == '__main__':
    main()