# megasena-web-scraper-resultados
# Escrito em 'Pure Python'

megasena_site_caixa_parser.py > Executa o parsing de todos os resultados
    da Mega Sena presentes no site da CAIXA
    para um arquivo final .csv.
    O programa cria 2 arquivos temporários
    antes de gravar o arquivo final.
    
_pesquisa_10_mega_csv.py > Pesquisa os 10 números mais sorteados
    e os 10 menos sorteados de todos os
    resultados da Mega Sena.
    Basta um arquivo em formato .csv.
    Exemplo de linha:  5,15,23,31,44,56
    Forma mais rápida de se iniciar um dicionário utilizando
    já as dezenas com seus respectivos valores em comparação
    com um loop for range(1, 61)
    cerca de 8x a 10x mais rápido
    
 _pesquisa_10_mega_csv_v2.py > Pesquisa os 10 números mais sorteados e os 10 menos sorteados de todos os resultados da Mega Sena. Basta um arquivo em formato .csv. Exemplo de linha: 5,15,23,31,44,56
 Forma mais lenta de se iniciar um dicionário utilizando
 loop for (range(1, 61))

_pesquisa_1_dezena.py > Pesquisa quantas vezes um número
    específico foi sorteado na história
    da MegaSena.

megasena_site_caixa_parser_v2_no_csv.py > Executa o parsing de todos os resultados
    da Mega Sena presentes no site da CAIXA
    para um arquivo final .csv.
    Escrito sem o módulo 'csv'.
