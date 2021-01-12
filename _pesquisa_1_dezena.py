#!/usr/bin/env python3

"""
    Pesquisa quantas vezes um número
    específico foi sorteado na história
    da MegaSena.

    PEP8 compliant
    "Simple is better than complex."
"""

nomearquivo = str(input("Digite o nome do arquivo .csv: "))

if nomearquivo == '':
    print('Nome do arquivo faltando.')
    exit()
elif nomearquivo.isdigit():
    print('Forneça nome do arquivo como string.')
    exit()

dezena = int(input("Escolha um número entre 1 e 60: "))
if dezena < 1 or dezena > 60:
    print('Escolha um número entre 1 e 60...!')
    exit()

with open(nomearquivo, 'r') as arquivocsv:
    total = 0
    conteudo = arquivocsv.read()
    for linhas in conteudo.split():
        for coluna in linhas.split(','):
            if coluna == str(dezena):
                total += 1
print(f'Número {dezena} saiu {total} vezes na MegaSena.')
