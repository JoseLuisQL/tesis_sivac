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


def _qn(tag: str):
    from docx.oxml.ns import qn

    return qn(tag)


_ALINEACIONES = ("left", "center", "right", "both", "justify")


def _fijar_alineacion_celda(tc, alineacion: str) -> None:
    """Fija <w:jc> en todos los párrafos de la celda respetando el orden de CT_PPr."""
    from docx.oxml import OxmlElement

    if alineacion not in _ALINEACIONES:
        raise ValueError(f"Alineación no válida: {alineacion}")
    for p in tc.findall(_qn("w:p")):
        pPr = p.find(_qn("w:pPr"))
        if pPr is None:
            from docx.oxml import OxmlElement as _OE

            pPr = _OE("w:pPr")
            p.insert(0, pPr)
        jc = pPr.find(_qn("w:jc"))
        if jc is None:
            jc = OxmlElement("w:jc")
            pPr.append(jc)
        jc.set(_qn("w:val"), "both" if alineacion == "justify" else alineacion)


def _fijar_texto_celda(tc, texto: str, alineacion: Optional[str] = None) -> None:
    """Reescribe el texto de una celda conservando el <w:rPr> del primer run."""
    from docx.oxml import OxmlElement

    p = tc.find(_qn("w:p"))
    if p is None:
        p = OxmlElement("w:p")
        tc.append(p)
    runs = p.findall(_qn("w:r"))
    for extra in p.findall(_qn("w:r"))[1:]:
        p.remove(extra)
    if runs:
        run = runs[0]
        for t in run.findall(_qn("w:t"))[1:]:
            run.remove(t)
        t = run.find(_qn("w:t"))
        if t is None:
            t = OxmlElement("w:t")
            run.append(t)
    else:
        run = OxmlElement("w:r")
        t = OxmlElement("w:t")
        run.append(t)
        p.append(run)
    t.text = texto
    if texto != texto.strip() or "  " in texto:
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    if alineacion:
        _fijar_alineacion_celda(tc, alineacion)


def _preparar_tr(tr, cant_split: bool = True, tbl_header: bool = False) -> None:
    """Garantiza <w:cantSplit/> y <w:tblHeader/> en el orden correcto de <w:trPr>."""
    from docx.oxml import OxmlElement

    trPr = tr.find(_qn("w:trPr"))
    if trPr is None:
        trPr = OxmlElement("w:trPr")
        tr.insert(0, trPr)
    cs = trPr.find(_qn("w:cantSplit"))
    if cant_split and cs is None:
        cs = OxmlElement("w:cantSplit")
        trPr.insert(0, cs)
    elif not cant_split and cs is not None:
        trPr.remove(cs)
    th = trPr.find(_qn("w:tblHeader"))
    if tbl_header and th is None:
        th = OxmlElement("w:tblHeader")
        cs_node = trPr.find(_qn("w:cantSplit"))
        trPr.insert(trPr.index(cs_node) + 1 if cs_node is not None else 0, th)
    elif not tbl_header and th is not None:
        trPr.remove(th)


_ORDEN_CELLMAR = ("w:top", "w:left", "w:bottom", "w:right")
_ORDEN_TBLPR_ANTES_CELLMAR = (
    "w:tblLayout",
    "w:shd",
    "w:tblBorders",
    "w:tblInd",
    "w:tblCellSpacing",
    "w:jc",
    "w:tblW",
    "w:tblStyle",
)


def _fijar_margenes_celda_tabla(tbl, izquierdo_dxa: int = 57, derecho_dxa: int = 57) -> None:
    """Fija los márgenes laterales de celda de toda la tabla mediante <w:tblCellMar>."""
    from docx.oxml import OxmlElement

    pr = tbl.find(_qn("w:tblPr"))
    if pr is None:
        pr = OxmlElement("w:tblPr")
        tbl.insert(0, pr)
    mar = pr.find(_qn("w:tblCellMar"))
    if mar is None:
        mar = OxmlElement("w:tblCellMar")
        ancla = None
        for etiqueta in _ORDEN_TBLPR_ANTES_CELLMAR:
            ancla = pr.find(_qn(etiqueta))
            if ancla is not None:
                break
        if ancla is not None:
            ancla.addnext(mar)
        else:
            pr.append(mar)
    for etiqueta, valor in (("w:left", izquierdo_dxa), ("w:right", derecho_dxa)):
        nodo = mar.find(_qn(etiqueta))
        if nodo is None:
            nodo = OxmlElement(etiqueta)
            orden = _ORDEN_CELLMAR.index(etiqueta)
            insertado = False
            for hijo in list(mar):
                nombre = "w:" + hijo.tag.split("}")[1]
                if nombre in _ORDEN_CELLMAR and _ORDEN_CELLMAR.index(nombre) > orden:
                    hijo.addprevious(nodo)
                    insertado = True
                    break
            if not insertado:
                mar.append(nodo)
        nodo.set(_qn("w:w"), str(int(valor)))
        nodo.set(_qn("w:type"), "dxa")


def _fijar_tamano_run(run, medios_puntos: int) -> bool:
    """Fija <w:sz>/<w:szCs> de un run respetando el orden de CT_RPr. Devuelve si cambió."""
    tamano = int(medios_puntos)
    rPr = run.find(_qn("w:rPr"))
    if rPr is None:
        from docx.oxml import OxmlElement

        rPr = OxmlElement("w:rPr")
        run.insert(0, rPr)
    cambio = False
    for etiqueta in ("w:sz", "w:szCs"):
        nodo = rPr.find(_qn(etiqueta))
        if nodo is None:
            _rpr_propiedad(rPr, etiqueta.split(":")[1], True)
            nodo = rPr.find(_qn(etiqueta))
        if nodo.get(_qn("w:val")) != str(tamano):
            nodo.set(_qn("w:val"), str(tamano))
            cambio = True
    return cambio


def _ancho_texto_dxa(
    texto: str,
    tamano_pt: float,
    archivo_fuente: Optional[str] = None,
    negrita: bool = False,
) -> Optional[float]:
    """Mide el ancho de avance de un texto en dxa con las métricas reales de la fuente."""
    import os

    try:
        from PIL import ImageFont
    except ImportError:  # pragma: no cover - Pillow es dependencia del proyecto
        return None
    if archivo_fuente is None:
        archivo_fuente = "timesbd.ttf" if negrita else "times.ttf"
    ruta = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / archivo_fuente
    if not ruta.exists():
        return None
    fuente = ImageFont.truetype(str(ruta), 1000)
    return float(fuente.getlength(texto)) / 1000.0 * float(tamano_pt) * 20.0


def _fijar_margenes_celda(tc, izquierdo_dxa: int, derecho_dxa: int) -> None:
    """Fija <w:tcMar> laterales de una celda respetando el orden de CT_TcPr."""
    from docx.oxml import OxmlElement

    orden = ("w:top", "w:left", "w:bottom", "w:right")
    tcPr = tc.find(_qn("w:tcPr"))
    if tcPr is None:
        tcPr = OxmlElement("w:tcPr")
        tc.insert(0, tcPr)
    mar = tcPr.find(_qn("w:tcMar"))
    if mar is None:
        mar = OxmlElement("w:tcMar")
        posteriores = ("w:textDirection", "w:tcFitText", "w:vAlign", "w:hideMark")
        ancla = None
        for hijo in list(tcPr):
            if "w:" + hijo.tag.split("}")[1] in posteriores:
                ancla = hijo
                break
        if ancla is not None:
            ancla.addprevious(mar)
        else:
            tcPr.append(mar)
    for etiqueta, valor in (("w:left", izquierdo_dxa), ("w:right", derecho_dxa)):
        nodo = mar.find(_qn(etiqueta))
        if nodo is None:
            nodo = OxmlElement(etiqueta)
            posicion = orden.index(etiqueta)
            insertado = False
            for hijo in list(mar):
                nombre = "w:" + hijo.tag.split("}")[1]
                if nombre in orden and orden.index(nombre) > posicion:
                    hijo.addprevious(nodo)
                    insertado = True
                    break
            if not insertado:
                mar.append(nodo)
        nodo.set(_qn("w:w"), str(int(valor)))
        nodo.set(_qn("w:type"), "dxa")


def _margenes_actuales(tbl):
    """Devuelve los márgenes laterales de celda vigentes en la tabla (dxa)."""
    mar = tbl.find(_qn("w:tblPr") + "/" + _qn("w:tblCellMar")) if tbl.find(_qn("w:tblPr")) is not None else None
    izquierdo = derecho = None
    if mar is not None:
        for etiqueta in ("w:left", "w:right"):
            nodo = mar.find(_qn(etiqueta))
            if nodo is not None and nodo.get(_qn("w:w")):
                if etiqueta == "w:left":
                    izquierdo = int(nodo.get(_qn("w:w")))
                else:
                    derecho = int(nodo.get(_qn("w:w")))
    return (izquierdo if izquierdo is not None else 108, derecho if derecho is not None else 108)


def _tamano_parrafo(parrafo) -> float:
    for run in parrafo.iter(_qn("w:r")):
        rPr = run.find(_qn("w:rPr"))
        if rPr is not None:
            sz = rPr.find(_qn("w:sz"))
            if sz is not None and sz.get(_qn("w:val")):
                return int(sz.get(_qn("w:val"))) / 2.0
    return 11.0


def _parrafo_negrita(parrafo) -> bool:
    """Indica si el texto del párrafo se imprime en negrita (métrica distinta a redonda)."""
    for run in parrafo.iter(_qn("w:r")):
        if not "".join(t.text or "" for t in run.iter(_qn("w:t"))).strip():
            continue
        rPr = run.find(_qn("w:rPr"))
        if rPr is None:
            return False
        b = rPr.find(_qn("w:b"))
        if b is None:
            return False
        if b.get(_qn("w:val")) in ("0", "false", "off"):
            return False
        return True
    return False


def _tokens_columna(trs, columna: int, tamano_pt: Optional[float], centrada: bool):
    """Tokens indivisibles de una columna con el tamaño y el peso con que se imprimen."""
    tokens = []
    for posicion, tr in enumerate(trs):
        celdas = tr.findall(_qn("w:tc"))
        if columna >= len(celdas):
            continue
        for parrafo in celdas[columna].iter(_qn("w:p")):
            if tamano_pt is None:
                tamano = _tamano_parrafo(parrafo)
            elif posicion == 0 or centrada:
                tamano = tamano_pt
            else:
                tamano = _tamano_parrafo(parrafo)
            negrita = _parrafo_negrita(parrafo)
            texto = "".join(t.text or "" for t in parrafo.iter(_qn("w:t")))
            for linea in texto.split("\n"):
                for token in linea.split():
                    if token.strip():
                        tokens.append((token.strip(), tamano, negrita))
    return tokens


def _medir_columnas(trs, grid, margenes_dxa: int, tamano_pt: float, columnas_centradas):
    """Ancho mínimo requerido por columna y verificación del token más largo."""
    mediciones = []
    for columna, ancho in enumerate(grid):
        centrada = columna in columnas_centradas
        tokens = _tokens_columna(trs, columna, tamano_pt, centrada)
        medidas = [(t, tam, _ancho_texto_dxa(t, tam, negrita=n)) for t, tam, n in tokens]
        medidas = [m for m in medidas if m[2] is not None]
        util = ancho - 2 * margenes_dxa
        if medidas:
            token, tam, ancho_glifo = max(medidas, key=lambda m: m[2])
        else:
            token, tam, ancho_glifo = "", None, 0.0
        mediciones.append(
            {
                "columna": columna,
                "ancho_dxa": ancho,
                "ancho_util_dxa": util,
                "token_mas_largo": token,
                "tamano_token_pt": tam,
                "ancho_token_dxa": round(ancho_glifo, 1),
                "requerido_dxa": int(round(ancho_glifo)) + 2 * margenes_dxa + 8,
                "cabe": ancho_glifo <= util,
            }
        )
    return mediciones


def _rebalancear_columnas(tbl, grid, mediciones, relleno_dxa: int = 8):
    """Redistribuye anchos conservando el total: cubre déficits con excedentes."""
    requeridos = [max(m["requerido_dxa"] + max(0, relleno_dxa - 8), 240) for m in mediciones]
    total = sum(grid)
    if sum(requeridos) > total:
        return {"aplicado": False, "motivo": "Los requerimientos exceden el ancho total de la tabla", "anchos_nuevos": grid}
    deficits = [max(0, requeridos[i] - grid[i]) for i in range(len(grid))]
    if not any(deficits):
        return {"aplicado": False, "motivo": "Ninguna columna requiere ensanche", "anchos_nuevos": grid}
    excedentes = [max(0, grid[i] - requeridos[i]) for i in range(len(grid))]
    nuevos = list(grid)
    pendiente = sum(deficits)
    tomado = [0] * len(grid)
    for i in sorted(range(len(grid)), key=lambda j: (-excedentes[j], j)):
        if pendiente <= 0:
            break
        tomar = min(excedentes[i], pendiente)
        nuevos[i] -= tomar
        tomado[i] = tomar
        pendiente -= tomar
    if pendiente > 0:
        return {"aplicado": False, "motivo": "No hay excedente suficiente para cubrir los déficits", "anchos_nuevos": grid}
    for i in range(len(grid)):
        nuevos[i] += deficits[i]
    if sum(nuevos) != total:  # ajuste de redondeo
        nuevos[-1] += total - sum(nuevos)

    for col, ancho in zip(tbl.find(_qn("w:tblGrid")).findall(_qn("w:gridCol")), nuevos):
        col.set(_qn("w:w"), str(ancho))
    for tr in tbl.findall(_qn("w:tr")):
        for columna, tc in enumerate(tr.findall(_qn("w:tc"))):
            if columna >= len(nuevos):
                continue
            tcPr = tc.find(_qn("w:tcPr"))
            if tcPr is None:
                continue
            tcW = tcPr.find(_qn("w:tcW"))
            if tcW is None:
                continue
            tcW.set(_qn("w:w"), str(nuevos[columna]))
            tcW.set(_qn("w:type"), "dxa")
    return {
        "aplicado": True,
        "anchos_anteriores": grid,
        "anchos_nuevos": nuevos,
        "ensanchadas": [i for i in range(len(grid)) if deficits[i] > 0],
        "donantes": [i for i in range(len(grid)) if tomado[i] > 0],
    }


def ajustar_matriz_anexo(
    documento,
    indices_tabla: Sequence[int],
    margenes_dxa: int = 57,
    tamano_pt: float = 8.0,
    columnas_centradas: Optional[Sequence[int]] = None,
    aplicar_margenes: bool = True,
    rebalancear: bool = True,
) -> Dict[str, Any]:
    """
    Ajusta las matrices de datos de anexos (18 columnas) por geometría y no por texto:
    márgenes laterales de celda, 8 pt en cabecera y celdas numéricas, encabezado
    repetido, filas no fragmentables y columnas de ítems/puntajes centradas.
    Si un token indivisible excede el ancho útil, redistribuye los anchos columnales
    conservando el ancho total de la tabla. ``aplicar_margenes=False`` conserva los
    márgenes vigentes y deja el desborde exclusivamente al rebalanceo.

    Devuelve, por tabla, el ancho de columna, el ancho útil y la verificación del
    glifo más largo contra ese ancho útil.
    """
    acciones: List[Dict[str, Any]] = []
    detalle_tablas: List[Dict[str, Any]] = []
    tablas = documento.tables
    for indice in indices_tabla:
        if not 0 <= indice < len(tablas):
            raise IndexError(f"Índice de tabla {indice} fuera de rango (0..{len(tablas) - 1})")
        table = tablas[indice]
        tbl = table._tbl
        trs = tbl.findall(_qn("w:tr"))
        grid = [int(g.get(_qn("w:w"))) for g in tbl.find(_qn("w:tblGrid")).findall(_qn("w:gridCol"))]
        columnas = list(columnas_centradas) if columnas_centradas is not None else list(range(2, len(grid)))

        if aplicar_margenes:
            _fijar_margenes_celda_tabla(tbl, margenes_dxa, margenes_dxa)
        for posicion, tr in enumerate(trs):
            _preparar_tr(tr, cant_split=True, tbl_header=(posicion == 0))
            for columna, tc in enumerate(tr.findall(_qn("w:tc"))):
                if aplicar_margenes:
                    _fijar_margenes_celda(tc, margenes_dxa, margenes_dxa)
                if columna in columnas:
                    _fijar_alineacion_celda(tc, "center")
                if posicion == 0 or columna in columnas:
                    for run in tc.iter(_qn("w:r")):
                        if not "".join(t.text or "" for t in run.iter(_qn("w:t"))).strip():
                            continue
                        _fijar_tamano_run(run, int(round(tamano_pt * 2)))

        margen_izq, margen_der = _margenes_actuales(tbl)
        margenes_medicion = max(margen_izq, margen_der)
        medicion = _medir_columnas(trs, grid, margenes_medicion, tamano_pt, columnas)
        rebalanceo = (
            _rebalancear_columnas(tbl, grid, medicion, relleno_dxa=90)
            if rebalancear
            else {"aplicado": False, "motivo": "Rebalanceo desactivado por parametro", "anchos_nuevos": grid}
        )
        if rebalanceo["aplicado"]:
            grid = rebalanceo["anchos_nuevos"]
            medicion = _medir_columnas(trs, grid, margenes_medicion, tamano_pt, columnas)

        columnas_desbordadas = [m["columna"] for m in medicion if not m["cabe"]]
        detalle_tablas.append(
            {
                "indice_tabla": indice,
                "columnas": len(grid),
                "filas": len(trs),
                "ancho_tabla_dxa": sum(grid),
                "margenes_laterales_dxa": margenes_medicion,
                "via_geometria": "margenes+rebalanceo" if (aplicar_margenes and rebalancear) else ("margenes" if aplicar_margenes else "rebalanceo"),
                "tamano_pt": tamano_pt,
                "columnas_centradas": len(columnas),
                "rebalanceo": rebalanceo,
                "verificacion_glifos": medicion,
                "columnas_desbordadas": columnas_desbordadas,
                "cabe_sin_desborde": not columnas_desbordadas,
            }
        )
        acciones.append(
            {
                "categoria": "matriz_anexo_geometria",
                "tabla": indice,
                "estado": "corregido" if not columnas_desbordadas else "parcial",
                "detalle": (
                    (
                        f"margenes laterales de celda fijados en {margenes_dxa} dxa; "
                        if aplicar_margenes
                        else f"margenes laterales vigentes conservados ({margenes_medicion} dxa); "
                    )
                    + f"cabecera y celdas numericas a {tamano_pt} pt; {len(columnas)} columnas "
                    f"centradas; tblHeader y cantSplit; rebalanceo="
                    f"{'si' if rebalanceo['aplicado'] else 'no'}; via={detalle_tablas[-1]['via_geometria']}"
                ),
            }
        )
    return {"acciones": acciones, "tablas": detalle_tablas}


def rebalancear_tabla(
    documento,
    indices_tabla: Sequence[int],
    relleno_dxa: int = 8,
) -> Dict[str, Any]:
    """
    Rebalanceo geométrico genérico: mide el token indivisible más largo de cada
    columna con el tamaño tipográfico real y redistribuye anchos conservando el
    ancho total de la tabla. No altera texto, márgenes ni tamaños de fuente.
    """
    acciones: List[Dict[str, Any]] = []
    detalle_tablas: List[Dict[str, Any]] = []
    tablas = documento.tables
    for indice in indices_tabla:
        if not 0 <= indice < len(tablas):
            raise IndexError(f"Índice de tabla {indice} fuera de rango (0..{len(tablas) - 1})")
        tbl = tablas[indice]._tbl
        trs = tbl.findall(_qn("w:tr"))
        grid = [int(g.get(_qn("w:w"))) for g in tbl.find(_qn("w:tblGrid")).findall(_qn("w:gridCol"))]
        margen_izq, margen_der = _margenes_actuales(tbl)
        margenes = max(margen_izq, margen_der)
        antes = _medir_columnas(trs, grid, margenes, None, ())
        rebalanceo = _rebalancear_columnas(tbl, grid, antes, relleno_dxa=relleno_dxa)
        if rebalanceo["aplicado"]:
            grid = rebalanceo["anchos_nuevos"]
        despues = _medir_columnas(trs, grid, margenes, None, ())
        desbordadas = [m["columna"] for m in despues if not m["cabe"]]
        detalle_tablas.append(
            {
                "indice_tabla": indice,
                "columnas": len(grid),
                "filas": len(trs),
                "ancho_tabla_dxa": sum(grid),
                "margenes_laterales_dxa": margenes,
                "via_geometria": "rebalanceo",
                "rebalanceo": rebalanceo,
                "verificacion_glifos": despues,
                "columnas_desbordadas": desbordadas,
                "cabe_sin_desborde": not desbordadas,
            }
        )
        acciones.append(
            {
                "categoria": "tabla_rebalanceo",
                "tabla": indice,
                "estado": "corregido" if not desbordadas else "parcial",
                "detalle": (
                    f"rebalanceo={'si' if rebalanceo['aplicado'] else 'no'}; "
                    f"anchos {rebalanceo.get('anchos_anteriores', grid)} -> {grid}"
                ),
            }
        )
    return {"acciones": acciones, "tablas": detalle_tablas}


def actualizar_nota_tabla(table, texto: str, tamano_pt: float = 9.5) -> bool:
    """
    Actualiza la nota inmediatamente posterior a la tabla conservando el prefijo
    «Nota.» en cursiva (TNR 9.5-10 pt, interlineado sencillo).
    """
    from docx.oxml import OxmlElement

    tbl = table._tbl
    hermana = tbl.getnext()
    if hermana is None or not hermana.tag.endswith("}p"):
        return False
    texto_actual = "".join(t.text or "" for t in hermana.iter(_qn("w:t")))
    if not texto_actual.lstrip().startswith("Nota."):
        return False

    runs = hermana.findall(_qn("w:r"))
    if not runs:
        return False
    prefijo = runs[0]
    for extra in runs[1:]:
        hermana.remove(extra)
    cuerpo = OxmlElement("w:r")
    rPr_ref = prefijo.find(_qn("w:rPr"))
    if rPr_ref is not None:
        from copy import deepcopy

        cuerpo.append(deepcopy(rPr_ref))
        i = cuerpo.find(_qn("w:rPr")).find(_qn("w:i"))
        if i is not None:
            cuerpo.find(_qn("w:rPr")).remove(i)
    t = OxmlElement("w:t")
    t.text = texto
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    cuerpo.append(t)
    hermana.append(cuerpo)

    pPr = hermana.find(_qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        hermana.insert(0, pPr)
    sp = pPr.find(_qn("w:spacing"))
    if sp is None:
        sp = OxmlElement("w:spacing")
        pPr.insert(0, sp)
    sp.set(_qn("w:line"), "240")
    sp.set(_qn("w:lineRule"), "auto")
    return True


_ORDEN_RPR = (
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike", "dstrike",
    "outline", "shadow", "emboss", "imprint", "noProof", "snapToGrid", "vanish", "webHidden",
    "color", "spacing", "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect",
    "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout",
    "specVanish", "oMath",
)


def _rpr_propiedad(rPr, etiqueta: str, activa: bool = True):
    """Activa o elimina una propiedad de <w:rPr> respetando el orden del esquema CT_RPr."""
    from docx.oxml import OxmlElement

    actual = rPr.find(_qn(f"w:{etiqueta}"))
    if not activa:
        if actual is not None:
            rPr.remove(actual)
        return None
    if actual is not None:
        return actual
    nuevo = OxmlElement(f"w:{etiqueta}")
    if etiqueta not in _ORDEN_RPR:
        rPr.append(nuevo)
        return nuevo
    limite = _ORDEN_RPR.index(etiqueta)
    for hijo in rPr:
        nombre = hijo.tag.split("}")[-1]
        if nombre in _ORDEN_RPR and _ORDEN_RPR.index(nombre) > limite:
            hijo.addprevious(nuevo)
            return nuevo
    rPr.append(nuevo)
    return nuevo


def _texto_parrafo(p) -> str:
    """Texto de un <w:p> uniendo solo los <w:t> (evita la triple lectura de python-docx)."""
    return "".join(t.text or "" for t in p.iter(_qn("w:t")))


def _parrafo_con_imagen(p) -> bool:
    return p is not None and p.tag == _qn("w:p") and p.find(".//" + _qn("w:drawing")) is not None


def _es_rotulo(p) -> bool:
    import re as _re

    if p is None or p.tag != _qn("w:p"):
        return False
    pPr = p.find(_qn("w:pPr"))
    if pPr is not None:
        if pPr.find(_qn("w:outlineLvl")) is not None:
            return False
        pStyle = pPr.find(_qn("w:pStyle"))
        if pStyle is not None and pStyle.get(_qn("w:val")) == "Tabladeilustraciones":
            return False
    return bool(_re.match(r"^(Figura|Tabla)\s+\d+", _texto_parrafo(p).strip()))


def reordenar_figuras_apa7(documento, desde: int = 11, hasta: int = 48) -> List[Dict[str, Any]]:
    """
    Coloca la imagen entre el rótulo y la nota (orden APA 7) en las figuras indicadas.
    Mueve el párrafo con el <w:drawing> sin duplicarlo ni eliminarlo.
    """
    import re as _re

    cuerpo = documento.element.body
    acciones: List[Dict[str, Any]] = []
    for indice, elemento in enumerate(list(cuerpo)):
        if not _es_rotulo(elemento):
            continue
        coincidencia = _re.match(r"^Figura\s+(\d+)", _texto_parrafo(elemento).strip())
        if not coincidencia:
            continue
        numero = int(coincidencia.group(1))
        if not desde <= numero <= hasta:
            continue
        previo = elemento.getprevious()
        if not _parrafo_con_imagen(previo):
            continue
        elemento.addnext(previo)
        acciones.append(
            {
                "categoria": "orden_figura_rotulo",
                "parrafo": indice,
                "figura": numero,
                "estado": "corregido",
                "detalle": "imagen movida delante del rótulo al espacio entre rótulo y nota",
            }
        )
    return acciones


def normalizar_rotulos_ilustracion(
    documento,
    estilo: str = "Rotulodeilustracion",
    figuras_excluidas: Sequence[int] = (49, 50, 51, 52),
) -> List[Dict[str, Any]]:
    """
    Aplica el estilo institucional de rótulo y fija la etiqueta y el número en negrita
    y el título descriptivo en cursiva, sin sangría.
    """
    import re as _re

    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml import OxmlElement

    estilos = documento.styles
    existentes = {s.name: s for s in estilos}
    if "Rotulo de ilustracion" in existentes:
        estilo_objeto = existentes["Rotulo de ilustracion"]
    else:
        estilo_objeto = estilos.add_style("Rotulo de ilustracion", WD_STYLE_TYPE.PARAGRAPH)
        estilo_objeto.base_style = estilos["Normal"]
        estilo_objeto.quick_style = True
        pPr = estilo_objeto.element.get_or_add_pPr()
        keep = OxmlElement("w:keepNext")
        pPr.append(keep)
        ind = OxmlElement("w:ind")
        ind.set(_qn("w:firstLine"), "0")
        ind.set(_qn("w:left"), "0")
        pPr.append(ind)
        rPr = estilo_objeto.element.get_or_add_rPr()
        fuentes = OxmlElement("w:rFonts")
        for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
            fuentes.set(_qn(atributo), "Times New Roman")
        rPr.append(fuentes)

    acciones: List[Dict[str, Any]] = []
    for indice, elemento in enumerate(list(documento.element.body)):
        if not _es_rotulo(elemento):
            continue
        texto = _texto_parrafo(elemento).strip()
        coincidencia = _re.match(r"^(Figura|Tabla)\s+(\d+)", texto)
        if not coincidencia:
            continue
        tipo, numero = coincidencia.group(1), int(coincidencia.group(2))
        if tipo == "Figura" and numero in set(figuras_excluidas):
            continue

        runs = elemento.findall(_qn("w:r"))
        fin_campo = None
        for pos, run in enumerate(runs):
            fld = run.find(_qn("w:fldChar"))
            if fld is not None and fld.get(_qn("w:fldCharType")) == "end":
                fin_campo = pos
        if fin_campo is None:
            continue
        etiqueta, numero_run, titulo = runs[0], runs[fin_campo - 1], runs[fin_campo + 1:]
        cambios = []

        for run in (etiqueta, numero_run):
            rPr = run.find(_qn("w:rPr"))
            if rPr is None:
                rPr = OxmlElement("w:rPr")
                run.insert(0, rPr)
            if rPr.find(_qn("w:b")) is None:
                _rpr_propiedad(rPr, "b", True)
                cambios.append("negrita")
        for run in titulo:
            if not _texto_parrafo(run).strip() and run.find(_qn("w:t")) is None:
                continue
            rPr = run.find(_qn("w:rPr"))
            if rPr is None:
                rPr = OxmlElement("w:rPr")
                run.insert(0, rPr)
            if rPr.find(_qn("w:i")) is None:
                _rpr_propiedad(rPr, "i", True)
                cambios.append("cursiva")
            if rPr.find(_qn("w:b")) is not None:
                _rpr_propiedad(rPr, "b", False)
                cambios.append("negrita_retirada_titulo")

        parrafo = None
        for p in documento.paragraphs:
            if p._p is elemento:
                parrafo = p
                break
        if parrafo is not None:
            parrafo.style = estilo_objeto
            cambios.append("estilo")

        acciones.append(
            {
                "categoria": "rotulo_formato",
                "parrafo": indice,
                "rotulo": f"{tipo} {numero}",
                "estado": "corregido" if cambios else "sin_cambios",
                "detalle": ", ".join(dict.fromkeys(cambios)),
            }
        )
    return acciones


def insertar_prefijo_notas(documento) -> List[Dict[str, Any]]:
    """
    Antepone «Nota.» en cursiva a las notas de tabla que carecen del prefijo,
    conservando su tamaño (9.5-10 pt) e interlineado sencillo.
    """
    from docx.oxml import OxmlElement

    cuerpo = documento.element.body
    acciones: List[Dict[str, Any]] = []
    indice_tabla = 0
    for elemento in list(cuerpo):
        if elemento.tag != _qn("w:tbl"):
            continue
        indice_tabla += 1
        siguiente = elemento.getnext()
        if siguiente is None or siguiente.tag != _qn("w:p"):
            continue
        texto = _texto_parrafo(siguiente).strip()
        if not texto or texto.startswith("Nota."):
            continue
        tamanos = set()
        for run in siguiente.iter(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            if rPr is not None and rPr.find(_qn("w:sz")) is not None:
                tamanos.add(rPr.find(_qn("w:sz")).get(_qn("w:val")))
        pPr = siguiente.find(_qn("w:pPr"))
        linea = None
        if pPr is not None and pPr.find(_qn("w:spacing")) is not None:
            linea = pPr.find(_qn("w:spacing")).get(_qn("w:line"))
        if not tamanos or not tamanos <= {"19", "20"} or linea != "240":
            continue
        if texto.startswith(("Figura", "Tabla")):
            continue

        prefijo = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        fuentes = OxmlElement("w:rFonts")
        for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
            fuentes.set(_qn(atributo), "Times New Roman")
        rPr.append(fuentes)
        rPr.append(OxmlElement("w:i"))
        sz = OxmlElement("w:sz")
        sz.set(_qn("w:val"), sorted(tamanos)[0])
        rPr.append(sz)
        szcs = OxmlElement("w:szCs")
        szcs.set(_qn("w:val"), sorted(tamanos)[0])
        rPr.append(szcs)
        prefijo.append(rPr)
        t = OxmlElement("w:t")
        t.text = "Nota. "
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        prefijo.append(t)
        if pPr is not None:
            pPr.addnext(prefijo)
        else:
            siguiente.insert(0, prefijo)
        acciones.append(
            {
                "categoria": "nota_sin_prefijo",
                "tabla": indice_tabla,
                "parrafo": list(cuerpo).index(siguiente),
                "estado": "corregido",
                "detalle": "prefijo Nota. en cursiva insertado; texto original intacto",
            }
        )
    return acciones


def _normalizar_referencia(texto: str) -> str:
    """Minúsculas, sin acentos ni puntuación, para comparar y ordenar referencias."""
    import re as _re
    import unicodedata

    descompuesto = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    return _re.sub(r"[^a-z0-9]+", " ", sin_acentos.lower()).strip()


def _clave_referencia(texto: str) -> str:
    """Clave autor-año para detectar duplicados bibliográficos."""
    import re as _re

    coincidencia = _re.match(r"^(.{1,90}?)\s*\((\d{4})[a-z]?\)", texto)
    if coincidencia:
        return _normalizar_referencia(coincidencia.group(1)) + "|" + coincidencia.group(2)
    return _normalizar_referencia(texto)[:60]


def _parrafos_referencia(documento):
    """Párrafos de la lista final: sangría francesa de 720 dxa."""
    from docx.text.paragraph import Paragraph

    salida = []
    for p in documento.paragraphs:
        pPr = p._p.find(_qn("w:pPr"))
        ind = pPr.find(_qn("w:ind")) if pPr is not None else None
        if ind is not None and ind.get(_qn("w:hanging")) == "720":
            salida.append(p)
    return salida


def _crear_parrafo_referencia(texto: str):
    """Crea <w:p> con sangría francesa 720/720, interlineado 360, TNR 12 pt y justificado."""
    from docx.oxml import OxmlElement

    p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    sp = OxmlElement("w:spacing")
    sp.set(_qn("w:before"), "0")
    sp.set(_qn("w:after"), "120")
    sp.set(_qn("w:line"), "360")
    sp.set(_qn("w:lineRule"), "auto")
    pPr.append(sp)
    ind = OxmlElement("w:ind")
    ind.set(_qn("w:left"), "720")
    ind.set(_qn("w:hanging"), "720")
    pPr.append(ind)
    jc = OxmlElement("w:jc")
    jc.set(_qn("w:val"), "both")
    pPr.append(jc)
    p.append(pPr)

    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    fuentes = OxmlElement("w:rFonts")
    for atributo in ("w:ascii", "w:hAnsi", "w:cs"):
        fuentes.set(_qn(atributo), "Times New Roman")
    rPr.append(fuentes)
    sz = OxmlElement("w:sz")
    sz.set(_qn("w:val"), "24")
    rPr.append(sz)
    szcs = OxmlElement("w:szCs")
    szcs.set(_qn("w:val"), "24")
    rPr.append(szcs)
    run.append(rPr)
    t = OxmlElement("w:t")
    t.text = texto
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    run.append(t)
    p.append(run)
    return p


def insertar_referencias(documento, inserciones: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Inserta referencias completas en la lista final, inmediatamente después de su
    ancla alfabética. Se ejecuta al final de la pasada para no desplazar índices.
    No reescribe ninguna referencia existente.
    """
    from docx.text.paragraph import Paragraph

    acciones: List[Dict[str, Any]] = []
    referencias = _parrafos_referencia(documento)
    claves = {_clave_referencia(p.text.strip()): p.text.strip()[:60] for p in referencias}
    orden_inicial = [_normalizar_referencia(p.text) for p in referencias]
    inversiones_iniciales = [
        (i, orden_inicial[i][:40], orden_inicial[i + 1][:40])
        for i in range(len(orden_inicial) - 1)
        if orden_inicial[i] > orden_inicial[i + 1]
    ]

    parrafos = list(documento.paragraphs)
    anterior = None
    for orden, insercion in enumerate(inserciones, 1):
        texto = insercion["texto"].strip()
        clave = _clave_referencia(texto)
        duplicada = clave in claves
        if insercion.get("encadenada") and anterior is not None:
            ancla = anterior
            criterio = "despues_de_insercion_previa"
        else:
            indice = insercion.get("ancla_indice")
            prefijo = _normalizar_referencia(insercion.get("ancla_texto", ""))
            candidato = parrafos[indice] if isinstance(indice, int) and 0 <= indice < len(parrafos) else None
            if candidato is not None and not _normalizar_referencia(candidato.text).startswith(prefijo):
                candidato = None
            if candidato is None and prefijo:
                candidato = next(
                    (p for p in parrafos if _normalizar_referencia(p.text).startswith(prefijo)),
                    None,
                )
            if candidato is None:
                raise ValueError(f"No se encontro el ancla de la referencia {orden}: {insercion.get('ancla_texto')}")
            ancla = candidato
            criterio = "ancla_alfabetica"

        nuevo = _crear_parrafo_referencia(texto)
        ancla._p.addnext(nuevo)
        anterior = Paragraph(nuevo, ancla._parent)
        claves[clave] = texto[:60]
        acciones.append(
            {
                "categoria": "referencia_insertada",
                "orden": orden,
                "ancla": insercion.get("ancla_texto", ""),
                "criterio": criterio,
                "referencia": texto[:90],
                "clave": clave,
                "duplicada": duplicada,
                "estado": "insertada",
            }
        )

    finales = _parrafos_referencia(documento)
    orden_final = [_normalizar_referencia(p.text) for p in finales]
    inversiones_finales = [
        (i, finales[i].text[:45], finales[i + 1].text[:45])
        for i in range(len(finales) - 1)
        if orden_final[i] > orden_final[i + 1]
    ]
    claves_finales = [_clave_referencia(p.text.strip()) for p in finales]
    duplicadas = sorted({c for c in claves_finales if claves_finales.count(c) > 1})
    return {
        "acciones": acciones,
        "entradas_antes": len(referencias),
        "entradas_despues": len(finales),
        "inversiones_antes": inversiones_iniciales,
        "inversiones_despues": inversiones_finales,
        "orden_alfabetico_conservado": not inversiones_finales,
        "claves_duplicadas": duplicadas,
    }


def _reemplazar_texto_parrafo(p, viejo: str, nuevo: str, maximo: Optional[int] = 1) -> int:
    """
    Sustituye un texto dentro de un párrafo conservando el formato de los runs.
    Devuelve el número de sustituciones efectivas.
    """
    if not viejo:
        return 0
    elemento = getattr(p, "_p", p)
    limite = maximo if maximo else 10 ** 6
    aplicadas = 0
    while aplicadas < limite:
        nodos = [t for t in elemento.iter(_qn("w:t"))]
        if not nodos:
            return aplicadas
        offsets = []
        acumulado = 0
        for nodo in nodos:
            texto_nodo = nodo.text or ""
            offsets.append((acumulado, acumulado + len(texto_nodo)))
            acumulado += len(texto_nodo)
        texto = "".join(nodo.text or "" for nodo in nodos)
        posicion = texto.find(viejo)
        if posicion < 0:
            return aplicadas
        fin = posicion + len(viejo)
        afectados = [
            i for i, (inicio, termino) in enumerate(offsets)
            if max(inicio, posicion) < min(termino, fin)
        ]
        if not afectados:
            return aplicadas
        primero, ultimo = afectados[0], afectados[-1]
        prefijo = (nodos[primero].text or "")[: posicion - offsets[primero][0]]
        if primero == ultimo:
            sufijo = (nodos[primero].text or "")[fin - offsets[primero][0]:]
            nodos[primero].text = prefijo + nuevo + sufijo
        else:
            nodos[primero].text = prefijo + nuevo
            for indice in afectados[1:-1]:
                nodos[indice].text = ""
            nodos[ultimo].text = (nodos[ultimo].text or "")[fin - offsets[ultimo][0]:]
        for nodo in nodos:
            if nodo.text and (nodo.text != nodo.text.strip() or "  " in nodo.text):
                nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        aplicadas += 1
    return aplicadas


def _texto_normalizado(texto: str) -> str:
    import re as _re

    return _re.sub(r"\s+", " ", texto).strip()


def _reemplazar_flexible(p, viejo: str, nuevo: str, maximo: Optional[int] = 1) -> int:
    """
    Sustituye un texto aunque el ancla use espacios donde el párrafo tiene saltos de
    línea. Si el reemplazo literal falla, aplica solo los tramos que difieren,
    conservando los saltos y el formato del resto del párrafo.
    """
    aplicadas = _reemplazar_texto_parrafo(p, viejo, nuevo, maximo)
    if aplicadas or not viejo or not nuevo:
        return aplicadas
    import difflib

    comparador = difflib.SequenceMatcher(None, viejo, nuevo, autojunk=False)
    tramos = []
    actual = None
    for etiqueta, i1, i2, j1, j2 in comparador.get_opcodes():
        if etiqueta == "equal":
            if actual is not None and (i2 - i1) < 5:
                continue
            if actual is not None:
                tramos.append(actual)
                actual = None
            continue
        if actual is None:
            actual = [i1, i2, j1, j2]
        else:
            actual[1], actual[3] = i2, j2
    if actual is not None:
        tramos.append(actual)

    texto = p.text
    total = 0
    for i1, i2, j1, j2 in tramos:
        viejo_tramo, nuevo_tramo = viejo[i1:i2], nuevo[j1:j2]
        if not viejo_tramo or texto.count(viejo_tramo) != 1:
            return total
        if _reemplazar_texto_parrafo(p, viejo_tramo, nuevo_tramo, 1) != 1:
            return total
        total += 1
    return total


def _buscar_unico(documento, viejo: str):
    """Devuelve el párrafo único que contiene el ancla, o None si hay cero o varias."""
    objetivo = _texto_normalizado(viejo)
    candidatos = [p for p in documento.paragraphs if objetivo in _texto_normalizado(p.text)]
    return candidatos[0] if len(candidatos) == 1 else None


_ESPACIOS_COLA = " \t "


def sanear_espacios_finales(documento) -> Dict[str, Any]:
    """
    Recorta los espacios y tabuladores residuales de la cola del texto de cada
    párrafo del cuerpo. Actúa sobre el último run con texto y sobre los runs
    posteriores que solo contengan espacios, sin eliminar runs ni alterar el
    formato. Los párrafos cuyo texto íntegro sea espacio en blanco no se tocan.
    """
    acciones: List[Dict[str, Any]] = []
    for indice, parrafo in enumerate(documento.paragraphs):
        elemento = getattr(parrafo, "_p", parrafo)
        runs = [r for r in elemento.findall(_qn("w:r")) if r.find(_qn("w:t")) is not None]
        if not runs:
            continue
        texto_parrafo = "".join(
            t.text or "" for r in runs for t in r.findall(_qn("w:t"))
        )
        if not texto_parrafo or not texto_parrafo.strip():
            continue

        ultimo_con_texto = None
        for run in runs:
            if any((t.text or "").strip(_ESPACIOS_COLA) for t in run.findall(_qn("w:t"))):
                ultimo_con_texto = run
        if ultimo_con_texto is None:
            continue

        recortado = 0
        nodos = ultimo_con_texto.findall(_qn("w:t"))
        for nodo in reversed(nodos):
            actual = nodo.text or ""
            limpio = actual.rstrip(_ESPACIOS_COLA)
            if limpio != actual:
                recortado += len(actual) - len(limpio)
                nodo.text = limpio
                nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            if limpio:
                break

        posteriores = runs[runs.index(ultimo_con_texto) + 1:]
        for run in posteriores:
            for nodo in run.findall(_qn("w:t")):
                actual = nodo.text or ""
                if actual and not actual.strip(_ESPACIOS_COLA):
                    recortado += len(actual)
                    nodo.text = ""
                    nodo.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

        if recortado:
            acciones.append(
                {
                    "categoria": "saneamiento_espacios_finales",
                    "parrafo": indice,
                    "caracteres_recortados": recortado,
                    "estado": "corregido",
                }
            )
    return {
        "acciones": acciones,
        "parrafos_saneados": len(acciones),
        "indices": [a["parrafo"] for a in acciones],
        "caracteres_recortados": sum(a["caracteres_recortados"] for a in acciones),
    }


def aplicar_ordenes_edicion(
    ruta_origen: Union[str, Path],
    lotes: Sequence[Tuple[str, Dict[str, Any]]],
    ruta_destino: Optional[Union[str, Path]] = None,
    solo_verificar: bool = False,
    tablas_matriz: Sequence[int] = (),
    margenes_matriz_dxa: int = 57,
    tamano_matriz_pt: float = 8.0,
    via_matriz: str = "rebalanceo",
    tablas_rebalanceo: Sequence[int] = (),
    sanear_espacios: bool = False,
) -> Dict[str, Any]:
    """
    Aplica lotes de órdenes de sustitución sobre un DOCX sin insertar ni eliminar
    párrafos. Cada orden se direcciona por índice base 0 de párrafo o de tabla
    (fila y columna base 1, con encabezado incluido). En modo ``solo_verificar``
    no escribe archivo alguno y reporta qué órdenes se aplicarían.

    ``via_matriz`` elige una sola vía geométrica para las matrices de anexos:
    ``margenes`` (tcMar), ``rebalanceo`` (anchos columnares) o ``ambas``.
    ``tablas_rebalanceo`` rebalancea tablas adicionales conservando su ancho total.
    """
    import re as _re

    import docx

    if via_matriz not in ("margenes", "rebalanceo", "ambas"):
        raise ValueError("via_matriz debe ser 'margenes', 'rebalanceo' o 'ambas'")

    origen = Path(ruta_origen)
    documento = docx.Document(str(origen))
    acciones: List[Dict[str, Any]] = []
    resumen_lotes: List[Dict[str, Any]] = []

    matrices: Dict[str, Any] = {"acciones": [], "tablas": []}
    if tablas_matriz and not solo_verificar:
        matrices = ajustar_matriz_anexo(
            documento,
            tablas_matriz,
            margenes_dxa=margenes_matriz_dxa,
            tamano_pt=tamano_matriz_pt,
            aplicar_margenes=via_matriz in ("margenes", "ambas"),
            rebalancear=via_matriz in ("rebalanceo", "ambas"),
        )
        acciones += matrices["acciones"]

    rebalanceos: Dict[str, Any] = {"acciones": [], "tablas": []}
    if tablas_rebalanceo and not solo_verificar:
        rebalanceos = rebalancear_tabla(documento, tablas_rebalanceo)
        acciones += rebalanceos["acciones"]

    for nombre, datos in lotes:
        ordenes = datos.get("sustituciones", datos if isinstance(datos, list) else [])
        aplicadas = 0
        fallidas = 0
        detalles = []
        for orden in ordenes:
            viejo = orden.get("ancla_original", "")
            nuevo = orden.get("texto_nuevo", "")
            ocurrencias = orden.get("ocurrencias") or 1
            ubicacion = orden.get("ubicacion") or ""
            indice = orden.get("indice_docx")
            modo = "indice"
            aplicadas_orden = 0

            coincidencia_tabla = _re.match(r"TABLA\s+(\d+),\s*fila\s+(\d+),\s*columna\s+(\d+)", ubicacion)
            if coincidencia_tabla:
                numero_tabla = int(coincidencia_tabla.group(1))
                fila, columna = int(coincidencia_tabla.group(2)), int(coincidencia_tabla.group(3))
                objetivo = _texto_normalizado(viejo)
                candidatas = []
                if 0 <= numero_tabla < len(documento.tables):
                    candidatas.append(documento.tables[numero_tabla])
                if isinstance(indice, int) and 0 <= indice < len(documento.tables):
                    if not candidatas or documento.tables[indice] is not candidatas[0]:
                        candidatas.append(documento.tables[indice])
                celda = None
                for tabla in candidatas:
                    if fila - 1 >= len(tabla.rows):
                        continue
                    fila_celdas = tabla.rows[fila - 1].cells
                    if columna - 1 < len(fila_celdas):
                        posible = fila_celdas[columna - 1]
                        if objetivo in _texto_normalizado(posible.text):
                            celda = posible
                            break
                    encontradas = [c for c in fila_celdas if objetivo in _texto_normalizado(c.text)]
                    if len(encontradas) == 1:
                        celda = encontradas[0]
                        modo = "celda_reubicada"
                        break
                if celda is None and objetivo:
                    ubicaciones = []
                    for tabla in documento.tables:
                        for row in tabla.rows:
                            for c in row.cells:
                                if objetivo in _texto_normalizado(c.text):
                                    ubicaciones.append(c)
                    if len(ubicaciones) == 1:
                        celda = ubicaciones[0]
                        modo = "celda_reubicada"
                if celda is not None:
                    for parrafo in celda.paragraphs:
                        if _texto_normalizado(viejo) in _texto_normalizado(parrafo.text):
                            aplicadas_orden += _reemplazar_flexible(parrafo, viejo, nuevo, ocurrencias)
                if aplicadas_orden == 0:
                    modo = "fallida"
            else:
                if isinstance(indice, int) and 0 <= indice < len(documento.paragraphs):
                    parrafo = documento.paragraphs[indice]
                    if _texto_normalizado(viejo) in _texto_normalizado(parrafo.text):
                        aplicadas_orden = _reemplazar_flexible(parrafo, viejo, nuevo, ocurrencias)
                if aplicadas_orden == 0:
                    unico = _buscar_unico(documento, viejo) if viejo else None
                    if unico is not None:
                        aplicadas_orden = _reemplazar_flexible(unico, viejo, nuevo, ocurrencias)
                        modo = "busqueda_unica"
                    else:
                        modo = "fallida"

            if aplicadas_orden:
                aplicadas += 1
            else:
                fallidas += 1
            detalles.append(
                {
                    "indice_docx": indice,
                    "ubicacion": ubicacion or None,
                    "ancla": viejo[:80],
                    "sustituciones": aplicadas_orden,
                    "modo": modo,
                    "estado": "aplicada" if aplicadas_orden else "fallida",
                }
            )
        acciones.extend(
            {
                "categoria": "orden_edicion",
                "lote": nombre,
                "indice_docx": d["indice_docx"],
                "ubicacion": d["ubicacion"],
                "estado": d["estado"],
                "detalle": f"{d['sustituciones']} sustitucion(es); modo {d['modo']}",
            }
            for d in detalles
        )
        resumen_lotes.append(
            {
                "lote": nombre,
                "total": len(ordenes),
                "aplicadas": aplicadas,
                "fallidas": fallidas,
                "detalles": detalles,
            }
        )

    saneamiento: Dict[str, Any] = {"acciones": [], "parrafos_saneados": 0, "indices": [], "caracteres_recortados": 0}
    if sanear_espacios:
        saneamiento = sanear_espacios_finales(documento)
        acciones += saneamiento["acciones"]

    destino = None
    sha_destino = None
    if not solo_verificar:
        if ruta_destino is None:
            raise ValueError("Se requiere ruta_destino cuando solo_verificar es False")
        destino = Path(ruta_destino)
        seguridad.asegurar_no_sobrescribe(origen, destino)
        seguridad.asegurar_escritura_permitida(destino)
        documento.save(str(destino))
        sha_destino = seguridad.sha256_archivo(destino)

    verificacion = docx.Document(str(destino)) if destino is not None else documento
    return {
        "origen": str(origen),
        "destino": str(destino) if destino else None,
        "solo_verificar": solo_verificar,
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_destino": sha_destino,
        "parrafos": len(verificacion.paragraphs),
        "tablas": len(verificacion.tables),
        "total_ordenes": sum(r["total"] for r in resumen_lotes),
        "total_aplicadas": sum(r["aplicadas"] for r in resumen_lotes),
        "total_fallidas": sum(r["fallidas"] for r in resumen_lotes),
        "lotes": resumen_lotes,
        "matrices_anexo": matrices["tablas"],
        "tablas_rebalanceadas": rebalanceos["tablas"],
        "saneamiento_espacios": saneamiento,
        "acciones": acciones,
    }


def detectar_duplicados_editoriales(documento, ventana: int = 60) -> Dict[str, Any]:
    """
    Verificación previa/posterior de las categorías 2 y 3 de la auditoría:
    bloque duplicado por doble orilla literal y encabezados consecutivos repetidos.
    """
    cuerpo = documento.element.body
    con_cola = []
    consecutivos = []
    anterior = None
    for indice, elemento in enumerate(list(cuerpo)):
        if elemento.tag != _qn("w:p"):
            anterior = None
            continue
        texto = _texto_parrafo(elemento).strip()
        if len(texto) >= 2 * ventana and texto[:ventana] == texto[-ventana:]:
            con_cola.append({"parrafo": indice, "orilla": texto[:ventana]})
        pPr = elemento.find(_qn("w:pPr"))
        nivel = pPr.find(_qn("w:outlineLvl")) if pPr is not None else None
        if nivel is not None and texto:
            if anterior is not None and anterior[1] == texto:
                consecutivos.append({"parrafo": indice, "texto": texto[:80]})
            anterior = (indice, texto)
        else:
            anterior = None
    return {"bloques_duplicados": con_cola, "encabezados_consecutivos_repetidos": consecutivos}


def contadores_estructurales(documento) -> Dict[str, int]:
    """Cuenta las categorías auditadas para el antes/después del reporte."""
    import re as _re

    cuerpo = documento.element.body
    imagen_antes = 0
    sin_estilo = 0
    total_rotulos = 0
    for elemento in list(cuerpo):
        if not _es_rotulo(elemento):
            continue
        total_rotulos += 1
        pPr = elemento.find(_qn("w:pPr"))
        if pPr is None or pPr.find(_qn("w:pStyle")) is None:
            sin_estilo += 1
        if _re.match(r"^Figura\s+(1[1-9]|[2-4]\d)\b", _texto_parrafo(elemento).strip()):
            if _parrafo_con_imagen(elemento.getprevious()):
                imagen_antes += 1
    notas_sin_prefijo = 0
    for elemento in list(cuerpo):
        if elemento.tag != _qn("w:tbl"):
            continue
        siguiente = elemento.getnext()
        if siguiente is None or siguiente.tag != _qn("w:p"):
            continue
        texto = _texto_parrafo(siguiente).strip()
        if not texto or texto.startswith(("Nota.", "Figura", "Tabla")):
            continue
        tamanos = set()
        for run in siguiente.iter(_qn("w:r")):
            rPr = run.find(_qn("w:rPr"))
            if rPr is not None and rPr.find(_qn("w:sz")) is not None:
                tamanos.add(rPr.find(_qn("w:sz")).get(_qn("w:val")))
        pPr = siguiente.find(_qn("w:pPr"))
        linea = None
        if pPr is not None and pPr.find(_qn("w:spacing")) is not None:
            linea = pPr.find(_qn("w:spacing")).get(_qn("w:line"))
        if tamanos and tamanos <= {"19", "20"} and linea == "240":
            notas_sin_prefijo += 1
    return {
        "rotulos_total": total_rotulos,
        "rotulos_sin_estilo": sin_estilo,
        "figuras_imagen_antes_del_rotulo": imagen_antes,
        "notas_sin_prefijo": notas_sin_prefijo,
    }


def corregir_estructura_editorial(
    ruta_origen: Union[str, Path],
    ruta_destino: Union[str, Path],
    figuras_desde: int = 11,
    figuras_hasta: int = 48,
    figuras_excluidas: Sequence[int] = (49, 50, 51, 52),
    tablas_matriz: Sequence[int] = (),
    margenes_matriz_dxa: int = 57,
    tamano_matriz_pt: float = 8.0,
    referencias: Sequence[Dict[str, Any]] = (),
    sanear_espacios: bool = False,
) -> Dict[str, Any]:
    """
    Pasada única y trazable de corrección estructural APA 7 sobre un informe:
    orden figura/rótulo, formato y estilo de rótulos, prefijo de notas de tabla,
    ajuste geométrico de las matrices de datos de anexos y, opcionalmente,
    recorte de espacios residuales de cola.
    No crea texto, no altera tablas de datos ni referencias.
    """
    import docx

    origen = Path(ruta_origen)
    destino = Path(ruta_destino)
    seguridad.asegurar_no_sobrescribe(origen, destino)
    seguridad.asegurar_escritura_permitida(destino)

    documento = docx.Document(str(origen))
    antes = contadores_estructurales(documento)
    duplicados_antes = detectar_duplicados_editoriales(documento)

    acciones = []
    acciones += reordenar_figuras_apa7(documento, figuras_desde, figuras_hasta)
    acciones += normalizar_rotulos_ilustracion(documento, figuras_excluidas=figuras_excluidas)
    acciones += insertar_prefijo_notas(documento)
    matrices: Dict[str, Any] = {"acciones": [], "tablas": []}
    if tablas_matriz:
        matrices = ajustar_matriz_anexo(
            documento,
            tablas_matriz,
            margenes_dxa=margenes_matriz_dxa,
            tamano_pt=tamano_matriz_pt,
        )
        acciones += matrices["acciones"]
    resultado_referencias: Dict[str, Any] = {}
    if referencias:
        resultado_referencias = insertar_referencias(documento, referencias)
        acciones += resultado_referencias["acciones"]
    saneamiento: Dict[str, Any] = {"acciones": [], "parrafos_saneados": 0, "indices": [], "caracteres_recortados": 0}
    if sanear_espacios:
        saneamiento = sanear_espacios_finales(documento)
        acciones += saneamiento["acciones"]

    destino.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(destino))

    verificacion = docx.Document(str(destino))
    despues = contadores_estructurales(verificacion)
    duplicados_despues = detectar_duplicados_editoriales(verificacion)
    return {
        "origen": str(origen),
        "destino": str(destino),
        "sha256_origen": seguridad.sha256_archivo(origen),
        "sha256_destino": seguridad.sha256_archivo(destino),
        "parrafos_antes": len(docx.Document(str(origen)).paragraphs),
        "parrafos_despues": len(verificacion.paragraphs),
        "tablas_antes": len(docx.Document(str(origen)).tables),
        "tablas_despues": len(verificacion.tables),
        "antes": antes,
        "despues": despues,
        "duplicados_antes": duplicados_antes,
        "duplicados_despues": duplicados_despues,
        "matrices_anexo": matrices["tablas"],
        "referencias": resultado_referencias,
        "saneamiento_espacios": saneamiento,
        "acciones": acciones,
    }


def reconstruir_tabla_filas(
    ruta_origen: Union[str, Path],
    ruta_destino: Union[str, Path],
    indice_tabla: int,
    filas: Sequence[Any],
    alineaciones: Optional[Sequence[str]] = None,
    fila_total: Optional[Any] = None,
    columnas: Optional[Sequence[str]] = None,
    nota: Optional[str] = None,
    porcentaje_compacto: bool = False,
) -> Dict[str, Any]:
    """
    Reconstruye las filas de datos de una tabla nativa clonando la geometría y el formato
    de una fila de datos existente (w:tblGrid, w:tcPr, fuente, w:cantSplit).

    Conserva la fila 0 de encabezado (con w:tblHeader y las tres líneas APA 7) y la fila
    final de Total, que solo se reescribe si se entrega ``fila_total``.

    ``filas`` admite listas de celdas o diccionarios (claves en ``columnas``). Devuelve el
    detalle fila por fila para el reporte de auditoría.
    """
    from copy import deepcopy

    import docx

    origen = Path(ruta_origen)
    destino = Path(ruta_destino)
    seguridad.asegurar_no_sobrescribe(origen, destino)
    seguridad.asegurar_escritura_permitida(destino)

    sha_origen = seguridad.sha256_archivo(origen)
    documento = docx.Document(str(origen))
    tablas_antes = len(documento.tables)
    parrafos_antes = len(documento.paragraphs)
    if not 0 <= indice_tabla < tablas_antes:
        raise IndexError(f"Índice de tabla {indice_tabla} fuera de rango (0..{tablas_antes - 1})")

    table = documento.tables[indice_tabla]
    tbl = table._tbl
    grid = [int(g.get(_qn("w:w"))) for g in tbl.tblGrid.gridCol_lst]
    ancho = sum(grid)

    trs = tbl.tr_lst
    if len(trs) < 2:
        raise ValueError("La tabla no tiene filas de datos que clonar")
    filas_antes = len(trs)
    plantilla = deepcopy(trs[1])
    tr_total = trs[-1] if fila_total is not None else None
    for tr in trs[1:-1] if fila_total is not None else trs[1:]:
        tbl.remove(tr)

    if columnas is None and filas and isinstance(filas[0], dict):
        columnas = list(filas[0].keys())
    alineaciones = list(alineaciones or ["left"] * len(grid))
    if len(alineaciones) < len(grid):
        alineaciones += ["left"] * (len(grid) - len(alineaciones))

    def _valores(fila: Any) -> List[str]:
        if isinstance(fila, dict):
            if columnas is None:
                raise ValueError("Se requiere 'columnas' para filas en formato diccionario")
            valores = [str(fila.get(c, "")) for c in columnas]
        else:
            valores = [str(v) for v in fila]
        if porcentaje_compacto:
            import re as _re

            valores = [_re.sub(r"(\d)\s+%", r"\1%", v) for v in valores]
        return valores

    detalle: List[Dict[str, Any]] = []
    for k, fila in enumerate(filas, start=1):
        nuevo = deepcopy(plantilla)
        _preparar_tr(nuevo, cant_split=True, tbl_header=False)
        valores = _valores(fila)
        celdas = nuevo.findall(_qn("w:tc"))
        if len(valores) != len(celdas):
            raise ValueError(f"La fila {k} tiene {len(valores)} valores y la tabla {len(celdas)} columnas")
        for j, tc in enumerate(celdas):
            _fijar_texto_celda(tc, valores[j], alineaciones[j])
            tcW = tc.find(_qn("w:tcPr")).find(_qn("w:tcW"))
            if tcW is not None:
                tcW.set(_qn("w:w"), str(grid[j]))
                tcW.set(_qn("w:type"), "dxa")
        if tr_total is not None:
            tr_total.addprevious(nuevo)
        else:
            tbl.append(nuevo)
        detalle.append({"indice": k, "origen": "plantilla_fila_1", "celdas": valores})

    if fila_total is not None and tr_total is not None:
        _preparar_tr(tr_total, cant_split=True, tbl_header=False)
        valores = _valores(fila_total)
        celdas = tr_total.findall(_qn("w:tc"))
        if len(valores) != len(celdas):
            raise ValueError("La fila Total no coincide en columnas con la tabla")
        for j, tc in enumerate(celdas):
            _fijar_texto_celda(tc, valores[j], alineaciones[j])
            tcW = tc.find(_qn("w:tcPr")).find(_qn("w:tcW"))
            if tcW is not None:
                tcW.set(_qn("w:w"), str(grid[j]))
        detalle.append({"indice": len(filas) + 1, "origen": "fila_total_conservada", "celdas": valores})

    nota_actualizada = actualizar_nota_tabla(table, nota) if nota else False
    destino.parent.mkdir(parents=True, exist_ok=True)
    documento.save(str(destino))

    verificacion = docx.Document(str(destino))
    tabla_final = verificacion.tables[indice_tabla]
    trs_final = tabla_final._tbl.tr_lst
    return {
        "tabla_indice": indice_tabla,
        "filas_antes": filas_antes,
        "filas_despues": len(trs_final),
        "encabezado_conservado": trs_final[0].find(_qn("w:trPr")).find(_qn("w:tblHeader")) is not None,
        "total_al_final": "".join(t.text or "" for t in trs_final[-1].iter(_qn("w:t"))).strip().startswith("Total"),
        "cant_split": sum(1 for tr in trs_final if tr.find(_qn("w:trPr")) is not None and tr.find(_qn("w:trPr")).find(_qn("w:cantSplit")) is not None),
        "tabla_flotante": tabla_final._tbl.tblPr.find(_qn("w:tblpPr")) is not None,
        "grid": grid,
        "ancho_total_dxa": ancho,
        "parrafos_antes": parrafos_antes,
        "parrafos_despues": len(verificacion.paragraphs),
        "tablas_antes": tablas_antes,
        "tablas_despues": len(verificacion.tables),
        "nota_actualizada": nota_actualizada,
        "sha256_origen": sha_origen,
        "sha256_destino": seguridad.sha256_archivo(destino),
        "destino": str(destino),
        "detalle_filas": detalle,
    }


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
        choices=["auditar", "blindar-todas", "exportar-pdf", "renderizar-paginas", "reconstruir-tabla", "corregir-estructura", "aplicar-ordenes"],
        nargs="?",
        default="auditar",
    )
    parser.add_argument("ruta_docx", nargs="?", help="Ruta al archivo .docx o .pdf a inspeccionar")
    parser.add_argument("--paginas", default="1", help="Páginas a renderizar")
    parser.add_argument("--dpi", type=int, default=300, help="Resolución DPI")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON")
    parser.add_argument("--salida", help="DOCX de destino (comando reconstruir-tabla)")
    parser.add_argument("--tabla", type=int, default=None, help="Índice base 0 de la tabla a reconstruir")
    parser.add_argument("--filas", help="Archivo JSON con las filas de datos")
    parser.add_argument("--clave", help="Clave del objeto JSON que contiene la lista de filas")
    parser.add_argument("--ultima-fila-es-total", action="store_true", help="El último elemento de la lista es la fila Total")
    parser.add_argument("--columnas", help="Claves de columna separadas por coma")
    parser.add_argument("--alineaciones", default="left,left,center,center", help="Alineación por columna")
    parser.add_argument("--nota", help="Texto de la nota posterior a la tabla")
    parser.add_argument("--porcentaje-compacto", action="store_true", help="Elimina el espacio antes del signo %% (estilo 14.29%%)")
    parser.add_argument("--reporte", help="Archivo JSON donde escribir el detalle de la reconstrucción")
    parser.add_argument("--figuras-desde", type=int, default=11, help="Primera figura a reordenar")
    parser.add_argument("--figuras-hasta", type=int, default=48, help="Última figura a reordenar")
    parser.add_argument("--figuras-excluidas", default="49,50,51,52", help="Figuras que se dejan intactas")
    parser.add_argument("--tablas-matriz", default="", help="Índices base 0 de las matrices de anexo a ajustar (ej. 52,53)")
    parser.add_argument("--margenes-matriz", type=int, default=57, help="Márgenes laterales de celda en dxa para las matrices")
    parser.add_argument("--tamano-matriz", type=float, default=8.0, help="Tamaño en pt para cabecera y celdas numéricas de las matrices")
    parser.add_argument("--via-matriz", choices=["margenes", "rebalanceo", "ambas"], default="rebalanceo", help="Única vía geométrica para las matrices de anexo")
    parser.add_argument("--tablas-rebalanceo", default="", help="Índices base 0 de tablas adicionales a rebalancear conservando su ancho total")
    parser.add_argument("--referencias", help="Archivo JSON con las referencias a insertar (se aplican al final)")
    parser.add_argument("--lotes", help="Rutas de los JSON de órdenes separadas por coma, en el orden de aplicación")
    parser.add_argument("--solo-verificar", action="store_true", help="No escribe archivo: solo comprueba qué órdenes se aplicarían")
    parser.add_argument("--sanear-espacios", action="store_true", help="Recorta espacios y tabuladores residuales al final de cada párrafo antes de guardar")
    args = parser.parse_args()

    if args.comando == "aplicar-ordenes":
        if not (args.ruta_docx and args.lotes):
            parser.error("aplicar-ordenes requiere <docx> y --lotes")
        if not args.solo_verificar and not args.salida:
            parser.error("aplicar-ordenes requiere --salida cuando no se usa --solo-verificar")
        lotes = []
        for ruta_lote in [r.strip() for r in args.lotes.split(",") if r.strip()]:
            datos = json.loads(Path(ruta_lote).read_text(encoding="utf-8"))
            lotes.append((Path(ruta_lote).stem, datos))
        reporte = aplicar_ordenes_edicion(
            Path(args.ruta_docx),
            lotes,
            Path(args.salida) if args.salida else None,
            solo_verificar=args.solo_verificar,
            tablas_matriz=[int(x) for x in args.tablas_matriz.split(",") if x.strip()],
            margenes_matriz_dxa=args.margenes_matriz,
            tamano_matriz_pt=args.tamano_matriz,
            via_matriz=args.via_matriz,
            tablas_rebalanceo=[int(x) for x in args.tablas_rebalanceo.split(",") if x.strip()],
            sanear_espacios=args.sanear_espacios,
        )
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        resumen = {
            "solo_verificar": reporte["solo_verificar"],
            "sha256_origen": reporte["sha256_origen"],
            "sha256_destino": reporte["sha256_destino"],
            "parrafos": reporte["parrafos"],
            "tablas": reporte["tablas"],
            "total_ordenes": reporte["total_ordenes"],
            "total_aplicadas": reporte["total_aplicadas"],
            "total_fallidas": reporte["total_fallidas"],
            "saneamiento_espacios": {
                "parrafos_saneados": reporte["saneamiento_espacios"]["parrafos_saneados"],
                "caracteres_recortados": reporte["saneamiento_espacios"]["caracteres_recortados"],
            },
            "lotes": [
                {k: v for k, v in lote.items() if k != "detalles"} for lote in reporte["lotes"]
            ],
        }
        print(json.dumps(resumen, indent=2, ensure_ascii=False))
        return 0

    if args.comando == "corregir-estructura":
        if not (args.ruta_docx and args.salida):
            parser.error("corregir-estructura requiere <docx> y --salida")
        reporte = corregir_estructura_editorial(
            Path(args.ruta_docx),
            Path(args.salida),
            figuras_desde=args.figuras_desde,
            figuras_hasta=args.figuras_hasta,
            figuras_excluidas=[int(x) for x in args.figuras_excluidas.split(",") if x.strip()],
            tablas_matriz=[int(x) for x in args.tablas_matriz.split(",") if x.strip()],
            margenes_matriz_dxa=args.margenes_matriz,
            tamano_matriz_pt=args.tamano_matriz,
            referencias=(
                json.loads(Path(args.referencias).read_text(encoding="utf-8"))
                if args.referencias
                else ()
            ),
            sanear_espacios=args.sanear_espacios,
        )
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({k: v for k, v in reporte.items() if k != "acciones"}, indent=2, ensure_ascii=False))
        print(json.dumps({"acciones": len(reporte["acciones"])}, ensure_ascii=False))
        return 0

    if args.comando == "reconstruir-tabla":
        if not (args.ruta_docx and args.salida and args.tabla is not None and args.filas):
            parser.error("reconstruir-tabla requiere <docx>, --salida, --tabla y --filas")
        datos = json.loads(Path(args.filas).read_text(encoding="utf-8"))
        if args.clave:
            datos = datos[args.clave]
        filas = list(datos)
        fila_total = None
        if args.ultima_fila_es_total:
            fila_total = filas.pop()
        reporte = reconstruir_tabla_filas(
            Path(args.ruta_docx),
            Path(args.salida),
            args.tabla,
            filas,
            alineaciones=[a.strip() for a in args.alineaciones.split(",") if a.strip()],
            fila_total=fila_total,
            columnas=[c.strip() for c in args.columnas.split(",")] if args.columnas else None,
            nota=args.nota,
            porcentaje_compacto=args.porcentaje_compacto,
        )
        if args.reporte:
            Path(args.reporte).parent.mkdir(parents=True, exist_ok=True)
            Path(args.reporte).write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(reporte, indent=2, ensure_ascii=False))
        return 0

    if not args.ruta_docx:
        print(json.dumps({"estado": "listo", "motor": "docx_quirurgico.py", "regla": "APA 7 / UNAJMA"}, ensure_ascii=False))
        return 0

    reporte = auditar_docx_openxml(args.ruta_docx)
    print(json.dumps(reporte, indent=2, ensure_ascii=False))
    return 0 if reporte.get("cumple_apa7", False) else 1


if __name__ == "__main__":
    sys.exit(main())
