#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB - Editor quirúrgico de .docx con normas APA 7 / UNAJMA.

Edita una COPIA versionada del informe sin romper formato, secciones, numeración,
campos ni imágenes. Nunca modifica el original: `destino` debe ser distinto de `origen`
y no puede estar en referencias/, datos/raw/ ni syncova.

Operaciones (clase EditorDocx):
    buscar_parrafos      localizar párrafos (texto o regex, filtro de estilo)
    reemplazar_texto     sustituir texto aunque cruce varios runs, conservando el formato
    insertar_parrafo_despues   clona el formato de un párrafo modelo
    insertar_tabla_apa7  tabla nativa de 3 líneas, encabezado repetible, filas indivisibles
    insertar_figura_apa7 figura centrada; exige >= 300 DPI efectivos al ancho pedido
    insertar_referencia_apa7   sangría francesa, en orden alfabético, sin duplicar
    eliminar_parrafo     con salvaguardas (no borra saltos de sección ni imágenes sin `forzar`)

Toda operación admite `dry_run` (solo informa) y queda registrada en
`<destino>.cambios.json` junto con el SHA-256 del original.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt  # noqa: E402
from docx.text.paragraph import Paragraph  # noqa: E402
from lxml import etree  # noqa: E402
from PIL import Image  # noqa: E402
from unidecode import unidecode  # noqa: E402

from scripts.comun import rutas, seguridad  # noqa: E402

FUENTE = "Times New Roman"
DPI_MINIMO = 299.5  # tolerancia de redondeo sobre 300
_TITULOS_REFERENCIAS = {"referencias", "referencias bibliograficas", "bibliografia", "lista de referencias"}


class EditorError(Exception):
    """Operación rechazada por una salvaguarda del editor."""


class AnclaError(EditorError):
    """El ancla no existe o es ambigua."""


# --------------------------------------------------------------------------- utilidades
def _bajo(ruta: Path, base: Path) -> bool:
    try:
        ruta.relative_to(Path(base).resolve(strict=False))
        return True
    except ValueError:
        return False


def validar_destino(origen: str | Path, destino: str | Path) -> Path:
    """Destino distinto del original y fuera de las zonas inmutables."""
    d = seguridad.asegurar_no_sobrescribe(origen, destino)
    for veto in (rutas.REFERENCIAS, rutas.DATOS_RAW, rutas.SYNCOVA):
        if _bajo(d, veto):
            raise seguridad.EscrituraProhibida(f"Escritura denegada (zona inmutable): {d}")
    if d.suffix.lower() != ".docx":
        raise EditorError(f"El destino debe ser .docx: {d}")
    return d


def siguiente_version(carpeta: str | Path | None = None, prefijo: str = "informe_final") -> Path:
    """Siguiente `informe_final_vNN.docx` libre en la carpeta de documentos."""
    carpeta = Path(carpeta) if carpeta else rutas.SALIDAS_DOCUMENTOS
    mayor = 0
    if carpeta.is_dir():
        for p in carpeta.glob(f"{prefijo}_v*.docx"):
            m = re.fullmatch(rf"{re.escape(prefijo)}_v(\d+)\.docx", p.name)
            if m:
                mayor = max(mayor, int(m.group(1)))
    return carpeta / f"{prefijo}_v{mayor + 1:02d}.docx"


_RE_MARCA = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*)")


def _segmentos(texto: str) -> list[tuple[str, bool, bool]]:
    """Divide '**negrita**' y '*cursiva*' en (texto, negrita, cursiva)."""
    salida = []
    for t in _RE_MARCA.split(texto):
        if not t:
            continue
        if t.startswith("**") and t.endswith("**") and len(t) >= 4:
            salida.append((t[2:-2], True, False))
        elif t.startswith("*") and t.endswith("*") and len(t) >= 2:
            salida.append((t[1:-1], False, True))
        else:
            salida.append((t, False, False))
    return salida


def _clave_orden(texto: str) -> str:
    """Orden alfabético letra por letra, sin tildes ni signos."""
    return re.sub(r"[^a-z0-9]", "", unidecode(texto).lower())


def _norm(texto: str) -> str:
    return re.sub(r"\s+", " ", unidecode(texto).lower()).strip()


def _insertar_en_orden(padre, elemento, sucesores: tuple[str, ...]) -> None:
    """Inserta respetando el orden del esquema OOXML: antes del primer hijo que deba ir después."""
    tags = {qn(f"w:{s}") for s in sucesores}
    for hijo in padre:
        if hijo.tag in tags:
            hijo.addprevious(elemento)
            return
    padre.append(elemento)


def _firma_seccion(sec) -> str:
    return etree.tostring(sec._sectPr, method="c14n").decode("utf-8")


def _instantanea(doc) -> dict:
    return {
        "secciones": [_firma_seccion(s) for s in doc.sections],
        "tablas": len(doc.tables),
        "imagenes": len(doc.inline_shapes),
        "parrafos": len(doc.paragraphs),
    }


# --------------------------------------------------------------------------- editor
class EditorDocx:
    def __init__(self, origen: str | Path, destino: str | Path, dry_run: bool = False,
                 sobrescribir: bool = False):
        self.origen = Path(origen).resolve(strict=True)
        if self.origen.suffix.lower() != ".docx":
            raise EditorError(f"El origen debe ser .docx: {self.origen}")
        self.destino = validar_destino(self.origen, destino)
        if self.destino.exists() and not sobrescribir and not dry_run:
            raise FileExistsError(f"Ya existe {self.destino}; use una versión nueva o sobrescribir=True")
        self.dry_run = dry_run
        self.sha_origen = seguridad.sha256_archivo(self.origen)
        self.doc = Document(str(self.origen))
        self.inicial = _instantanea(self.doc)
        self.cambios: list[dict] = []
        self._delta = {"tablas": 0, "imagenes": 0}

    # ---- registro ------------------------------------------------------------
    def _registrar(self, operacion: str, **datos) -> dict:
        reg = {"operacion": operacion, "dry_run": self.dry_run, **datos}
        self.cambios.append(reg)
        return reg

    # ---- búsqueda ------------------------------------------------------------
    def buscar_parrafos(self, patron: str, regex: bool = False, estilo: str | None = None) -> list[dict]:
        rx = re.compile(patron, re.I) if regex else None
        salida = []
        for i, p in enumerate(self.doc.paragraphs):
            if estilo and (p.style.name if p.style is not None else "") != estilo:
                continue
            txt = p.text
            ok = bool(rx.search(txt)) if rx else patron.lower() in txt.lower()
            if ok:
                salida.append({"indice": i, "estilo": p.style.name if p.style is not None else None,
                               "texto": txt[:160], "anterior": self.doc.paragraphs[i - 1].text[:80] if i else "",
                               "siguiente": self.doc.paragraphs[i + 1].text[:80] if i + 1 < len(self.doc.paragraphs) else ""})
        return salida

    def _ancla(self, ancla: int | str, ocurrencia: int | None = None) -> Paragraph:
        pars = self.doc.paragraphs
        if isinstance(ancla, int) or (isinstance(ancla, str) and ancla.isdigit()):
            i = int(ancla)
            if not 0 <= i < len(pars):
                raise AnclaError(f"Índice de párrafo fuera de rango: {i} (0..{len(pars) - 1})")
            return pars[i]
        hallados = [i for i, p in enumerate(pars) if str(ancla).lower() in p.text.lower()]
        if not hallados:
            raise AnclaError(f"Ancla no encontrada: {ancla!r}")
        if ocurrencia is None:
            if len(hallados) > 1:
                raise AnclaError(f"Ancla ambigua ({len(hallados)} coincidencias en párrafos {hallados[:10]}); "
                                 f"indique ocurrencia o el índice del párrafo")
            return pars[hallados[0]]
        if not 1 <= ocurrencia <= len(hallados):
            raise AnclaError(f"Ocurrencia {ocurrencia} fuera de rango (hay {len(hallados)})")
        return pars[hallados[ocurrencia - 1]]

    @staticmethod
    def _termina_seccion(par: Paragraph) -> bool:
        ppr = par._p.pPr
        return ppr is not None and ppr.find(qn("w:sectPr")) is not None

    # ---- reemplazo -----------------------------------------------------------
    @staticmethod
    def _run_solo_texto(run) -> bool:
        permitidos = {qn("w:rPr"), qn("w:t"), qn("w:tab"), qn("w:br"), qn("w:cr")}
        return all(ch.tag in permitidos for ch in run._r)

    def reemplazar_texto(self, buscar: str, nuevo: str, ocurrencia: int | None = None) -> dict:
        """Sustituye `buscar` por `nuevo` (texto literal, sin marcado) conservando el formato del primer run."""
        if not buscar:
            raise EditorError("El texto a buscar no puede estar vacío")
        hallazgos = []
        for i, p in enumerate(self.doc.paragraphs):
            texto = "".join(r.text for r in p.runs)
            ini = 0
            while True:
                k = texto.find(buscar, ini)
                if k < 0:
                    break
                hallazgos.append((i, k))
                ini = k + max(1, len(buscar))
        if not hallazgos:
            raise AnclaError(f"Texto no encontrado en los runs del cuerpo: {buscar!r} "
                             f"(si está dentro de un hipervínculo, tabla o campo no se edita)")
        if ocurrencia is None and len(hallazgos) > 1:
            raise AnclaError(f"Texto ambiguo: {len(hallazgos)} ocurrencias en párrafos "
                             f"{sorted({h[0] for h in hallazgos})[:10]}; indique ocurrencia")
        elegido = hallazgos[0 if ocurrencia is None else ocurrencia - 1] if (
            ocurrencia is None or 1 <= ocurrencia <= len(hallazgos)) else None
        if elegido is None:
            raise AnclaError(f"Ocurrencia {ocurrencia} fuera de rango (hay {len(hallazgos)})")
        idx, s = elegido
        par = self.doc.paragraphs[idx]
        runs = par.runs
        textos = [r.text for r in runs]
        spans, pos = [], 0
        for t in textos:
            spans.append((pos, pos + len(t)))
            pos += len(t)
        e = s + len(buscar)
        afectados = [i for i, (a, b) in enumerate(spans) if a < e and b > s]
        for i in afectados:
            if not self._run_solo_texto(runs[i]):
                raise EditorError("El texto cruza un run con imagen, campo u otro objeto; no se edita para no perderlo")
        reg = self._registrar("reemplazar_texto", parrafo=idx, antes=buscar[:120], despues=nuevo[:120],
                              runs_afectados=len(afectados))
        if self.dry_run:
            return reg
        for k, i in enumerate(afectados):
            a, b = spans[i]
            t = textos[i]
            ini, fin = max(s, a) - a, min(e, b) - a
            if len(afectados) == 1:
                runs[i].text = t[:ini] + nuevo + t[fin:]
            elif k == 0:
                runs[i].text = t[:ini] + nuevo
            elif k == len(afectados) - 1:
                resto = t[fin:]
                if resto:
                    runs[i].text = resto
                else:
                    runs[i]._r.getparent().remove(runs[i]._r)
            else:
                runs[i]._r.getparent().remove(runs[i]._r)
        return reg

    # ---- párrafos ------------------------------------------------------------
    def _nuevo_parrafo(self, modelo: Paragraph | None) -> Paragraph:
        p = OxmlElement("w:p")
        if modelo is not None and modelo._p.pPr is not None:
            ppr = copy.deepcopy(modelo._p.pPr)
            for s in ppr.findall(qn("w:sectPr")):
                ppr.remove(s)  # nunca duplicar un salto de sección
            p.append(ppr)
        return Paragraph(p, self.doc._body)

    @staticmethod
    def _rpr_modelo(modelo: Paragraph | None):
        if modelo is None:
            return None
        for r in modelo.runs:
            if r._r.rPr is not None:
                return r._r.rPr
        return None

    def _escribir(self, par: Paragraph, texto: str, rpr_modelo=None, fuente_pt: float | None = None,
                  negrita: bool | None = None, cursiva: bool | None = None, explicita: bool = False) -> None:
        for seg, b, i in _segmentos(texto):
            r = par.add_run(seg)
            if rpr_modelo is not None:
                if r._r.rPr is not None:
                    r._r.remove(r._r.rPr)
                r._r.insert(0, copy.deepcopy(rpr_modelo))
            if explicita:
                r.font.name = FUENTE
                r._r.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), FUENTE)
            if fuente_pt:
                r.font.size = Pt(fuente_pt)
            if negrita is not None:
                r.bold = negrita
            if cursiva is not None:
                r.italic = cursiva
            if b:
                r.bold = True
            if i:
                r.italic = True

    def insertar_parrafo_despues(self, ancla: int | str, texto: str, modelo: int | str | None = None,
                                 ocurrencia: int | None = None) -> dict:
        """Nuevo párrafo tras `ancla` con el formato de `modelo` (por defecto, el propio ancla)."""
        a = self._ancla(ancla, ocurrencia)
        m = self._ancla(modelo) if modelo is not None else a
        reg = self._registrar("insertar_parrafo", despues_de=a.text[:80], modelo=m.text[:60], texto=texto[:120],
                              aviso=("el ancla cierra una sección: el párrafo quedará en la sección siguiente"
                                     if self._termina_seccion(a) else None))
        if self.dry_run:
            return reg
        nuevo = self._nuevo_parrafo(m)
        self._escribir(nuevo, texto, self._rpr_modelo(m))
        a._p.addnext(nuevo._p)
        return reg

    # ---- encabezados de tabla/figura ------------------------------------------
    def _rotulo(self, etiqueta: str, titulo: str) -> tuple[Paragraph, Paragraph]:
        def formato(p: Paragraph) -> None:
            pf = p.paragraph_format
            pf.space_before, pf.space_after = Pt(6), Pt(0)
            pf.line_spacing = 1.15
            pf.first_line_indent = Pt(0)
            pf.keep_with_next = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        num = Paragraph(OxmlElement("w:p"), self.doc._body)
        formato(num)
        self._escribir(num, etiqueta, fuente_pt=12, negrita=True, explicita=True)
        tit = Paragraph(OxmlElement("w:p"), self.doc._body)
        formato(tit)
        self._escribir(tit, titulo, fuente_pt=12, cursiva=True, explicita=True)
        return num, tit

    def _nota(self, texto: str) -> Paragraph:
        p = Paragraph(OxmlElement("w:p"), self.doc._body)
        p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(4), Pt(12)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.first_line_indent = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        self._escribir(p, "Nota. ", fuente_pt=10, cursiva=True, explicita=True)
        self._escribir(p, texto, fuente_pt=10, explicita=True)
        return p

    def insertar_tabla_apa7(self, despues_de: int | str, numero: int | str, titulo: str,
                            encabezados: list[str], filas: list[list], nota: str | None = None,
                            anchos_cm: list[float] | None = None, ocurrencia: int | None = None) -> dict:
        """Tabla nativa APA 7: 3 líneas horizontales, sin verticales, encabezado repetible, filas indivisibles."""
        if not encabezados:
            raise EditorError("La tabla necesita encabezados")
        for n, f in enumerate(filas, 1):
            if len(f) != len(encabezados):
                raise EditorError(f"Fila {n} tiene {len(f)} celdas; se esperaban {len(encabezados)}")
        if anchos_cm and len(anchos_cm) != len(encabezados):
            raise EditorError("Cantidad de anchos distinta de la de columnas")
        a = self._ancla(despues_de, ocurrencia)
        reg = self._registrar("insertar_tabla", despues_de=a.text[:80], numero=str(numero), titulo=titulo[:100],
                              filas=len(filas), columnas=len(encabezados))
        if self.dry_run:
            return reg
        num, tit = self._rotulo(f"Tabla {numero}", titulo)
        tbl = self.doc.add_table(rows=len(filas) + 1, cols=len(encabezados))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        tblPr = tbl._tbl.tblPr
        for hijo in list(tblPr):
            if hijo.tag in (qn("w:tblStyle"), qn("w:tblBorders"), qn("w:tblCellMar")):
                tblPr.remove(hijo)
        bordes = OxmlElement("w:tblBorders")
        for lado, val in (("top", "single"), ("left", "none"), ("bottom", "single"), ("right", "none"),
                          ("insideH", "none"), ("insideV", "none")):
            e = OxmlElement(f"w:{lado}")
            e.set(qn("w:val"), val)
            if val == "single":
                e.set(qn("w:sz"), "6")
                e.set(qn("w:space"), "0")
                e.set(qn("w:color"), "000000")
            bordes.append(e)
        _insertar_en_orden(tblPr, bordes, ("shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption", "tblDescription"))
        mar = OxmlElement("w:tblCellMar")
        for lado, w in (("top", 40), ("left", 100), ("bottom", 40), ("right", 100)):
            e = OxmlElement(f"w:{lado}")
            e.set(qn("w:w"), str(w))
            e.set(qn("w:type"), "dxa")
            mar.append(e)
        _insertar_en_orden(tblPr, mar, ("tblLook", "tblCaption", "tblDescription"))

        for r_idx, row in enumerate(tbl.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(OxmlElement("w:cantSplit"))  # cantSplit va antes de tblHeader en el esquema
            if r_idx == 0:
                trPr.append(OxmlElement("w:tblHeader"))
            valores = encabezados if r_idx == 0 else filas[r_idx - 1]
            for c_idx, cel in enumerate(row.cells):
                if anchos_cm:
                    cel.width = Cm(anchos_cm[c_idx])
                if r_idx == 0:
                    tcPr = cel._tc.get_or_add_tcPr()
                    tcb = OxmlElement("w:tcBorders")
                    inf = OxmlElement("w:bottom")
                    for k, v in (("val", "single"), ("sz", "6"), ("space", "0"), ("color", "000000")):
                        inf.set(qn(f"w:{k}"), v)
                    tcb.append(inf)
                    _insertar_en_orden(tcPr, tcb, ("shd", "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark"))
                p = cel.paragraphs[0]
                p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.first_line_indent = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
                self._escribir(p, str(valores[c_idx]), fuente_pt=10, negrita=True if r_idx == 0 else None, explicita=True)

        cursor = a._p
        for el in (num._p, tit._p, tbl._tbl):
            cursor.addnext(el)
            cursor = el
        if nota:
            n = self._nota(nota)
            cursor.addnext(n._p)
        self._delta["tablas"] += 1
        return reg

    def insertar_figura_apa7(self, despues_de: int | str, numero: int | str, titulo: str, ruta_imagen: str | Path,
                             nota: str, ancho_cm: float = 14.0, ocurrencia: int | None = None) -> dict:
        """Figura centrada. Aborta si el ancho pedido deja < 300 DPI efectivos (no reescala hacia arriba)."""
        ruta = Path(ruta_imagen)
        if not ruta.is_file():
            raise EditorError(f"La imagen no existe: {ruta}")
        try:
            with Image.open(ruta) as im:
                ancho_px, alto_px = im.size
        except Exception as e:  # noqa: BLE001
            raise EditorError(f"No se pudo abrir la imagen {ruta.name}: {e}") from e
        dpi_ef = ancho_px / (ancho_cm / 2.54)
        if dpi_ef < DPI_MINIMO:
            maximo = ancho_px / 300 * 2.54
            raise EditorError(f"Resolución insuficiente: {ancho_px} px a {ancho_cm} cm = {dpi_ef:.0f} DPI efectivos "
                              f"(mínimo 300). Ancho máximo admisible: {maximo:.1f} cm")
        a = self._ancla(despues_de, ocurrencia)
        reg = self._registrar("insertar_figura", despues_de=a.text[:80], numero=str(numero), titulo=titulo[:100],
                              imagen=ruta.name, px=[ancho_px, alto_px], ancho_cm=ancho_cm, dpi_efectivo=round(dpi_ef))
        if self.dry_run:
            return reg
        num, tit = self._rotulo(f"Figura {numero}", titulo)
        img = self.doc.add_paragraph()
        img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img.paragraph_format.space_before = img.paragraph_format.space_after = Pt(4)
        img.paragraph_format.first_line_indent = Pt(0)
        img.paragraph_format.keep_with_next = True
        img.add_run().add_picture(str(ruta), width=Cm(ancho_cm))
        n = self._nota(nota)
        cursor = a._p
        for el in (num._p, tit._p, img._p, n._p):
            cursor.addnext(el)
            cursor = el
        self._delta["imagenes"] += 1
        return reg

    # ---- referencias ---------------------------------------------------------
    def insertar_referencia_apa7(self, texto: str) -> dict:
        """Inserta una referencia (sangría francesa 1.27 cm) en su lugar alfabético; rechaza duplicados."""
        pars = self.doc.paragraphs
        cab = next((i for i, p in enumerate(pars) if _norm(p.text) in _TITULOS_REFERENCIAS), None)
        if cab is None:
            raise AnclaError("No se encontró el encabezado 'Referencias'")
        entradas = []
        for p in pars[cab + 1:]:
            if p.style is not None and p.style.name.lower().startswith(("heading", "título", "titulo")):
                break
            if p.text.strip():
                entradas.append(p)
        clave = _clave_orden(texto.replace("*", ""))
        for p in entradas:
            if _clave_orden(p.text)[:70] == clave[:70]:
                raise EditorError(f"Referencia duplicada: {p.text[:90]!r}")
        destino_previo = None
        for p in entradas:
            if _clave_orden(p.text) > clave:
                destino_previo = p
                break
        reg = self._registrar("insertar_referencia", texto=texto[:140],
                              antes_de=destino_previo.text[:60] if destino_previo else None)
        if self.dry_run:
            return reg
        nuevo = Paragraph(OxmlElement("w:p"), self.doc._body)
        pf = nuevo.paragraph_format
        pf.left_indent, pf.first_line_indent = Cm(1.27), Cm(-1.27)
        pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(6), 1.5
        nuevo.alignment = WD_ALIGN_PARAGRAPH.LEFT
        self._escribir(nuevo, texto, fuente_pt=12, explicita=True)
        if destino_previo is not None:
            destino_previo._p.addprevious(nuevo._p)
        elif entradas:
            entradas[-1]._p.addnext(nuevo._p)
        else:
            pars[cab]._p.addnext(nuevo._p)
        return reg

    # ---- eliminar ------------------------------------------------------------
    def eliminar_parrafo(self, ancla: int | str, confirmar: bool = False, forzar: bool = False,
                         ocurrencia: int | None = None) -> dict:
        a = self._ancla(ancla, ocurrencia)
        if self._termina_seccion(a):
            raise EditorError("El párrafo contiene un salto de sección; eliminarlo rompería la numeración/márgenes")
        tiene_img = bool(a._p.findall(".//" + qn("w:drawing")))
        if tiene_img and not forzar:
            raise EditorError("El párrafo contiene una imagen; use forzar=True si es intencional")
        if not confirmar:
            raise EditorError("Eliminar exige confirmar=True")
        reg = self._registrar("eliminar_parrafo", texto=a.text[:140], con_imagen=tiene_img)
        if self.dry_run:
            return reg
        a._p.getparent().remove(a._p)
        if tiene_img:
            self._delta["imagenes"] -= 1
        return reg

    # ---- guardar y verificar ---------------------------------------------------
    def guardar(self) -> dict:
        informe = {"origen": str(self.origen), "destino": str(self.destino), "sha256_origen": self.sha_origen,
                   "marca_tiempo": time.strftime("%Y-%m-%d %H:%M:%S"), "dry_run": self.dry_run, "cambios": self.cambios}
        if self.dry_run:
            informe["verificacion"] = {"ok": True, "detalle": ["dry-run: no se escribió nada"]}
            return informe
        if seguridad.sha256_archivo(self.origen) != self.sha_origen:
            raise EditorError("El original cambió mientras se editaba; se aborta para no mezclar versiones")
        self.destino.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(self.destino))
        informe["verificacion"] = self.verificar()
        (self.destino.parent / (self.destino.name + ".cambios.json")).write_text(
            json.dumps(informe, ensure_ascii=False, indent=1), encoding="utf-8")
        return informe

    def verificar(self) -> dict:
        """Reabre el destino y comprueba que no se perdieron secciones, tablas ni imágenes."""
        detalle, ok = [], True
        doc = Document(str(self.destino))
        ahora = _instantanea(doc)
        if ahora["secciones"] != self.inicial["secciones"]:
            ok = False
            detalle.append("Las propiedades de sección (márgenes, numeración, encabezados) cambiaron")
        else:
            detalle.append(f"{len(ahora['secciones'])} sección(es) idénticas al original")
        esperado_t = self.inicial["tablas"] + self._delta["tablas"]
        esperado_i = self.inicial["imagenes"] + self._delta["imagenes"]
        if ahora["tablas"] != esperado_t:
            ok = False
            detalle.append(f"Tablas: {ahora['tablas']} (esperadas {esperado_t})")
        if ahora["imagenes"] != esperado_i:
            ok = False
            detalle.append(f"Imágenes en línea: {ahora['imagenes']} (esperadas {esperado_i})")
        if ok:
            detalle.append(f"Tablas {ahora['tablas']} e imágenes {ahora['imagenes']} coherentes con las operaciones")
        return {"ok": ok, "detalle": detalle}


# --------------------------------------------------------------------------- CLI
def _resumen(inf: dict) -> str:
    L = [f"{'[DRY-RUN] ' if inf['dry_run'] else ''}Origen : {inf['origen']}", f"Destino: {inf['destino']}",
         f"SHA-256 del original: {inf['sha256_origen'][:16]}…"]
    for c in inf["cambios"]:
        L.append("  - " + ", ".join(f"{k}={v}" for k, v in c.items() if k != "dry_run" and v not in (None, "")))
    v = inf["verificacion"]
    L.append(("VERIFICACIÓN OK: " if v["ok"] else "VERIFICACIÓN FALLÓ: ") + "; ".join(v["detalle"]))
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    seguridad.configurar_utf8()
    ap = argparse.ArgumentParser(description="Editor quirúrgico de .docx (APA 7) sobre copias versionadas.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comunes(p, con_destino=True):
        p.add_argument("origen")
        if con_destino:
            p.add_argument("destino")
            p.add_argument("--dry-run", action="store_true")
            p.add_argument("--sobrescribir", action="store_true")
        p.add_argument("--json", action="store_true")

    p = sub.add_parser("siguiente-version")
    p.add_argument("--dir", default=None)
    p = sub.add_parser("buscar")
    comunes(p, False)
    p.add_argument("patron")
    p.add_argument("--regex", action="store_true")
    p.add_argument("--estilo")
    p = sub.add_parser("reemplazar")
    comunes(p)
    p.add_argument("buscar")
    p.add_argument("nuevo")
    p.add_argument("--ocurrencia", type=int)
    p = sub.add_parser("insertar-parrafo")
    comunes(p)
    p.add_argument("--despues-de", required=True)
    p.add_argument("--texto", required=True)
    p.add_argument("--modelo")
    p.add_argument("--ocurrencia", type=int)
    p = sub.add_parser("insertar-tabla")
    comunes(p)
    p.add_argument("--entrada", required=True, help="JSON: despues_de, numero, titulo, encabezados, filas, nota, anchos_cm")
    p = sub.add_parser("insertar-figura")
    comunes(p)
    p.add_argument("--despues-de", required=True)
    p.add_argument("--numero", required=True)
    p.add_argument("--titulo", required=True)
    p.add_argument("--imagen", required=True)
    p.add_argument("--nota", required=True)
    p.add_argument("--ancho-cm", type=float, default=14.0)
    p = sub.add_parser("insertar-referencia")
    comunes(p)
    p.add_argument("texto")
    p = sub.add_parser("eliminar")
    comunes(p)
    p.add_argument("ancla")
    p.add_argument("--confirmar", action="store_true")
    p.add_argument("--forzar", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0

    try:
        if a.cmd == "siguiente-version":
            print(siguiente_version(a.dir))
            return 0
        if a.cmd == "buscar":
            ed = EditorDocx(a.origen, Path(a.origen).with_name("_lectura.docx"), dry_run=True)
            res = ed.buscar_parrafos(a.patron, a.regex, a.estilo)
            print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else
                  "\n".join(f"[{r['indice']}] ({r['estilo']}) {r['texto']}" for r in res) or "sin coincidencias")
            return 0 if res else 1
        ed = EditorDocx(a.origen, a.destino, dry_run=a.dry_run, sobrescribir=a.sobrescribir)
        if a.cmd == "reemplazar":
            ed.reemplazar_texto(a.buscar, a.nuevo, a.ocurrencia)
        elif a.cmd == "insertar-parrafo":
            ed.insertar_parrafo_despues(a.despues_de, a.texto, a.modelo, a.ocurrencia)
        elif a.cmd == "insertar-tabla":
            datos = json.loads(Path(a.entrada).read_text(encoding="utf-8-sig"))
            ed.insertar_tabla_apa7(datos["despues_de"], datos["numero"], datos["titulo"], datos["encabezados"],
                                   datos["filas"], datos.get("nota"), datos.get("anchos_cm"), datos.get("ocurrencia"))
        elif a.cmd == "insertar-figura":
            ed.insertar_figura_apa7(a.despues_de, a.numero, a.titulo, a.imagen, a.nota, a.ancho_cm)
        elif a.cmd == "insertar-referencia":
            ed.insertar_referencia_apa7(a.texto)
        elif a.cmd == "eliminar":
            ed.eliminar_parrafo(a.ancla, a.confirmar, a.forzar)
        inf = ed.guardar()
        print(json.dumps(inf, ensure_ascii=False, indent=1) if a.json else _resumen(inf))
        return 0 if inf["verificacion"]["ok"] else 1
    except (EditorError, seguridad.EscrituraProhibida, FileExistsError, FileNotFoundError, KeyError,
            json.JSONDecodeError) as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
