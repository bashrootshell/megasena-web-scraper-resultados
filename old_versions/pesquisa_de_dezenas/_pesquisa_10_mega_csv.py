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

""" forma mais rápida de se iniciar um dicionário utilizando
    já as dezenas com seus respectivos valores em comparação
    com um loop for range(1, 61)
    cerca de 8x a 10x mais rápido  """

mega_dezenas = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0,
                '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0,
                '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,
                '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0,
                '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0,
                '37': 0, '38': 0, '39': 0, '40': 0, '41': 0, '42': 0, '43': 0,
                '44': 0, '45': 0, '46': 0, '47': 0, '48': 0, '49': 0, '50': 0,
                '51': 0, '52': 0, '53': 0, '54': 0, '55': 0, '56': 0, '57': 0,
                '58': 0, '59': 0, '60': 0}

mega_dezenas_ordenado = {}

if len(sys.argv) < 2:
    print('Argumento faltando: nome do arquivo .csv')
else:
    with open(sys.argv[1], 'r') as arquivocsv:
        conteudo = arquivocsv.read()
        for linhas in conteudo.split():
            for dezena in linhas.split(','):
                if dezena in mega_dezenas:
                    mega_dezenas[dezena] += 1

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
