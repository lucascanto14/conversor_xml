import os
import re

def buscar_arquivos_ftpdetectinfo(diretorio_raiz):
    """
    Varre o diretorio e subpastas buscando arquivos no formato:
    FTPdetectinfo_<ESTACAO>_<DATA>_<HORA>_<ID>.txt
    """
    # Padrao Regex:
    # FTPdetectinfo_ -> prefixo fixo
    # ([A-Za-z0-9]+) -> captura o codigo da estacao (ex: BR0017, US0001, etc.)
    # _\d{8}_\d{6}_\d{6}\.txt -> padrao de data, hora e extensao .txt
    padrao = re.compile(r"^FTPdetectinfo_([A-Za-z0-9]+)_\d{8}_\d{6}_\d{6}\.txt$", re.IGNORECASE)
    
    arquivos_encontrados = []

    print(f"\nBuscando arquivos em: {diretorio_raiz}...\n")

    for raiz, _, arquivos in os.walk(diretorio_raiz):
        for arquivo in arquivos:
            match = padrao.match(arquivo)
            if match:
                caminho_completo = os.path.join(raiz, arquivo)
                estacao = match.group(1) # Extrai o nome da estação automaticamente
                
                arquivos_encontrados.append({
                    'caminho': caminho_completo,
                    'nome': arquivo,
                    'estacao': estacao
                })

    return arquivos_encontrados


# --- Exemplo de Integração ---

def selecionar_e_converter():
    pasta_base = input("Digite a pasta raiz para buscar (ENTER para pasta atual): ").strip('"\' ')
    if not pasta_base:
        pasta_base = os.getcwd()

    # Busca todos os arquivos FTPdetectinfo válidos
    lista_capturas = buscar_arquivos_ftpdetectinfo(pasta_base)

    if not lista_capturas:
        print("[!] Nenhum arquivo de captura FTPdetectinfo foi encontrado.")
        input("\nPressione ENTER...")
        return

    # Exibe a lista numerada com o nome da estação em destaque
    print("=" * 60)
    print("ARQUIVOS DE CAPTURA ENCONTRADOS:")
    print("=" * 60)
    for i, item in enumerate(lista_capturas, 1):
        print(f"[{i}] Estação: {item['estacao']} -> {item['nome']}")

    # Seleção pelo terminal
    while True:
        try:
            escolha = int(input("\nDigite o número do arquivo que deseja converter: "))
            if 1 <= escolha <= len(lista_capturas):
                txt_path = lista_capturas[escolha - 1]['caminho']
                break
            print("Número inválido.")
        except ValueError:
            print("Digite apenas números.")

    print(f"\nArquivo selecionado: {txt_path}")
    # Aqui você prossegue com o seu fluxo chamando o xml_template e a função de conversão