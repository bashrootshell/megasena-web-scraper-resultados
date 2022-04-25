#!/usr/bin/env python3

from bs4 import BeautifulSoup as bsoup
from requests import Session, get, exceptions
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

"""
    PEP8 compliant
    “Readability counts."
    “Beautiful is better than ugly.”
    — The Zen of Python
"""


""" URL site CAIXA com todos os resultados da megasena   """

url_caixa = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/\
megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMP\
I0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2\
I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI\
9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QP\
VN93KQ10G1/res/id=historicoHTML/c=cacheLevelPage/=/'

lista_nao_processada = []

lista_final = []

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


""" requisicao HTTP URL CAIXA 3 e 9 seg timeout (conexao e gravacao)
    3 tentativas em caso de problemas de conexao    """

try:

    requisicao = Session()
    tentativas = Retry(total=2, backoff_factor=4,
                       status_forcelist=[400, 403, 408, 500, 502, 503, 504])
    requisicao.mount("http://", HTTPAdapter(max_retries=tentativas))

    print('Conectando com o site CAIXA...')
    carregaurl = requisicao.get(url_caixa, timeout=(2, 5), stream=True)
    
    if carregaurl:
        print('Conexão feita com sucesso.\n'
              'Processando conteúdo da URL...\n')
        
        for linha_tr in bsoup(carregaurl.content, "lxml").findAll('tr'):
            saida_col = []
            for coluna in linha_tr.findAll('td'):
                saida_col.append(coluna.text)
            lista_nao_processada.append(saida_col)
        print('Conteúdo Web processado. Gerando as dezenas mais sorteadas...\n')

except exceptions.ConnectionError as erro:
    print(f'--- Erro na conexao HTTP com o site CAIXA ---: {erro}')

for linha in list(lista_nao_processada):
    if linha[3:9] != []:  # [3:9] > colunas das dezenas sorteadas
        """ transforma os digitos do formato 005,010,020 em 5,10,20  """
        dez1 = int(linha[3])
        dez2 = int(linha[4])
        dez3 = int(linha[5])
        dez4 = int(linha[6])
        dez5 = int(linha[7])
        dez6 = int(linha[8])
        dezenas = f'{dez1},{dez2},{dez3},{dez4},{dez5},{dez6}'
        lista_final.append(dezenas)

for linhas in lista_final:
    for dezena in linhas.split(','):
        if dezena in mega_dezenas:
            mega_dezenas[dezena] += 1

for qtd_sorted in sorted(mega_dezenas.values()):
    for dezena_items, qtd_items in mega_dezenas.items():
        if qtd_sorted == qtd_items:
            mega_dezenas_ordenado[dezena_items] = qtd_sorted

print('--- As 10 dezenas mais (+) sorteadas na MegaSena até hoje ---\n')
for dezena, vezes in list(reversed(mega_dezenas_ordenado.items()))[:10]:
    print(f'{vezes} vezes > dezena: {dezena}')

print('')

print('--- As 10 dezenas menos (-) sorteadas na MegaSena até hoje ---\n')
for dezena, vezes in list(mega_dezenas_ordenado.items())[:10]:
    print(f'{vezes} vezes > dezena: {dezena}')