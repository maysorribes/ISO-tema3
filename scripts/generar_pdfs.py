#!/usr/bin/env python3
"""Genera el PDF de cada práctica a partir de su Markdown.

Uso (desde la carpeta del proyecto):
    python3 scripts/generar_pdfs.py           # regenera solo los que han cambiado
    python3 scripts/generar_pdfs.py --todos   # regenera los ocho

Necesita: pip install markdown pymdown-extensions  y  wkhtmltopdf instalado.
Los PDF se guardan en docs/practicas/pdf/.
"""
import base64
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parent.parent
PRACTICAS = RAIZ / "docs" / "practicas"
SALIDA = PRACTICAS / "pdf"
LOGO = RAIZ / "docs" / "img" / "tux.png"

FICHEROS = {
    "p1-archivos": "UT3_P1_Archivos",
    "p2-comodines": "UT3_P2_Comodines",
    "p3-procesos": "UT3_P3_Procesos",
    "p4-filtros": "UT3_P4_Filtros",
    "p5-usuarios": "UT3_P5_Usuarios",
    "p6-permisos": "UT3_P6_Permisos",
    "p7-enlaces-fhs": "UT3_P7_Enlaces_FHS",
    "p8-paquetes": "UT3_P8_Paquetes",
}

CSS = """
@page { margin: 0; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10.5pt;
       line-height: 1.45; color: #222; margin: 0; }
p, li { text-align: justify; }
.cabecera { width: 100%; border-collapse: collapse; border-bottom: 3px solid #3f51b5; margin-bottom: 18px; }
.cabecera td { border: none; padding: 0 0 10px 0; vertical-align: middle; }
.cabecera td.logo { width: 24mm; }
.cabecera td.logo img { width: 20mm; }
.cabecera td.textos {
            text-align: center; }
.cabecera .ciclo { font-size: 9.5pt; color: #555; }
.cabecera .modulo { font-size: 13pt; font-weight: bold; letter-spacing: 1px; color: #3f51b5;
                    margin: 4px 0; }
.cabecera .ut { font-size: 10pt; color: #555; }
.cabecera .num { font-size: 18pt; font-weight: bold; margin-top: 8px; }
.cabecera .titulo { font-size: 13pt; margin-top: 2px; }
h2 { color: #3f51b5; font-size: 13pt; border-bottom: 1px solid #c5cae9; padding-bottom: 2px;
     margin-top: 22px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 9.5pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #c5cae9; padding: 4px 7px; text-align: left; vertical-align: top; }
th { background: #3f51b5; color: #fff; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt; background: #f0f1f7;
       padding: 0 3px; border-radius: 2px; }
pre { background: #f0f1f7; border-left: 3px solid #3f51b5; padding: 7px 10px; font-size: 8.8pt;
      line-height: 1.35; white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
.admonition { border-left: 4px solid #3f51b5; background: #f5f6fb; padding: 6px 12px;
              margin: 12px 0; page-break-inside: avoid; }
.admonition.warning { border-color: #ff9100; background: #fff5e6; }
.admonition.question { border-color: #64dd17; background: #f2fbe9; }
.admonition.tip { border-color: #00bfa5; background: #e9f9f6; }
.admonition-title { font-weight: bold; margin: 2px 0 4px 0; }
.admonition p { margin: 4px 0; }
kbd { border: 1px solid #999; border-radius: 3px; padding: 0 3px; font-size: 8.5pt;
      background: #fafafa; }
.filename { font-size: 8.5pt; color: #555; font-weight: bold; }
ol li, ul li { margin: 3px 0; }
th:empty { display: none; }
"""

EXTENSIONES = [
    "admonition", "tables", "attr_list", "md_in_html",
    "pymdownx.superfences", "pymdownx.highlight", "pymdownx.keys",
    "pymdownx.fancylists",
]
CONFIG = {"pymdownx.highlight": {"use_pygments": False}}


def convertir(fuente: Path, destino: Path) -> None:
    texto = fuente.read_text(encoding="utf-8")
    # Título "# Práctica N · Título" -> cabecera institucional
    m = re.match(r"# (Práctica \d+) · (.+)\n", texto)
    num, titulo = m.group(1), m.group(2)
    texto = texto[m.end():]
    # Quitar el botón de descarga del PDF
    texto = re.sub(r"^\[Descargar el enunciado en PDF\].*\n", "", texto, flags=re.M)
    # Bloques de código con título: el título pasa a ser una etiqueta encima
    texto = re.sub(r'^(\s*)```(\w+) title="([^"]+)"', r'\1<p class="filename">\3</p>\n\n\1```\2', texto, flags=re.M)
    cuerpo = markdown.markdown(texto, extensions=EXTENSIONES, extension_configs=CONFIG)
    logo = base64.b64encode(LOGO.read_bytes()).decode()
    cabecera = (
        '<table class="cabecera"><tr>'
        f'<td class="logo"><img src="data:image/png;base64,{logo}" alt="Tux"></td>'
        '<td class="textos">'
        '<div class="ciclo">CFGS Administración de Sistemas Informáticos en Red</div>'
        '<div class="modulo">IMPLANTACIÓN DE SISTEMAS OPERATIVOS</div>'
        '<div class="ut">UT3 · Configuración básica de Linux</div>'
        f'<div class="num">{num}</div><div class="titulo">{titulo}</div>'
        '</td><td class="logo"></td></tr></table>'
    )
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<style>{CSS}</style></head><body>{cabecera}{cuerpo}</body></html>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
    subprocess.run(
        ["wkhtmltopdf", "--quiet", "--encoding", "utf-8",
         "--margin-top", "18mm", "--margin-bottom", "18mm",
         "--margin-left", "18mm", "--margin-right", "18mm",
         tmp.name, str(destino)],
        check=True, capture_output=True,
    )
    Path(tmp.name).unlink()


def necesita_regenerar(fuente: Path, destino: Path) -> bool:
    """True si el PDF no existe o es más antiguo que su .md, el logo o este script."""
    if not destino.exists():
        return True
    ultima = max(fuente.stat().st_mtime, LOGO.stat().st_mtime, Path(__file__).stat().st_mtime)
    return destino.stat().st_mtime < ultima


def generar(todos: bool = False) -> list[str]:
    """Genera los PDF necesarios y devuelve la lista de los generados."""
    if shutil.which("wkhtmltopdf") is None:
        raise RuntimeError("no se encuentra wkhtmltopdf; instálalo para generar los PDF")
    SALIDA.mkdir(exist_ok=True)
    generados = []
    for nombre, pdf in FICHEROS.items():
        fuente = PRACTICAS / f"{nombre}.md"
        destino = SALIDA / f"{pdf}.pdf"
        if todos or necesita_regenerar(fuente, destino):
            convertir(fuente, destino)
            generados.append(destino.name)
    return generados


def main() -> None:
    generados = generar(todos="--todos" in sys.argv)
    if generados:
        for nombre in generados:
            print("Generado", nombre)
    else:
        print("Los PDF ya están al día.")


if __name__ == "__main__":
    main()
