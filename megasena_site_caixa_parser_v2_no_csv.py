#!/usr/bin/env python3

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup as sp

"""
    Executa o parsing de todos os resultados
    da Mega Sena presentes no site da CAIXA
    para um arquivo final .csv.
    Escrito sem os módulos 'csv' 're'.

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

""" requisicao HTTP URL CAIXA 3 e 9 seg timeout (conexao e gravacao)
    3 tentativas em caso de problemas de conexao    """

try:

    requisicao = requests.Session()
    tentativas = Retry(total=3, backoff_factor=8,
                       status_forcelist=[400, 403, 408, 500, 502, 503, 504])
    requisicao.mount("http://", HTTPAdapter(max_retries=tentativas))

    print('Conectando com o site CAIXA...')

    with requisicao.get(url_caixa, timeout=(3, 9), stream=True) as carregaurl:
        with open('resultadoscaixa.htm', 'wb') as arquivoinicial:
            arquivoinicial.truncate(0)
            arquivoinicial.write(carregaurl.content)
    print('Conexão feita com sucesso!')

except Exception:
    print('--- Erro na conexao HTTP com o site CAIXA ---')
    exit()

"""" rotina para parsear arquivo 'baixado', retirar somente dezenas sorteadas
     das correspondentes linhas no formato 001, 010, 025, etc..
     e transformar formato HTML em csv """

with open('resultadoscaixa.htm', 'r') as arq,\
     open('mega_result_final.csv', 'wt') as arqfinal:

    arqfinal.truncate(0)
    saida_geral = []
    for linhas_tr in sp(arq, "lxml").findAll('tr'):
        saida_col = []
        for coluna in linhas_tr.findAll('td'):
            saida_col.append(coluna.text)
        saida_geral.append(saida_col)

    for linhas_2 in list(saida_geral):
        if linhas_2[3:9] != []:  # [3:9] > colunas das dezenas sorteadas
            """ transforma os digitos do formato 005,010,020 em 5,10,20  """
            dez1 = int(linhas_2[3])
            dez2 = int(linhas_2[4])
            dez3 = int(linhas_2[5])
            dez4 = int(linhas_2[6])
            dez5 = int(linhas_2[7])
            dez6 = int(linhas_2[8])
            print(f'{dez1},{dez2},{dez3},{dez4},{dez5},{dez6}', file=arqfinal)

    print(f'Arquivo gravado com sucesso!')
