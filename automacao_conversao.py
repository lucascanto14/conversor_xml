import os
import re
from datetime import datetime, timedelta


opcao = input("Escolha um menu (1, 2 ou 3): ")

match opcao:
#extrair todos os arquivos
    case "1":
        arquivo_alvo = re.compile(r"^FTPdetectinfo_([A-Za-z0-9]+)_\d{8}_\d{6}_\d{6}\.txt$", re.IGNORECASE)
#extrair com base na data(da data ate o mais atual)
    case "2":
        data_inicial = input("Digite a data inicial (DD/MM/AAAA): ")
        datas = gerar_lista_datas(data_inicial)
        padrao_datas = f"({'|'.join(datas)})"

        arquivo_alvo = re.compile(rf"^FTPdetectinfo_([A-Za-z0-9]+)_{padrao_datas}_\d{{6}}_\d{{6}}\.txt$", 
        re.IGNORECASE)
#extrair o ultimo arquivo gerado
    case "3":
        data_ontem = datetime.now() - timedelta(days=1)
        data_str = data_ontem.strftime("%Y%m%d")
        arquivo_alvo = re.compile(rf"^FTPdetectinfo_([A-Za-z0-9]+)_{data_str}_\d{{6}}_\d{{6}}\.txt$", re.IGNORECASE)
        #nenhuma opcao
    case _:
        print("Opção inválida!")

diretorio_raiz = os.getcwd()
arquivo_alvo = re.compile(r"^FTPdetectinfo_([A-Za-z0-9]+)_\d{8}_\d{6}_\d{6}\.txt$", re.IGNORECASE)
arquivos_converter = []

for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
    for nome_arquivo in arquivos:
        if arquivo_alvo.match(nome_arquivo):
            caminho_completo = os.path.join(pasta_atual, nome_arquivo)
            arquivos_converter.append(caminho_completo)


def gerar_lista_datas(data_inicio_str):
    # Converte a string de entrada para um objeto datetime (formato esperado: DD/MM/AAAA)
    data_atual = datetime.now()
    data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
    
    lista_datas = []
    data_cursor = data_inicio
    
    # Percorre da data inicial até a data atual
    while data_cursor <= data_atual:
        # Formata no padrão MMDDYYYY (%m = mês, %d = dia, %Y = ano com 4 dígitos)
        lista_datas.append(data_cursor.strftime("%m%d%Y"))
        data_cursor += timedelta(days=1)
      
    return lista_datas
    
         