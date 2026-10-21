# -*- coding: utf-8 -*-
"""Regresion minima del expediente COMPLETO de validacion Fany x3 v05 (tres
hojas de evaluacion por dimension + certificado 03 + fichas de contexto): el
DOCX guardado debe verificar y las mutaciones deben fallar."""
import sys
from pathlib import Path

import docx
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "compiladores"))
import generar_expediente_integral_fany_x3 as g  # noqa: E402


def _guardar(doc, tmp_path):
    ruta = tmp_path / "exp.docx"
    doc.save(str(ruta))
    return ruta


def _fallas(ruta):
    return [n for n, ok, _ in g.verificar_docx(ruta) if not ok]


def test_expediente_conforme(tmp_path):
    assert _fallas(_guardar(g.construir_expediente(1), tmp_path)) == []


def test_tres_hojas_presentes(tmp_path):
    d = g.construir_expediente(1)
    hojas = g._tablas_hoja(d)
    # Hojas 01 y 02 apaisadas (14000 dxa, 9 columnas, encabezado de elementos).
    assert len(hojas) == 2
    n1 = sum(len(filas) for _, filas in g.GRUPOS_HOJA_01)
    n2 = sum(len(filas) for _, filas in g.GRUPOS_HOJA_02)
    assert n1 == 12 and n2 == 20
    # Los 8 criterios de conformidad estan en filas separadas (ids 7 a 14).
    ids = [num for _, filas in g.GRUPOS_HOJA_02 for num, _ in filas]
    assert ids == list(range(1, 21))


def test_certificado_unico_estructura(tmp_path):
    d = g.construir_expediente(1)
    certs = g._tabla_certificado(d)
    # Exactamente una tabla de validez a 8788 dxa: la del Instrumento 03.
    assert len(certs) == 1
    trs = certs[0]._tbl.findall(qn("w:tr"))
    # 2 encabezado + 2 indicadores (AP, UP) + 8 reactivos = 12 filas.
    assert len(trs) == 12


def test_mutacion_calificacion_en_certificado_falla(tmp_path):
    d = g.construir_expediente(1)
    t = g._tabla_certificado(d)[0]
    trs = t._tbl.findall(qn("w:tr"))
    # Fila 3 = primer reactivo (AP-01); columna 2 = Pertinencia Si.
    tc = trs[3].findall(qn("w:tc"))[2]
    p = tc.find(qn("w:p"))
    p.append(docx.oxml.parse_xml('<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:t>X</w:t></w:r>'))
    assert _fallas(_guardar(d, tmp_path))


def test_mutacion_calificacion_en_hoja01_falla(tmp_path):
    d = g.construir_expediente(1)
    t = g._tablas_hoja(d)[0]
    trs = t._tbl.findall(qn("w:tr"))
    # Primera fila de elemento (tras 2 encabezado + 1 grupo); columna 2 = Pertinencia.
    tc = trs[3].findall(qn("w:tc"))[2]
    p = tc.find(qn("w:p"))
    p.append(docx.oxml.parse_xml('<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:t>X</w:t></w:r>'))
    assert _fallas(_guardar(d, tmp_path))


def test_mutacion_texto_elemento_hoja02_falla(tmp_path):
    d = g.construir_expediente(1)
    t = g._tablas_hoja(d)[1]
    trs = t._tbl.findall(qn("w:tr"))
    # Ultima fila (elemento 20); columna 1 = texto del elemento.
    tc = trs[-1].findall(qn("w:tc"))[1]
    for tnode in tc.iter(qn("w:t")):
        if tnode.text and len(tnode.text) > 20:
            tnode.text = tnode.text.replace("concordantes", "concordante")  # mutacion real
            break
    assert _fallas(_guardar(d, tmp_path))


def test_eliminar_hoja01_falla(tmp_path):
    d = g.construir_expediente(1)
    t = g._tablas_hoja(d)[0]
    t._tbl.getparent().remove(t._tbl)
    fallas = _fallas(_guardar(d, tmp_path))
    assert any("Hojas de evaluacion" in f for f in fallas)


def test_eliminar_hoja02_falla(tmp_path):
    d = g.construir_expediente(1)
    t = g._tablas_hoja(d)[1]
    t._tbl.getparent().remove(t._tbl)
    fallas = _fallas(_guardar(d, tmp_path))
    assert any("Hojas de evaluacion" in f for f in fallas)


def test_eliminar_fila_elemento_hoja01_falla(tmp_path):
    d = g.construir_expediente(1)
    t = g._tablas_hoja(d)[0]
    tr = t._tbl.findall(qn("w:tr"))[-1]
    t._tbl.remove(tr)
    assert _fallas(_guardar(d, tmp_path))


def test_mutacion_cierre_hoja02_falla(tmp_path):
    d = g.construir_expediente(1)
    # Vaciar la linea de firma del SEGUNDO bloque de cierre (hoja 02).
    vistas = 0
    for p in d.paragraphs:
        if p.text.startswith("Firma del juez validador"):
            vistas += 1
            if vistas == 2:
                for r in p.runs:
                    r.text = ""
                break
    f = _fallas(_guardar(d, tmp_path))
    assert any("cierre" in x.lower() for x in f)


def test_mutacion_item_literal_ap_falla(tmp_path):
    d = g.construir_expediente(1)
    for t in d._body._body.iter(qn("w:t")):
        if t.text and t.text.startswith("El procedimiento actual para asentar"):
            t.text = t.text.replace("ágil", "rápido")
    assert _fallas(_guardar(d, tmp_path))


def test_mutacion_item_literal_up_falla(tmp_path):
    d = g.construir_expediente(1)
    for t in d._body._body.iter(qn("w:t")):
        if t.text and t.text.startswith("El mecanismo de registro utilizado"):
            t.text = t.text.replace("fidedigna", "fidedigno")
    assert _fallas(_guardar(d, tmp_path))


def test_mutacion_bloque_inferior_falla(tmp_path):
    d = g.construir_expediente(1)
    for p in d.paragraphs:
        if p.text.startswith("Firma del juez validador"):
            for r in p.runs:
                r.text = ""
            break
    f = _fallas(_guardar(d, tmp_path))
    assert any("cierre" in x.lower() for x in f)


def test_mutacion_blindaje_y_contacto_fallan(tmp_path):
    d = g.construir_expediente(1)
    tr = d.tables[0]._tbl.find(qn("w:tr"))
    trPr = tr.find(qn("w:trPr"))
    trPr.remove(trPr.find(qn("w:cantSplit")))
    d.add_paragraph("Contacto: jquispe@unajma.edu.pe")
    f = _fallas(_guardar(d, tmp_path))
    assert any("cantSplit" in x for x in f) and any("jquispe" in x.lower() or "contactos" in x.lower() for x in f)


def test_legado_v03_excluido(tmp_path):
    d = g.construir_expediente(1)
    ruta = _guardar(d, tmp_path)
    f = _fallas(ruta)
    assert not any("legado v03" in x for x in f)
    # Ademas: sin las 8 preguntas nuevas D1/D2 de v03, sin PU/PE como
    # dimensiones VI y sin codigos internos ni stack en el texto visible.
    texto = "\n".join(t.text or "" for t in d.element.body.iter(qn("w:t")))
    assert "(Sin el sistema / tras la implantación" not in texto
    assert "Dimensión 1: Utilidad percibida del software SIVAC" not in texto
    assert "Dimensión 2: Facilidad de uso percibida del software SIVAC" not in texto
    assert "Node.js" not in texto and "PostgreSQL" not in texto


def test_especificacion_json_conciliada_con_word(tmp_path):
    """Cada texto_evaluado de la especificacion durable debe aparecer en el
    Word guardado, junto con los 3 nombres de dimension y los 3 titulos."""
    import json
    ruta_json = Path(g.__file__).resolve().parents[2] / "salidas" / "documentos" / "anexos_fany" / "textos_tabla_fichas_v05.json"
    spec = json.loads(ruta_json.read_text(encoding="utf-8"))
    d = g.construir_expediente(1)
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    norm = g.fany._normalizar
    plano = norm(texto)
    faltantes = []
    for inst in spec["instrumentos"]:
        for gr in inst["grupos"]:
            for fila in gr["filas"]:
                if norm(fila["texto_evaluado"]) not in plano:
                    faltantes.append((inst["numero"], fila["id"]))
    assert faltantes == []
    # 3 nombres de dimension y 3 titulos (los del generador; el campo
    # titulo_hoja del JSON es metadato del especialista y no se imprime).
    for dim in ("Oportunidad de procesamiento", "Consistencia documental", "Satisfacción del usuario"):
        assert dim in texto
    for titulo in (g.TITULO_HOJA_01, g.TITULO_HOJA_02, g.TITULO_CERT_03):
        assert norm(titulo) in plano


# ------------------------------------------------------------------ v06 compacto


def test_compacto_conforme(tmp_path):
    assert [n for n, ok, _ in g.verificar_compacto(_guardar(g.construir_compacto(), tmp_path)) if not ok] == []


def test_compacto_estructura_minima(tmp_path):
    d = g.construir_compacto()
    # 2 tablas: criterios (2 col) + UNA tabla de certificado (9 col, 8788).
    assert len(d.tables) == 2
    cert = g.verificar_compacto.__globals__  # noqa: F841 (documento de intencion)
    tabla_cert = [t for t in d.tables
                  if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9]
    assert len(tabla_cert) == 1
    trs = tabla_cert[0]._tbl.findall(qn("w:tr"))
    # 2 encabezado + 3 dimensiones + 12 elementos = 17 filas.
    assert len(trs) == 17


def test_compacto_json_durable_fiel(tmp_path):
    """El generador compacto debe cargar el JSON durable y exponer 2+2+8 filas
    con ids continuos 1..12 y los 8 reactivos de satisfaccion identicos."""
    espec = g._cargar_compacto()
    grupos = espec["grupos"]
    assert [len(f) for _, f in grupos] == [2, 2, 8]
    ids = [i for _, filas in grupos for i, _ in filas]
    assert ids == list(range(1, 13))
    norm = g.fany._normalizar
    literales = [norm(x) for _, filas in grupos for _, x in filas][4:]
    assert literales == [norm(x) for x in g.ITEMS_AP + g.ITEMS_UP]


def test_compacto_un_cierre_y_sin_anexos(tmp_path):
    d = g.construir_compacto()
    ruta = _guardar(d, tmp_path)
    doc = docx.Document(str(ruta))
    texto = "\n".join(t.text or "" for t in doc.element.body.iter(qn("w:t")))
    assert texto.count("Firma del juez validador") == 1
    assert texto.count("Opinión de aplicabilidad:") == 1
    # Ninguna pieza del integral v05 presente.
    for m in g.MARCADORES_ANEXOS_V05:
        assert m not in texto
    # Orden modelo ITEM.
    pars = ["".join(t.text or "" for t in p.iter(qn("w:t"))) for p in doc.element.body.findall(qn("w:p"))]
    pos = [next((i for i, t in enumerate(pars) if t.startswith(m)), None)
           for m in g.MARCADORES_COMPACTO]
    assert None not in pos and pos == sorted(pos)


def test_compacto_mutacion_quitar_dimension_falla(tmp_path):
    d = g.construir_compacto()
    tabla_cert = [t for t in d.tables
                  if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9][0]
    trs = tabla_cert._tbl.findall(qn("w:tr"))
    # Eliminar la fila de la Dimension 3 (fila 8: 2 encabezado + 2 dims + 4+2
    # elementos ya escritos...; localizar por texto).
    idx = next(i for i, tr in enumerate(trs)
               if "Dimensión 3" in "".join(t.text or "" for t in tr.iter(qn("w:t"))))
    tabla_cert._tbl.remove(trs[idx])
    fallas = [n for n, ok, _ in g.verificar_compacto(_guardar(d, tmp_path)) if not ok]
    assert any("filas" in f or "17" in f for f in fallas)


def test_compacto_mutacion_alterar_item_falla(tmp_path):
    d = g.construir_compacto()
    tabla_cert = [t for t in d.tables
                  if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9][0]
    trs = tabla_cert._tbl.findall(qn("w:tr"))
    for tnode in trs[-1].iter(qn("w:t")):
        if tnode.text and len(tnode.text) > 20:
            tnode.text = tnode.text.replace("abastecimiento", "abastecimientos")
            break
    fallas = [n for n, ok, _ in g.verificar_compacto(_guardar(d, tmp_path)) if not ok]
    assert any("literales" in f for f in fallas)


def test_compacto_mutacion_duplicar_cierre_falla(tmp_path):
    d = g.construir_compacto()
    g.construir_bloque_cierre(d)
    fallas = [n for n, ok, _ in g.verificar_compacto(_guardar(d, tmp_path)) if not ok]
    assert any("cierre" in f.lower() for f in fallas)


def test_compacto_mutacion_agregar_anexo_falla(tmp_path):
    d = g.construir_compacto()
    d.add_paragraph(g.TITULO_PANORAMA)
    fallas = [n for n, ok, _ in g.verificar_compacto(_guardar(d, tmp_path)) if not ok]
    assert any("anexo" in f.lower() for f in fallas)


def test_compacto_marca_prellenada_falla(tmp_path):
    d = g.construir_compacto()
    tabla_cert = [t for t in d.tables
                  if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9][0]
    trs = tabla_cert._tbl.findall(qn("w:tr"))
    # Primera fila de elemento (tras 2 encabezado + 1 dimension); celda 2 = Pertinencia Si.
    tc = trs[3].findall(qn("w:tc"))[2]
    p = tc.find(qn("w:p"))
    p.append(docx.oxml.parse_xml(
        '<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:t>X</w:t></w:r>'))
    fallas = [n for n, ok, _ in g.verificar_compacto(_guardar(d, tmp_path)) if not ok]
    assert any("vacias" in f or "marcas" in f for f in fallas)


# ---------------------------------------------------------------------- v07


def _fallas_v07(ruta):
    return [n for n, ok, _ in g.verificar_v07(ruta) if not ok]


def test_v07_conforme(tmp_path):
    assert _fallas_v07(_guardar(g.construir_v07(), tmp_path)) == []


def test_v07_estructura_anexos(tmp_path):
    d = g.construir_v07()
    # Matriz de validez unica de 9 columnas a 8788 dxa con 17 filas.
    cert = [t for t in d.tables
            if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9
            and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == g.ANCHO_RETRATO]
    assert len(cert) == 1
    assert len(cert[0]._tbl.findall(qn("w:tr"))) == 17
    # Rejilla cerrada presente en la matriz de validez (6 lados single).
    tb = cert[0]._tbl.tblPr.find(qn("w:tblBorders"))
    lados = [l for l in ("top", "left", "bottom", "right", "insideH", "insideV")
             if tb.find(qn("w:" + l)) is not None and tb.find(qn("w:" + l)).get(qn("w:val")) == "single"]
    assert len(lados) == 6
    # Los 3 instrumentos estan presentes con sus titulos oficiales.
    texto = "\n".join(t.text or "" for t in d.element.body.iter(qn("w:t")))
    assert "FICHA DE OBSERVACIÓN SISTEMÁTICA Y MEDICIÓN DE TIEMPOS CRONOMETRADOS" in texto
    assert "FICHA DE REGISTRO Y COTEJO DOCUMENTAL DE CONSISTENCIA" in texto
    assert "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO Y ACEPTACIÓN TECNOLÓGICA" in texto


def test_v07_todos_los_reactivos_literales(tmp_path):
    d = g.construir_v07()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    norm = g.fany._normalizar
    plano = norm(texto)
    for e in g.ITEMS_AP + g.ITEMS_UP + g.ITEMS_PU + g.ITEMS_PE:
        assert norm(e) in plano


def test_v07_tablas_ancho_pleno(tmp_path):
    d = g.construir_v07()
    for t in d.tables:
        w = int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w")))
        grid = sum(int(gc.get(qn("w:w"))) for gc in t._tbl.tblGrid.findall(qn("w:gridCol")))
        assert w == grid and w in (g.ANCHO_RETRATO, g.ANCHO_APAISADA)


def test_v07_eliminar_instrumento02_falla(tmp_path):
    d = g.construir_v07()
    for p in list(d.element.body.findall(qn("w:p"))):
        if "".join(t.text or "" for t in p.iter(qn("w:t"))).startswith("INSTRUMENTO N.° 02"):
            p.getparent().remove(p)
            break
    fallas = _fallas_v07(_guardar(d, tmp_path))
    assert any("Instrumento 02" in f or "orden" in f.lower() for f in fallas)


def test_v07_eliminar_escala_likert_falla(tmp_path):
    d = g.construir_v07()
    for t in list(d.tables):
        if "Totalmente en Desacuerdo" in "".join(tt.text or "" for tt in t._tbl.iter(qn("w:t"))):
            t._tbl.getparent().remove(t._tbl)
            break
    fallas = _fallas_v07(_guardar(d, tmp_path))
    assert any("Escala Likert" in f for f in fallas)


def test_v07_eliminar_item_ap01_falla(tmp_path):
    d = g.construir_v07()
    for t in d.tables:
        for tr in t._tbl.findall(qn("w:tr")):
            tx = "".join(tt.text or "" for tt in tr.iter(qn("w:t")))
            if tx.startswith("AP-01"):
                t._tbl.remove(tr)
                fallas = _fallas_v07(_guardar(d, tmp_path))
                assert any("AP/UP" in f or "literales" in f for f in fallas)
                return
    raise AssertionError("fila AP-01 no encontrada")


def test_v07_encoger_tabla_fuera_de_margen_falla(tmp_path):
    d = g.construir_v07()
    t = d.tables[0]
    grid = t._tbl.tblGrid
    primera = grid.find(qn("w:gridCol"))
    primera.set(qn("w:w"), "300")  # rompe la suma = ancho declarado
    fallas = _fallas_v07(_guardar(d, tmp_path))
    assert any("ancho util" in f or "desbordes" in f for f in fallas)


def test_v07_quitar_rejilla_de_matriz_validez_falla(tmp_path):
    d = g.construir_v07()
    cert = [t for t in d.tables
            if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 9
            and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == g.ANCHO_RETRATO][0]
    tb = cert._tbl.tblPr.find(qn("w:tblBorders"))
    vertical = tb.find(qn("w:insideV"))
    tb.remove(vertical)
    fallas = _fallas_v07(_guardar(d, tmp_path))
    assert any("rejilla" in f or "Bordes" in f for f in fallas)


def test_v07_psicometria_excluida(tmp_path):
    d = g.construir_v07()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    plano = texto.lower()
    for prohibido in ("alfa de cronbach", "omega de mcdonald", "baremo", "tercil", "muestra piloto",
                      "puntaje global"):
        assert prohibido not in plano
    # Cero OMML en el paquete.
    assert len(d.element.body.xpath('.//*[local-name()="oMath"]')) == 0


def test_v07_fechas_formulario_en_blanco(tmp_path):
    d = g.construir_v07()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    # Las fechas de aplicacion y la ventana de auditoria del formulario estan totalmente vacias.
    assert texto.count("______ / ______ / ______") >= 3
    assert "Del ____ / ____ / ______  al  ____ / ____ / ______" in texto
    # Ninguna fecha de formulario forzada a 2025.
    import re as _re
    assert not _re.search(r"Fecha de (aplicación|la observación|ejecución)[^\n]*2025", texto)
    assert not _re.search(r"Ventana de auditor[^\n]*2025", texto)


# ---------------------------------------------------------------------- v08 vertical


def _fallas_v08(ruta):
    return [n for n, ok, _ in g.verificar_v08(ruta) if not ok]


def test_v08_conforme(tmp_path):
    assert _fallas_v08(_guardar(g.construir_v08(), tmp_path)) == []


def test_v08_matriz_validacion_8_columnas(tmp_path):
    d = g.construir_v08()
    # Exactamente una tabla de 8 columnas a 8788 dxa.
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8
             and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == g.ANCHO_RETRATO]
    assert len(certs) == 1
    t_val = certs[0]
    # 2 encabezado + 12 elementos continuos = 14 filas.
    assert len(t_val._tbl.findall(qn("w:tr"))) == 14
    grid_w = [int(gc.get(qn("w:w"))) for gc in t_val._tbl.tblGrid.findall(qn("w:gridCol"))]
    assert grid_w == g.ANCHOS_MATRIZ_VALIDEZ_V08
    # Rejilla cerrada completa.
    tb = t_val._tbl.tblPr.find(qn("w:tblBorders"))
    lados = [l for l in ("top", "left", "bottom", "right", "insideH", "insideV")
             if tb.find(qn("w:" + l)) is not None and tb.find(qn("w:" + l)).get(qn("w:val")) == "single"]
    assert len(lados) == 6


def test_v08_cierre_decision_final_y_firma(tmp_path):
    d = g.construir_v08()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "DECISIÓN FINAL SOBRE LA APLICABILIDAD DEL INSTRUMENTO" in texto
    assert "[   ] Aplicable sin modificaciones" in texto
    assert "[   ] Aplicable con modificaciones menores" in texto
    assert "[   ] Requiere revisión y reestructuración sustancial" in texto
    assert "[   ] No aplicable" in texto
    assert "¿Los elementos propuestos son suficientes para medir la variable en estudio?" in texto
    assert texto.count("Firma del juez validador") == 1
    assert texto.count("Apellidos y nombres del juez validador:") == 1


def test_v08_reactivos_reformulados_atomicos(tmp_path):
    d = g.construir_v08()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    norm = g.fany._normalizar
    plano = norm(texto)
    for it in g.ITEMS_AP_V08 + g.ITEMS_UP_V08:
        assert norm(it) in plano


def test_v08_ficha01_mediana_y_promedio(tmp_path):
    d = g.construir_v08()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert texto.count("Mediana de las tres tareas (estadístico principal):") == 2
    assert texto.count("Promedio (descriptivo complementario):") == 2
    assert "Regla de pausa" in texto


def test_v08_ficha02_encabezado_y_criterio4(tmp_path):
    d = g.construir_v08()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "Unidad de análisis documental" in texto
    assert "Movimiento individual de vacuna registrado en documento oficial" in texto
    assert "Documentos fuente consultados" in texto
    assert "nota de modificación autorizada" in texto


def test_v08_matriz_consistencia_integracion(tmp_path):
    d = g.construir_v08()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "La hipótesis general será contrastada a partir de la integración" in texto
    assert "Se acepta si se rechaza la hipótesis nula" not in texto


def test_v08_mutacion_calificacion_matriz_falla(tmp_path):
    d = g.construir_v08()
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8][0]
    trs = certs._tbl.findall(qn("w:tr"))
    # Fila 2 = primer elemento (Treg); celda 4 = Pertinencia.
    tc = trs[2].findall(qn("w:tc"))[4]
    p = tc.find(qn("w:p"))
    p.append(docx.oxml.parse_xml('<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:t>4</w:t></w:r>'))
    assert _fallas_v08(_guardar(d, tmp_path))


def test_v08_prohibicion_guion_largo(tmp_path):
    d = g.construir_v08()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "—" not in texto


def test_v08_100_porciento_vertical_a4(tmp_path):
    d = g.construir_v08()
    for s in d.sections:
        assert s.page_width.cm < s.page_height.cm
        assert round(s.page_width.cm, 1) == 21.0
        assert round(s.page_height.cm, 1) == 29.7


# ---------------------------------------------------------------------- v09 mixto


def _fallas_v09(ruta):
    return [n for n, ok, _ in g.verificar_v09(ruta) if not ok]


def test_v09_conforme(tmp_path):
    assert _fallas_v09(_guardar(g.construir_v09(), tmp_path)) == []


def test_v09_arquitectura_secciones_mixta(tmp_path):
    d = g.construir_v09()
    assert len(d.sections) == 3
    s0, s1, s2 = d.sections[0], d.sections[1], d.sections[2]
    # Sección 1: Retrato A4
    assert s0.page_width.cm < s0.page_height.cm
    assert round(s0.page_width.cm, 1) == 21.0
    assert round(s0.page_height.cm, 1) == 29.7
    assert round(s0.left_margin.cm, 1) == 3.0
    # Sección 2: Apaisada A4 (14000 dxa)
    assert s1.page_width.cm > s1.page_height.cm
    assert round(s1.page_width.cm, 1) == 29.7
    assert round(s1.page_height.cm, 1) == 21.0
    assert round(s1.left_margin.cm, 1) == 2.5
    # Sección 3: Retrato A4
    assert s2.page_width.cm < s2.page_height.cm
    assert round(s2.page_width.cm, 1) == 21.0
    assert round(s2.page_height.cm, 1) == 29.7
    assert round(s2.left_margin.cm, 1) == 3.0


def test_v09_matriz_validacion_8_columnas(tmp_path):
    d = g.construir_v09()
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8
             and int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == g.ANCHO_RETRATO]
    assert len(certs) == 1
    t_val = certs[0]
    # 2 encabezado + 12 elementos continuos = 14 filas
    assert len(t_val._tbl.findall(qn("w:tr"))) == 14
    grid_w = [int(gc.get(qn("w:w"))) for gc in t_val._tbl.tblGrid.findall(qn("w:gridCol"))]
    assert grid_w == g.ANCHOS_MATRIZ_VALIDEZ_V08
    # Rejilla cerrada completa (6 lados)
    tb = t_val._tbl.tblPr.find(qn("w:tblBorders"))
    lados = [l for l in ("top", "left", "bottom", "right", "insideH", "insideV")
             if tb.find(qn("w:" + l)) is not None and tb.find(qn("w:" + l)).get(qn("w:val")) == "single"]
    assert len(lados) == 6


def test_v09_matrices_apaisadas_apa7(tmp_path):
    d = g.construir_v09()
    # Dos tablas a 14000 dxa en Sección 2
    apa_tables = [t for t in d.tables if int(t._tbl.tblPr.find(qn("w:tblW")).get(qn("w:w"))) == g.ANCHO_APAISADA]
    assert len(apa_tables) == 2
    for t in apa_tables:
        tb = t._tbl.tblPr.find(qn("w:tblBorders"))
        assert tb.find(qn("w:top")).get(qn("w:val")) == "single"
        assert tb.find(qn("w:bottom")).get(qn("w:val")) == "single"
        assert tb.find(qn("w:left")) is None or tb.find(qn("w:left")).get(qn("w:val")) == "none"
        assert tb.find(qn("w:right")) is None or tb.find(qn("w:right")).get(qn("w:val")) == "none"
        assert tb.find(qn("w:insideV")) is None or tb.find(qn("w:insideV")).get(qn("w:val")) == "none"


def test_v09_aspecto1_separacion_modalidad_b(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "las tres dimensiones definidas para la variable dependiente" in texto
    assert "las tres dimensiones oficiales de la variable dependiente" not in texto
    assert "Modalidad B como anexo complementario de consulta técnica para la evaluación descriptiva postest" in texto
    assert "sin formar parte de la escala de la variable dependiente" in texto
    # Punto 2 de la carta ajustado: erradicar unidad dual y declarar unidad documental
    assert "Cada movimiento o entrega constituye una unidad de registro documental; posteriormente, los resultados se consolidan en porcentajes por operador para el contraste estadístico pretest–postest." in texto
    assert "con unidad de análisis dual y consolidación por operador" not in texto
    # Matriz de validación tiene exactamente 12 elementos (sin reactivos de Modalidad B)
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8][0]
    assert len(certs._tbl.findall(qn("w:tr"))) == 14


def test_v09_aspecto2_v_aiken_y_corte(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "procesamiento de la validez de contenido mediante el coeficiente V de Aiken, calculado para cada elemento y criterio de evaluación" in texto
    assert "concordancia entre jueces" not in texto
    assert "coeficiente V de Aiken alcance o supere el valor mínimo establecido para la investigación (V >= 0.80)" in texto
    assert "El valor mínimo de V de Aiken será interpretado conjuntamente con las observaciones cualitativas de los jueces expertos." in texto


def test_v09_aspecto3_ficha01_tarea_unica_ensayos(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "Registro de salida programada de tres biológicos con lote, cantidad, fecha, destino y responsable" in texto
    assert "REG-E1" in texto and "REG-E2" in texto and "REG-E3" in texto
    assert "Emisión de vale oficial para salida programada de tres biológicos a un establecimiento de salud" in texto
    assert "VALE-E1" in texto and "VALE-E2" in texto and "VALE-E3" in texto
    # Protocolo de cronometraje: control de sesgo de aprendizaje y comparabilidad de los 3 ensayos
    assert "Los tres ensayos se realizarán con casos equivalentes en complejidad, cantidad de biológicos, datos requeridos y flujo operativo" in texto
    assert "El orden de los tres ensayos será el mismo en pretest y postest para todos los participantes." in texto
    # Punto final uniforme de emisión de vales
    assert "Tiempo de emisión de vales: inicia cuando el operador recibe o abre la solicitud de pedido y termina cuando el vale o comprobante de salida ha sido generado y queda disponible para su entrega, impresión o registro institucional" in texto
    assert texto.count("Mediana de los tres ensayos (estadístico principal por operador): ____________ min          Promedio: ____________ min") == 2


def test_v09_aspecto4_ficha02_unidad_analisis_wilcoxon(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "Código del operador auditado" in texto
    assert "Código del operador o centro auditado" not in texto
    assert "Unidad de registro documental" in texto
    assert "Unidad de análisis para el contraste estadístico pretest-postest" in texto
    assert "Cada operador evaluado (TRAB-01 a TRAB-14)" in texto
    assert "14 pares de observaciones para la prueba de Wilcoxon" in texto


def test_v09_aspecto5_criterio4_rsd_perfeccionado(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    norm = g.fany._normalizar
    criterio4 = (
        "Cantidad registrada concordante con el documento fuente que sustenta el movimiento. "
        "En entradas, se verifica la concordancia con el acta, guía de remisión o documento de recepción; "
        "en salidas, con la orden de pedido, vale autorizado o nota de modificación; "
        "y en ajustes, con el documento de autorización correspondiente."
    )
    assert norm(criterio4) in norm(texto)


def test_v09_reactivos_atomicos_modalidad_a(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    norm = g.fany._normalizar
    plano = norm(texto)
    for it in g.ITEMS_AP_V09 + g.ITEMS_UP_V09:
        assert norm(it) in plano
    # Reactivos atómicos específicos
    assert norm("El tiempo destinado a gestionar los movimientos de vacunas es compatible con mis demás actividades laborales.") in plano
    assert norm("El procedimiento de emisión de comprobantes facilita la asignación correcta de los biológicos solicitados.") in plano
    assert norm("El procedimiento de conciliación facilita identificar y sustentar documentalmente las diferencias entre las cantidades programadas y entregadas.") in plano
    assert norm("El procedimiento de gestión facilita el seguimiento oportuno de las existencias de vacunas en los establecimientos de salud.") in plano
    # Encabezado del Instrumento N.° 03
    assert "CUESTIONARIO DE SATISFACCIÓN DEL USUARIO CON EL PROCESO OPERATIVO Y MÓDULO COMPLEMENTARIO DE ACEPTACIÓN TECNOLÓGICA DE SIVAC" in texto
    # Síntesis del indicador UP en la tabla de operacionalización
    assert "Percepción de oportunidad informativa, asignación correcta de biológicos, sustento documental y seguimiento de existencias" in texto
    # Nota metodológica de la matriz de consistencia
    assert norm("Considerando el tamaño muestral de 14 participantes y el carácter pareado de las mediciones, la contrastación de hipótesis se realizará mediante la prueba no paramétrica de rangos con signo de Wilcoxon") in plano


def test_v09_mutacion_calificacion_falla(tmp_path):
    d = g.construir_v09()
    certs = [t for t in d.tables if len(t._tbl.tblGrid.findall(qn("w:gridCol"))) == 8][0]
    trs = certs._tbl.findall(qn("w:tr"))
    # Fila 2 = primer elemento (Treg); celda 4 = Pertinencia.
    tc = trs[2].findall(qn("w:tc"))[4]
    p = tc.find(qn("w:p"))
    p.append(docx.oxml.parse_xml('<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:t>4</w:t></w:r>'))
    assert _fallas_v09(_guardar(d, tmp_path))


def test_v09_prohibicion_guion_largo(tmp_path):
    d = g.construir_v09()
    ruta = _guardar(d, tmp_path)
    texto = "\n".join(t.text or "" for t in docx.Document(str(ruta)).element.body.iter(qn("w:t")))
    assert "—" not in texto

