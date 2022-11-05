#!/usr/bin/env python3

from operator import itemgetter
from requests import get, exceptions
from bs4 import BeautifulSoup as sp


"""
    Executa o parsing de todos os resultados
    da Mega Sena.

    PEP8 compliant
    “Readability counts."
    “Beautiful is better than ugly.”
    — The Zen of Python
"""


""" URL com todos os resultados da megasena   """

url = 'https://asloterias.com.br/lista-de-resultados-da-mega-sena'

mega_dezenas = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0,
                '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0,
                '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,
                '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0,
                '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0,
                '37': 0, '38': 0, '39': 0, '40': 0, '41': 0, '42': 0, '43': 0,
                '44': 0, '45': 0, '46': 0, '47': 0, '48': 0, '49': 0, '50': 0,
                '51': 0, '52': 0, '53': 0, '54': 0, '55': 0, '56': 0, '57': 0,
                '58': 0, '59': 0, '60': 0}

numero_dezenas = int(input('Informe a quantidade de dezenas que deseja verificar: '))

try:

    print('Conectando-se ao site "asloterias.com.br" ...')

    with get(url, stream=True) as carregaurl:
        print('Conexão feita com sucesso!\n\n')
        saida_colunas = []
        for linhas_tr in sp(carregaurl.content, "lxml")\
                .findAll("div", class_="limpar_flutuacao"):
            saida_colunas.append(linhas_tr.previous_sibling)

except exceptions.HTTPError as erro:
    exit(f'--- Erro {erro} na conexao HTTP com o site ---')

with open('todos_os_resultados.csv', 'w') as arquivo_com_resultados:

    arquivo_com_resultados.truncate(0)
    for resultado in list(saida_colunas):
        dez1 = int(resultado[17:19])
        dez2 = int(resultado[20:22])
        dez3 = int(resultado[23:25])
        dez4 = int(resultado[26:28])
        dez5 = int(resultado[29:31])
        dez6 = int(resultado[32:34])
        dezenas = f'{dez1},{dez2},{dez3},{dez4},{dez5},{dez6}'
        print(dezenas, file=arquivo_com_resultados)
        for dezena in dezenas.split(','):
            if dezena in mega_dezenas:
                mega_dezenas[dezena] += 1

print(f'--- As {numero_dezenas} dezenas mais (+) sorteadas na MegaSena até hoje ---\n')
for dezena, vezes in sorted(mega_dezenas.items(), key=itemgetter(1),
                            reverse=True)[:numero_dezenas]:
    print(f'{vezes:10} vezes > dezena: {dezena:10}'
          f'\r')

print(f'\n--- As {numero_dezenas} dezenas menos (-) sorteadas na MegaSena até hoje ---\n')
for dezena, vezes in sorted(mega_dezenas.items(), key=itemgetter(1))[:numero_dezenas]:
    print(f'{vezes:10} vezes > dezena: {dezena:10}'
          f'\r')
