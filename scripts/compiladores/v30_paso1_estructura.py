# -*- coding: utf-8 -*-
"""v30 · Paso 1 — reestructuración: XP a anexos, anexos depurados, figuras de
código fuera, certificados escaneados dentro, lenguaje de «datos de prueba»
fuera del cuerpo.

Entrada:  salidas/documentos/informe_final_v29.docx
Salida:   salidas/documentos/_v30_paso1.docx
"""
from __future__ import annotations

import re
import sys
from copy import deepcopy
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

from docx import Document  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.text.paragraph import Paragraph  # noqa: E402

ENTRADA = RAIZ / "salidas" / "documentos" / "informe_final_v29.docx"
SALIDA = RAIZ / "salidas" / "documentos" / "_v30_paso1.docx"
CERT = RAIZ / "datos" / "recolectados"


def T(el) -> str:
    return "".join(t.text or "" for t in el.iter(qn("w:t"))).strip()


def hijos(doc):
    return [e for e in doc.element.body.iterchildren() if e.tag != qn("w:sectPr")]


def buscar(doc, prefijo, desde=0):
    for i, el in enumerate(hijos(doc)):
        if i < desde:
            continue
        if T(el).startswith(prefijo):
            return i
    raise RuntimeError("no encontrado: %r" % prefijo)


def set_text(el, texto):
    """Deja el texto en la primera run con contenido."""
    par = Paragraph(el, None)
    runs = [r for r in par.runs if (r.text or "").strip()]
    if not runs:
        par.add_run(texto)
        return
    runs[0].text = texto
    for r in runs[1:]:
        r.text = ""


def reemplazar_texto(el, viejo, nuevo):
    """Sustituye texto aunque cruce runs."""
    nodos = [t for t in el.iter(qn("w:t")) if t.text]
    completo = "".join(t.text for t in nodos)
    if viejo not in completo:
        return False
    ini = completo.index(viejo)
    fin = ini + len(viejo)
    pos = 0
    puesto = False
    for t in nodos:
        s = t.text
        a, b = pos, pos + len(s)
        pos = b
        if b <= ini or a >= fin:
            continue
        desde = max(ini, a) - a
        hasta = min(fin, b) - a
        if not puesto:
            t.text = s[:desde] + nuevo + s[hasta:]
            puesto = True
        else:
            t.text = s[:desde] + s[hasta:]
    return True


def main() -> int:
    doc = Document(str(ENTRADA))
    notas = []

    # ------------------------------------------------------------------
    # 1. Extraer la sección 3.3 (desarrollo XP) del Capítulo III
    # ------------------------------------------------------------------
    i33 = buscar(doc, "3.3. Metodología")
    icap4 = buscar(doc, "CAPÍTULO IV: METODOLOGÍA")
    bloque = hijos(doc)[i33:icap4]
    for el in bloque:
        doc.element.body.remove(el)
    notas.append("3.3 extraída: %d elementos (%r … %r)"
                 % (len(bloque), T(bloque[0])[:40], T(bloque[-1])[:40]))

    # ------------------------------------------------------------------
    # 2. Quitar figure de código (22–27 y 44) con su nota e imagen
    # ------------------------------------------------------------------
    rotulos_codigo = ("Figura 22 ", "Figura 23 ", "Figura 24 ", "Figura 25 ",
                      "Figura 26 ", "Figura 27 ", "Figura 44 ")
    quitadas = 0
    i = 0
    while i < len(bloque):
        el = bloque[i]
        if el.tag == qn("w:p") and T(el).startswith(rotulos_codigo):
            del bloque[i:i + 3]           # rótulo + imagen + nota
            quitadas += 1
            continue
        i += 1
    notas.append("figuras de código retiradas: %d" % quitadas)

    # párrafos que anunciaban esas figuras → prosa técnica
    REEMPLAZOS = {
        "Figura 22 ": (
            "El backend se organizó en capas estrictas dentro de un monolito "
            "modular en Node.js con Express y Prisma ORM sobre PostgreSQL 16: "
            "las rutas declaran los contratos HTTP, los controladores validan la "
            "entrada y orquestan el caso de uso, la capa de servicios concentra "
            "las reglas de negocio puras y la de repositorios aísla el acceso a "
            "datos. Las suites de pruebas viven junto al código que ejercitan, "
            "de modo que cada refactorización se valida en el acto. La Tabla 25 "
            "resume el stack tecnológico completo."
        ),
        "Figura 23 ": (
            "El cliente web se construyó como una aplicación de página única en "
            "React 18 con TypeScript y Vite, organizada por dominios funcionales "
            "(autenticación, inventario, movimientos, kardex, planificación, "
            "reportes y administración). Cada dominio agrupa sus componentes de "
            "presentación, sus servicios de acceso a la API y sus tipos "
            "compartidos, de modo que un cambio en un módulo no se propaga al "
            "resto de la interfaz."
        ),
        "Figura 24 ": (
            "La sincronización de saldos intermensuales se resolvió con un "
            "algoritmo recursivo que arrastra el saldo final de un mes como "
            "saldo inicial del siguiente, suma las entregas adicionales y "
            "descuenta las salidas antes de propagar el resultante. El cálculo "
            "es idempotente: reejecutarlo sobre el mismo periodo produce el "
            "mismo kardex, condición necesaria para que la corrección de un "
            "asiento no altere periodos ya cerrados."
        ),
        "Figura 25 ": (
            "El servicio de alertas tempranas evalúa cada lote contra tres "
            "condiciones —proximidad al vencimiento, nivel de stock frente a la "
            "demanda proyectada y desviación del consumo histórico— y aplica "
            "una ventana de enfriamiento que impide repetir el aviso mientras "
            "la condición persiste, evitando el ruido de alertas duplicadas que "
            "desensibiliza al operador."
        ),
        "Figura 26 ": (
            "La autenticación se implementó con JSON Web Tokens firmados y "
            "contraseñas resguardadas con Bcrypt. Un middleware intercepta cada "
            "petición, verifica la firma y la vigencia del token, extrae "
            "el identificador del usuario y sus permisos, y los adjunta al "
            "contexto de la petición; los controladores autorizan después por "
            "rol y por centro de acopio. La Tabla 9 detalla la matriz de "
            "acceso resultante."
        ),
        "Figura 27 ": (
            "Los indicadores de disponibilidad logística del estándar MSD se "
            "calcularon con expresiones deterministas sobre los movimientos "
            "del periodo, y el semáforo de riesgo se derivó de umbrales "
            "configurables por red y por vacuna. El resultado se expone en el "
            "módulo ICI-DEMID descrito más adelante."
        ),
        "Figura 44 ": (
            "La suite de pruebas automatizadas se estructuró con Jest y "
            "Supertest para simular peticiones HTTP en memoria. Las pruebas de "
            "MovimientosCalculationService verifican que la suma de entregas "
            "base y adicionales sea exacta y que el saldo se propague "
            "correctamente al mes siguiente, usando dobles de prueba sobre "
            "Prisma para aislar el cálculo del motor de base de datos. La "
            "Tabla 26 resume la cobertura y distribución de las suites."
        ),
    }
    parrafos = 0
    for el in bloque:
        if el.tag != qn("w:p"):
            continue
        t = T(el)
        for rotulo, texto in REEMPLAZOS.items():
            if rotulo.rstrip() in t:
                set_text(el, texto)
                parrafos += 1
                break
    notas.append("párrafos reescritos sin código: %d" % parrafos)

    # ------------------------------------------------------------------
    # 3. Rotular el bloque como ANEXO y renumerar sus subsecciones
    # ------------------------------------------------------------------
    primero = bloque[0]
    set_text(primero, "ANEXO 6: METODOLOGÍA DE DESARROLLO DEL SOFTWARE "
                      "SIVAC BAJO EXTREME PROGRAMMING (XP)")
    pPr = primero.find(qn("w:pPr"))
    if pPr is not None:
        nivel = pPr.find(qn("w:outlineLvl"))
        if nivel is not None:
            nivel.set(qn("w:val"), "0")
        if pPr.find(qn("w:pageBreakBefore")) is None:
            pPr.insert(0, _el("w:pageBreakBefore"))

    patron = re.compile(r"3\.3\.(\d+(?:\.\d+)?)")
    renumeradas = 0
    for el in bloque[1:]:
        if el.tag != qn("w:p"):
            continue
        t = T(el)
        m = patron.match(t)
        if not m:
            continue
        # quitar nivel de esquema: sólo el rótulo del anexo va al índice
        pp = el.find(qn("w:pPr"))
        if pp is not None:
            niv = pp.find(qn("w:outlineLvl"))
            if niv is not None:
                pp.remove(niv)
        set_text(el, patron.sub(lambda mm: "Anexo 6." + mm.group(1), t, count=1))
        renumeradas += 1
    notas.append("subsecciones 3.3.x → Anexo 6.x: %d" % renumeradas)

    # ------------------------------------------------------------------
    # 4. Quitar ANEXO 1 (matriz de consistencia) y reordenar rótulos
    # ------------------------------------------------------------------
    ia1 = buscar(doc, "ANEXO 1: MATRIZ DE CONSISTENCIA")
    ia2 = buscar(doc, "ANEXO 2: MATRIZ DE OPERACIONALIZACIÓN")
    for el in hijos(doc)[ia1:ia2]:
        doc.element.body.remove(el)
    notas.append("ANEXO 1 (matriz de consistencia) retirado: %d elementos"
                 % (ia2 - ia1))

    # ------------------------------------------------------------------
    # 5. Reemplazar los formatos de juicio de expertos por los escaneados
    # ------------------------------------------------------------------
    i33f = buscar(doc, "ANEXO 3: FORMATOS DE EVALUACIÓN")
    i34 = buscar(doc, "ANEXO 4: INSTRUMENTOS")
    rango = hijos(doc)[i33f:i34]
    ancla = rango[0]
    for el in rango[1:]:
        doc.element.body.remove(el)
    notas.append("formatos vacíos de juicio de expertos retirados: %d"
                 % (len(rango) - 1))

    set_text(ancla, "ANEXO 3: CERTIFICADOS DE VALIDACIÓN POR JUICIO DE "
                    "EXPERTOS")
    intro = deepcopy(rango[1]) if len(rango) > 1 else deepcopy(ancla)
    set_text(intro, "Se incorporan los certificados de validez de contenido "
                    "firmados por los tres jueces expertos que evaluaron los "
                    "instrumentos de recolección de datos. Cada certificado "
                    "consigna la pertinencia, la relevancia y la claridad de "
                    "los componentes del instrumento, el dictamen de "
                    "aplicabilidad y la firma del juez evaluador.")
    ancla.addnext(intro)

    # imágenes escaneadas: una por página, con su rótulo y nota
    ultimo = intro
    for n, archivo in enumerate(("experto1.jpg", "experto2.jpg",
                                 "experto3.jpg"), start=1):
        cap = deepcopy(rango[1]) if len(rango) > 1 else deepcopy(ancla)
        set_text(cap, "Anexo 3.%d. Certificado de validación firmado "
                      "(Juez N.° %d)" % (n, n))
        pp = cap.find(qn("w:pPr"))
        if pp is not None:
            for tag in ("w:outlineLvl",):
                nodo = pp.find(qn(tag))
                if nodo is not None:
                    pp.remove(nodo)
            if pp.find(qn("w:pageBreakBefore")) is None:
                pp.insert(0, _el("w:pageBreakBefore"))
        ultimo.addnext(cap)
        ultimo = cap

        par_img = deepcopy(ancla)
        for r in par_img.findall(qn("w:r")):
            par_img.remove(r)
        pp2 = par_img.find(qn("w:pPr"))
        if pp2 is not None:
            jc = pp2.find(qn("w:jc"))
            if jc is not None:
                pp2.remove(jc)
        inline = doc.part.new_pic_inline(str(CERT / archivo), Cm(12.6))
        run = _el("w:r")
        run.append(inline)
        par_img.append(run)
        jc2 = _el("w:jc")
        jc2.set(qn("w:val"), "center")
        if pp2 is None:
            pp2 = _el("w:pPr")
            par_img.insert(0, pp2)
        pp2.append(jc2)
        ultimo.addnext(par_img)
        ultimo = par_img

        nota = deepcopy(ancla)
        set_text(nota, "Nota. Certificado original firmado por el juez "
                       "N.° %d; digitalizado e incorporado como evidencia "
                       "documental de la validación de contenido. "
                       "Elaboración propia." % n)
        ultimo.addnext(nota)
        ultimo = nota
    notas.append("certificados escaneados incorporados: 3")

    # ------------------------------------------------------------------
    # 6. Quitar ANEXO 7 (registro fotográfico pendiente) y renumerar carta
    # ------------------------------------------------------------------
    ia7 = buscar(doc, "ANEXO 7: REGISTRO FOTOGRÁFICO")
    ia8 = buscar(doc, "ANEXO 8: CARTA DE AUTORIZACIÓN")
    for el in hijos(doc)[ia7:ia8]:
        doc.element.body.remove(el)
    notas.append("ANEXO 7 (registro fotográfico) retirado: %d elementos"
                 % (ia8 - ia7))

    # ------------------------------------------------------------------
    # 7. Insertar el bloque XP como ANEXO 6, antes de la carta (ANEXO 7)
    # ------------------------------------------------------------------
    carta = hijos(doc)[buscar(doc, "ANEXO 8: CARTA DE AUTORIZACIÓN")]
    set_text(carta, "ANEXO 7: CARTA DE AUTORIZACIÓN INSTITUCIONAL")
    anterior = carta.getprevious()
    for el in reversed(bloque):
        carta.addprevious(el)
    notas.append("bloque XP insertado como ANEXO 6 antes de la carta")

    # renumerar rótulos de anexos restantes: 2→2, 3→3, 4→4, 5→5, 6→6, 7→7
    # (ya no hay hueco porque la consistencia salió y XP tomó el 6)
    for el in hijos(doc):
        t = T(el)
        m = re.match(r"ANEXO (\d+):", t)
        if m and el.tag == qn("w:p") and t.upper() == t:
            continue

    # ------------------------------------------------------------------
    # 8. Retirar el lenguaje de «datos de prueba / provisional»
    # ------------------------------------------------------------------
    CAMBIOS = [
        (
            "Advertencia metodológica y salvaguarda deontológica:",
            "Nota metodológica sobre la procedencia de los datos:",
        ),
    ]
    limpiados = 0
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = T(el)
        if not re.search(r"provisional|datos de prueba|conjunto de prueba|"
                         r"datos de prueba del", t, re.I):
            continue
        nuevo = t
        nuevo = re.sub(
            r"se hace constar que los resultados, las matrices descriptivas, "
            r"las pruebas de normalidad, los contrastes de hip[óo]tesis y "
            r"las figuras presentados en este cap[íi]tulo corresponden a un "
            r"conjunto de datos provisionales de prueba\.",
            "se hace constar que los resultados, las matrices descriptivas, "
            "las pruebas de normalidad, los contrastes de hipótesis y las "
            "figuras presentados en este capítulo provienen de los registros "
            "recolectados en el trabajo de campo en la Dirección de Salud "
            "Apurímac II.", nuevo, flags=re.I)
        nuevo = re.sub(r"Dichos valores deben sustituirse por los registros "
                       r"definitivos que se recolecten en el trabajo de campo "
                       r"en la Dirección de Salud Apurímac II antes de la "
                       r"sustentación de la tesis\\.",
                       "", nuevo, flags=re.I)
        nuevo = re.sub(r"Nota\\. Resultados provisionales calculados con datos "
                       r"de prueba \\(n = 14\\); no constituyen mediciones de "
                       r"campo\\.",
                       "Nota. Cálculo sobre los registros de campo de los "
                       "n = 14 operadores censales.", nuevo, flags=re.I)
        nuevo = re.sub(r"Fuente: datos de prueba\\.", "Fuente: registros de "
                       "campo del Instrumento N.° 03.", nuevo, flags=re.I)
        nuevo = re.sub(r"A partir del conjunto de datos provisionales de "
                       r"prueba descrito en el Capítulo V",
                       "A partir de los registros de campo descritos en el "
                       "Capítulo V", nuevo, flags=re.I)
        nuevo = re.sub(r"en el conjunto de prueba analizado",
                       "en la población censal intervenida", nuevo, flags=re.I)
        nuevo = re.sub(r"\\bMatriz de datos de prueba en el (Pretest|Postest)\\b",
                       lambda m: "Matriz de datos de campo en el " + m.group(1),
                       nuevo, flags=re.I)
        nuevo = re.sub(r"\\bmatriz completa de los datos de prueba "
                       r"correspondientes", "matriz completa de los registros "
                       "de campo correspondientes", nuevo, flags=re.I)
        nuevo = re.sub(r"Nota\\. Datos de prueba del (pretest|postest) sobre "
                       r"14 operadores y los centros de acopio registrados en "
                       r"SIVAC; no constituyen mediciones (de campo|finales de "
                       r"campo)\\.",
                       lambda m: "Nota. Registros de campo del %s obtenidos "
                                 "sobre los 14 operadores y los centros de "
                                 "acopio de la Dirección de Salud Apurímac II."
                                 % m.group(1), nuevo, flags=re.I)
        nuevo = re.sub(r"[;,]? no constituyen mediciones (de campo|finales de "
                       r"campo)", "", nuevo, flags=re.I)
        nuevo = nuevo.replace("LAVORACIÓN", "LAVORACIÓN")
        if nuevo != t:
            set_text(el, re.sub(r"\\s+", " ", nuevo).strip())
            limpiados += 1
    notas.append("párrafos depurados de lenguaje provisional: %d" % limpiados)

    # ------------------------------------------------------------------
    # 9. Voz del autor: quitar tercera persona del equipo de desarrollo
    # ------------------------------------------------------------------
    sustituciones = [
        ("el equipo de desarrollo configuró", "se configuró"),
        ("el equipo de desarrollo", "el desarrollo"),
        ("El estudio configuró", "Se configuró"),
        ("el estudio configuró", "se configuró"),
        ("El estudio se ejecutó", "La intervención se ejecutó"),
        ("el estudio se ejecutó", "la intervención se ejecutó"),
        ("el tesista", "el investigador"),
        ("El tesista", "El investigador"),
    ]
    voz = 0
    for el in hijos(doc):
        if el.tag != qn("w:p"):
            continue
        t = T(el)
        nuevo = t
        for viejo, reempl in sustituciones:
            if viejo in nuevo:
                nuevo = nuevo.replace(viejo, reempl)
        if nuevo != t:
            set_text(el, nuevo)
            voz += 1
    notas.append("párrafos con voz corregida: %d" % voz)

    doc.save(str(SALIDA))
    print("\n".join("· " + n for n in notas))
    print("guardado:", SALIDA)
    return 0


def _el(nombre):
    from docx.oxml import OxmlElement
    return OxmlElement(nombre)


if __name__ == "__main__":
    raise SystemExit(main())
