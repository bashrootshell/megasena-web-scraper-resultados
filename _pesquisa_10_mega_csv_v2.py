#!/usr/bin/env python3

import sys

"""
    Pesquisa os 10 números mais sorteados
    e os 10 menos sorteados de todos os
    resultados da Mega Sena.
    Basta um arquivo em formato .csv.
    Exemplo de linha:  5,15,23,31,44,56

    PEP8 compliant
    "Simple is better than complex."
"""

""" forma mais lenta de se iniciar um dicionário utilizando
    loop for (range(1, 61)) """

mega_dezenas = {}
mega_dezenas_ordenado = {}

if len(sys.argv) < 2:
    print('Argumento faltando: nome do arquivo .csv')
else:
    with open(sys.argv[1], 'r') as arquivocsv:
        conteudo = arquivocsv.read()
        for numero in range(1, 61):  # forma mais lenta
            mega_dezenas[numero] = 0
            for linhas in conteudo.split():
                for dezena in linhas.split(','):
                    if dezena == str(numero):
                        mega_dezenas[numero] += 1

    for qtd_sort in sorted(mega_dezenas.values()):
        for dezena_items, qtd_items in mega_dezenas.items():
            if qtd_sort == qtd_items:
                mega_dezenas_ordenado[dezena_items] = qtd_sort

    print('--- As 10 dezenas mais (+) sorteadas na MegaSena até hoje ---\n')
    for dezena, vezes in list(reversed(mega_dezenas_ordenado.items()))[:10]:
        print(f'{vezes} vezes > dezena: {dezena}')

    print('')

    print('--- As 10 dezenas menos (-) sorteadas na MegaSena até hoje ---\n')
    for dezena, vezes in list(mega_dezenas_ordenado.items())[:10]:
        print(f'{vezes} vezes > dezena: {dezena}')
