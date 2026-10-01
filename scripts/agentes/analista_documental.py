#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB (Squad E) - Analista documental: desglose estructural fiel, de solo lectura.

Descompone documentos modelo (.docx, .pdf, .xlsx) en un inventario verificable y compara
formatos entre documentos. Nunca modifica el documento analizado: solo lee y, si se pide,
escribe JSON/Markdown en una ruta de salida permitida (nunca en referencias/).

Subcomandos
-----------
  desglosar ARCHIVO [--json] [--salida-json R] [--salida-md R] [--bloques] [--forzar]
  comparar A B [--json]
  plantilla-estructura PDF [--salida R] [--forzar] [--json]

Qué extrae
----------
.docx  secciones (márgenes, orientación, pgNumType, encabezados/pies referenciados), estilos
       USADOS con propiedades resueltas (cadena basedOn + docDefaults + tema), jerarquía de
       encabezados con numeración (automática calculada o manual), tablas (dimensiones, bordes,
       encabezado repetido, anchos), imágenes (formato, px, DPI efectivo), encabezados/pies con
       campos, rótulos de tablas/figuras y su formato, campos del cuerpo, comentarios y cambios.
.pdf   por página: fuente/tamaño dominante, bloques (opcional), etiqueta impresa, imágenes y
       dibujos (vía ingesta_pdf.cargar_indice); títulos por criterio explícito; TOC embebido
       (get_toc) e índice impreso (líneas con puntos guía); márgenes estimados; numeración.
.xlsx  hojas, rango usado, fórmulas (openpyxl sin data_only) y valores en caché.

Principios anti-alucinación
---------------------------
* Lo que no puede confirmarse queda en null o "[VERIFICAR: motivo]" (p. ej. etiqueta impresa).
* Páginas PDF sin capa de texto se reportan como "requiere OCR"; no se inventa texto. Tesseract
  se detecta con shutil.which / ruta por defecto, pero este módulo no ejecuta OCR.
* Las métricas estimadas (márgenes e interlineado de PDF) se rotulan "estimado".

Efectos secundarios (únicos): (a) la caché de índices de ingesta_pdf (<slug>.idx.json). Solo se usa
la caché compartida del vault (rutas.INDICES_PDF) para los PDF de PDFS_FUENTES y de
referencias/modelos_tesis; un PDF cualquiera se indexa EN MEMORIA y no escribe nada. --carpeta-indices
fuerza una caché en otra carpeta y --sin-cache obliga a indexar siempre en memoria. (b) Solo se escribe
lo pedido con --salida-json/--salida-md/--salida (nunca en referencias/).

Códigos de salida: 0 ok, 1 hallazgos/fallos (diferencias en 'comparar', archivo inexistente,
corrupto o cifrado), 2 uso incorrecto (formato no soportado, argumentos).
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import statistics
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad  # noqa: E402
from scripts.fuentes import texto as tx  # noqa: E402

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
VML_NS = "urn:schemas-microsoft-com:vml"
TWIPS_POR_CM = 566.929
EMU_POR_PULGADA = 914400.0
TESSERACT_DEFECTO = r"C:/Users/jquis/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
RE_ROTULO = re.compile(r"^\s*(Tabla|Figura|Cuadro|Gráfico|Grafico|Table|Figure)\s+(\d+(?:\.\d+)?)", re.I)
ALTURA_LINEA_NATURAL = 1.15  # factor típico de Times New Roman / Arial (estimación)


class FormatoNoSoportado(ValueError):
    """Extensión que el módulo no sabe analizar (uso incorrecto: código de salida 2)."""


class ArchivoNoLegible(Exception):
    """Archivo corrupto, cifrado o que no corresponde a su extensión (código de salida 1)."""


def q(etq: str) -> str:
    return f"{{{W_NS}}}{etq}"


def _tw_cm(valor: str | None) -> float | None:
    try:
        return round(int(valor) / TWIPS_POR_CM, 2)
    except (TypeError, ValueError):
        return None


def _onoff(el) -> bool | None:
    """Interpreta <w:b/>, <w:b w:val="0"/> ... -> True/False; None si el elemento no existe."""
    if el is None:
        return None
    return el.get(q("val")) not in ("0", "false", "off")


def tesseract_disponible() -> str | None:
    """Ruta de Tesseract si existe (PATH o ubicación por defecto); None si no."""
    return shutil.which("tesseract") or (TESSERACT_DEFECTO if Path(TESSERACT_DEFECTO).exists() else None)


# ======================================================================================
# DOCX - resolución de estilos, numeración y tema
# ======================================================================================

def _leer_rpr(rpr) -> dict:
    """Propiedades de carácter presentes en un <w:rPr> (solo las declaradas)."""
    salida: dict = {}
    if rpr is None:
        return salida
    rf = rpr.find(q("rFonts"))
    if rf is not None:
        fuente = rf.get(q("ascii")) or rf.get(q("hAnsi")) or rf.get(q("cs"))
        tema = rf.get(q("asciiTheme")) or rf.get(q("hAnsiTheme"))
        if tema:
            salida["fuente_tema"] = tema
        if fuente:
            salida["fuente"] = fuente
    sz = rpr.find(q("sz"))
    if sz is not None and sz.get(q("val"), "").isdigit():
        salida["tam_pt"] = int(sz.get(q("val"))) / 2
    for clave, etq in (("negrita", "b"), ("cursiva", "i"), ("versalitas", "smallCaps"), ("mayusculas", "caps")):
        v = _onoff(rpr.find(q(etq)))
        if v is not None:
            salida[clave] = v
    u = rpr.find(q("u"))
    if u is not None:
        salida["subrayado"] = u.get(q("val")) not in (None, "none")
    return salida


_JC = {"left": "izquierda", "start": "izquierda", "center": "centrada", "right": "derecha",
       "end": "derecha", "both": "justificada", "distribute": "distribuida"}


def _leer_ppr(ppr) -> dict:
    """Propiedades de párrafo presentes en un <w:pPr> (solo las declaradas)."""
    salida: dict = {}
    if ppr is None:
        return salida
    jc = ppr.find(q("jc"))
    if jc is not None:
        salida["alineacion"] = _JC.get(jc.get(q("val")), jc.get(q("val")))
    sp = ppr.find(q("spacing"))
    if sp is not None:
        if sp.get(q("line")) and sp.get(q("line")).isdigit():
            regla = sp.get(q("lineRule"), "auto")
            linea = int(sp.get(q("line")))
            salida["interlineado"] = ({"valor": round(linea / 240, 3), "regla": "multiple"} if regla == "auto"
                                      else {"valor": round(linea / 20, 2), "regla": "exacto" if regla == "exact" else "minimo", "unidad": "pt"})
        for clave, atr in (("antes_pt", "before"), ("despues_pt", "after")):
            if sp.get(q(atr)) and sp.get(q(atr)).lstrip("-").isdigit():
                salida[clave] = int(sp.get(q(atr))) / 20
    ind = ppr.find(q("ind"))
    if ind is not None:
        s = {}
        for clave, atrs in (("izq_cm", ("left", "start")), ("der_cm", ("right", "end")),
                            ("primera_linea_cm", ("firstLine",)), ("francesa_cm", ("hanging",))):
            for a in atrs:
                v = _tw_cm(ind.get(q(a)))
                if v is not None:
                    s[clave] = v
                    break
        if s:
            salida["sangria"] = s
    ol = ppr.find(q("outlineLvl"))
    if ol is not None and (ol.get(q("val")) or "").isdigit():
        salida["nivel_esquema"] = int(ol.get(q("val"))) + 1
    npr = ppr.find(q("numPr"))
    if npr is not None:
        nid, lv = npr.find(q("numId")), npr.find(q("ilvl"))
        salida["num"] = {"numId": nid.get(q("val")) if nid is not None else None,
                         "ilvl": int(lv.get(q("val"))) if lv is not None and (lv.get(q("val")) or "").isdigit() else None}
    for clave, etq in (("conservar_con_siguiente", "keepNext"), ("salto_antes", "pageBreakBefore")):
        v = _onoff(ppr.find(q(etq)))
        if v is not None:
            salida[clave] = v
    return salida


def _leer_bordes(contenedor) -> dict:
    """<w:tblBorders>/<w:tcBorders> -> {lado: {val, sz_pt, color}}."""
    salida = {}
    if contenedor is None:
        return salida
    for lado in ("top", "left", "start", "bottom", "right", "end", "insideH", "insideV"):
        b = contenedor.find(q(lado))
        if b is not None:
            sz = b.get(q("sz"))
            salida[lado] = {"val": b.get(q("val")), "sz_pt": int(sz) / 8 if sz and sz.isdigit() else None,
                            "color": b.get(q("color"))}
    return salida


def _borde_visible(b: dict | None) -> bool:
    return bool(b) and b.get("val") not in (None, "nil", "none") and (b.get("sz_pt") in (None,) or b["sz_pt"] > 0)


class Estilos:
    """Resuelve propiedades efectivas: docDefaults -> cadena basedOn -> formato directo."""

    def __init__(self, doc):
        raiz = doc.styles.element
        self.por_id = {s.get(q("styleId")): s for s in raiz.findall(q("style"))}
        self.tema = self._fuentes_tema(doc)
        dd = raiz.find(q("docDefaults"))
        self.def_r = _leer_rpr(dd.find(f"{q('rPrDefault')}/{q('rPr')}")) if dd is not None else {}
        self.def_p = _leer_ppr(dd.find(f"{q('pPrDefault')}/{q('pPr')}")) if dd is not None else {}
        self.parrafo_defecto = next((i for i, s in self.por_id.items()
                                     if s.get(q("type")) == "paragraph" and s.get(q("default")) in ("1", "true")), None)
        self._cache: dict = {}

    @staticmethod
    def _fuentes_tema(doc) -> dict:
        from lxml import etree
        for parte in doc.part.package.iter_parts():
            if str(parte.partname).endswith("theme1.xml"):
                try:
                    arbol = etree.fromstring(parte.blob)
                    ns = {"a": A_NS}
                    return {"majorHAnsi": (arbol.xpath("//a:majorFont/a:latin/@typeface", namespaces=ns) or [None])[0],
                            "minorHAnsi": (arbol.xpath("//a:minorFont/a:latin/@typeface", namespaces=ns) or [None])[0]}
                except Exception:  # noqa: BLE001
                    return {}
        return {}

    def nombre(self, style_id: str | None) -> str | None:
        s = self.por_id.get(style_id)
        if s is None:
            return style_id
        n = s.find(q("name"))
        return n.get(q("val")) if n is not None else style_id

    def cadena(self, style_id: str | None) -> list:
        """Estilos desde el más base hasta el derivado."""
        cad, visto = [], set()
        while style_id and style_id in self.por_id and style_id not in visto:
            visto.add(style_id)
            s = self.por_id[style_id]
            cad.append(s)
            b = s.find(q("basedOn"))
            style_id = b.get(q("val")) if b is not None else None
        return list(reversed(cad))

    def _aplicar_tema(self, r: dict) -> dict:
        if "fuente" not in r and r.get("fuente_tema") in self.tema and self.tema[r["fuente_tema"]]:
            r["fuente"] = self.tema[r["fuente_tema"]]
        return r

    def estilo(self, style_id: str | None) -> dict:
        """{'p': ..., 'r': ...} resueltos para un estilo de párrafo o carácter."""
        if style_id in self._cache:
            return self._cache[style_id]
        r, p = dict(self.def_r), dict(self.def_p)
        for s in self.cadena(style_id):
            r.update(_leer_rpr(s.find(q("rPr"))))
            p.update(_leer_ppr(s.find(q("pPr"))))
        res = {"p": p, "r": self._aplicar_tema(r)}
        self._cache[style_id] = res
        return res

    def bordes_tabla(self, style_id: str | None) -> dict:
        b: dict = {}
        for s in self.cadena(style_id):
            b.update(_leer_bordes(s.find(f"{q('tblPr')}/{q('tblBorders')}")))
        return b

    def bordes_condicionales(self, style_id: str | None, tipo: str) -> dict:
        """Bordes del formato condicional <w:tblStylePr w:type=tipo> (firstRow, lastRow...) a lo largo de la
        cadena basedOn: {'tc': bordes de celda, 'tbl': bordes de tabla}. Solo son efectivos si el
        <w:tblLook> de la tabla activa ese tipo (ver `_tbl_look`)."""
        res: dict = {"tc": {}, "tbl": {}}
        for s in self.cadena(style_id):
            for sp in s.findall(q("tblStylePr")):
                if sp.get(q("type")) != tipo:
                    continue
                res["tc"].update(_leer_bordes(sp.find(f"{q('tcPr')}/{q('tcBorders')}")))
                res["tbl"].update(_leer_bordes(sp.find(f"{q('tblPr')}/{q('tblBorders')}")))
        return res


_ROMANOS = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
            (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def _romano(n: int) -> str:
    salida = ""
    for v, s in _ROMANOS:
        while n >= v:
            salida += s
            n -= v
    return salida


def _formato_num(n: int, fmt: str) -> str:
    if fmt == "decimalZero":
        return f"{n:02d}"
    if fmt == "upperRoman":
        return _romano(n)
    if fmt == "lowerRoman":
        return _romano(n).lower()
    if fmt in ("upperLetter", "lowerLetter") and 1 <= n <= 26:
        c = chr(64 + n)
        return c if fmt == "upperLetter" else c.lower()
    return str(n)


class Numeracion:
    """Contadores de listas de Word (numbering.xml). El número resultante es CALCULADO (aprox.)."""

    def __init__(self, doc):
        self.abstractos: dict = {}
        self.num_a_abs: dict = {}
        self.contadores: dict = {}
        try:
            raiz = doc.part.numbering_part.element
        except Exception:  # noqa: BLE001
            return
        for a in raiz.findall(q("abstractNum")):
            niveles = {}
            for lv in a.findall(q("lvl")):
                g = lambda e, lv=lv: (lv.find(q(e)).get(q("val")) if lv.find(q(e)) is not None else None)  # noqa: E731
                niveles[int(lv.get(q("ilvl")))] = {"fmt": g("numFmt"), "texto": g("lvlText"),
                                                   "inicio": int(g("start") or 1), "pStyle": g("pStyle")}
            self.abstractos[a.get(q("abstractNumId"))] = niveles
        for n in raiz.findall(q("num")):
            ab = n.find(q("abstractNumId"))
            if ab is not None:
                self.num_a_abs[n.get(q("numId"))] = ab.get(q("val"))

    def nivel_de_estilo(self, num_id: str, style_id: str | None) -> int:
        for lv, d in self.abstractos.get(self.num_a_abs.get(num_id), {}).items():
            if style_id and d.get("pStyle") == style_id:
                return lv
        return 0

    def siguiente(self, num_id: str | None, ilvl: int) -> dict | None:
        if not num_id or num_id == "0" or num_id not in self.num_a_abs:
            return None
        ab = self.num_a_abs[num_id]
        niveles = self.abstractos.get(ab, {})
        if ilvl not in niveles:
            return None
        cont = self.contadores.setdefault(ab, [None] * 9)
        d = niveles[ilvl]
        if d["fmt"] == "bullet":
            return {"numId": num_id, "ilvl": ilvl, "formato": "bullet", "numero": None}
        cont[ilvl] = d["inicio"] if cont[ilvl] is None else cont[ilvl] + 1
        for k in range(ilvl + 1, 9):
            cont[k] = None
        texto = d["texto"] or ""
        for k in range(ilvl + 1):
            marca = f"%{k + 1}"
            if marca in texto:
                v = cont[k] if cont[k] is not None else niveles.get(k, {}).get("inicio", 1)
                texto = texto.replace(marca, _formato_num(v, niveles.get(k, {}).get("fmt") or "decimal"))
        return {"numId": num_id, "ilvl": ilvl, "formato": d["fmt"], "numero": texto}


# ======================================================================================
# DOCX - análisis
# ======================================================================================

def _texto_parrafo(p) -> str:
    return "".join(t.text or "" for t in p.iter(q("t")))


MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"


def _en_fallback(p) -> bool:
    """True si el párrafo está en <mc:Fallback> (duplicado de un <mc:Choice>; se omite para no contar doble)."""
    return any(a.tag == f"{{{MC_NS}}}Fallback" for a in p.iterancestors())


def _en_tabla(p) -> bool:
    return any(a.tag == q("tbl") for a in p.iterancestors())


def _campos(raiz) -> list[str]:
    """Instrucciones de campo (PAGE, SEQ, TOC...) presentes bajo `raiz`."""
    instr = [f.get(q("instr")) or "" for f in raiz.iter(q("fldSimple"))]
    instr += [t.text or "" for t in raiz.iter(q("instrText"))]
    return [i.strip() for i in instr if i.strip()]


def _sect(sect) -> dict:
    g = lambda e: sect.find(q(e))  # noqa: E731
    sz, mar, nt, cols, tipo = g("pgSz"), g("pgMar"), g("pgNumType"), g("cols"), g("type")
    salida: dict = {"pagina_cm": None, "orientacion": None, "margenes_cm": None}
    if sz is not None:
        w, h = _tw_cm(sz.get(q("w"))), _tw_cm(sz.get(q("h")))
        salida["pagina_cm"] = [w, h]
        salida["orientacion"] = sz.get(q("orient")) or ("horizontal" if (w or 0) > (h or 0) else "vertical")
        if salida["orientacion"] == "landscape":
            salida["orientacion"] = "horizontal"
        elif salida["orientacion"] == "portrait":
            salida["orientacion"] = "vertical"
    if mar is not None:
        salida["margenes_cm"] = {k: _tw_cm(mar.get(q(a))) for k, a in (
            ("izq", "left"), ("der", "right"), ("sup", "top"), ("inf", "bottom"),
            ("encabezado", "header"), ("pie", "footer"), ("encuadernacion", "gutter"))}
    salida["pgNumType"] = ({"formato": nt.get(q("fmt")) or "decimal", "inicio": nt.get(q("start"))}
                           if nt is not None else None)
    salida["tipo_salto"] = tipo.get(q("val")) if tipo is not None else "nextPage (por defecto)"
    salida["columnas"] = int(cols.get(q("num"), 1)) if cols is not None and (cols.get(q("num")) or "1").isdigit() else 1
    salida["portada_distinta (titlePg)"] = g("titlePg") is not None
    salida["referencias_cabecera_pie"] = [
        {"elemento": "cabecera" if r.tag == q("headerReference") else "pie",
         "tipo": r.get(q("type")), "rId": r.get(f"{{{R_NS}}}id")}
        for r in sect if r.tag in (q("headerReference"), q("footerReference"))]
    return salida


def _contar_graficos(raiz) -> dict:
    """Clasifica los gráficos bajo `raiz` sin contar dos veces las alternativas <mc:Fallback>:
    imagenes (a:blip o VML con imagedata), formas (cuadros de texto y formas sin mapa de bits) y
    vml_fallback_omitidos (w:pict duplicados dentro de mc:Fallback)."""
    imagenes = formas = omitidos = 0
    for d in raiz.iter(q("drawing")):
        if _en_fallback(d):
            continue
        if next(d.iter(f"{{{A_NS}}}blip"), None) is not None:
            imagenes += 1
        else:
            formas += 1
    for pc in raiz.iter(q("pict")):
        if _en_fallback(pc):
            omitidos += 1
        elif any(e.tag == f"{{{VML_NS}}}imagedata" for e in pc.iter()):
            imagenes += 1
        else:
            formas += 1
    return {"imagenes": imagenes, "formas": formas, "vml_fallback_omitidos": omitidos}


def _imagenes(doc) -> list[dict]:
    """Imágenes del cuerpo (solo las que contienen mapa de bits, a:blip): formato, píxeles y DPI efectivo
    (px / pulgadas en página). Los cuadros de texto y formas se cuentan aparte (`_contar_graficos`)."""
    from PIL import Image
    salida = []
    for d in doc.element.body.iter(q("drawing")):
        if _en_fallback(d) or next(d.iter(f"{{{A_NS}}}blip"), None) is None:
            continue
        contenedor = d[0] if len(d) else None
        if contenedor is None:
            continue
        ext = contenedor.find(f"{{{WP_NS}}}extent")
        docpr = contenedor.find(f"{{{WP_NS}}}docPr")
        blip = next(contenedor.iter(f"{{{A_NS}}}blip"), None)
        reg = {"tipo": "en línea" if contenedor.tag.endswith("inline") else "flotante",
               "nombre": docpr.get("name") if docpr is not None else None,
               "texto_alternativo": (docpr.get("descr") or None) if docpr is not None else None,
               "ancho_cm": None, "alto_cm": None, "formato": None, "px": None, "dpi_efectivo": None,
               "dpi_metadatos": None}
        if ext is not None:
            cx, cy = int(ext.get("cx", 0)), int(ext.get("cy", 0))
            reg["ancho_cm"], reg["alto_cm"] = round(cx / EMU_POR_PULGADA * 2.54, 2), round(cy / EMU_POR_PULGADA * 2.54, 2)
        rid = blip.get(f"{{{R_NS}}}embed") if blip is not None else None
        if rid:
            try:
                parte = doc.part.related_parts[rid]
                reg["archivo"] = str(parte.partname)
                im = Image.open(io.BytesIO(parte.blob))
                reg["formato"], reg["px"] = im.format, [im.width, im.height]
                dpi = im.info.get("dpi")
                reg["dpi_metadatos"] = [round(float(dpi[0]), 1), round(float(dpi[1]), 1)] if dpi else None
                if ext is not None and int(ext.get("cx", 0)) > 0:
                    reg["dpi_efectivo"] = round(im.width / (int(ext.get("cx")) / EMU_POR_PULGADA), 1)
            except Exception as e:  # noqa: BLE001
                reg["aviso"] = f"[VERIFICAR: no se pudo leer la imagen ({type(e).__name__})]"
        salida.append(reg)
    return salida


_MASCARAS_LOOK = {"firstRow": 0x0020, "lastRow": 0x0040, "firstColumn": 0x0080, "lastColumn": 0x0100,
                  "noHBand": 0x0200, "noVBand": 0x0400}


def _tbl_look(tblpr) -> dict:
    """Opciones de estilo de tabla activas (<w:tblLook>): atributos explícitos o, si faltan, máscara hex de w:val.
    Sin <w:tblLook> se asume todo desactivado (no se activa ningún formato condicional)."""
    look = tblpr.find(q("tblLook")) if tblpr is not None else None
    salida = {k: False for k in _MASCARAS_LOOK}
    if look is None:
        return salida
    try:
        mascara = int(look.get(q("val")) or "0", 16)
    except ValueError:
        mascara = 0
    for k, bit in _MASCARAS_LOOK.items():
        explicito = look.get(q(k))
        salida[k] = (explicito in ("1", "true", "on")) if explicito is not None else bool(mascara & bit)
    return salida


def _celdas_todas(fila, lado: str) -> bool:
    """True si TODAS las celdas de la fila declaran borde visible `lado` en su propio <w:tcBorders>."""
    tcs = fila.findall(q("tc"))
    return bool(tcs) and all(
        _borde_visible(_leer_bordes(tc.find(f"{q('tcPr')}/{q('tcBorders')}")).get(lado)) for tc in tcs)


def _lineas_tabla(filas: list, bordes: dict, cond_pri: dict, cond_ult: dict) -> dict:
    """Líneas horizontales efectivas de una tabla, integrando estilo, formato condicional y celdas.

    Devuelve superior, bajo_encabezado (None si <2 filas), inferior, interiores (líneas entre filas de datos),
    origen_bajo_encabezado y vertical_condicional (verticales aportadas por el formato condicional).
    """
    vis = _borde_visible
    superior = (vis(bordes.get("top")) or (bool(filas) and _celdas_todas(filas[0], "top"))
                or vis(cond_pri["tc"].get("top")) or vis(cond_pri["tbl"].get("top")))
    inferior = (vis(bordes.get("bottom")) or (bool(filas) and _celdas_todas(filas[-1], "bottom"))
                or vis(cond_ult["tc"].get("bottom")) or vis(cond_ult["tbl"].get("bottom")))
    inside_h = vis(bordes.get("insideH"))
    origen = None
    if len(filas) >= 2:
        if vis(cond_pri["tc"].get("bottom")):
            origen = "estilo condicional firstRow (tcBorders.bottom)"
        elif _celdas_todas(filas[0], "bottom"):
            origen = "formato directo: borde inferior de las celdas de la fila 1"
        elif _celdas_todas(filas[1], "top"):
            origen = "formato directo: borde superior de las celdas de la fila 2"
        elif inside_h:
            origen = "insideH (la misma línea se repite entre todas las filas)"
    interiores = inside_h and len(filas) > 2 or any(_celdas_todas(f, "bottom") for f in filas[1:-1])
    vert_cond = any(vis(cond.get(k)) for cond in (cond_pri["tc"], cond_ult["tc"])
                    for k in ("left", "right", "start", "end", "insideV"))
    return {"superior": bool(superior), "bajo_encabezado": (origen is not None) if len(filas) >= 2 else None,
            "inferior": bool(inferior), "interiores": bool(interiores), "origen_bajo_encabezado": origen,
            "vertical_condicional": bool(vert_cond)}


def _veredicto_tres_lineas(l: dict, vertical: bool) -> tuple[bool | None, list[str]]:
    """Regla 03 (APA 7): línea superior, línea bajo el encabezado y línea inferior; sin verticales ni interiores."""
    if l["bajo_encabezado"] is None:
        return None, ["tabla de una sola fila: no evaluable"]
    fallos = []
    if not l["superior"]:
        fallos.append("falta la línea superior")
    if not l["bajo_encabezado"]:
        fallos.append("falta la línea bajo el encabezado")
    if not l["inferior"]:
        fallos.append("falta la línea inferior")
    if l["interiores"]:
        fallos.append("hay líneas horizontales interiores (no es de tres líneas)")
    if vertical:
        fallos.append("hay bordes verticales")
    return (not fallos), fallos


def _tablas(doc, est: Estilos) -> list[dict]:
    salida = []
    for i, t in enumerate(doc.element.body.findall(q("tbl")), 1):
        tblpr = t.find(q("tblPr"))
        sid = tblpr.find(q("tblStyle")).get(q("val")) if tblpr is not None and tblpr.find(q("tblStyle")) is not None else None
        directos = _leer_bordes(tblpr.find(q("tblBorders"))) if tblpr is not None else {}
        bordes = {**est.bordes_tabla(sid), **directos}
        filas = t.findall(q("tr"))
        grid = [gc.get(q("w")) for gc in t.findall(f"{q('tblGrid')}/{q('gridCol')}")]
        ncol = len(grid) or max((len(f.findall(q("tc"))) for f in filas), default=0)
        tcb = sum(1 for tc in t.iter(q("tcBorders")) for lado in tc if lado.tag in (q("left"), q("right"), q("start"), q("end"))
                  and lado.get(q("val")) not in (None, "nil", "none"))
        trpr = filas[0].find(q("trPr")) if filas else None
        encabezado_repetido = bool(trpr is not None and trpr.find(q("tblHeader")) is not None)
        look = _tbl_look(tblpr)
        cond_pri = est.bordes_condicionales(sid, "firstRow") if look["firstRow"] else {"tc": {}, "tbl": {}}
        cond_ult = est.bordes_condicionales(sid, "lastRow") if look["lastRow"] else {"tc": {}, "tbl": {}}
        lineas = _lineas_tabla(filas, bordes, cond_pri, cond_ult)
        vertical = (any(_borde_visible(bordes.get(k)) for k in ("left", "right", "start", "end", "insideV"))
                    or tcb > 0 or lineas["vertical_condicional"])
        cumple, incumplimientos = _veredicto_tres_lineas(lineas, vertical)
        tw = tblpr.find(q("tblW")) if tblpr is not None else None
        prev, sig = _vecino_rotulo(t, -1), _vecino_rotulo(t, +1)
        primera = [_texto_parrafo(tc).strip() for tc in filas[0].findall(q("tc"))] if filas else []
        salida.append({
            "n": i, "filas": len(filas), "columnas": ncol, "estilo": est.nombre(sid) if sid else None,
            "bordes": bordes, "bordes_verticales": vertical,
            "bordes_horizontales_sup_inf_interno": [_borde_visible(bordes.get(k)) for k in ("top", "bottom", "insideH")],
            "bordes_horizontales_sup_inf_interno_nota": "solo tblBorders (directo + estilo); el efectivo está en 'lineas_horizontales'",
            "tblLook": look,
            "formato_condicional": {"firstRow": cond_pri if look["firstRow"] else None,
                                    "lastRow": cond_ult if look["lastRow"] else None},
            "lineas_horizontales": lineas,
            "cumple_tres_lineas_apa7": cumple, "incumplimientos_tres_lineas": incumplimientos,
            "encabezado_repetido": encabezado_repetido,
            "anchos_cm": [_tw_cm(w) for w in grid],
            "ancho_tabla": ({"tipo": tw.get(q("type")), "valor": tw.get(q("w"))} if tw is not None else None),
            "celdas_con_bordes_verticales_propios": tcb,
            "primera_fila": primera[:8],
            "rotulo_antes": prev, "rotulo_despues": sig,
        })
    return salida


def _vecino_rotulo(elem, sentido: int) -> str | None:
    """Texto del rótulo (Tabla/Figura N) en los 2 párrafos no vacíos contiguos a `elem`."""
    actual, vistos = elem, 0
    while vistos < 2:
        actual = actual.getprevious() if sentido < 0 else actual.getnext()
        if actual is None:
            return None
        if actual.tag != q("p"):
            return None
        t = _texto_parrafo(actual).strip()
        if not t:
            continue
        vistos += 1
        if RE_ROTULO.match(t):
            return t[:120]
    return None


def _resumen_runs(p, est: Estilos, base: dict, limite: int = 4) -> list[dict]:
    out = []
    for r in p.findall(q("r")):
        t = "".join(x.text or "" for x in r.findall(q("t")))
        if not t.strip():
            continue
        props = _run_efectivo(r, est, base)
        out.append({"texto": t[:40], "negrita": bool(props.get("negrita")), "cursiva": bool(props.get("cursiva")),
                    "tam_pt": props.get("tam_pt"), "fuente": props.get("fuente")})
        if len(out) >= limite:
            break
    return out


def _run_efectivo(r, est: Estilos, base_r: dict) -> dict:
    """Propiedades efectivas de un run: base del párrafo -> estilo de carácter -> formato directo."""
    props = dict(base_r)
    rpr = r.find(q("rPr"))
    if rpr is not None:
        rs = rpr.find(q("rStyle"))
        if rs is not None:
            props.update({k: v for k, v in est.estilo(rs.get(q("val")))["r"].items() if k in _leer_rpr(est.por_id[rs.get(q("val"))].find(q("rPr")) if rs.get(q("val")) in est.por_id else None)})
        props.update(_leer_rpr(rpr))
    return est._aplicar_tema(props)


def _es_entrada_indice(est: Estilos, sid: str | None) -> bool:
    n = (est.nombre(sid) or "").lower()
    return bool(sid) and (n.startswith("toc") or n.startswith("table of") or "tabla de" in n or "índice" in n or n.startswith("ndice"))


def analizar_docx(ruta: str | Path) -> dict:
    """Desglose estructural completo de un .docx (solo lectura)."""
    import docx
    ruta = Path(ruta)
    doc = docx.Document(str(ruta))
    est, num = Estilos(doc), Numeracion(doc)
    cuerpo = doc.element.body
    avisos: list[str] = []

    # --- secciones ------------------------------------------------------------------
    secciones, acum = [], {"parrafos": 0, "caracteres": 0, "primer_encabezado": None}
    for hijo in cuerpo:
        if hijo.tag == q("p"):
            acum["parrafos"] += 1
            acum["caracteres"] += len(_texto_parrafo(hijo).strip())
            ppr = hijo.find(q("pPr"))
            if ppr is not None and ppr.find(q("sectPr")) is not None:
                secciones.append({**acum, **_sect(ppr.find(q("sectPr")))})
                acum = {"parrafos": 0, "caracteres": 0, "primer_encabezado": None}
    if cuerpo.find(q("sectPr")) is not None:
        secciones.append({**acum, **_sect(cuerpo.find(q("sectPr")))})
    for i, s in enumerate(secciones, 1):
        s["n"] = i
    predominante = max(secciones, key=lambda s: s["caracteres"])["n"] if secciones else None

    # --- recorrido de párrafos -------------------------------------------------------
    usos: Counter = Counter()
    fuente_peso: Counter = Counter()
    interl_peso: Counter = Counter()
    encabezados, rotulos, campos_cuerpo = [], [], Counter()
    entradas_indice = 0
    for idx, p in enumerate(cuerpo.iter(q("p"))):
        if _en_fallback(p):
            continue
        ppr = p.find(q("pPr"))
        ps = ppr.find(q("pStyle")) if ppr is not None else None
        sid = ps.get(q("val")) if ps is not None else est.parrafo_defecto
        base = est.estilo(sid)
        efectivo_p = {**base["p"], **_leer_ppr(ppr)}
        texto = _texto_parrafo(p).strip()
        dentro_tabla = _en_tabla(p)
        for c in _campos(p):
            campos_cuerpo[c.split()[0].upper()] += 1
        if texto:
            usos[sid] += 1
        if _es_entrada_indice(est, sid):
            entradas_indice += 1
            continue
        if not texto:
            continue
        # peso de fuente/tamaño/interlineado (cuerpo: párrafos de texto fuera de tablas)
        for r in p.findall(q("r")):
            t = "".join(x.text or "" for x in r.findall(q("t")))
            if t.strip():
                pr = _run_efectivo(r, est, base["r"])
                fuente_peso[(pr.get("fuente"), pr.get("tam_pt"))] += len(t)
        nombre = est.nombre(sid) or ""
        nivel = efectivo_p.get("nivel_esquema")
        m = re.match(r"^(?:heading|t[ií]tulo|titulo)\s*(\d)$", nombre.strip(), re.I)
        if m:
            nivel = int(m.group(1))
        # numeración automática
        numinfo = efectivo_p.get("num")
        numero_auto = None
        if numinfo and numinfo.get("numId") not in (None, "0"):
            ilvl = numinfo.get("ilvl")
            if ilvl is None:
                ilvl = num.nivel_de_estilo(numinfo["numId"], sid)
            numero_auto = num.siguiente(numinfo["numId"], ilvl)
        if nivel is not None and nivel <= 9 and not dentro_tabla:
            manual = re.match(r"^((?:\d+\.)+\d*|\d+(?=\s)|[IVXLC]+\.|CAP[ÍI]TULO\s+[IVXLC\d]+\.?)(?=\s)", texto, re.I)
            encabezados.append({
                "nivel": nivel, "texto": texto[:160], "estilo": nombre,
                "numeracion_automatica": numero_auto["numero"] if numero_auto else None,
                "numeracion_manual": manual.group(1) if manual else None,
                "alineacion": efectivo_p.get("alineacion"),
                "fuente": base["r"].get("fuente"), "tam_pt": base["r"].get("tam_pt"),
                "negrita": base["r"].get("negrita"), "cursiva": base["r"].get("cursiva"),
                "orden_parrafo": idx,
            })
        elif not dentro_tabla and "interlineado" in efectivo_p and len(texto) > 60:
            interl_peso[json.dumps(efectivo_p["interlineado"], sort_keys=True)] += len(texto)
        if RE_ROTULO.match(texto) or "caption" in nombre.lower() or "leyenda" in nombre.lower():
            rotulos.append({
                "texto": texto[:120], "estilo": nombre, "alineacion": efectivo_p.get("alineacion"),
                "campo_SEQ": any(c.upper().startswith("SEQ") for c in _campos(p)),
                "formato_runs": _resumen_runs(p, est, base["r"]), "orden_parrafo": idx,
            })

    # --- estilos usados ----------------------------------------------------------------
    estilos_usados = []
    for sid, n in usos.most_common():
        e = est.estilo(sid)
        estilos_usados.append({
            "id": sid, "nombre": est.nombre(sid), "usos": n,
            "basado_en": next((b.get(q("val")) for s in [est.por_id.get(sid)] if s is not None
                               for b in [s.find(q("basedOn"))] if b is not None), None),
            "fuente": e["r"].get("fuente"), "tam_pt": e["r"].get("tam_pt"),
            "negrita": e["r"].get("negrita"), "cursiva": e["r"].get("cursiva"),
            "interlineado": e["p"].get("interlineado"), "antes_pt": e["p"].get("antes_pt"),
            "despues_pt": e["p"].get("despues_pt"), "sangria": e["p"].get("sangria"),
            "alineacion": e["p"].get("alineacion"), "nivel_esquema": e["p"].get("nivel_esquema"),
        })

    # --- cabeceras y pies -----------------------------------------------------------------
    cab_pies, vistos = [], set()
    for s in secciones:
        for ref in s["referencias_cabecera_pie"]:
            if not ref["rId"] or ref["rId"] in vistos:
                continue
            vistos.add(ref["rId"])
            try:
                parte = doc.part.related_parts[ref["rId"]]
                el = parte.element
                alin = [_leer_ppr(p.find(q("pPr"))).get("alineacion") for p in el.iter(q("p"))]
                cab_pies.append({**ref, "seccion": s["n"], "parte": str(parte.partname),
                                 "texto": " | ".join(t for t in (_texto_parrafo(p).strip() for p in el.iter(q("p"))) if t)[:200],
                                 "campos": _campos(el), "alineaciones": [a for a in alin if a],
                                 **_contar_graficos(el)})
            except Exception as e:  # noqa: BLE001
                cab_pies.append({**ref, "seccion": s["n"], "aviso": f"[VERIFICAR: {type(e).__name__}]"})

    # --- comentarios / cambios ------------------------------------------------------------
    n_coment = 0
    for parte in doc.part.package.iter_parts():
        if str(parte.partname).endswith("/comments.xml"):
            from lxml import etree
            n_coment = len(etree.fromstring(parte.blob).findall(q("comment")))
    cambios = {"insertados": len(list(cuerpo.iter(q("ins")))), "eliminados": len(list(cuerpo.iter(q("del"))))}

    imgs = _imagenes(doc)
    graficos = _contar_graficos(cuerpo)
    tablas = _tablas(doc, est)
    evaluables = [t for t in tablas if t["cumple_tres_lineas_apa7"] is not None]
    resumen_tablas = {"total": len(tablas), "evaluables": len(evaluables),
                      "cumplen_tres_lineas_apa7": sum(1 for t in evaluables if t["cumple_tres_lineas_apa7"]),
                      "incumplen": [t["n"] for t in evaluables if not t["cumple_tres_lineas_apa7"]]}
    if resumen_tablas["incumplen"]:
        avisos.append(f"Tablas que no cumplen el formato APA 7 de tres líneas (regla 03): {resumen_tablas['incumplen']}.")
    bajas = [i for i in imgs if i["dpi_efectivo"] is not None and i["dpi_efectivo"] < 300]
    if bajas:
        avisos.append(f"{len(bajas)} de {len(imgs)} imágenes con DPI efectivo < 300 (criterio de la regla 03).")
    if entradas_indice:
        avisos.append(f"{entradas_indice} párrafos son entradas de índice/tabla de contenido/figuras y se excluyen del inventario de rótulos.")

    fuente_dom = fuente_peso.most_common(1)[0][0] if fuente_peso else (None, None)
    interl_dom = json.loads(interl_peso.most_common(1)[0][0]) if interl_peso else None
    sec_pred = next((s for s in secciones if s["n"] == predominante), None)
    perfil = {
        "pagina_cm": sec_pred["pagina_cm"] if sec_pred else None,
        "orientacion": sec_pred["orientacion"] if sec_pred else None,
        "margenes_cm": {k: sec_pred["margenes_cm"][k] for k in ("izq", "der", "sup", "inf")} if sec_pred and sec_pred["margenes_cm"] else None,
        "fuente_cuerpo": fuente_dom[0], "tam_cuerpo_pt": fuente_dom[1],
        "interlineado_cuerpo": interl_dom or est.estilo(est.parrafo_defecto)["p"].get("interlineado"),
        "formatos_numeracion_pagina": sorted({(s["pgNumType"] or {}).get("formato", "decimal (hereda/por defecto)") for s in secciones}),
        "seccion_predominante": predominante, "n_secciones": len(secciones),
        "encabezados_nivel1": [e["texto"] for e in encabezados if e["nivel"] == 1],
        "n_encabezados": len(encabezados), "precision": "exacto (XML de Word)",
    }
    return {
        "tipo": "docx",
        "fuente": {"archivo": str(ruta), "sha256": seguridad.sha256_archivo(ruta), "bytes": ruta.stat().st_size},
        "perfil": perfil, "secciones": secciones, "estilos_usados": estilos_usados,
        "encabezados": encabezados, "tablas": tablas, "resumen_tablas": resumen_tablas,
        "imagenes": imgs, "graficos_cuerpo": graficos,
        "cabeceras_pies": cab_pies, "rotulos": rotulos,
        "campos_cuerpo": dict(campos_cuerpo), "comentarios": n_coment, "cambios_registrados": cambios,
        "estilos_definidos": len(est.por_id), "avisos": avisos,
    }


# ======================================================================================
# PDF - análisis
# ======================================================================================

_RE_CAP = re.compile(r"^(?:(\d+)\.\s*)?CAP[ÍI]TULO\s+([IVXLC]+|\d+)\b\s*[:\-–.]?\s*(.*)$", re.I)
_RE_NUM = re.compile(r"^(\d{1,2}(?:\.\d{1,2})*)(?:\.\s*|\s+)(\S.*)$")  # admite "3.1.Bases" (sin espacio tras el punto)
_RE_ROM = re.compile(r"^([IVX]{1,5})\.\s+(\S.*)$")
_RE_LIDER = re.compile(r"^(.+?)\s*(?:\.\s?){3,}\s*(\d{1,4}|[ivxlcIVXLC]{1,7})\s*$")
_RE_PROD = re.compile(r"^\s*(Tabla|Figura|Cuadro|Table|Figure|Fuente|Nota|Elaboraci[óo]n)\b", re.I)


def _es_negrita(span: dict) -> bool:
    return bool(span["flags"] & 16) or "bold" in span["font"].lower()


def _num_visible(t: dict) -> str:
    """Número del título solo si el texto no lo repite ya."""
    n = t.get("numero")
    if not n:
        return ""
    txt, num = tx.canonico(t["texto"]), tx.canonico(str(n))
    # el número ya figura si el texto lo contiene (p. ej. "2. CAPITULO II: ..." contiene "capitulo ii")
    return "" if txt.startswith(num) or num in txt[:40] else f"{n} "


def _tipo_etiqueta(et: str | None) -> str | None:
    if et is None:
        return None
    return "arabigo" if et.isdigit() else "romano" if re.fullmatch(r"[ivxlcIVXLC]+", et) else "otro"


def _posicion(bbox, ancho: float, alto: float) -> str:
    vert = "superior" if bbox[1] < alto / 2 else "inferior"
    cx = (bbox[0] + bbox[2]) / 2
    horiz = "izquierda" if cx < ancho / 3 else "derecha" if cx > 2 * ancho / 3 else "centro"
    return f"{vert}-{horiz}"


def _recoger_lineas(doc) -> list[dict]:
    """Líneas de cada página con tamaño, fuente y negrita (una sola pasada por PyMuPDF)."""
    paginas = []
    for pag in doc:
        info = {"indice": pag.number + 1, "ancho": pag.rect.width, "alto": pag.rect.height, "bloques": []}
        for b in pag.get_text("dict", sort=True)["blocks"]:
            if b.get("type") != 0:
                continue
            lineas = []
            for ln in b["lines"]:
                sp = [s for s in ln["spans"] if s["text"].strip()]
                if not sp:
                    continue
                pesos = Counter()
                for s in sp:
                    pesos[(s["font"], round(s["size"], 1))] += len(s["text"])
                (fuente, tam), _ = pesos.most_common(1)[0]
                lineas.append({"texto": "".join(s["text"] for s in ln["spans"]).strip(), "bbox": list(ln["bbox"]),
                               "fuente": fuente, "tam": tam, "negrita": all(_es_negrita(s) for s in sp),
                               "cursiva": all(bool(s["flags"] & 2) or "italic" in s["font"].lower() for s in sp)})
            if lineas:
                info["bloques"].append({"bbox": list(b["bbox"]), "lineas": lineas})
        paginas.append(info)
    return paginas


def _clasificar_titulo(texto: str, tam: float, negrita: bool, centrada: bool, tam_cuerpo: float) -> dict | None:
    """Criterio EXPLÍCITO de título (ver `CRITERIO_TITULOS`). Devuelve {nivel, numero, texto, criterio} o None."""
    t = re.sub(r"\s+", " ", texto).strip()
    if len(t) < 3 or len(t) > 140 or _RE_PROD.match(t):
        return None
    m = _RE_CAP.match(t)
    if m and (negrita or tam >= tam_cuerpo + 1 or t.isupper()):
        rot = f"CAPÍTULO {m.group(2).upper()}" + (f" {m.group(1)}" if False else "")
        return {"nivel": 1, "numero": rot, "texto": t, "criterio": "patron CAPÍTULO"}
    m = _RE_NUM.match(t)
    if m and (negrita or tam >= tam_cuerpo + 1):
        prof = m.group(1).count(".") + 1
        resto = m.group(2)
        if prof == 1 and not (resto.isupper() or len(resto.split()) <= 6):
            return None
        if not re.match(r"^[A-ZÁÉÍÓÚÑa-záéíóúñ(“\"]", resto) or re.fullmatch(r"[\d.,\s%]+", resto):
            return None
        return {"nivel": prof, "numero": m.group(1), "texto": t, "criterio": "numeración decimal + negrita/tamaño"}
    m = _RE_ROM.match(t)
    if m and (negrita or tam >= tam_cuerpo + 1):
        return {"nivel": 1, "numero": m.group(1), "texto": t, "criterio": "numeración romana + negrita/tamaño"}
    letras = re.sub(r"[^A-Za-zÁÉÍÓÚÑáéíóúñ]", "", t)
    if (negrita or tam >= tam_cuerpo + 1.5) and len(letras) >= 4 and not t.endswith((":", ",", ";")):
        if t.isupper():
            return {"nivel": 1 if centrada else 2, "numero": None, "texto": t,
                    "criterio": "mayúsculas sostenidas + negrita/tamaño"}
        if tam >= tam_cuerpo + 1.5 and len(t.split()) <= 12:
            return {"nivel": 1 if centrada else 2, "numero": None, "texto": t, "criterio": "tamaño ≥ cuerpo+1.5 pt"}
    return None


CRITERIO_TITULOS = (
    "Título = bloque de hasta 3 líneas, ≤140 caracteres, fuera de las franjas de 40 pt de cabecera/pie, "
    "que (a) empiece por 'CAPÍTULO n', numeración decimal (1.2.3.) o romana (I.) y esté en negrita o con "
    "tamaño ≥ cuerpo+1 pt, o (b) sin numeración, en negrita o con tamaño ≥ cuerpo+1.5 pt, en MAYÚSCULAS "
    "(≥4 letras). Nivel = profundidad de la numeración; sin numeración: 1 si está centrado, 2 si no. "
    "Se descartan rótulos (Tabla/Figura/Fuente/Nota) y páginas con >8 candidatos (p. ej. tablas con "
    "encabezados en negrita). Es una inferencia tipográfica, no el índice oficial."
)


def _indice_impreso(paginas_lineas: list[dict]) -> list[dict]:
    """Entradas 'Título ........ 12' de las páginas de índice (puntos guía); páginas con ≥5 entradas."""
    out = []
    for pg in paginas_lineas:
        entradas = []
        for b in pg["bloques"]:
            for ln in b["lineas"]:
                m = _RE_LIDER.match(ln["texto"])
                if m:
                    entradas.append({"titulo": m.group(1).strip(" ."), "pagina_impresa": m.group(2),
                                     "pagina_fisica_indice": pg["indice"]})
        if len(entradas) >= 5:
            out.extend(entradas)
    return out


def _en_cache_compartida(ruta: Path) -> bool:
    """True si el PDF pertenece a las carpetas cuyo índice se comparte en el vault (fuentes y tesis modelo)."""
    r = ruta.resolve(strict=False)
    for base in (rutas.PDFS_FUENTES, rutas.MODELOS_TESIS):
        try:
            r.relative_to(base.resolve(strict=False))
            return True
        except ValueError:
            continue
    return False


def analizar_pdf(ruta: str | Path, carpeta_indices: Path | None = None, incluir_bloques: bool = False,
                 usar_cache: bool | None = None) -> dict:
    """Desglose de un PDF reutilizando ingesta_pdf para etiquetas, imágenes y dibujos.

    Caché de índices: `usar_cache=None` (auto) la usa solo si se indica `carpeta_indices` o si el PDF está en
    PDFS_FUENTES / referencias/modelos_tesis; en otro caso el índice se construye en memoria y no se escribe
    nada. `usar_cache=False` fuerza memoria; `True` fuerza caché (en `carpeta_indices` o en el vault).
    """
    import pymupdf
    from scripts.fuentes import ingesta_pdf
    ruta = Path(ruta)
    if usar_cache is None:
        usar_cache = carpeta_indices is not None or _en_cache_compartida(ruta)
    try:
        idx = ingesta_pdf.cargar_indice(ruta, carpeta_indices) if usar_cache else ingesta_pdf.ingestar(ruta)
        doc = pymupdf.open(str(ruta))
    except pymupdf.FileDataError as e:
        raise ArchivoNoLegible(f"PDF corrupto o no es un PDF válido: {ruta.name}") from e
    except RuntimeError as e:
        if "cifrado" in str(e).lower() or "encrypt" in str(e).lower():
            raise ArchivoNoLegible(f"PDF cifrado (protegido con contraseña), no se puede analizar: {ruta.name}") from e
        raise ArchivoNoLegible(f"No se pudo abrir el PDF {ruta.name}: {e}") from e
    try:
        toc = [{"nivel": n, "titulo": t, "pagina_fisica": p} for n, t, p in doc.get_toc()]
        meta = {k: v for k, v in (doc.metadata or {}).items() if v}
        pags = _recoger_lineas(doc)
    finally:
        doc.close()
    por_indice = {p["indice"]: p for p in idx["paginas"]}

    peso: Counter = Counter()
    for pg in pags:
        for b in pg["bloques"]:
            for ln in b["lineas"]:
                peso[(ln["fuente"], ln["tam"])] += len(ln["texto"])
    (fuente_cuerpo, tam_cuerpo), _ = peso.most_common(1)[0] if peso else ((None, 0.0), 0)
    tam_cuerpo = float(tam_cuerpo or 0)

    paginas_res, titulos, izq, der, sup, inf, pasos, pos_num = [], [], [], [], [], [], [], Counter()
    for pg in pags:
        meta_i = por_indice.get(pg["indice"], {})
        etiqueta = meta_i.get("etiqueta_impresa")
        pesos_pg: Counter = Counter()
        cand = []
        xs0, xs1, ys0, ys1 = [], [], [], []
        for b in pg["bloques"]:
            for ln in b["lineas"]:
                pesos_pg[(ln["fuente"], ln["tam"])] += len(ln["texto"])
                x0, y0, x1, y1 = ln["bbox"]
                if len(ln["texto"]) >= 20 and 40 < y0 and y1 < pg["alto"] - 40:
                    xs0.append(x0), xs1.append(x1), ys0.append(y0), ys1.append(y1)
                if etiqueta and ln["texto"].strip() == str(etiqueta) and (y0 < 60 or y1 > pg["alto"] - 60):
                    pos_num[_posicion(ln["bbox"], pg["ancho"], pg["alto"])] += 1
            if len(b["lineas"]) <= 3 and b["bbox"][1] > 40 and b["bbox"][3] < pg["alto"] - 40:
                todas_neg = all(l["negrita"] for l in b["lineas"])
                tam_b = max(l["tam"] for l in b["lineas"])
                if todas_neg or tam_b >= tam_cuerpo + 1:
                    texto = " ".join(l["texto"] for l in b["lineas"])
                    centro = (b["bbox"][0] + b["bbox"][2]) / 2
                    r = _clasificar_titulo(texto, tam_b, todas_neg, abs(centro - pg["ancho"] / 2) < 45, tam_cuerpo)
                    if r:
                        cand.append({**r, "pagina_fisica": pg["indice"], "etiqueta_impresa": etiqueta,
                                     "tam_pt": tam_b, "negrita": todas_neg})
        # paso de línea: líneas consecutivas de la página con el tamaño del cuerpo y misma fuente
        lin_cuerpo = sorted((l for b in pg["bloques"] for l in b["lineas"]
                             if abs(l["tam"] - tam_cuerpo) < 0.2 and len(l["texto"]) >= 25 and 60 < l["bbox"][1] < pg["alto"] - 60),
                            key=lambda l: l["bbox"][1])
        for l1, l2 in zip(lin_cuerpo, lin_cuerpo[1:]):
            dy = l2["bbox"][1] - l1["bbox"][1]
            if 0.9 * tam_cuerpo <= dy <= 2.6 * tam_cuerpo:
                pasos.append(round(dy * 2) / 2)
        if len(cand) <= 8:
            titulos.extend(cand)
        if xs0:
            izq.append(min(xs0)), der.append(pg["ancho"] - max(xs1)), sup.append(min(ys0)), inf.append(pg["alto"] - max(ys1))
        dom = pesos_pg.most_common(1)[0][0] if pesos_pg else (None, None)
        reg = {"pagina_fisica": pg["indice"], "etiqueta_impresa": etiqueta,
               "metodo_etiqueta": meta_i.get("metodo_etiqueta"),
               "etiqueta_estado": None if etiqueta else "[VERIFICAR: etiqueta impresa no determinada]",
               "sin_capa_texto": bool(meta_i.get("sin_capa_texto")),
               "fuente_dominante": dom[0], "tam_dominante": dom[1], "n_bloques": len(pg["bloques"]),
               "n_imagenes": meta_i.get("n_imagenes"), "n_dibujos": meta_i.get("n_dibujos"),
               "titulos": [t["texto"] for t in titulos if t["pagina_fisica"] == pg["indice"]]}
        if incluir_bloques:
            reg["bloques"] = [{"bbox": [round(v, 1) for v in b["bbox"]], "n_lineas": len(b["lineas"]),
                               "tam": b["lineas"][0]["tam"], "fuente": b["lineas"][0]["fuente"],
                               "negrita": all(l["negrita"] for l in b["lineas"]),
                               "texto": " ".join(l["texto"] for l in b["lineas"])[:80]} for b in pg["bloques"]]
        paginas_res.append(reg)

    med = lambda v: round(statistics.median(v) / 72 * 2.54, 2) if v else None  # noqa: E731
    p10 = lambda v: round(sorted(v)[max(0, int(len(v) * 0.10) - (0 if len(v) < 10 else 0))] / 72 * 2.54, 2) if v else None  # noqa: E731
    tipos = Counter(_tipo_etiqueta(p["etiqueta_impresa"]) for p in paginas_res)
    rangos = {}
    for tipo in ("romano", "arabigo"):
        fis = [p["pagina_fisica"] for p in paginas_res if _tipo_etiqueta(p["etiqueta_impresa"]) == tipo]
        rangos[tipo] = {"paginas": len(fis), "fisicas": [min(fis), max(fis)] if fis else None}
    titulos = _fusionar_rotulos_capitulo(titulos)
    primera_arabiga = rangos["arabigo"]["fisicas"][0] if rangos["arabigo"]["fisicas"] else None
    for t in titulos:
        t["zona"] = "cuerpo" if primera_arabiga and t["pagina_fisica"] >= primera_arabiga else "preliminar"
    paso = Counter(pasos).most_common(1)[0][0] if pasos else None
    dist_pasos = [{"paso_pt": k, "lineas": n} for k, n in Counter(pasos).most_common(3)]
    sin_texto = [p["pagina_fisica"] for p in paginas_res if p["sin_capa_texto"]]
    ocr = tesseract_disponible()
    avisos = []
    if sin_texto:
        avisos.append(f"{len(sin_texto)} páginas sin capa de texto (requiere OCR; "
                      f"Tesseract {'disponible en ' + ocr if ocr else 'NO instalado'}): "
                      f"{_compactar_rangos(sin_texto)}. Su estructura no está incluida.")
    ind_imp = _indice_impreso(pags)
    if ind_imp:
        from rapidfuzz import fuzz
        canon = [tx.canonico(t["texto"]) for t in titulos]
        for e in ind_imp:
            c = tx.canonico(e["titulo"])
            e["coincide_con_titulo_detectado"] = any(fuzz.ratio(c, x) >= 88 for x in canon)
    perfil = {
        "pagina_cm": [round(pags[0]["ancho"] / 72 * 2.54, 2), round(pags[0]["alto"] / 72 * 2.54, 2)] if pags else None,
        "orientacion": "horizontal" if pags and pags[0]["ancho"] > pags[0]["alto"] else "vertical",
        "margenes_cm": {"izq": p10(izq), "der": p10(der), "sup": p10(sup), "inf": p10(inf)},
        "margenes_criterio": "percentil 10 de la distancia texto-borde por página (páginas llenas; evita páginas cortas)",
        "fuente_cuerpo": fuente_cuerpo, "tam_cuerpo_pt": tam_cuerpo or None,
        "interlineado_paso_pt": paso, "interlineado_pasos_frecuentes": dist_pasos,
        "interlineado_relativo_al_tamano": round(paso / tam_cuerpo, 2) if paso and tam_cuerpo else None,
        "interlineado_equivalente": (round(paso / (ALTURA_LINEA_NATURAL * tam_cuerpo), 1) if paso and tam_cuerpo else None),
        "formatos_numeracion_pagina": [k for k in ("romano", "arabigo") if rangos[k]["paginas"]],
        "posicion_numero_pagina": pos_num.most_common(1)[0][0] if pos_num else None,
        "encabezados_nivel1": [t["texto"] for t in titulos if t["nivel"] == 1],
        "n_encabezados": len(titulos),
        "precision": "estimado (geometría del texto)",
    }
    return {
        "tipo": "pdf",
        "fuente": {"archivo": str(ruta), "sha256": idx["fuente"]["sha256"], "n_paginas": idx["fuente"]["n_paginas"]},
        "metadatos_pdf": meta, "perfil": perfil, "toc_embebido": toc,
        "indice_impreso": ind_imp, "estructura_inferida": titulos, "criterio_titulos": CRITERIO_TITULOS,
        "numeracion": {"tipos": {str(k): v for k, v in tipos.items()}, "rangos": rangos,
                       "posicion_numero_pagina": perfil["posicion_numero_pagina"],
                       "paginas_sin_etiqueta": tipos.get(None, 0)},
        "calidad": idx.get("calidad"), "ocr": {"tesseract": ocr, "paginas_requieren_ocr": sin_texto},
        "paginas": paginas_res, "avisos": avisos,
    }


def _fusionar_rotulos_capitulo(titulos: list[dict]) -> list[dict]:
    """Une 'CAPÍTULO II' (línea sola) con el título del capítulo que sigue en la misma página."""
    salida, i = [], 0
    while i < len(titulos):
        t = titulos[i]
        m = _RE_CAP.match(t["texto"])
        sig = titulos[i + 1] if i + 1 < len(titulos) else None
        if (t["criterio"] == "patron CAPÍTULO" and m and not m.group(3).strip() and sig
                and sig["pagina_fisica"] == t["pagina_fisica"] and sig["nivel"] == 1 and sig["numero"] is None):
            salida.append({**t, "texto": f"{t['texto']} {sig['texto']}".strip(), "criterio": "patron CAPÍTULO + título contiguo"})
            i += 2
            continue
        salida.append(t)
        i += 1
    return salida


def _compactar_rangos(nums: list[int]) -> str:
    if not nums:
        return ""
    nums, out, ini, ant = sorted(nums), [], None, None
    for n in nums:
        if ini is None:
            ini = ant = n
        elif n == ant + 1:
            ant = n
        else:
            out.append(f"{ini}-{ant}" if ant > ini else str(ini))
            ini = ant = n
    out.append(f"{ini}-{ant}" if ant > ini else str(ini))
    return ", ".join(out)


# ======================================================================================
# XLSX - análisis
# ======================================================================================

def analizar_xlsx(ruta: str | Path, max_celdas: int = 300) -> dict:
    """Hojas, rango usado, fórmulas (sin data_only) y valores en caché (con data_only)."""
    import openpyxl
    ruta = Path(ruta)
    wf = openpyxl.load_workbook(str(ruta), data_only=False)
    wv = openpyxl.load_workbook(str(ruta), data_only=True)
    hojas, avisos = [], []
    for ws in wf.worksheets:
        wsv = wv[ws.title]
        formulas, valores, n_formulas, n_valores, sin_cache = [], [], 0, 0, 0
        for fila in ws.iter_rows():
            for c in fila:
                if c.value is None:
                    continue
                es_f = isinstance(c.value, str) and c.value.startswith("=") or type(c.value).__name__ == "ArrayFormula"
                if es_f:
                    n_formulas += 1
                    cache = wsv[c.coordinate].value
                    sin_cache += cache is None
                    if len(formulas) < max_celdas:
                        formulas.append({"celda": c.coordinate,
                                         "formula": c.value if isinstance(c.value, str) else getattr(c.value, "text", str(c.value)),
                                         "valor_en_cache": cache})
                else:
                    n_valores += 1
                    if len(valores) < max_celdas:
                        valores.append({"celda": c.coordinate, "valor": c.value if isinstance(c.value, (int, float, bool)) else str(c.value)})
        hojas.append({"nombre": ws.title, "estado": ws.sheet_state, "rango_usado": ws.dimensions,
                      "filas": ws.max_row, "columnas": ws.max_column,
                      "celdas_combinadas": [str(r) for r in ws.merged_cells.ranges][:50],
                      "n_formulas": n_formulas, "n_valores": n_valores, "formulas_sin_valor_en_cache": sin_cache,
                      "formulas": formulas, "valores": valores,
                      "truncado": n_formulas > max_celdas or n_valores > max_celdas})
        if sin_cache:
            avisos.append(f"Hoja '{ws.title}': {sin_cache} fórmulas sin valor en caché (libro no recalculado/guardado por Excel).")
    return {"tipo": "xlsx", "fuente": {"archivo": str(ruta), "sha256": seguridad.sha256_archivo(ruta)},
            "hojas": hojas, "nombres_definidos": list(wf.defined_names.keys()) if hasattr(wf.defined_names, "keys") else [],
            "avisos": avisos}


# ======================================================================================
# Despacho, Markdown y comparación
# ======================================================================================

def analizar(ruta: str | Path, **kw) -> dict:
    """Despacha por extensión. Lanza FileNotFoundError, FormatoNoSoportado o ArchivoNoLegible (corrupto/cifrado)."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(f"No existe: {ruta}")
    ext = ruta.suffix.lower()
    if ext not in (".docx", ".pdf", ".xlsx", ".xlsm"):
        raise FormatoNoSoportado(f"Formato no soportado: {ext or '(sin extensión)'} (use .docx, .pdf o .xlsx)")
    if ext == ".pdf":
        return analizar_pdf(ruta, kw.get("carpeta_indices"), kw.get("incluir_bloques", False), kw.get("usar_cache"))
    try:
        return analizar_docx(ruta) if ext == ".docx" else analizar_xlsx(ruta)
    except (zipfile.BadZipFile, KeyError, OSError, ValueError, AttributeError) as e:
        raise ArchivoNoLegible(f"{ext[1:].upper()} corrupto o no es un {ext[1:].upper()} válido: {ruta.name} ({type(e).__name__})") from e
    except Exception as e:  # noqa: BLE001  (PackageNotFoundError, InvalidFileException, XMLSyntaxError...)
        if type(e).__name__ in ("PackageNotFoundError", "InvalidFileException", "XMLSyntaxError"):
            raise ArchivoNoLegible(f"{ext[1:].upper()} corrupto o no es un {ext[1:].upper()} válido: {ruta.name} ({type(e).__name__})") from e
        raise


def _v(x) -> str:
    return "—" if x is None or x == "" else str(x).replace("|", "\\|")


def _tabla_md(cab: list[str], filas: list[list]) -> list[str]:
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(_v(c) for c in f) + " |" for f in filas]
    return out


def _interl_txt(i) -> str:
    if not i:
        return "—"
    return f"{i['valor']}×" if i.get("regla") == "multiple" else f"{i['valor']} pt ({i['regla']})"


def _perfil_md(p: dict) -> list[str]:
    m = p.get("margenes_cm") or {}
    filas = [["Página (cm)", p.get("pagina_cm")], ["Orientación", p.get("orientacion")],
             ["Márgenes izq/der/sup/inf (cm)", f"{_v(m.get('izq'))} / {_v(m.get('der'))} / {_v(m.get('sup'))} / {_v(m.get('inf'))}"],
             ["Fuente del cuerpo", p.get("fuente_cuerpo")], ["Tamaño del cuerpo (pt)", p.get("tam_cuerpo_pt")]]
    if "interlineado_cuerpo" in p:
        filas.append(["Interlineado del cuerpo", _interl_txt(p["interlineado_cuerpo"])])
    if "interlineado_paso_pt" in p:
        filas.append(["Paso de línea (pt) / relativo al tamaño", f"{_v(p['interlineado_paso_pt'])} pt / {_v(p['interlineado_relativo_al_tamano'])} (≈ {_v(p.get('interlineado_equivalente'))}× interlineado natural)"])
    filas += [["Numeración de páginas", ", ".join(p.get("formatos_numeracion_pagina") or []) or "—"],
              ["Encabezados detectados", p.get("n_encabezados")], ["Precisión", p.get("precision")]]
    return _tabla_md(["Aspecto", "Valor"], filas)


def a_markdown(res: dict) -> str:
    L = [f"# Desglose estructural ({res['tipo']}): {Path(res['fuente']['archivo']).name}", "",
         f"- Archivo: `{res['fuente']['archivo']}`", f"- SHA-256: `{res['fuente']['sha256']}`", ""]
    if res["tipo"] == "docx":
        L += ["## Perfil de formato comparable", ""] + _perfil_md(res["perfil"])
        L += ["", "## Secciones", ""] + _tabla_md(
            ["N", "Páginas (cm)", "Orient.", "Márgenes izq/der/sup/inf", "pgNumType", "Portada distinta", "Párrafos", "Caracteres"],
            [[s["n"], s["pagina_cm"], s["orientacion"],
              "/".join(_v((s["margenes_cm"] or {}).get(k)) for k in ("izq", "der", "sup", "inf")),
              (s["pgNumType"] and f"{s['pgNumType']['formato']} inicio={_v(s['pgNumType']['inicio'])}") or "hereda",
              s["portada_distinta (titlePg)"], s["parrafos"], s["caracteres"]] for s in res["secciones"]])
        L += ["", "## Estilos usados (propiedades resueltas)", ""] + _tabla_md(
            ["Estilo", "Usos", "Fuente", "Tam", "B", "I", "Interlineado", "Sangría (cm)", "Alineación"],
            [[e["nombre"], e["usos"], e["fuente"], e["tam_pt"], e["negrita"], e["cursiva"],
              _interl_txt(e["interlineado"]), e["sangria"], e["alineacion"]] for e in res["estilos_usados"]])
        L += ["", "## Jerarquía de encabezados", ""]
        for e in res["encabezados"]:
            num = e["numeracion_automatica"] or ""  # la manual ya forma parte del texto
            L.append(f"{'  ' * (e['nivel'] - 1)}- [N{e['nivel']}] {num + ' ' if num else ''}{e['texto']}  _({e['estilo']}; {_v(e['fuente'])} {_v(e['tam_pt'])} pt)_")
        if not res["encabezados"]:
            L.append("_Sin párrafos con estilo de encabezado ni nivel de esquema._")
        rt = res.get("resumen_tablas") or {}
        L += ["", f"## Tablas ({len(res['tablas'])})", "",
              f"Formato APA 7 de tres líneas: {_v(rt.get('cumplen_tres_lineas_apa7'))} de {_v(rt.get('evaluables'))} tablas evaluables "
              "cumplen (se integran el formato condicional del estilo, tblLook y los bordes de celda).", ""]
        L += _tabla_md(
            ["N", "Filas×Col", "Estilo", "Verticales", "Sup / bajo enc. / inf / interiores", "Tres líneas APA 7", "Enc. repetido", "Anchos (cm)", "Rótulo"],
            [[t["n"], f"{t['filas']}×{t['columnas']}", t["estilo"], t["bordes_verticales"],
              " / ".join(str(t["lineas_horizontales"][k]) for k in ("superior", "bajo_encabezado", "inferior", "interiores")),
              _v(t["cumple_tres_lineas_apa7"]) + ("" if t["cumple_tres_lineas_apa7"] in (True, None) else " — " + "; ".join(t["incumplimientos_tres_lineas"])),
              t["encabezado_repetido"], t["anchos_cm"], t["rotulo_antes"] or t["rotulo_despues"]] for t in res["tablas"]])
        g = res.get("graficos_cuerpo") or {}
        L += ["", f"## Imágenes ({len(res['imagenes'])})", "",
              f"Formas o cuadros de texto sin mapa de bits: {_v(g.get('formas'))}; alternativas VML omitidas por duplicar un gráfico: {_v(g.get('vml_fallback_omitidos'))}.", ""] + _tabla_md(
            ["Nombre", "Formato", "px", "Tamaño (cm)", "DPI efectivo", "DPI metadatos"],
            [[i["nombre"], i["formato"], i["px"], f"{_v(i['ancho_cm'])}×{_v(i['alto_cm'])}", i["dpi_efectivo"], i["dpi_metadatos"]] for i in res["imagenes"]])
        L += ["", "## Cabeceras y pies", ""] + _tabla_md(
            ["Sec.", "Elemento", "Tipo", "Texto", "Campos", "Alineación", "Imágenes", "Formas"],
            [[c["seccion"], c["elemento"], c["tipo"], c.get("texto"), c.get("campos"), c.get("alineaciones"),
              c.get("imagenes"), c.get("formas")] for c in res["cabeceras_pies"]])
        L += ["", f"## Rótulos de tablas y figuras ({len(res['rotulos'])})", ""] + _tabla_md(
            ["Texto", "Estilo", "Alineación", "SEQ", "Runs (negrita/cursiva)"],
            [[r["texto"], r["estilo"], r["alineacion"], r["campo_SEQ"],
              "; ".join(f"{x['texto'][:18]}:{'B' if x['negrita'] else ''}{'I' if x['cursiva'] else ''}" for x in r["formato_runs"])] for r in res["rotulos"]])
        L += ["", f"Campos en el cuerpo: {_v(res['campos_cuerpo'])}. Comentarios: {res['comentarios']}. Cambios: {res['cambios_registrados']}."]
    elif res["tipo"] == "pdf":
        L += ["## Perfil de formato comparable", ""] + _perfil_md(res["perfil"])
        L += ["", f"## Numeración de páginas", "", f"- Tipos: {res['numeracion']['tipos']}", f"- Rangos: {res['numeracion']['rangos']}",
              f"- Posición típica: {_v(res['numeracion']['posicion_numero_pagina'])}", ""]
        L += [f"## TOC embebido ({len(res['toc_embebido'])} entradas)", ""]
        L += [f"{'  ' * (e['nivel'] - 1)}- {e['titulo']} (p. física {e['pagina_fisica']})" for e in res["toc_embebido"]] or ["_El PDF no trae marcadores (get_toc vacío)._"]
        L += ["", f"## Índice impreso detectado ({len(res['indice_impreso'])} entradas)", ""]
        L += [f"- {e['titulo']} ..... {e['pagina_impresa']}" for e in res["indice_impreso"][:120]] or ["_No se detectaron líneas con puntos guía._"]
        L += ["", f"## Estructura inferida ({len(res['estructura_inferida'])} títulos)", "", f"_Criterio: {res['criterio_titulos']}_", ""]
        for t in res["estructura_inferida"]:
            L.append(f"{'  ' * (t['nivel'] - 1)}- [N{t['nivel']}] {_num_visible(t)}{t['texto']} — p. física {t['pagina_fisica']}, "
                     f"impresa {_v(t['etiqueta_impresa'])} ({t['zona']}; {t['tam_pt']} pt)")
    else:
        for h in res["hojas"]:
            L += [f"## Hoja '{h['nombre']}' ({h['estado']}) rango {h['rango_usado']}", "",
                  f"- Fórmulas: {h['n_formulas']} (sin valor en caché: {h['formulas_sin_valor_en_cache']}); valores: {h['n_valores']}; combinadas: {h['celdas_combinadas']}", ""]
            L += _tabla_md(["Celda", "Fórmula", "Valor en caché"], [[f["celda"], f["formula"], f["valor_en_cache"]] for f in h["formulas"][:60]])
            L += [""] + _tabla_md(["Celda", "Valor"], [[v["celda"], v["valor"]] for v in h["valores"][:60]]) + [""]
    if res.get("avisos"):
        L += ["", "## Avisos", ""] + [f"- {a}" for a in res["avisos"]]
    return "\n".join(L) + "\n"


# --- comparación --------------------------------------------------------------------------

def _norm_fuente(f: str | None) -> str | None:
    if not f:
        return None
    s = re.sub(r"[^a-z0-9]", "", f.lower())
    for suf in ("bold", "italic", "regular", "oblique"):
        s = s.replace(suf, "")
    for suf in ("psmt", "mt", "ps"):
        if s.endswith(suf):
            s = s[: -len(suf)]
            break
    return s


def _norm_numeracion(fmts: list[str]) -> list[str]:
    out = set()
    for f in fmts:
        f = f.lower()
        out.add("romano" if "roman" in f else "arabigo" if ("decimal" in f or f == "arabigo") else f)
    return sorted(out)


def _paso_docx(p: dict) -> float | None:
    i, tam = p.get("interlineado_cuerpo"), p.get("tam_cuerpo_pt")
    if not i or not tam:
        return None
    return round(i["valor"] * ALTURA_LINEA_NATURAL * tam, 1) if i.get("regla") == "multiple" else float(i["valor"])


def _norm_titulo(t: str) -> str:
    t = re.sub(r"^(?:\d+\.\s*)?CAP[ÍI]TULO\s+[IVXLC\d]+\s*[:.\-–]?\s*", "", t, flags=re.I)
    t = re.sub(r"^(?:[IVX]+\.|\d+(?:\.\d+)*\.?)\s*", "", t)
    return tx.canonico(t).strip()


def comparar(a: dict, b: dict, tol_cm: float = 0.15, tol_rel: float = 0.12) -> dict:
    """Contrasta los perfiles de formato de dos resultados de `analizar`."""
    pa, pb = a["perfil"], b["perfil"]
    diffs: list[dict] = []

    def add(aspecto, va, vb, iguales, nota=None):
        diffs.append({"aspecto": aspecto, "A": va, "B": vb, "coincide": bool(iguales), "nota": nota})

    for k, nombre in (("izq", "Margen izquierdo (cm)"), ("der", "Margen derecho (cm)"),
                      ("sup", "Margen superior (cm)"), ("inf", "Margen inferior (cm)")):
        va, vb = (pa.get("margenes_cm") or {}).get(k), (pb.get("margenes_cm") or {}).get(k)
        ok = va is not None and vb is not None and abs(va - vb) <= tol_cm
        add(nombre, va, vb, ok, f"tolerancia ±{tol_cm} cm" + ("; alguno es estimado" if "estimado" in (pa["precision"] + pb["precision"]) else ""))
    add("Tamaño de página (cm)", pa.get("pagina_cm"), pb.get("pagina_cm"),
        pa.get("pagina_cm") and pb.get("pagina_cm") and all(abs(x - y) <= 0.3 for x, y in zip(pa["pagina_cm"], pb["pagina_cm"])))
    add("Orientación", pa.get("orientacion"), pb.get("orientacion"), pa.get("orientacion") == pb.get("orientacion"))
    fa, fb = _norm_fuente(pa.get("fuente_cuerpo")), _norm_fuente(pb.get("fuente_cuerpo"))
    add("Fuente del cuerpo", pa.get("fuente_cuerpo"), pb.get("fuente_cuerpo"), fa and fa == fb)
    ta, tb = pa.get("tam_cuerpo_pt"), pb.get("tam_cuerpo_pt")
    add("Tamaño del cuerpo (pt)", ta, tb, ta is not None and tb is not None and abs(ta - tb) < 0.3)
    sa = _paso_docx(pa) if a["tipo"] == "docx" else pa.get("interlineado_paso_pt")
    sb = _paso_docx(pb) if b["tipo"] == "docx" else pb.get("interlineado_paso_pt")
    add("Paso de línea del cuerpo (pt)", sa, sb, sa and sb and abs(sa - sb) / max(sa, sb) <= tol_rel,
        f"tolerancia ±{int(tol_rel * 100)} %; en DOCX se convierte con factor {ALTURA_LINEA_NATURAL}×tamaño (estimación)")
    na, nb = _norm_numeracion(pa.get("formatos_numeracion_pagina") or []), _norm_numeracion(pb.get("formatos_numeracion_pagina") or [])
    add("Formatos de numeración de página", na, nb, na == nb)
    ca, cb = pa.get("encabezados_nivel1") or [], pb.get("encabezados_nivel1") or []
    na_, nb_ = {_norm_titulo(x): x for x in ca if _norm_titulo(x)}, {_norm_titulo(x): x for x in cb if _norm_titulo(x)}
    comunes = sorted(set(na_) & set(nb_))
    add("Estructura de capítulos (encabezados nivel 1)", len(ca), len(cb), set(na_) == set(nb_),
        f"comunes={len(comunes)}; solo A={len(set(na_) - set(nb_))}; solo B={len(set(nb_) - set(na_))}")
    return {
        "A": a["fuente"]["archivo"], "B": b["fuente"]["archivo"], "tipos": [a["tipo"], b["tipo"]],
        "diferencias": [d for d in diffs if not d["coincide"]], "coincidencias": [d for d in diffs if d["coincide"]],
        "capitulos": {"comunes": [na_[k] for k in comunes],
                      "solo_A": [na_[k] for k in na_ if k not in nb_], "solo_B": [nb_[k] for k in nb_ if k not in na_]},
        "precision": {"A": pa["precision"], "B": pb["precision"]},
    }


def comparacion_a_markdown(c: dict) -> str:
    L = [f"# Comparación de formato", "", f"- A: `{c['A']}` ({c['tipos'][0]}; {c['precision']['A']})",
         f"- B: `{c['B']}` ({c['tipos'][1]}; {c['precision']['B']})", "",
         f"## Diferencias ({len(c['diferencias'])})", ""]
    L += _tabla_md(["Aspecto", "A", "B", "Nota"], [[d["aspecto"], d["A"], d["B"], d["nota"]] for d in c["diferencias"]])
    L += ["", f"## Coincidencias ({len(c['coincidencias'])})", ""]
    L += _tabla_md(["Aspecto", "A", "B"], [[d["aspecto"], d["A"], d["B"]] for d in c["coincidencias"]])
    L += ["", "## Capítulos (nivel 1)", "", f"- Comunes: {c['capitulos']['comunes']}", f"- Solo en A: {c['capitulos']['solo_A']}",
          f"- Solo en B: {c['capitulos']['solo_B']}"]
    return "\n".join(L) + "\n"


# --- plantilla de estructura ---------------------------------------------------------------

def plantilla_estructura_md(res: dict) -> str:
    """Lista de capítulos/secciones de una tesis modelo PDF, en Markdown reutilizable como plantilla."""
    nombre = Path(res["fuente"]["archivo"]).name
    L = [f"# Plantilla de estructura derivada de: {nombre}", "",
         "> Derivada automáticamente (solo lectura) de un documento modelo. Es una inferencia tipográfica: "
         "verificar contra el índice oficial antes de adoptarla. Las etiquetas impresas no confirmadas se marcan [VERIFICAR].", "",
         f"- SHA-256 del modelo: `{res['fuente']['sha256']}`", f"- Páginas físicas: {res['fuente']['n_paginas']}",
         f"- Fuente del cuerpo: {_v(res['perfil']['fuente_cuerpo'])} {_v(res['perfil']['tam_cuerpo_pt'])} pt; "
         f"márgenes izq/der/sup/inf (cm, estimado): {'/'.join(_v((res['perfil']['margenes_cm'] or {}).get(k)) for k in ('izq', 'der', 'sup', 'inf'))}",
         f"- Criterio: {res['criterio_titulos']}", ""]
    if res["toc_embebido"]:
        L += ["## Marcadores embebidos (get_toc)", ""] + [f"{'  ' * (e['nivel'] - 1)}- {e['titulo']} (p. física {e['pagina_fisica']})" for e in res["toc_embebido"]] + [""]
    for zona, titulo in (("preliminar", "Preliminares"), ("cuerpo", "Cuerpo de la tesis")):
        L += [f"## {titulo}", ""]
        ts = [t for t in res["estructura_inferida"] if t["zona"] == zona]
        for t in ts:
            et = t["etiqueta_impresa"] or "[VERIFICAR: etiqueta impresa no determinada]"
            L.append(f"{'  ' * (t['nivel'] - 1)}- {_num_visible(t)}{t['texto']} — p. física {t['pagina_fisica']}, impresa {et}")
        if not ts:
            L.append("_Sin títulos detectados en esta zona._")
        L.append("")
    if res["indice_impreso"]:
        ok = sum(1 for e in res["indice_impreso"] if e.get("coincide_con_titulo_detectado"))
        L += [f"## Índice impreso del modelo ({len(res['indice_impreso'])} entradas; {ok} coinciden con títulos detectados)", ""]
        L += [f"- {e['titulo']} ..... {e['pagina_impresa']} {'' if e.get('coincide_con_titulo_detectado') else '(sin coincidencia detectada)'}" for e in res["indice_impreso"]]
        L.append("")
    if res["avisos"]:
        L += ["## Avisos", ""] + [f"- {a}" for a in res["avisos"]]
    return "\n".join(L) + "\n"


# ======================================================================================
# CLI
# ======================================================================================

def _escribir(ruta: str | Path, contenido: str, forzar: bool) -> Path:
    dest = seguridad.asegurar_escritura_permitida(ruta)
    # seguridad.py solo protege 3 subcarpetas; aquí se protege TODO referencias/ (capa 1 inmutable).
    try:
        dest.relative_to(rutas.REFERENCIAS.resolve(strict=False))
    except ValueError:
        pass
    else:
        raise seguridad.EscrituraProhibida(f"Escritura denegada: referencias/ es inmutable ({dest}).")
    if dest.exists() and not forzar:
        raise FileExistsError(f"Ya existe {dest}; use --forzar para reemplazar.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(contenido, encoding="utf-8")
    return dest


def _json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)


def _opciones_cache(sp) -> None:
    g = sp.add_argument_group("caché de índices PDF")
    g.add_argument("--carpeta-indices", default=None,
                   help="Carpeta alternativa para la caché de índices PDF (por defecto: la del vault solo para "
                        "PDFs de fuentes/tesis modelo; otros PDF se indexan en memoria sin escribir)")
    g.add_argument("--sin-cache", action="store_true", help="Indexar siempre en memoria; no leer ni escribir caché")


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Analista documental (Squad E): desglose estructural de solo lectura.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("desglosar", help="Desglosa un .docx, .pdf o .xlsx")
    d.add_argument("archivo")
    d.add_argument("--json", action="store_true", help="Salida JSON por stdout")
    d.add_argument("--salida-json", default=None)
    d.add_argument("--salida-md", default=None)
    d.add_argument("--bloques", action="store_true", help="PDF: incluir bloques por página")
    d.add_argument("--forzar", action="store_true")
    _opciones_cache(d)
    c = sub.add_parser("comparar", help="Compara el formato de dos .docx/.pdf")
    c.add_argument("a")
    c.add_argument("b")
    c.add_argument("--json", action="store_true")
    _opciones_cache(c)
    p = sub.add_parser("plantilla-estructura", help="Lista de capítulos/secciones de una tesis modelo PDF")
    p.add_argument("pdf")
    p.add_argument("--salida", default=None, help="Markdown de salida (por defecto salidas/documentos/)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--forzar", action="store_true")
    _opciones_cache(p)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:  # argparse ya imprimió el uso; se normaliza al contrato (2 = uso incorrecto)
        return 2 if e.code not in (0, None) else 0
    opc = {"carpeta_indices": Path(a.carpeta_indices) if a.carpeta_indices else None,
           "usar_cache": False if a.sin_cache else None}

    try:
        if a.cmd == "desglosar":
            res = analizar(a.archivo, incluir_bloques=a.bloques, **opc)
            if a.salida_json:
                print(f"JSON: {_escribir(a.salida_json, _json(res), a.forzar)}", file=sys.stderr)
            if a.salida_md:
                print(f"Markdown: {_escribir(a.salida_md, a_markdown(res), a.forzar)}", file=sys.stderr)
            print(_json(res) if a.json else a_markdown(res))
            return 0
        if a.cmd == "comparar":
            for r in (a.a, a.b):
                if Path(r).suffix.lower() not in (".docx", ".pdf"):
                    print(f"ERROR: 'comparar' solo admite .docx o .pdf: {r}", file=sys.stderr)
                    return 2
            cmp_ = comparar(analizar(a.a, **opc), analizar(a.b, **opc))
            print(_json(cmp_) if a.json else comparacion_a_markdown(cmp_))
            return 1 if cmp_["diferencias"] else 0
        if a.cmd == "plantilla-estructura":
            if Path(a.pdf).suffix.lower() != ".pdf":
                print("ERROR: se requiere un PDF.", file=sys.stderr)
                return 2
            if not Path(a.pdf).exists():
                raise FileNotFoundError(f"No existe: {a.pdf}")
            res = analizar_pdf(a.pdf, opc["carpeta_indices"], usar_cache=opc["usar_cache"])
            md = plantilla_estructura_md(res)
            dest = a.salida or rutas.SALIDAS_DOCUMENTOS / f"plantilla_estructura_{tx.slug(Path(a.pdf).stem, 50)}.md"
            print(f"Markdown: {_escribir(dest, md, a.forzar)}", file=sys.stderr)
            print(_json({k: res[k] for k in ('fuente', 'perfil', 'estructura_inferida', 'indice_impreso', 'avisos')}) if a.json else md)
            return 0 if res["estructura_inferida"] else 1
    except FormatoNoSoportado as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except (FileNotFoundError, FileExistsError, ArchivoNoLegible, ValueError, seguridad.EscrituraProhibida) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"ERROR inesperado ({type(e).__name__}): {e}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
