#!/usr/bin/env python3

import csv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
from bs4 import BeautifulSoup as sp

"""
    Executa o parsing de todos os resultados
    da Mega Sena presentes no site da CAIXA
    para um arquivo final .csv.
    O programa cria 2 arquivos temporários
    antes de gravar o arquivo final.

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

with open('resultadoscaixa.htm', 'r') as arq, open('temp.csv', 'w') as temp1:

    saida_geral = []
    for linhas_tr in sp(arq, "lxml").findAll('tr'):
        saida_col = []
        for coluna in linhas_tr.findAll('td'):
            saida_col.append(coluna.text)
        saida_geral.append(saida_col)

    csv.writer(temp1).writerows(saida_geral)
    """ exemplo de linha gerada pela rotina
    1,"Brasília, DF",11/03/1996,004,005,030,033,041,052,0,17,2016,"0,00" """


with open('temp.csv', 'r') as temp2, open('mega_result_final.csv', 'w') as res:

    res.truncate(0)

    for linha in csv.DictReader(temp2):
        for chave, valor in linha.items():

            """  regex para encontrar somente linhas que iniciam com digitos
                na celula 0, e retorna somente linhas com os resultados """

            expressao_regular = re.findall(r'^([0-9])', valor[0])
            if expressao_regular:
                """
                  retira 0's a esquerda apenas com a funcao int()
                """
                dez1 = int(valor[3])
                dez2 = int(valor[4])
                dez3 = int(valor[5])
                dez4 = int(valor[6])
                dez5 = int(valor[7])
                dez6 = int(valor[8])
                var_tmp = [dez1, dez2, dez3, dez4, dez5, dez6]
                csv.writer(res).writerow(var_tmp)

    print(f'Arquivo gravado com sucesso!')
