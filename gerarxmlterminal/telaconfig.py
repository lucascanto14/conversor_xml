import xml.etree.ElementTree as ET
from xml.dom import minidom

print("=== GERADOR DO XML MODELO ===")
print("Pressione ENTER para manter o valor padrão (0).\n")


def ler(nome, padrao="0"):
    valor = input(f"{nome}: ")
    return valor if valor != "" else padrao


# --------------------------
# ATRIBUTOS DO UFOANALYZER
# --------------------------

atributos_ufo = {
    "version": ler("version", "200"),
    "clip_name": ler("clip_name"),
    "y": ler("y"),
    "mo": ler("mo"),
    "d": ler("d"),
    "observer": ler("observer"),
    "cam": ler("cam"),
    "lens": ler("lens"),
    "cap": ler("cap"),
    "u2": ler("u2"),
    "ua": ler("ua"),
    "memo": ler("memo"),
    "az": ler("az"),
    "ev": ler("ev"),
    "rot": ler("rot"),
    "vx": ler("vx"),
    "yx": ler("yx"),
    "dx": ler("dx"),
    "dy": ler("dy"),
    "k4": ler("k4"),
    "k3": ler("k3"),
    "k2": ler("k2"),
    "atc": ler("atc"),
    "BVF": ler("BVF"),
    "maxLev": ler("maxLev"),
    "maxMag": ler("maxMag"),
    "minLev": ler("minLev"),
    "mimMag": ler("mimMag"),
    "dl": ler("dl"),
    "leap": ler("leap"),
    "pixs": ler("pixs"),
    "rstar": ler("rstar"),
    "ddega": ler("ddega"),
    "ddegm": ler("ddegm"),
    "errm": ler("errm"),
    "Lmrgn": ler("Lmrgn"),
    "Rmrgn": ler("Rmrgn"),
    "Dmrgn": ler("Dmrgn"),
    "Umrgn": ler("Umrgn")
}


# --------------------------
# ATRIBUTOS DO OBJETO
# --------------------------

atributos_objeto = {
    "fs": ler("fs"),
    "fe": ler("fe"),
    "fN": ler("fN"),
    "sN": ler("sN"),
    "sec": ler("sec"),
    "av": ler("av"),
    "pix": ler("pix"),
    "bmax": ler("bmax"),
    "mag": ler("mag"),
    "cdeg": ler("cdeg"),
    "cdegmax": ler("cdegmax"),
    "io": ler("io"),
    "raP": ler("raP"),
    "dcP": ler("dcP"),
    "av1": ler("av1"),
    "x1": ler("x1"),
    "y1": ler("y1"),
    "x2": ler("x2"),
    "y2": ler("y2"),
    "az1": ler("az1"),
    "ev1": ler("ev1"),
    "az2": ler("az2"),
    "ev2": ler("ev2"),
    "azm": ler("azm"),
    "evm": ler("evm"),
    "ra1": ler("ra1"),
    "dc1": ler("dc1"),
    "ra2": ler("ra2"),
    "dc2": ler("dc2"),
    "ram": ler("ram"),
    "dcm": ler("dcm"),
    "class": ler("class"),
    "m": ler("m"),
    "dr": ler("dr"),
    "dv": ler("dv"),
    "Vo": ler("Vo"),
    "lng1": ler("lng1"),
    "lat1": ler("lat1"),
    "h1": ler("h1"),
    "dist1": ler("dist1"),
    "gd1": ler("gd1"),
    "azL1": ler("azL1"),
    "evL1": ler("evL1"),
    "lng2": ler("lng2"),
    "lat2": ler("lat2"),
    "h2": ler("h2"),
    "dist2": ler("dist2"),
    "gd2": ler("gd2"),
    "len": ler("len"),
    "GV": ler("GV"),
    "rao": ler("rao"),
    "dco": ler("dco"),
    "Voo": ler("Voo"),
    "rat": ler("rat"),
    "dct": ler("dct"),
    "memo": ler("memo")
}

# --------------------------
# CRIA O XML
# --------------------------

raiz = ET.Element("ufoanalyzer_record", atributos_ufo)

ua2_objects = ET.SubElement(raiz, "ua2_objects")

ET.SubElement(ua2_objects, "ua2_object", atributos_objeto)

xml = ET.tostring(
    raiz,
    encoding="utf-8",
    short_empty_elements=False
)

pretty = minidom.parseString(xml).toprettyxml(indent="    ")

with open("registro_ufo.xml", "w", encoding="utf-8") as f:
    f.write(pretty)

print("\nModelo salvo como registro_ufo.xml")