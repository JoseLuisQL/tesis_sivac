# -*- coding: utf-8 -*-
"""Guía de llenado del paquete de instrumentos v22.

Los tres instrumentos imprimibles dicen qué casilla existe, pero no qué se
escribe en ella ni cómo se comprueba que el dato quedó completo. Esta guía
cierra ese hueco: qué se imprime y cuántas veces, en qué orden se aplica una
sesión, qué recibe cada columna, qué se calcula en la hoja y cuáles son las
comprobaciones que deben cerrar antes de que el auditor firme. Es un documento
operativo: no es anexo de la tesis ni sustituye a las fichas.

Uso
---
    python scripts/compiladores/guia_campo_v22_builder.py
    python scripts/compiladores/guia_campo_v22_builder.py --sin-pdf
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import instrumentos_recoleccion_v22_builder as base  # noqa: E402

VERSION = "v22"
BASE = RAIZ / "salidas" / "instrumentos" / ("INSTRUMENTOS_DEFINITIVOS_" + VERSION)
DIR_GUIA = BASE / "05_GUIA"

NOMBRE = "GUIA_DE_LLENADO"


# ---------------------------------------------------------------------------
# Utilidades de maqueta
# ---------------------------------------------------------------------------

def _titulo(doc, seccion: str, texto: str, nueva: bool = True) -> None:
    base.rotulo(doc, seccion, texto, nueva_hoja=nueva)


def _cuadro(doc, filas: List[List[Any]], anchos: List[float],
            alturas: List[float] | None = None, size: float = 9.0,
            izq: tuple = ()) -> None:
    """Rejilla de la guía: la primera fila es encabezado y las columnas se
    marcan a la izquierda, porque todas contienen texto, no marcas."""
    base.tabla(doc, filas, anchos, alturas=alturas, size=size,
               negritas=(0,), izq=tuple(range(len(anchos))),
               margenes=(60, 20))


def _interlinea1(doc, texto: str, antes: float = 6, despues: float = 8) -> None:
    """Epígrafe de sección. Se mantiene junto al párrafo o tabla que abre."""
    p = base.par(doc, texto, size=base.CUERPO, bold=True, antes=antes,
                 despues=despues, alineacion="left", interlinea=1.15)
    p.paragraph_format.keep_with_next = True


def _parrafo(doc, texto: str, antes: float = 6, despues: float = 6) -> None:
    base.par(doc, texto, size=base.CUERPO, sangria=True, antes=antes,
             despues=despues, alineacion="justify", interlinea=1.15)


def _vineta(doc, numero: str, texto: str) -> None:
    base.par(doc, f"{numero} {texto}", size=base.CUERPO, sangria=True,
             antes=0, despues=4, alineacion="justify", interlinea=1.15)


# ---------------------------------------------------------------------------
# Contenido
# ---------------------------------------------------------------------------

def pagina_estado(doc) -> None:
    _titulo(doc, "Guía de campo.",
            "Llenado del paquete de instrumentos y control de la sesión")

    _parrafo(doc,
             "Esta guía acompaña a los tres imprimibles del paquete v22 y "
             "ordena el trabajo de una sesión de medición: qué se imprime, en "
             "qué orden se aplica, qué recibe cada casilla, qué se calcula en "
             "la propia hoja y qué debe cuadrar antes de firmar. No es un "
             "anexo de la tesis ni un formato de validación: no se entrega a "
             "los expertos ni se cita como fuente.")

    _interlinea1(doc, "1. Qué es y qué no es el conjunto de datos disponible")

    _parrafo(doc,
             "El archivo datos/recolectados/SIVAC_DATOS_CAMPO.md lleva en su "
             "encabezado el estado DATOS DE PRUEBA — REEMPLAZAR (DEC-007): sus "
             "cifras se derivan del conjunto sintético de datos/prueba_sintetica/ "
             "(semilla 20261026) y no acreditan medición de campo. Sirve para "
             "comprobar que la estructura, los identificadores y las reglas de "
             "cálculo cierran; no sirve como registro que se traslada al papel. "
             "La ficha impresa es el documento primario: lo que se escribe en "
             "ella durante la observación es lo que después se digita, y el "
             "registro en Markdown se regenera desde esa digitación. Copiar los "
             "valores del archivo a las hojas invertiría el orden y produciría "
             "un instrumento que parece medido sin haberlo sido.")

    _cuadro(doc, [
        ["Elemento", "Estado", "Uso previsto"],
        ["Ficha de tiempos (Anexo 4.1)",
         "Blanco, listo para imprimir",
         "Se llena con cronómetro durante la operación observada."],
        ["Ficha documental (Anexo 4.2)",
         "Blanco, listo para imprimir",
         "Se llena revisando el kardex y las guías del periodo auditado."],
        ["Cuestionario (Anexo 4.3)",
         "Blanco, listo para imprimir",
         "Lo responde el operador; el encuestador solo identifica la hoja."],
        ["SIVAC_DATOS_CAMPO.md",
         "Conjunto de prueba (DEC-007)",
         "Referencia de estructura y de aritmética; se reemplaza al digitar."],
        ["pretest_campo.csv / posttest_campo.csv",
         "Consolidado de prueba (DEC-007)",
         "Se sobrescriben con lo digitado de las fichas."],
    ], [4.6, 4.0, 6.9], [0.52, 0.60, 0.60, 0.60, 0.60, 0.60], size=8.5,
        izq=(0, 1, 2))

    _interlinea1(doc, "2. Qué se imprime y cuántas veces")

    _parrafo(doc,
             "Una sesión es un operador en un momento: catorce operadores por "
             "dos momentos dan veintiocho sesiones. Cada sesión usa cinco "
             "hojas de instrumento y una hoja de observaciones; esta última se "
             "imprime siempre, porque en ella se anota lo que no cabe en las "
             "columnas de las otras.")

    _cuadro(doc, [
        ["Documento", "Hojas", "Por sesión", "Total (28 sesiones)"],
        ["03 · Instrumento 01 · tiempos", "1", "1", "28"],
        ["04 · Instrumento 02 · kardex (asientos 1 a 20)", "1", "1", "28"],
        ["04 · Instrumento 02 · kardex (asientos 21 a 40)", "1", "1", "28"],
        ["04 · Instrumento 02 · despachos (25)", "1", "1", "28"],
        ["05 · Instrumento 03 · cuestionario TAM", "1", "1", "28"],
        ["Hoja de observaciones de la sesión", "1", "1", "28"],
        ["Total de hojas por juego", "6", "6", "168"],
    ], [8.0, 1.6, 2.2, 3.7], [0.52] + [0.40] * 6 + [0.46], size=8.5,
        izq=(0,))

    _parrafo(doc,
             "Se imprime además la carta de autorización institucional "
             "(01_CARTA_AUTORIZACION_v22.pdf): es el oficio escaneado de la "
             "DISA Apurímac II y se adjunta a cada juego de campo, uno por "
             "centro de acopio. El formato de validación por juez no se "
             "imprime: pertenece al expediente de expertos y no forma parte "
             "del paquete de campo. Las hojas se toman de la carpeta "
             "01_IMPRIMIBLES del paquete v22; la v21 no admite el registro: no "
             "tiene pausa ni motivo, une documento y lote en una celda, no "
             "declara el tipo de asiento, no tiene columna de validez y no deja "
             "anotar la observación de cada fila.")

    _interlinea1(doc, "3. Orden de la sesión")

    _cuadro(doc, [
        ["Paso", "Qué se hace", "Hoja"],
        ["1", "Identificar la hoja antes de observar: operador (TRAB-01 a "
              "TRAB-14), centro de acopio con su código, fecha, momento "
              "(Antes o Con el SIVAC) y observador. No se escribe el nombre del "
              "trabajador ni su documento.", "Todas"],
        ["2", "Cronometrar las tres réplicas de registro y las tres de emisión, "
              "en ese orden, sin intercalar otras tareas.", "Anexo 4.1"],
        ["3", "Auditar cuarenta asientos del kardex del periodo, veinte por "
              "hoja.", "Anexo 4.2 A"],
        ["4", "Conciliar veinticinco despachos del mismo periodo.",
         "Anexo 4.2 B"],
        ["5", "Entregar el cuestionario, recogerlo, sumar AP, UP y TAM y fijar "
              "el nivel.", "Anexo 4.3"],
        ["6", "Comprobar los totales de la sección 7, firmar cada hoja y "
              "archivar el juego completo.", "Todas"],
    ], [1.1, 11.4, 3.0], [0.44] + [0.62] * 6, size=8.2, izq=(1, 2))

    _interlinea1(doc, "4. Códigos de la población censal")

    _parrafo(doc,
             "Los catorce operadores se identifican con el código, nunca con el "
             "nombre. El código del centro se copia en la casilla «Centro de "
             "acopio» de todas las hojas y es el que permite agrupar después "
             "por establecimiento. Dos operadores comparten el almacén de "
             "Chanka: son dos sesiones distintas con el mismo código de centro.")

    _cuadro(doc, [
        ["Operador", "Centro de acopio", "Código", "Operador", "Centro de acopio",
         "Código"],
        ["TRAB-01", "ALMACÉN (CHANKA)", "CHANKA-001", "TRAB-08", "Huancaray",
         "4158"],
        ["TRAB-02", "ALMACÉN (CHANKA)", "CHANKA-001", "TRAB-09", "Chicmo",
         "4202"],
        ["TRAB-03", "Hospital Andahuaylas", "S/C", "TRAB-10", "Huancabamba",
         "4172"],
        ["TRAB-04", "Hospital ESSALUD Andahuaylas", "11214", "TRAB-11",
         "Pampachiri", "4167"],
        ["TRAB-05", "Centro de Salud Andahuaylas", "6804", "TRAB-12",
         "San Antonio de Cachi", "4160"],
        ["TRAB-06", "Talavera", "4195", "TRAB-13", "Turpo", "4163"],
        ["TRAB-07", "San Jeronimo", "4167-SJ", "TRAB-14", "Kishuara", "4183"],
    ], [1.75, 3.95, 2.15, 1.75, 3.75, 2.15], [0.46] + [0.44] * 7, size=8.0,
        izq=(0, 1, 3, 4))

    base.nota(doc, "S/C: el establecimiento no consigna código en el padrón de "
                   "la red; se anota así, sin inventar un número.", antes=4)

    _interlinea1(doc, "5. Reglas de escritura de las hojas")

    _parrafo(doc,
             "Las reglas son las mismas en los tres instrumentos y existen para "
             "que la hoja pueda auditarse meses después, cuando quien la llenó "
             "ya no esté disponible para explicarla. La hoja no se reescribe en "
             "limpio: se corrige sobre ella y la corrección queda visible.")

    _cuadro(doc, [
        ["Situación", "Qué se hace", "Qué no se hace"],
        ["Tinta", "Azul o negra, letra legible, cifras claras.",
         "Lápiz, ni borrado, ni corrector."],
        ["Error en una cifra", "Una línea sobre el valor, el correcto al lado y "
                               "la rúbrica de quien corrige.",
         "Tachar hasta ocultar el valor original."],
        ["Campo que no aplica", "N/A, con la causa en observaciones si no es "
                                "evidente.",
         "Dejarlo en blanco sin explicación."],
        ["Valor igual a cero", "0, que es un dato.",
         "Confundirlo con el campo vacío."],
        ["Cifras", "Minutos con cuatro decimales, porcentajes con dos, dosis "
                   "enteras.", "Redondear al escribir."],
        ["Fechas", "dd/mm/aaaa, la del día de la observación.",
         "Fechas estimadas o posteriores al llenado."],
        ["Firma", "Cada hoja, con nombre y cargo en la hoja de observaciones.",
         "Firmar en blanco o delegar la firma."],
    ], [3.1, 6.6, 5.8], [0.46] + [0.56] * 7, size=8.0, izq=(0, 1, 2))


def pagina_tiempos(doc) -> None:
    _titulo(doc, "Instrumento 01.",
            "Qué se anota en la ficha de tiempos")

    _parrafo(doc,
             "La ficha registra seis operaciones por sesión: tres de registro "
             "del movimiento y tres de emisión del vale. Cada fila es una "
             "réplica y cada réplica se mide con cronómetro, no se estima. El "
             "encabezado de la ficha pide operador, centro, fecha, momento, "
             "observador y periodo; el periodo es el intervalo del kardex que "
             "se está midiendo y solo se usa para enlazar la ficha con la "
             "auditoría documental del mismo día.")

    _cuadro(doc, [
        ["Casilla", "Qué se escribe", "Regla"],
        ["Escenario y tarea", "Ya impreso (T1 a T6).",
         "No se modifica: la tarea define qué operación se mide."],
        ["Documento N.°", "Número del ingreso, salida o transferencia (T1 a T3); "
                          "vale PECOSA (T4 a T6).",
         "Se copia literal del documento. Si no existe, la réplica no es válida."],
        ["Lote", "Código del biológico (por ejemplo ROTA-2605-833M).",
         "Solo en T1 a T3. En los vales se deja en blanco."],
        ["Hora de inicio / de corte", "HH:MM:SS con segundos.",
         "En el vale, la hora de solicitud y la de emisión. Se lee del "
         "cronómetro, no del reloj de pared."],
        ["Pausa (s)", "Segundos enteros de interrupción externa.",
         "Se anota 0 o se deja en blanco cuando no hubo pausa."],
        ["Motivo", "P1 atención en ventanilla · P2 llamada del establecimiento "
                   "· P3 corte breve de energía · P4 verificación de existencias.",
         "Toda pausa lleva motivo; un motivo sin pausa es un error de llenado."],
        ["T_reg / T_vale (min)", "Corte − inicio − pausa, en minutos con cuatro "
                                 "decimales.",
         "Se calcula al cerrar la fila. La aritmética debe cuadrar al segundo."],
        ["Válida (S/N)", "S si la operación se completó sin interrupción no "
                         "anotada.", "Si es N, se explica en observaciones y se "
                                     "repite hasta tener tres válidas."],
    ], [3.1, 6.4, 6.0], [0.52, 0.52, 0.90, 0.52, 0.66, 0.52, 0.90, 0.90, 0.66],
        size=8.2, izq=(0, 1, 2))

    _interlinea1(doc, "Comprobación de la hoja", antes=8, despues=4)

    _parrafo(doc,
             "En cada fila, hora de corte − hora de inicio debe igualar la "
             "duración neta más la pausa. En el resumen se escriben los dos "
             "promedios con cuatro decimales y el número de réplicas válidas "
             "sobre seis. Si una réplica quedó inválida, el resumen lo refleja y "
             "la réplica de reemplazo se mide el mismo día, en una fila adicional "
             "de la hoja de observaciones con la misma estructura de columnas.")

    _cuadro(doc, [
        ["Ejemplo (TRAB-01, pretest, T2)",
         "Inicio 08:05:22 · corte 08:46:25 · pausa 90 s"],
        ["Intervalo", "41 min 03 s = 2463 s"],
        ["Duración neta", "2463 − 90 = 2373 s = 39.5500 min"],
        ["Registro en la ficha", "39.5500 en T_reg · P3 en Motivo · S en Válida"],
    ], [4.6, 10.9], [0.44, 0.44, 0.44, 0.44], size=8.5, izq=(0, 1))


def pagina_documental(doc) -> None:
    _titulo(doc, "Instrumento 02.",
            "Qué se anota en la ficha de auditoría y en la conciliación")

    _parrafo(doc,
             "La ficha tiene dos bloques. El bloque A audita cuarenta asientos "
             "del kardex con ocho criterios binarios, en dos hojas de veinte "
             "renglones; el bloque B concilia veinticinco despachos. Los tres "
             "documentos cubren el mismo periodo auditado, que se escribe como "
             "intervalo de fechas en el encabezado: en la práctica, los treinta "
             "días anteriores a la sesión.")

    _interlinea1(doc, "Bloque A. Asientos del kardex", antes=8, despues=4)

    _cuadro(doc, [
        ["Casilla", "Qué se escribe", "Regla"],
        ["Fecha", "dd/mm/aaaa del asiento; dentro del periodo auditado.", ""],
        ["Tipo", "ING · SAL · TRA · DEV · AJU.",
         "Es el tipo del documento, no el signo del movimiento."],
        ["Documento", "Número completo del asiento.", "Se copia del kardex."],
        ["Biológico / Lote", "Sigla del biológico y código del lote.",
         "Dos columnas distintas: el criterio 1 y el 2 se marcan por separado."],
        ["Cant.", "Dosis del asiento, en unidades enteras.", "Sin decimales."],
        ["Criterios 1 a 8", "S o N en cada casilla.",
         "1 biológico · 2 lote · 3 vencimiento · 4 cantidad física · "
         "5 origen y destino · 6 responsable y firma · 7 saldo aritmético · "
         "8 correlatividad."],
        ["Conf.", "S solo si los ocho criterios están en S.",
         "Un solo N vuelve no conforme el asiento."],
        ["Motivo", "Los códigos de los criterios marcados N, unidos con + "
                   "(por ejemplo M2+M8).",
         "Se imprime solo cuando el asiento no es conforme."],
        ["Observación", "Frase breve del auditor (hasta unas cuarenta letras).",
         "Obligatoria cuando hay motivo; describe el hecho, no la corrección."],
    ], [2.9, 6.6, 6.0], [0.52, 0.52, 0.52, 0.52, 0.52, 0.52, 0.90, 0.90, 0.90],
        size=8.2, izq=(0, 1, 2))

    _parrafo(doc,
             "Al pie de cada hoja se anotan los asientos revisados, los "
             "conformes y el RSD de esa hoja; la hoja 2 cierra con el total de "
             "cuarenta. RSD es conformes entre revisados por cien. Si el kardex "
             "del periodo tiene menos asientos, se auditan los disponibles, se "
             "anota el total real en observaciones y el indicador se recalcula "
             "sobre ese total.")


    _interlinea1(doc, "Bloque B. Conciliación de despachos", antes=8, despues=4)

    _parrafo(doc,
             "La segunda hoja concilia veinticinco despachos del mismo operador "
             "y momento. Se llena con la guía de remisión o la PECOSA a la vista "
             "y con el conteo físico de la entrega, no con el saldo del sistema: "
             "el propósito es comparar lo programado con lo entregado, y "
             "corregir una cifra en la hoja anularía la comparación.")

    _cuadro(doc, [
        ["Casilla", "Qué se escribe", "Regla"],
        ["Programado / Entregado", "Dosis previstas y dosis físicamente "
                                   "entregadas.", "Ambas se leen del documento y "
                                                "del conteo, no se corrigen entre sí."],
        ["Diferencia", "Entregado − programado.",
         "Negativa, faltante; positiva, exceso; cero, concordante."],
        ["Documento", "Guía de remisión o PECOSA; «Sin guía» si no existe.",
         "Un despacho sin documento no es conforme aunque la cantidad cuadre."],
        ["Conf.", "Sí solo si la diferencia es cero y el documento coincide con "
                  "el registro.", "Se anota el hecho; la hoja no se corrige."],
        ["Obs.", "Frase breve del auditor.", "Explica la causa aparente del "
                                             "faltante o exceso."],
    ], [3.4, 6.4, 5.7], [0.52, 0.66, 0.66, 0.90, 0.66], size=8.2,
        izq=(0, 1, 2))

    _parrafo(doc,
             "El cierre anota despachos evaluados, conformes y CPE, que es "
             "conformes dividido entre evaluados por cien. Si el periodo tiene "
             "menos de veinticinco despachos, se concilian los existentes y se "
             "declara el total real en observaciones; el indicador se calcula "
             "sobre ese total.")


def pagina_cuestionario(doc) -> None:
    _titulo(doc, "Instrumento 03.",
            "Qué se anota en el cuestionario de satisfacción")

    _parrafo(doc,
             "El cuestionario tiene ocho reactivos con escala de 1 a 5 y se "
             "aplica en las dos fases. El operador marca una sola casilla por "
             "reactivo; el encuestador no sugiere respuestas ni comenta los "
             "enunciados más allá de leerlos tal como están impresos. La hoja no "
             "lleva nombre: la identificación es el código del operador.")

    _cuadro(doc, [
        ["Casilla", "Qué se escribe", "Regla"],
        ["Operador / Centro", "TRAB-01 a TRAB-14 y código del centro.",
         "El mismo código que en las fichas 01 y 02 de la sesión."],
        ["Momento", "Antes o Con el SIVAC.", "Debe coincidir con las otras dos "
                                             "fichas de la sesión."],
        ["Reactivos AP-01 a AP-04", "Entero de 1 a 5.",
         "Aceptación del proceso; suma máxima 20."],
        ["Reactivos UP-01 a UP-04", "Entero de 1 a 5.",
         "Utilidad percibida; suma máxima 20."],
        ["AP / UP / TAM", "Sumas de los cuatro reactivos de cada bloque y total.",
         "Se completan al final; el encuestado no los ve."],
        ["Nivel", "Bajo 8 a 18 · Medio 19 a 29 · Alto 30 a 40.",
         "Baremo fijado antes de observar los datos."],
    ], [3.9, 6.2, 5.4], [0.52, 0.66, 0.52, 0.52, 0.52, 0.52, 0.66], size=8.2,
        izq=(0, 1, 2))

    _parrafo(doc,
             "Un reactivo sin marcar no se imputa: se devuelve la hoja al "
             "operador en el mismo acto y, si ya no es posible, se anota la "
             "ausencia en observaciones y el puntaje se calcula sobre los "
             "reactivos respondidos, dejando constancia. Si el operador declara "
             "no haber usado el sistema en la fase con SIVAC, la sesión de ese "
             "operador se registra como no aplicable en la fase y no se fuerza "
             "una respuesta.")

    _interlinea1(doc, "Módulo B del postest", antes=8, despues=4)

    _parrafo(doc,
             "El cuestionario complementario de ocho reactivos (PU y PE) se "
             "aplica solo en el postest y no forma parte del paquete v22 porque "
             "no integra el anexo de la tesis. Cuando se aplique, se usa el "
             "imprimible del paquete de campo "
             "(02_POST/09_CUESTIONARIO_B_POST.pdf), se archiva junto con la "
             "sesión y sus puntajes se presentan como caracterización "
             "descriptiva: no se suman al TAM, no se comparan con él y no "
             "entran en las pruebas de hipótesis.")


def pagina_cierre(doc) -> None:
    _titulo(doc, "Cierre de la sesión.",
            "Digitación, control de calidad y pendientes")

    _interlinea1(doc, "6. De la hoja al archivo")

    _parrafo(doc,
             "Cada fila de la ficha se convierte en una fila del libro de "
             "captura y, después, en una fila del consolidado. El orden es "
             "siempre el mismo: primero la ficha en papel, luego el libro de "
             "captura y por último los dos archivos consolidados, uno por fase. "
             "El libro de captura conserva el detalle que el consolidado "
             "resume: las 168 réplicas, los 1 120 asientos, los 700 despachos y "
             "los 224 reactivos. Las columnas llevan el nombre del diccionario "
             "de variables, de modo que el consolidado se obtiene agrupando y "
             "promediando, sin volver a teclear valores.")

    _parrafo(doc,
             "El libro es el archivo LIBRO_DE_CAPTURA_v22.xlsx de la carpeta "
             "07_CAPTURA y ya trae una fila por cada registro previsto, con la "
             "identificación escrita —operador, centro, momento, fecha, "
             "observador, tarea y número de réplica o de asiento— y las celdas "
             "de medición en blanco. Solo se teclean las columnas con fondo "
             "crema; las grises no se tocan. Si una fila no existe en el papel, "
             "se deja vacía y se explica en la hoja de observaciones; nunca se "
             "borra ni se duplica.")

    _cuadro(doc, [
        ["Hoja del libro", "Una fila por", "Filas esperadas",
         "Qué se digita"],
        ["01_replicas", "réplica cronometrada", "168",
         "documento, lote, horas, pausa, motivo y validez"],
        ["02_asientos", "asiento auditado", "1 120",
         "fecha, tipo, biológico, lote, cantidad, c1 a c8, conf. y motivo"],
        ["02_despachos", "despacho conciliado", "700",
         "fecha, biológico, programado, entregado y documento"],
        ["03_reactivos", "reactivo respondido por fase", "224",
         "valor 1 a 5 y observación"],
    ], [3.9, 4.4, 2.6, 5.0], [0.44, 0.44, 0.44, 0.44, 0.52], size=8.2,
        izq=(0, 1, 2, 3))

    _interlinea1(doc, "7. Comprobaciones antes de firmar")

    for n, texto in enumerate([
        "La identificación de todas las hojas coincide: operador, centro, "
        "fecha y momento.",
        "En la ficha 01, la aritmética cuadra al segundo en las seis filas y el "
        "resumen tiene dos promedios y el conteo de válidas.",
        "En la ficha 02, la suma de asientos revisados de las dos hojas da "
        "cuarenta y el RSD del cierre coincide con el recálculo.",
        "En la conciliación, la diferencia de cada fila es entregado menos "
        "programado y la columna Conf. coincide con la diferencia cero.",
        "En el cuestionario, las sumas AP, UP y TAM cuadran con los reactivos "
        "marcados y el nivel corresponde al baremo.",
        "Cada hoja lleva la firma de quien la llenó; ninguna tiene espacios en "
        "blanco sin explicación en observaciones.",
    ], 1):
        _vineta(doc, f"{n}.", texto)

    _interlinea1(doc, "8. Decisiones que quedan en manos del tesista")

    _parrafo(doc,
             "Estas cuatro decisiones no las resuelve la maqueta y conviene "
             "tomarlas antes de la primera sesión, porque cambian lo que se "
             "imprime o lo que se declara en el informe. Primera: si la "
             "autorización institucional se gestiona por centro o de forma "
             "global para la red. Segunda: quién firma como auditor en cada "
             "centro, ya que la ficha pide una firma que acredite la medición. "
             "Tercera: si las réplicas inválidas se repiten el mismo día o se "
             "trasladan a una segunda visita, lo que afecta la fecha que se "
             "declara en el padrón. Cuarta: si el Módulo B se aplicará en esta "
             "campaña, porque su imprimible vive en el paquete de campo y no en "
             "el anexo.")

    _interlinea1(doc, "9. Qué se archiva al cerrar la campaña")

    _parrafo(doc,
             "Al término de las veintiocho sesiones el expediente de campo "
             "tiene tres cuerpos y conviene guardarlos por separado, porque "
             "tienen destinos distintos: el papel firmado es la evidencia "
             "primaria y no se presta; el libro de captura es el respaldo "
             "digitado y se copia junto con el consolidado; la guía y los "
             "editables son material de trabajo y no se anexan a la tesis.")

    _cuadro(doc, [
        ["Cuerpo", "Contenido", "Dónde"],
        ["Evidencia primaria", "168 hojas firmadas (6 por sesión) más las "
                               "réplicas de reemplazo y las cartas de "
                               "autorización",
         "Archivador físico, por operador y momento"],
        ["Respaldo digitado", "LIBRO_DE_CAPTURA_v22.xlsx y los dos CSV "
                              "consolidados",
         "07_CAPTURA y datos/recolectados/"],
        ["Material de trabajo", "Guía de llenado y los cuatro editables DOCX",
         "05_GUIA y 02_EDITABLES"],
    ], [3.6, 7.6, 4.3], [0.44, 0.70, 0.58, 0.52], size=8.2, izq=(0, 1, 2))

    _parrafo(doc,
             "Con esas decisiones tomadas y las hojas impresas, la campaña "
             "puede comenzar: el paquete v22 admite el registro completo, la "
             "aritmética de las tres fichas cierra en cada hoja y el "
             "consolidado se regenera desde el libro de captura sin intervenir "
             "los valores.")


def documento():
    doc = base.nueva_pagina()
    pagina_estado(doc)
    pagina_tiempos(doc)
    pagina_documental(doc)
    pagina_cuestionario(doc)
    pagina_cierre(doc)
    return doc


DOCUMENTOS = {NOMBRE: ("Guía de llenado y plan de impresión", documento)}


def compilar(con_pdf: bool = True) -> Dict[str, Any]:
    DIR_GUIA.mkdir(parents=True, exist_ok=True)
    for viejo in DIR_GUIA.glob("*.png"):
        viejo.unlink()

    manifiesto: Dict[str, Any] = {
        "version": VERSION,
        "documento": "05_GUIA/" + NOMBRE + "_" + VERSION,
        "caracter": "Documento operativo de campo. No es anexo de la tesis.",
        "documentos": {},
    }
    for nombre, (descripcion, constructor) in DOCUMENTOS.items():
        docx = DIR_GUIA / f"{nombre}_{VERSION}.docx"
        constructor().save(docx)
        base.fijar_marcas_zip(docx)
        entrada: Dict[str, Any] = {
            "descripcion": descripcion,
            "docx": str(docx.relative_to(RAIZ)),
            "sha256_docx": base.sha256(docx),
        }
        if con_pdf:
            pdf = DIR_GUIA / f"{nombre}_{VERSION}.pdf"
            base.exportar_pdf(docx, pdf)
            import fitz
            documento_pdf = fitz.open(pdf)
            entrada.update({"pdf": str(pdf.relative_to(RAIZ)),
                            "paginas": documento_pdf.page_count,
                            "sha256_pdf": base.sha256(pdf)})
            base.control_visual(pdf, DIR_GUIA)
            documento_pdf.close()
        manifiesto["documentos"][nombre] = entrada
        print(f"{nombre}: {entrada.get('paginas', '-')} p.")

    (DIR_GUIA / f"MANIFIESTO_{NOMBRE}_{VERSION}.json").write_text(
        json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifiesto


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sin-pdf", action="store_true")
    args = parser.parse_args()
    compilar(con_pdf=not args.sin_pdf)


if __name__ == "__main__":
    main()
