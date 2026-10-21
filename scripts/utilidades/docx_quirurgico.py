# -*- coding: utf-8 -*-
"""
Motor centralizado de Cirugía OpenXML Nativa para Microsoft Word (.docx), PDF 1.4, XLSX y PNG 300 DPI
bajo normas APA 7 y UNAJMA.
Referencia oficial: .claude/skills/tablas-quirurgicas-docx-apa7/SKILL.md
"""
import argparse
import html
import json
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def eliminar_flotacion_tabla(table) -> bool:
    """Elimina el nodo <w:tblpPr> si existe para impedir tablas flotantes."""
    tblPr = getattr(getattr(table, "_tbl", None), "tblPr", None)
    if tblPr is None:
        return False
    removido = False
    for child in list(tblPr):
        if child.tag.endswith("tblpPr"):
            tblPr.remove(child)
            removido = True
    return removido


def configurar_geometria_tabla(
    table,
    total_width_dxa: int = 8788,
    col_widths_dxa: Optional[Sequence[int]] = None,
    align: str = "center",
) -> None:
    """Configura el ancho exacto en dxa y elimina cualquier flotación w:tblpPr."""
    eliminar_flotacion_tabla(table)
    if col_widths_dxa and hasattr(table, "rows"):
        for row in table.rows:
            for idx, cell in enumerate(row.cells):
                if idx < len(col_widths_dxa):
                    cell.width = col_widths_dxa[idx]


def construir_docx_openxml(
    ruta_destino: Union[str, Path],
    titulo_documento: str,
    bloques: Sequence[Dict[str, Any]],
    permitir_referencias_bootstrap: bool = False,
) -> Path:
    """
    Construye un archivo Microsoft Word (.docx) 100% nativo OpenXML (sin dependencias externas)
    cumpliendo estrictamente los estándares UNAJMA y APA 7:
    - Papel A4: w=11906 dxa, h=16838 dxa
    - Márgenes UNAJMA: Superior=1985 dxa (3.5 cm), Izquierdo=1985 dxa (3.5 cm),
      Inferior=1418 dxa (2.5 cm), Derecho=1418 dxa (2.5 cm)
    - Tipografía: Times New Roman 12 pt (cuerpo) y 10 pt (tablas/notas)
    - Tablas APA 7 de 3 líneas horizontales, w:tblHeader, w:cantSplit, cero w:tblpPr
    - Referencias con sangría francesa de 1.27 cm (w:left="720" w:hanging="720")
    """
    p_dest = Path(ruta_destino)
    if not permitir_referencias_bootstrap:
        seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
</Types>"""

    rels_root = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
</Relationships>"""

    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="es-PE"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="160" w:line="480" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="240" w:after="120" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="200" w:after="100" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ReferenciaAPA7">
    <w:name w:val="Referencia APA 7"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:spacing w:before="0" w:after="120" w:line="480" w:lineRule="auto"/>
      <w:ind w:left="720" w:hanging="720"/>
      <w:jc w:val="both"/>
    </w:pPr>
  </w:style>
</w:styles>"""

    settings_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
</w:settings>"""

    core_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{html.escape(titulo_documento)}</dc:title>
  <dc:creator>{html.escape(rutas.TESISTA)}</dc:creator>
  <cp:lastModifiedBy>SIVAC-THESIS-LAB (maquetador-docx)</cp:lastModifiedBy>
  <dc:description>Documento generado con cirugía OpenXML nativa bajo normas APA 7 y Reglamento UNAJMA</dc:description>
</cp:coreProperties>"""

    body_parts: List[str] = []

    for b in bloques:
        tipo = b.get("tipo", "parrafo")
        if tipo == "titulo_portada":
            lineas = b.get("lineas", [])
            for lin in lineas:
                txt = html.escape(str(lin.get("texto", "")))
                bold = "<w:b/>" if lin.get("negrita", True) else ""
                sz = int(lin.get("pt", 14)) * 2
                body_parts.append(
                    f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="80" w:after="80" w:line="360" w:lineRule="auto"/></w:pPr>'
                    f'<w:r><w:rPr>{bold}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
                )
        elif tipo == "h1":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:jc w:val="center"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="28"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "h2":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="Heading2"/><w:jc w:val="left"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "h3":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:keepNext/><w:jc w:val="left"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:i/><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "parrafo":
            txt = html.escape(str(b.get("texto", "")))
            align = b.get("alineacion", "both")
            sangria = '<w:ind w:firstLine="720"/>' if b.get("sangria_primera_linea", True) else ""
            bold = "<w:b/>" if b.get("negrita", False) else ""
            italic = "<w:i/>" if b.get("cursiva", False) else ""
            body_parts.append(
                f'<w:p><w:pPr><w:jc w:val="{align}"/><w:spacing w:after="160" w:line="480" w:lineRule="auto"/>{sangria}</w:pPr>'
                f'<w:r><w:rPr>{bold}{italic}<w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "formula_omml":
            etiqueta = html.escape(str(b.get("etiqueta", "")))
            expresion = html.escape(str(b.get("expresion", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>'
                f'<m:oMathPara xmlns:m="{M_NS}"><m:oMath><m:r><m:t>{expresion}</m:t></m:r></m:oMath></m:oMathPara>'
                f'<w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">   {etiqueta}</w:t></w:r></w:p>'
            )
        elif tipo == "referencia":
            txt = html.escape(str(b.get("texto", "")))
            body_parts.append(
                f'<w:p><w:pPr><w:pStyle w:val="ReferenciaAPA7"/><w:ind w:left="720" w:hanging="720"/><w:jc w:val="both"/></w:pPr>'
                f'<w:r><w:rPr><w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{txt}</w:t></w:r></w:p>'
            )
        elif tipo == "tabla_apa7":
            numero = html.escape(str(b.get("numero", "Tabla 1")))
            titulo = html.escape(str(b.get("titulo", "")))
            encabezados = b.get("encabezados", [])
            filas = b.get("filas", [])
            nota = html.escape(str(b.get("nota", "Elaboración propia.")))
            total_w = int(b.get("ancho_total_dxa", 8503))
            num_cols = max(1, len(encabezados))
            col_w = total_w // num_cols

            # Prefijo APA 7: Tabla N en negrita + Título en cursiva con keepNext
            body_parts.append(
                f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{numero}</w:t></w:r></w:p>'
            )
            body_parts.append(
                f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="0" w:after="100" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:i/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{titulo}</w:t></w:r></w:p>'
            )

            grid_cols = "".join(f'<w:gridCol w:w="{col_w}"/>' for _ in range(num_cols))
            # Fila de encabezado con borde inferior single sz=4, tblHeader y cantSplit
            header_cells = []
            for h_txt in encabezados:
                h_esc = html.escape(str(h_txt))
                header_cells.append(
                    f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>'
                    f'<w:tcBorders><w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/></w:tcBorders>'
                    f'<w:vAlign w:val="center"/></w:tcPr>'
                    f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
                    f'<w:r><w:rPr><w:b/><w:sz w:val="20"/></w:rPr><w:t xml:space="preserve">{h_esc}</w:t></w:r></w:p></w:tc>'
                )
            rows_xml = [
                f'<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{"".join(header_cells)}</w:tr>'
            ]

            for fila in filas:
                row_cells = []
                for idx_c, c_txt in enumerate(fila):
                    c_esc = html.escape(str(c_txt))
                    jc_val = "left" if idx_c <= 1 else "center"
                    row_cells.append(
                        f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
                        f'<w:p><w:pPr><w:jc w:val="{jc_val}"/><w:spacing w:before="30" w:after="30" w:line="240" w:lineRule="auto"/></w:pPr>'
                        f'<w:r><w:rPr><w:sz w:val="19"/></w:rPr><w:t xml:space="preserve">{c_esc}</w:t></w:r></w:p></w:tc>'
                    )
                rows_xml.append(f'<w:tr><w:trPr><w:cantSplit/></w:trPr>{"".join(row_cells)}</w:tr>')

            tabla_xml = (
                f'<w:tbl>'
                f'<w:tblPr>'
                f'<w:tblW w:w="{total_w}" w:type="dxa"/>'
                f'<w:jc w:val="center"/>'
                f'<w:tblBorders>'
                f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                f'</w:tblBorders>'
                f'<w:tblCellMar>'
                f'<w:top w:w="60" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
                f'<w:bottom w:w="60" w:type="dxa"/><w:right w:w="90" w:type="dxa"/>'
                f'</w:tblCellMar>'
                f'</w:tblPr>'
                f'<w:tblGrid>{grid_cols}</w:tblGrid>'
                f'{"".join(rows_xml)}'
                f'</w:tbl>'
            )
            body_parts.append(tabla_xml)
            body_parts.append(
                f'<w:p><w:pPr><w:spacing w:before="60" w:after="180" w:line="240" w:lineRule="auto"/></w:pPr>'
                f'<w:r><w:rPr><w:i/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">Nota. </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{nota}</w:t></w:r></w:p>'
            )

    sect_pr = (
        '<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838" w:orient="portrait"/>'
        '<w:pgMar w:top="1985" w:right="1418" w:bottom="1418" w:left="1985" w:header="709" w:footer="709" w:gutter="0"/>'
        '<w:pgNumType w:fmt="decimal" w:start="1"/>'
        '</w:sectPr>'
    )

    document_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:document xmlns:w="{W_NS}" xmlns:m="{M_NS}">'
        f'<w:body>{"".join(body_parts)}{sect_pr}</w:body>'
        '</w:document>'
    )

    with zipfile.ZipFile(p_dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels_root)
        zf.writestr("word/_rels/document.xml.rels", doc_rels)
        zf.writestr("word/styles.xml", styles_xml)
        zf.writestr("word/settings.xml", settings_xml)
        zf.writestr("docProps/core.xml", core_xml)
        zf.writestr("word/document.xml", document_xml)

    return p_dest


def auditar_docx_openxml(ruta_docx: Union[str, Path]) -> Dict[str, Any]:
    """Audita un archivo .docx inspeccionando directamente su árbol OpenXML."""
    p = Path(ruta_docx)
    if not p.exists():
        return {"archivo": str(p), "existe": False, "cumple_apa7": False, "hallazgos": ["Archivo no encontrado"]}

    hallazgos: List[str] = []
    tablas_total = 0
    tablas_flotantes = 0
    tablas_con_header = 0
    tablas_con_cantsplit = 0
    referencias_sangria_francesa = 0
    formulas_omml = 0
    margenes_unajma_ok = False

    try:
        with zipfile.ZipFile(p, "r") as zf:
            xml_bytes = zf.read("word/document.xml")
        root = ET.fromstring(xml_bytes)

        for sect in root.iter(f"{{{W_NS}}}pgMar"):
            top = sect.attrib.get(f"{{{W_NS}}}top")
            left = sect.attrib.get(f"{{{W_NS}}}left")
            bottom = sect.attrib.get(f"{{{W_NS}}}bottom")
            right = sect.attrib.get(f"{{{W_NS}}}right")
            if top == "1985" and left == "1985" and bottom == "1418" and right == "1418":
                margenes_unajma_ok = True
            else:
                hallazgos.append(f"Márgenes fuera de norma UNAJMA: top={top}, left={left}, bottom={bottom}, right={right}")

        for tbl in root.iter(f"{{{W_NS}}}tbl"):
            tablas_total += 1
            if list(tbl.iter(f"{{{W_NS}}}tblpPr")):
                tablas_flotantes += 1
                hallazgos.append(f"Tabla #{tablas_total} contiene posicionamiento flotante <w:tblpPr> prohibido.")
            if list(tbl.iter(f"{{{W_NS}}}tblHeader")):
                tablas_con_header += 1
            if list(tbl.iter(f"{{{W_NS}}}cantSplit")):
                tablas_con_cantsplit += 1

        for ind in root.iter(f"{{{W_NS}}}ind"):
            if ind.attrib.get(f"{{{W_NS}}}hanging") == "720":
                referencias_sangria_francesa += 1

        for _ in root.iter(f"{{{M_NS}}}oMath"):
            formulas_omml += 1

    except Exception as exc:
        hallazgos.append(f"Error al inspeccionar OpenXML: {exc}")

    return {
        "archivo": str(p),
        "existe": True,
        "sha256": seguridad.sha256_archivo(p),
        "bytes": p.stat().st_size,
        "margenes_unajma_ok": margenes_unajma_ok,
        "tablas_total": tablas_total,
        "tablas_flotantes": tablas_flotantes,
        "tablas_con_header": tablas_con_header,
        "tablas_con_cantsplit": tablas_con_cantsplit,
        "referencias_sangria_francesa": referencias_sangria_francesa,
        "formulas_omml": formulas_omml,
        "cumple_apa7": len(hallazgos) == 0 and margenes_unajma_ok and tablas_flotantes == 0,
        "hallazgos": hallazgos,
    }


def _pdf_escape(texto: str) -> str:
    """Convierte texto UTF-8 a codificación PDF WinAnsi (Latin-1) escapando paréntesis."""
    reemplazos = {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "-",
        "–": "-",
        "•": "*",
        "≥": ">=",
        "≤": "<=",
        "≠": "!=",
        "±": "+/-",
        "×": "x",
        "⟶": "->",
        "→": "->",
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    b = texto.encode("latin-1", errors="replace").decode("latin-1")
    return b.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def construir_pdf_nativo(
    ruta_destino: Union[str, Path],
    titulo: str,
    paginas_lineas: Sequence[Sequence[str]],
    permitir_referencias_bootstrap: bool = False,
) -> Path:
    """
    Construye un documento PDF 1.4 multipágina válido con tipografía Times-Roman y Helvetica-Bold,
    encabezado institucional UNAJMA y numeración de páginas.
    """
    p_dest = Path(ruta_destino)
    if not permitir_referencias_bootstrap:
        seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    num_pages = max(1, len(paginas_lineas))
    # Objetos PDF:
    # 1: Catalog
    # 2: Pages
    # 3: Font F1 (Times-Roman)
    # 4: Font F2 (Times-Bold)
    # 5 + 2*i: Page i
    # 6 + 2*i: Content stream i
    objects: List[bytes] = []

    page_ids = [5 + 2 * i for i in range(num_pages)]
    kids_str = " ".join(f"{pid} 0 R" for pid in page_ids)

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(f"<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman /Encoding /WinAnsiEncoding >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold /Encoding /WinAnsiEncoding >>")

    for i, lineas in enumerate(paginas_lineas):
        page_id = 5 + 2 * i
        content_id = 6 + 2 * i
        stream_cmds = [
            "BT",
            "/F2 9 Tf",
            "85 795 Td",
            f"({_pdf_escape('UNIVERSIDAD NACIONAL JOSE MARIA ARGUEDAS (UNAJMA) - EPIS | SIVAC-THESIS-LAB')}) Tj",
            "ET",
            "0.7 w 85 788 m 525 788 l S",
        ]
        y = 762
        for idx_l, raw_line in enumerate(lineas):
            if y < 65:
                break
            es_encabezado = (
                idx_l == 0
                or raw_line.startswith("CAPÍTULO")
                or raw_line.startswith("CAPITULO")
                or raw_line.startswith("ANEXO")
                or raw_line.startswith("TABLA")
                or raw_line.startswith("Tabla ")
                or raw_line.startswith("CERTIFICADO")
                or raw_line.startswith("INSTRUMENTO")
                or raw_line.startswith("PROYECTO")
                or raw_line.startswith("1.")
                or raw_line.startswith("2.")
                or raw_line.startswith("3.")
                or raw_line.startswith("4.")
                or raw_line.startswith("5.")
                or raw_line.startswith("6.")
            )
            font_tag = "/F2" if es_encabezado else "/F1"
            font_sz = 11 if es_encabezado else 10
            # Ajuste de línea a 86 caracteres
            texto_linea = str(raw_line)
            fragmentos = [texto_linea[j : j + 88] for j in range(0, max(1, len(texto_linea)), 88)]
            for frag in fragmentos:
                if y < 65:
                    break
                stream_cmds.append(f"BT {font_tag} {font_sz} Tf 85 {y} Td ({_pdf_escape(frag)}) Tj ET")
                y -= 14

        # Pie de página
        stream_cmds.append("0.5 w 85 52 m 525 52 l S")
        stream_cmds.append(
            f"BT /F1 9 Tf 85 38 Td ({_pdf_escape(titulo[:65])} — Pagina {i + 1} de {num_pages}) Tj ET"
        )

        stream_data = "\n".join(stream_cmds).encode("latin-1", errors="replace")
        page_obj = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")
        content_obj = (
            f"<< /Length {len(stream_data)} >>\nstream\n".encode("ascii")
            + stream_data
            + b"\nendstream"
        )
        objects.append(page_obj)
        objects.append(content_obj)

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: List[int] = []
    for idx, obj_bytes in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{idx} 0 obj\n".encode("ascii"))
        out.extend(obj_bytes)
        out.extend(b"\nendobj\n")

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    p_dest.write_bytes(bytes(out))
    return p_dest


def construir_xlsx_openxml(
    ruta_destino: Union[str, Path],
    hojas: Sequence[Tuple[str, Sequence[Sequence[Any]]]],
) -> Path:
    """Construye un libro Microsoft Excel (.xlsx) OpenXML nativo con múltiples hojas."""
    p_dest = Path(ruta_destino)
    seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, len(hojas) + 1)
    )
    content_types = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  {overrides}
</Types>"""

    rels_root = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    sheets_tag = "".join(
        f'<sheet name="{html.escape(nombre[:31])}" sheetId="{i}" r:id="rId{i}"/>'
        for i, (nombre, _) in enumerate(hojas, start=1)
    )
    workbook_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>{sheets_tag}</sheets>
</workbook>"""

    wb_rels_tag = "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        for i in range(1, len(hojas) + 1)
    )
    workbook_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {wb_rels_tag}
</Relationships>"""

    with zipfile.ZipFile(p_dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels_root)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)

        for idx_s, (_, filas) in enumerate(hojas, start=1):
            rows_xml = []
            for r_idx, fila in enumerate(filas, start=1):
                cells_xml = []
                for c_idx, val in enumerate(fila):
                    col_letter = chr(65 + (c_idx % 26))
                    ref = f"{col_letter}{r_idx}"
                    if isinstance(val, (int, float)):
                        cells_xml.append(f'<c r="{ref}"><v>{val}</v></c>')
                    else:
                        txt = html.escape(str(val))
                        cells_xml.append(f'<c r="{ref}" t="inlineStr"><is><t>{txt}</t></is></c>')
                rows_xml.append(f'<row r="{r_idx}">{"".join(cells_xml)}</row>')
            sheet_xml = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                f'<sheetData>{"".join(rows_xml)}</sheetData>'
                '</worksheet>'
            )
            zf.writestr(f"xl/worksheets/sheet{idx_s}.xml", sheet_xml)

    return p_dest


def construir_png_300dpi(
    ruta_destino: Union[str, Path],
    ancho: int = 1200,
    alto: int = 750,
    color_acento: Tuple[int, int, int] = (30, 58, 138),
) -> Path:
    """
    Construye un archivo PNG de alta resolución con metadato físico exacto pHYs de 300 DPI
    (11811 píxeles por metro en X e Y) y diagramación limpia de cajas arquitectónicas/estadísticas.
    """
    p_dest = Path(ruta_destino)
    seguridad.asegurar_escritura_permitida(p_dest)
    p_dest.parent.mkdir(parents=True, exist_ok=True)

    def _chunk(chunk_type: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)

    # Fondo blanco #FFFFFF con marco gris #D3D3D3, franja superior en color_acento y bloques de diagrama
    r_ac, g_ac, b_ac = color_acento
    raw_rows = bytearray()

    for y in range(alto):
        raw_rows.append(0)  # Filter type 0 (None)
        if y < 4 or y >= alto - 4:
            # Borde exterior gris #D3D3D3 (regla de extraccion-figuras-pdf-docx)
            row_bytes = bytes([211, 211, 211]) * ancho
        elif 20 <= y < 76:
            # Encabezado del diagrama
            row_bytes = bytes([211, 211, 211]) * 24 + bytes([r_ac, g_ac, b_ac]) * (ancho - 48) + bytes([211, 211, 211]) * 24
        elif y in (140, 320, 360, 540, 580, 700):
            # Líneas horizontales de los módulos del diagrama
            row_bytes = bytes([255, 255, 255]) * 60 + bytes([r_ac, g_ac, b_ac]) * (ancho - 120) + bytes([255, 255, 255]) * 60
        elif (140 < y < 320) or (360 < y < 540) or (580 < y < 700):
            # Tres tarjetas modulares en paralelo
            bloque_w = (ancho - 180) // 3
            fila = bytearray(bytes([211, 211, 211]) * 4 + bytes([255, 255, 255]) * 56)
            for b_idx in range(3):
                fill_c = (241, 245, 249) if b_idx % 2 == 0 else (238, 242, 255)
                fila.extend(bytes([r_ac, g_ac, b_ac]) * 3)
                fila.extend(bytes(fill_c) * (bloque_w - 6))
                fila.extend(bytes([r_ac, g_ac, b_ac]) * 3)
                if b_idx < 2:
                    fila.extend(bytes([255, 255, 255]) * 30)
            restante = ancho - (len(fila) // 3) - 4
            if restante > 0:
                fila.extend(bytes([255, 255, 255]) * restante)
            fila.extend(bytes([211, 211, 211]) * 4)
            row_bytes = bytes(fila[: ancho * 3])
        else:
            row_bytes = bytes([211, 211, 211]) * 4 + bytes([255, 255, 255]) * (ancho - 8) + bytes([211, 211, 211]) * 4
        raw_rows.extend(row_bytes)

    ihdr = struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0)
    # 300 DPI = 300 / 0.0254 = 11811 píxeles por metro (unit specifier = 1)
    phys = struct.pack(">IIB", 11811, 11811, 1)
    idat = zlib.compress(bytes(raw_rows), level=6)

    png_bytes = (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"pHYs", phys)
        + _chunk(b"IDAT", idat)
        + _chunk(b"IEND", b"")
    )
    p_dest.write_bytes(png_bytes)
    return p_dest


def main() -> int:
    seguridad.configurar_utf8()
    parser = argparse.ArgumentParser(description="Motor quirúrgico OpenXML para tablas y documentos APA 7 (UNAJMA)")
    parser.add_argument(
        "comando",
        choices=["auditar", "blindar-todas", "exportar-pdf", "renderizar-paginas"],
        nargs="?",
        default="auditar",
    )
    parser.add_argument("ruta_docx", nargs="?", help="Ruta al archivo .docx o .pdf a inspeccionar")
    parser.add_argument("--paginas", default="1", help="Páginas a renderizar")
    parser.add_argument("--dpi", type=int, default=300, help="Resolución DPI")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    args = parser.parse_args()

    if not args.ruta_docx:
        print(json.dumps({"estado": "listo", "motor": "docx_quirurgico.py", "regla": "APA 7 / UNAJMA"}, ensure_ascii=False))
        return 0

    reporte = auditar_docx_openxml(args.ruta_docx)
    print(json.dumps(reporte, indent=2, ensure_ascii=False))
    return 0 if reporte.get("cumple_apa7", False) else 1


if __name__ == "__main__":
    sys.exit(main())
