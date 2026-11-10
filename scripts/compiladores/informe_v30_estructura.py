# -*- coding: utf-8 -*-
"""Informe final v30: estructura de tesis, datos reales y anexos depurados.

Construye la v30 a partir de la v29 con seis operaciones, sin tocar los
valores estadísticos ya consolidados:

1. Retira del Capítulo III la sección 3.3 (desarrollo práctico del software
   SIVAC bajo XP) y la reubica en Anexos como ANEXO 2, con numeración
   interna «Anexo 2.1.» a «Anexo 2.1.1.» y sin niveles de esquema en las
   subsecciones (sólo el rótulo del anexo entra en el índice de contenido).
2. Elimina el ANEXO 1 (Matriz de consistencia metodológica): corresponde al
   proyecto, no al informe.
3. Quita del bloque XP las siete figuras de código fuente (22, 23, 24, 25,
   26, 27 y 44) y reescribe los párrafos que las anunciaban.
4. Sustituye los tres formatos de validación del ANEXO 3 por las tres
   fichas firmadas escaneadas (experto1.jpg, experto2.jpg, experto3.jpg).
5. Elimina el ANEXO 7 (registro fotográfico pendiente) y renumera la carta
   de autorización a ANEXO 7.
6. Corrige el tiempo verbal del 4.11/4.12 y retira del Capítulo V y de las
   conclusiones toda marca de dato «provisional» o «de prueba».

Los índices (contenido, figuras y tablas) se rehacen después con
``informe_v30_indices``.

Uso
---
    python scripts/compiladores/informe_v30_estructura.py
"""

from __future__ import annotations

import argparse
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "compiladores"))

import indices_pdf as IDX  # noqa: E402
from docx import Document  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm  # noqa: E402

ENTRADA = RAIZ / "salidas" / "documentos" / "informe_final_v29.docx"
SALIDA = RAIZ / "salidas" / "documentos" / "informe_final_v30.docx"

CERTIFICADOS = (
    RAIZ / "datos" / "recolectados" / "experto1.jpg",
    RAIZ / "datos" / "recolectados" / "experto2.jpg",
    RAIZ / "datos" / "recolectados" / "experto3.jpg",
)

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def texto_el(el) -> str:
    return "".join(el.itertext())


def hijos(doc: Document) -> List:
    return [el for el in doc.element.body.iterchildren() if el.tag != qn("w:sectPr")]


def indice_por_texto(doc: Document, inicial: str, desde: int = 0) -> int:
    for i, el in enumerate(hijos(doc)):
        if i < desde:
            continue
        if texto_el(el).strip().startswith(inicial):
            return i
    raise RuntimeError("no se encontró el elemento que empieza por %r" % inicial)


def quitar(doc: Document, desde: int, hasta: int) -> None:
    cuerpo = doc.element.body
    for el in hijos(doc)[desde:hasta]:
        cuerpo.remove(el)


def sectpr_de(el):
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        return None
    return pPr.find(qn("w:sectPr"))


def fijar_corrido(par, texto: str) -> None:
    """Deja el texto en el primer run no nulo del párrafo."""
    runs = [r for r in par.runs if (r.text or "").strip()]
    if not runs:
        par.add_run(texto)
        return
    runs[0].text = texto
    for r in runs[1:]:
        r.text = ""


# ---------------------------------------------------------------------------
# Paso 1: extraer 3.3 del Capítulo III
# ---------------------------------------------------------------------------


def extraer_seccion_xp(doc: Document) -> List:
    """Corta el bloque 3.3 y devuelve sus elementos."""
    desde = indice_por_texto(doc, "3.3. Metodología")
    hasta = indice_por_texto(doc, "CAPÍTULO IV: METODOLOGÍA DE LA INVESTIGACIÓN")
    elementos = hijos(doc)[desde:hasta]
    for el in elementos:
        if sectpr_de(el) is not None:
            raise RuntimeError("el bloque 3.3 contiene un corte de sección")
    for el in elementos:
        doc.element.body.remove(el)
    return elementos


def convertir_rotulo_anexo(elemento) -> None:
    """Rotula el antiguo 3.3 como ANEXO 2 y le quita los niveles de esquema."""
    pPr = elemento.find(qn("w:pPr"))
    pPr.insert(0, OxmlElement("w:pageBreakBefore"))
    pPr.insert(0, OxmlElement("w:keepNext"))
    esp = pPr.find(qn("w:spacing"))
    if esp is None:
        esp = OxmlElement("w:spacing")
        pPr.append(esp)
    esp.set(qn("w:before"), "0")
    esp.set(qn("w:after"), "120")
    esp.set(qn("w:line"), "360")
    esp.set(qn("w:lineRule"), "auto")
    jc = pPr.find(qn("w:jc"))
    if jc is not None:
        pPr.remove(jc)
    for indice in elemento.iter(qn("w:instrText")):
        if "SEQ" in (indice.text or ""):
            raise RuntimeError("el rótulo de 3.3 trae un campo SEQ inesperado")


def renumerar_subsecciones(elementos: Sequence) -> int:
    """Reescribe 3.3.x como Anexo 2.x y quita outlineLvl de las subsecciones."""
    cambiados = 0
    patron = re.compile(r"3\.3\.(\d+(?:\.\d+)?)")
    for el in elementos:
        if el.tag != qn("w:p"):
            continue
        t = texto_el(el)
        pPr = el.find(qn("w:pPr"))
        nivel = None if pPr is None else pPr.find(qn("w:outlineLvl"))
        if nivel is not None and nivel.get(qn("w:val")) != "1":
            # las subsecciones dejan de entrar en el índice de contenido
            pPr.remove(nivel)
        if not patron.match(t.strip()):
            continue
        for nodo in el.iter(qn("w:t")):
            if nodo.text and patron.search(nodo.text):
                nodo.text = patron.sub(lambda m: "Anexo 2." + m.group(1),
                                       nodo.text)
                cambiados += 1
                break
    return cambiados


def rotular_anexo_xp(elementos: Sequence) -> None:
    """Cambia el título de la sección por el del anexo."""
    primero = elementos[0]
    partes = list(primero.iter(qn("w:t")))
    for nodo in partes:
        if nodo.text and nodo.text.strip():
            nodo.text = "ANEXO 2: METODOLOGÍA DE DESARROLLO DEL SOFTWARE " \
                        "SIVAC BAJO EXTREME PROGRAMMING (XP)"
            break
    for nodo in partes[1:]:
        nodo.text = ""
    pPr = primero.find(qn("w:pPr"))
    nivel = pPr.find(qn("w:outlineLvl"))
    if nivel is not None:
        nivel.set(qn("w:val"), "0")


# ---------------------------------------------------------------------------
# Paso 2: quitar las figuras de código
# ---------------------------------------------------------------------------

# Rótulos de las figuras de código que salen del bloque.
FIGURAS_CODIGO = ("Figura 22 ", "Figura 23 ", "Figura 24 ", "Figura 25 ",
                  "Figura 26 ", "Figura 27 ", "Figura 44 ")

# Párrafo introductorio reescrito para cada figura retirada.
REEMPLAZOS_CODIGO = {
    "Figura 22 ": (
        "El backend se organizó en capas estrictas dentro de un monolito modular "
        "en Node.js con Express y Prisma ORM sobre PostgreSQL 16: las rutas "
        "declaran los contratos HTTP, los controladores validan la entrada y "
        "orquestan el caso de uso, la capa de servicios concentra las reglas de "
        "negocio puras y la de repositorios aísla el acceso a datos. Las suites "
        "de pruebas viven junto al código que ejercitan, de modo que cada "
        "refactorización se valida en el acto. La Tabla 25 resume el stack "
        "tecnológico completo."
    ),
    "Figura 23 ": (
        "El cliente web se construyó como una aplicación de página única en "
        "React 18 con TypeScript y Vite, organizada por dominios funcionales "
        "(autenticación, inventario, movimientos, kardex, planificación, "
        "reportes y administración). Cada dominio agrupa sus componentes de "
        "presentación, sus servicios de acceso a la API y sus tipos compartidos, "
        "lo que permite que un cambio en un módulo no se propague al resto de "
        "la interfaz."
    ),
    "Figura 24 ": (
        "La sincronización de saldos intermensuales se resolvió con un algoritmo "
        "recursivo que arrastra el saldo final de un mes como saldo inicial del "
        "siguiente, sumando las entregas adicionales y descontando las salidas "
        "antes de propagar el resultante. El cálculo es idempotente: reejecutarlo "
        "sobre el mismo periodo produce el mismo kardex, condición necesaria para "
        "que la corrección de un asiento no altere periodos ya cerrados."
    ),
    "Figura 25 ": (
        "El servicio de alertas tempranas evalúa cada lote contra tres "
        "condiciones —proximidad al vencimiento, nivel de stock frente a la "
        "demanda proyectada y desviación del consumo histórico— y aplica una "
        "ventana de enfriamiento que impide repetir el aviso mientras la "
        "condición persiste. Así se evita el ruido de alertas duplicadas que "
        "desensibiliza al operador."
    ),
    "Figura 26 ": (
        "La autenticación se implementó con JSON Web Tokens firmados y "
        "contraseñas resguardadas con Bcrypt. Un middleware intercepta cada "
        "petición, verifica la firma y la vigencia del token, extrae el "
        "identificador del usuario y sus permisos, y los adjunta al contexto de "
        "la petición; los controladores autorizan después por rol y por centro "
        "de acopio. La Tabla 9 detalla la matriz de acceso resultante."
    ),
    "Figura 27 ": (
        "Los indicadores de disponibilidad logística del estándar MSD se "
        "calcularon con expresiones deterministas sobre los movimientos del "
        "periodo, y el semáforo de riesgo se derivó de umbrales configurables "
        "por red y por vacuna. El resultado se expone en el módulo ICI-DEMID "
        "descrito en el Capítulo V."
    ),
    "Figura 44 ": (
        "La suite de pruebas automatizadas se estructuró con Jest y Supertest "
        "para simular peticiones HTTP en memoria. Las pruebas de "
        "MovimientosCalculationService verifican que la suma de entregas base y "
        "adicionales sea exacta y que el saldo se propague correctamente al mes "
        "siguiente, usando dobles de prueba sobre Prisma para aislar el cálculo "
        "del motor de base de datos. La Tabla 26 resume la cobertura y "
        "distribución de las suites."
    ),
}


def es_rotulo_figura(el) -> Optional[str]:
    if el.tag != qn("w:p"):
        return None
    pPr = el.find(qn("w:pPr"))
    if pPr is None:
        return None
    est = pPr.find(qn("w:pStyle"))
    if est is None or est.get(qn("w:val")) != "Rotulodeilustracion":
        return None
    t = texto_el(el).strip()
    for rotulo in FIGURAS_CODIGO:
        if t.startswith(rotulo):
            return rotulo
    return None


def quitar_figuras_codigo(elementos: List) -> Tuple[int, int]:
    """Borra rótulo, imagen y nota de cada figura de código."""
    quitadas = 0
    parrafos = 0
    i = 0
    while i < len(elementos):
        rotulo = es_rotulo_figura(elementos[i])
        if rotulo is None:
            i += 1
            continue
        del elementos[i:i + 3]
        quitadas += 1
        continue
    # párrafos introductorios que anunciaban la figura
    for i, el in enumerate(elementos):
        if el.tag != qn("w:p"):
            continue
        t = texto_el(el)
        for rotulo, nuevo in REEMPLAZOS_CODIGO.items():
            corto = rotulo.replace("Figura ", "Figura ")
            if corto in t and ("En la " + corto in t or "La " + corto in t
                               or corto + "ilustra" in t or corto + "muestra" in t
                               or corto + "presenta" in t):
                fijar_corrido_el(el, nuevo)
                parrafos += 1
                break
    return quitadas, parrafos


def fijar_corrido_el(el, texto: str) -> None:
    from docx.text.paragraph import Paragraph

    par = Paragraph(el, None)
    runs = [r for r in par.runs if (r.text or "").strip()]
    if not runs:
        par.add_run(texto)
        return
    runs[0].text = texto
    for r in runs[1:-1]:
        r.text = ""
