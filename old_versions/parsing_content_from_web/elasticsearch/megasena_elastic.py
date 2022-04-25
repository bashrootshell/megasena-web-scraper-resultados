#!/usr/bin/env python3

from bs4 import BeautifulSoup as bsoup
from requests import Session, get, exceptions
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from elasticsearch import Elasticsearch as conexao
from sys import exit as callexit
import timeit

"""
    PEP8 compliant
    “Readability counts."
    “Beautiful is better than ugly.”
    — The Zen of Python
"""

ESEARCH = conexao(hosts=['http://10.10.10.10:9200'])

""" URL site CAIXA com todos_os_concursos os resultados da megasena   """

URL_CAIXA = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/\
megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMP\
I0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2\
I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI\
9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QP\
VN93KQ10G1/res/id=historicoHTML/c=cacheLevelPage/=/'

lista_nao_processada = []

mega_ = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0,
         '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0,
         '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,
         '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0,
         '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0,
         '37': 0, '38': 0, '39': 0, '40': 0, '41': 0, '42': 0, '43': 0,
         '44': 0, '45': 0, '46': 0, '47': 0, '48': 0, '49': 0, '50': 0,
         '51': 0, '52': 0, '53': 0, '54': 0, '55': 0, '56': 0, '57': 0,
         '58': 0, '59': 0, '60': 0}


def conexao_CAIXA():

    try:

        status_list = [400, 403, 408, 500, 502, 503, 504]
        requisicao = Session()
        tentativas = Retry(total=2, backoff_factor=4,
                           status_forcelist=[status_list])
        requisicao.mount("http://", HTTPAdapter(max_retries=tentativas))

        print('Conectando com o site CAIXA...')
        carregaurl = requisicao.get(URL_CAIXA, timeout=(2, 3), stream=True)

        if carregaurl:
            print('Conexão feita com sucesso.\n'
                  'Processando conteúdo da URL...\n')

            for linha_tr in bsoup(carregaurl.content, "lxml").findAll('tr'):
                saida_col = []
                for coluna in linha_tr.findAll('td'):
                    saida_col.append(coluna.text)
                lista_nao_processada.append(saida_col)
        return lista_nao_processada, True

    except exceptions.ConnectionError as erro:
        print(f'--- Erro na conexao HTTP com o site CAIXA ---: {erro}')
        return False


def checagem_resultados():

    global concursos_restantes

    if conexao_CAIXA() is False:
        callexit()
    docs_ELK = ESEARCH.search(index="megasena",
                                    body={"query":
                                          {"match_all": {}}}, size=3000)
    elk_res = []
    caixares = []
    print('Montando dados do ELK...')
    for hit in docs_ELK['hits']['hits']:
        concurso = hit['_source']['concurso']
        for chave, valores in concurso.items():
            elk_res.append(chave)
    print('Montando dados de resultados CAIXA...')
    for linha in list(lista_nao_processada):
        if len(linha[3:9]) != 0:
            concurso_temp = linha[0]
            caixares.append(concurso_temp)

    print('Comparando se há novos resultados entre o CouchDB e site CAIXA...')
    start1 = timeit.default_timer()
    concursos_restantes = (set(elk_res) ^ set(caixares))  # ~50x faster
    stop1 = timeit.default_timer()
    print(f'XOR Executado em {str(stop1 - start1)}')

    start2 = timeit.default_timer()
    list_non_matches = [i for i in caixares if i not in elk_res]
    stop2 = timeit.default_timer()
    print(f'List comprehension Executada em {str(stop2 - start2)}')

    print(len(list_non_matches), len(concursos_restantes))
    if len(concursos_restantes) == 0:
        callexit('Sem novos concursos para serem inseridos.')
        return False
    else:
        return concursos_restantes, True


def atualiza_resultados():

    checagem_resultados()
    for ocorrencia in concursos_restantes:
        for linha in list(lista_nao_processada):
            if len(linha[3:9]) != 0:
                if linha[0] == ocorrencia:
                    concurso = linha[0]
                    dez1 = int(linha[3])
                    dez2 = int(linha[4])
                    dez3 = int(linha[5])
                    dez4 = int(linha[6])
                    dez5 = int(linha[7])
                    dez6 = int(linha[8])
                    mega_dezenas = {'concurso': {concurso:
                                                 {'dezena1': dez1,
                                                  'dezena2': dez2,
                                                  'dezena3': dez3,
                                                  'dezena4': dez4,
                                                  'dezena5': dez5,
                                                  'dezena6': dez6}}}

                    ESEARCH.index(index="megasena", id=concurso,
                                  body=mega_dezenas)
                    print(f'Concurso {concurso} inserido com sucesso.')


def lista_tudo():

    docs_ELK = ESEARCH.search(index="megasena",
                                    body={"query":
                                          {"match_all": {}}}, size=3000)
    if docs_ELK['hits']['hits'] != []:
        for hit in docs_ELK['hits']['hits']:
            concurso = hit['_source']['concurso']
            for chave, valores in concurso.items():
                print(f"Concurso: {chave} - dezenas: "
                      f"{valores['dezena1']} {valores['dezena2']} "
                      f"{valores['dezena3']} {valores['dezena4']} "
                      f"{valores['dezena5']} {valores['dezena6']}")


def lista_10_():

    mega_ordenado = {}

    docs_ELK = ESEARCH.search(index="megasena",
                                    body={"query":
                                          {"match_all": {}}}, size=3000)
    if docs_ELK['hits']['hits'] != []:
        for hit in docs_ELK['hits']['hits']:
            concurso = hit['_source']['concurso']
            for chave, valores in concurso.items():
                for dezena in valores.items():
                    n = str(dezena[1])
                    if n in mega_:
                        mega_[n] += 1

        for qtd_sort in sorted(mega_.values()):
            for dezena_items, qtd_items in mega_.items():
                if qtd_sort == qtd_items:
                    mega_ordenado[dezena_items] = qtd_sort

    print('--- As 10 dezenas mais (+) sorteadas na MegaSena até hoje ---\n')
    for dezena, vezes in list(reversed(mega_ordenado.items()))[:10]:
        print(f'{vezes} vezes > dezena: {dezena}')

    print('')

    print('--- As 10 dezenas menos (-) sorteadas na MegaSena até hoje ---\n')
    for dezena, vezes in list(mega_ordenado.items())[:10]:
        print(f'{vezes} vezes > dezena: {dezena}')


def remove_documentos():

    resultado = ESEARCH.delete_by_query(
        index="megasena", body={"query": {"match_all": {}}})
    print(resultado)


def main():

    _t = '-' * 12
    print(f'|{_t} MENU DE OPCOES {_t}|')

    escolha = int(input("1 - Insere/Atualiza os jogos da MegaSena\n"
                        "2 - Lista todos_os_concursos os concursos até hoje\n"
                        "3 - Lista as 10 dezenas + - sorteadas\n"
                        "4 - Remove todos os resultados do índice\n"
                        ">>  "))

    if escolha in range(1, 9):
        if escolha == 1:
            atualiza_resultados()
        elif escolha == 2:
            lista_tudo()
        elif escolha == 3:
            lista_10_()
        elif escolha == 4:
            remove_documentos()
    else:
        callexit('Digite uma opção válida do menu')


if __name__ == "__main__":

    try:
        main()
    except ValueError as erro:
        print(f'Erro >> {erro}')
