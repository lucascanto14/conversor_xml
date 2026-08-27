import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import re
import copy


# ======================================================
# CARREGA O MODELO (config_estação.xml)
# ======================================================

def carregar_template(xml_template):

    tree = ET.parse(xml_template)
    root = tree.getroot()

    objetos = root.find("ua2_objects")

    if objetos is None:
        raise Exception(
            "O XML modelo não possui a tag <ua2_objects>."
        )

    objeto = objetos.find("ua2_object")

    if objeto is None:
        raise Exception(
            "O XML modelo não possui a tag <ua2_object>."
        )

    return objeto


# ======================================================
# SALVA O XML
# ======================================================

def salvar_arquivo_individual(xml_raiz,pasta_destino,nome_clip):

    xml_string = ET.tostring(
        xml_raiz,
        encoding="utf-8",
        short_empty_elements=False
    )

    pretty = minidom.parseString(
        xml_string
    ).toprettyxml(indent="    ")

    caminho_saida = os.path.join(
        pasta_destino,
        f"{nome_clip}.xml"
    )

    with open(
        caminho_saida,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(pretty)


# ======================================================
# input arquivos
# ======================================================

def selecionar_e_converter():

    print("=" * 60)
    print("CONVERSOR RMS -> UFOAnalyzer")
    print("=" * 60)

    pasta = os.getcwd()

    txt_path = os.path.join(
        pasta,
        input("Digite o nome do arquivo .txt das capturas: ")
    )

    xml_template = os.path.join(
        pasta,
        input("Digite o nome do arquivo de configuração da estação: ")
    )

    if not os.path.exists(txt_path):

        print("\nERRO!")
        print("Não encontrei o arquivo .txt das capturas na pasta:")
        print(pasta)
        input("\nPressione ENTER...")
        return

    if not os.path.exists(xml_template):

        print("\nERRO!")
        print("Não encontrei o arquivo de configuração na pasta:")
        print(pasta)
        input("\nPressione ENTER...")
        return

    try:

        total = processar_conversao_por_trajetoria(
            txt_path,
            xml_template
        )

        print(f"\n{total} arquivos XML foram gerados.")

    except Exception as e:

        print("\nERRO:")
        print(e)

    input("\nPressione ENTER para sair...")

# ======================================================
# PROCESSA O TXT
# ======================================================

def processar_conversao_por_trajetoria(
        txt_path,
        xml_template):

    # --------------------------
    # Carrega o modelo
    # --------------------------

    root_template, objeto_template = carregar_template(xml_template)

    with open(
        txt_path,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    pasta_destino = os.path.dirname(
        txt_path
    )

    id_camera_detetado = "UNKNOWN"

    for line in lines:

        if "FF folder" in line or "FF_" in line:

            match = re.search(
                r'(BR\d+|[A-Za-z]+\d+)',
                line
            )

            if match:

                id_camera_detetado = match.group(1)
                break

    root_xml = None
    container_objetos = None

    clip_name_atual = None

    proxima_linha_e_calibracao = False

    contador_trajetorias = 0

    # ==================================================
    # Percorre todas as linhas do TXT
    # ==================================================

    for line in lines:

        line = line.strip()

        # ----------------------------------------------
        # NOVA TRAJETÓRIA
        # ----------------------------------------------

        if line.startswith("FF_") and line.endswith(".fits"):

            # salva o XML anterior

            if (
                root_xml is not None
                and clip_name_atual is not None
            ):

                salvar_arquivo_individual(
                    root_xml,
                    pasta_destino,
                    clip_name_atual
                )

                contador_trajetorias += 1

            clip_name_atual = line.replace(
                ".fits",
                ""
            )

            partes = line.split("_")

            data = partes[2]
            hora = partes[3]

            # ------------------------------------------
            # Copia TODOS os atributos do config
            # ------------------------------------------

            atributos = copy.deepcopy(
                root_template.attrib
            )

            # Atualiza somente os campos variáveis

            atributos["version"] = "200"

            atributos["clip_name"] = clip_name_atual

            atributos["y"] = data[:4]

            atributos["mo"] = str(
            int(data[4:6])
            )

            atributos["d"] = str(
             int(data[6:8])
            )

            atributos["h"] = hora[:2]

            atributos["m"] = hora[2:4]

            atributos["s"] = hora[4:6]

            atributos["lid"] = id_camera_detetado

            atributos["cam"] = id_camera_detetado

            root_xml = ET.Element(
            "ufoanalyzer_record",
            atributos
            )

            container_objetos = ET.SubElement(
                root_xml,
                "ua2_objects"
            )

            # ==========================================
            # ADICIONA O ua2_object DO MODELO
            # ==========================================

            container_objetos.append(
                copy.deepcopy(
                    objeto_template
                )
            )

            proxima_linha_e_calibracao = False

            continue

        # -------------------------------------------------
        # Linha indicando que a próxima contém calibração
        # -------------------------------------------------

        if "Cam# Meteor#" in line:

            proxima_linha_e_calibracao = True
            continue


        # -------------------------------------------------
        # Lê os dados de calibração
        # -------------------------------------------------

        if proxima_linha_e_calibracao and root_xml is not None:

            cal_data = line.split()

            if len(cal_data) >= 10:

                root_xml.attrib.update({

                    "sid": cal_data[1],

                    "fps": str(
                        float(cal_data[3])
                    ),

                    "az": str(
                        float(cal_data[8])
                    ),

                    "ev": str(
                        float(cal_data[9])
                    )

                })

            proxima_linha_e_calibracao = False

            continue


        # -------------------------------------------------
        # Ignora linhas desnecessárias
        # -------------------------------------------------

        if (
            not line
            or line.startswith("-")
            or "Recalibrated" in line
            or "Per segment" in line
        ):

            continue


        if (
            any(
                line.startswith(cam)
                for cam in [
                    id_camera_detetado,
                    "BR"
                ]
            )
            and not line.endswith(".fits")
            and not proxima_linha_e_calibracao
        ):

            continue


        # -------------------------------------------------
        # Dados dos frames
        # -------------------------------------------------

        data = line.split()

        if (
            len(data) >= 12
            and container_objetos is not None
            and not proxima_linha_e_calibracao
        ):

            try:

                frame = ET.SubElement(

                    container_objetos,

                    "ua2_fdata2",

                    fno=data[0].zfill(4),

                    ra=data[3],

                    dec=data[4],

                    az=data[5],

                    ev=data[6],

                    mag=data[9]

                )

                frame.text = ""

            except:

                continue

def carregar_template(xml_template):

    tree = ET.parse(xml_template)

    root = tree.getroot()

    objetos = root.find("ua2_objects")

    if objetos is None:
        raise Exception(
            "O XML modelo não possui ua2_objects."
        )

    objeto = objetos.find("ua2_object")

    if objeto is None:
        raise Exception(
            "O XML modelo não possui ua2_object."
        )

    return root, objeto

    # ==================================================
    # Salva a última trajetória
    # ==================================================

    if (
        root_xml is not None
        and clip_name_atual is not None
    ):

        # ------------------------------------------
        # Atualiza fs, fe e fN automaticamente
        # ------------------------------------------

        ua2_object = container_objetos.find(
            "ua2_object"
        )

        frames = container_objetos.findall(
            "ua2_fdata2"
        )

        if (
            ua2_object is not None
            and len(frames) > 0
        ):

            primeiro_frame = frames[0].attrib["fno"]

            ultimo_frame = frames[-1].attrib["fno"]

            quantidade = len(frames)

            ua2_object.set(
                "fs",
                primeiro_frame
            )

            ua2_object.set(
                "fe",
                ultimo_frame
            )

            ua2_object.set(
                "fN",
                str(quantidade)
            )

        salvar_arquivo_individual(
            root_xml,
            pasta_destino,
            clip_name_atual
        )

        contador_trajetorias += 1

    return contador_trajetorias

# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    selecionar_e_converter()