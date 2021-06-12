#!/usr/bin/env python3

from bs4 import BeautifulSoup as bsoup
from requests import Session, get, exceptions
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from cloudant.client import CouchDB
from cloudant.result import Result
from sys import exit as callexit
from simple_term_menu import TerminalMenu
import timeit

DBADMIN = 'admin'
SENHADB = 'admin'
URL_COUCH = 'http://127.0.0.1:5984'
CONEXAO = CouchDB(DBADMIN, SENHADB, url=URL_COUCH, connect=True)
BANCODB = CONEXAO['megasena']

URL_CAIXA = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/\
megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMP\
I0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2\
I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI\
9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QP\
VN93KQ10G1/res/id=historicoHTML/c=cacheLevelPage/=/'

mega_dezenas = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0,
                '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0,
                '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0,
                '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0,
                '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0,
                '37': 0, '38': 0, '39': 0, '40': 0, '41': 0, '42': 0, '43': 0,
                '44': 0, '45': 0, '46': 0, '47': 0, '48': 0, '49': 0, '50': 0,
                '51': 0, '52': 0, '53': 0, '54': 0, '55': 0, '56': 0, '57': 0,
                '58': 0, '59': 0, '60': 0}


def conexao_CAIXA():

    global lista_nao_processada
    lista_nao_processada = []
    try:

        http_stats = [400, 403, 404, 408, 500, 502, 503, 504]
        requisicao = Session()
        tentativas = Retry(total=2, status_forcelist=[http_stats])
        requisicao.mount("http://", HTTPAdapter(max_retries=tentativas))

        print('Conectando com o site CAIXA...')
        carregaurl = requisicao.get(URL_CAIXA, timeout=(15), stream=True)

        if carregaurl:
            print('Conexão feita com sucesso.\n'
                  'Processando conteúdo da URL...\n')

            for linha_tr in bsoup(carregaurl.content, "lxml").findAll('tr'):
                saida_colunas = []
                for coluna in linha_tr.findAll('td'):
                    saida_colunas.append(coluna.text)
                lista_nao_processada.append(saida_colunas)

        return lista_nao_processada, True

    except exceptions.ConnectionError as erro:
        print(f'--- Erro na conexao HTTP com o site CAIXA ---: {erro}')
        return False


def checagem_resultados():

    global _restantes_xor

    if conexao_CAIXA() is False:
        callexit()

    docs_CouchDB = Result(BANCODB.all_docs, include_docs=True)

    print('Reunindo dados do CouchDB...')
    couch_DB_resultados = []
    for doc in docs_CouchDB:
        docs = doc['doc']['concurso']
        for chave, valores in docs.items():
            couch_DB_resultados.append(chave)

    print('Reunindo dados de resultados CAIXA...')
    caixa_resultados = []
    for linha in list(lista_nao_processada):
        if len(linha[3:9]) != 0:
            concurso_temp = linha[0]
            caixa_resultados.append(concurso_temp)

    print('Comparando se há novos resultados entre o CouchDB e site CAIXA...')
    start1 = timeit.default_timer()
    _restantes_xor = (set(couch_DB_resultados) ^ set(caixa_resultados))
    stop1 = timeit.default_timer()
    print(f'XOR Executado em {str(stop1 - start1)}')

    start2 = timeit.default_timer()
    _restantes_list_compr = [i for i in caixa_resultados
                             if i not in couch_DB_resultados]
    stop2 = timeit.default_timer()
    print(f'List comprehension Executada em {str(stop2 - start2)}')

    print(len(_restantes_list_compr), len(_restantes_xor))
    if len(_restantes_xor) == 0:
        callexit('Sem novos concursos para serem inseridos.')
        return False
    else:
        return _restantes_xor, True


def atualiza_resultados():

    megadict = {}
    checagem_resultados()
    for ocorrencia in sorted(_restantes_xor, key=int):
        for linha in list(lista_nao_processada):
            if len(linha[3:9]) != 0:
                if linha[0] == ocorrencia:
                    concurso = linha[0]
                    dezena1 = int(linha[3])
                    dezena2 = int(linha[4])
                    dezena3 = int(linha[5])
                    dezena4 = int(linha[6])
                    dezena5 = int(linha[7])
                    dezena6 = int(linha[8])
                    megadict = {'concurso': {concurso:
                                             {'dezena1': dezena1,
                                              'dezena2': dezena2,
                                              'dezena3': dezena3,
                                              'dezena4': dezena4,
                                              'dezena5': dezena5,
                                              'dezena6': dezena6}}}

                    if BANCODB.create_document(megadict):
                        print(f'Concurso {concurso} inserido com sucesso.')


def lista_tudo():

    for dic in BANCODB:
        concurso = dic['concurso']
        for chave, valor in concurso.items():
            print(f"Concurso: {chave} > Dezenas: "
                  f"{valor['dezena1']}, "
                  f"{valor['dezena2']}, "
                  f"{valor['dezena3']}, "
                  f"{valor['dezena4']}, "
                  f"{valor['dezena5']}, "
                  f"{valor['dezena6']}")


def lista_10_():

    megaordenado = {}
    for dic in BANCODB:
        concurso = dic['concurso']
        for chave, valores in concurso.items():
            for dezena in valores.items():
                if str(dezena[1]) in mega_dezenas:
                    mega_dezenas[str(dezena[1])] += 1

    for qtd_sort in sorted(mega_dezenas.values()):
        for dezena_items, qtd_items in mega_dezenas.items():
            if qtd_sort == qtd_items:
                megaordenado[dezena_items] = qtd_sort

    print('--- As 10 dezenas mais (+) sorteadas na MegaSena até hoje ---\n')
    for dezena, vezes in list(reversed(megaordenado.items()))[:10]:
        print(f'{vezes} vezes > dezena: {dezena}')

    print('')

    print('--- As 10 dezenas menos (-) sorteadas na MegaSena até hoje ---\n')
    for dezena, vezes in list(megaordenado.items())[:10]:
        print(f'{vezes} vezes > dezena: {dezena}')


def main_menu():

    global escolha, menu_loop

    choices = ["[x] Insere/Atualiza os jogos da MegaSena",
               "[x] Lista todos_os_concursos os concursos até hoje",
               "[x] Lista as 10 dezenas + e - sorteadas",
               "[x] Sai do programa"]

    print(f"{''}\n")
    escolha = TerminalMenu(menu_entries=choices,
                           title=f"{'-' * 16} OPCOES DO MENU {'-' * 16}",
                           menu_cursor="> ",
                           menu_cursor_style=("fg_red", "bold"),
                           menu_highlight_style=("bg_black", "fg_red"),
                           cycle_cursor=True).show()

    menu_loop = True
    return escolha, menu_loop


if __name__ == "__main__":

    try:

        while True:
            main_menu()
            if escolha == 0:
                atualiza_resultados()
            elif escolha == 1:
                lista_tudo()
            elif escolha == 2:
                lista_10_()
            elif escolha == 3:
                break

    except (ValueError, KeyboardInterrupt) as error:
        exit(f'Error >> {error}')