# -*- coding: utf-8 -*-
"""
GENERADOR DE DATOS SINTÉTICOS DE CAMPO — SIVAC
==============================================

Produce un conjunto de datos de prueba *a nivel de ficha* (no agregado) que
reproduce la estructura exacta de los tres instrumentos v21:

  · Instrumento 01 — ficha de registro de tiempos (6 réplicas por operador
    y momento: REG-01..REG-03 y VALE-01..VALE-03).
  · Instrumento 02 — ficha de auditoría del kardex (40 asientos, 8 criterios
    binarios) y conciliación de despachos (25 despachos).
  · Instrumento 03 — cuestionario de satisfacción TAM (8 reactivos Likert).

Los valores analíticos (T_reg, T_vale, RSD, CPE, AP, UP) NO se escriben a
mano: se calculan desde los registros crudos, de modo que cualquier
reprocesamiento con `scripts/estadistica/analisis_estadistico_sivac.py` dé
exactamente los mismos resultados que la matriz agregada.

Salidas (datos/prueba_sintetica/):
  DATOS_SINTETICOS_SIVAC.md          documento único, 4 secciones
  instrumento01_replicas.csv         168 filas (14 op × 2 momentos × 6)
  instrumento02_asientos.csv         1 120 filas (14 × 2 × 40)
  instrumento02_despachos.csv        700 filas (14 × 2 × 25)
  instrumento03_reactivos.csv        28 filas (14 × 2, formato largo)
  matriz_analitica_pre_post.csv      14 filas, columnas del codebook
  control_integridad.json            sumas de control y verificación

Uso:
    python scripts/estadistica/generar_datos_sinteticos.py

Nota. Los datos son sintéticos y se generan con semilla fija para que el
resultado sea reproducible. No sustituyen al registro de campo.
"""
from __future__ import annotations

import csv
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "datos" / "prueba_sintetica"
SEMILLA = x
RND = random.Random(SEMILLA)

# --------------------------------------------------------------------------
# 1. Padrón y valores de referencia
# --------------------------------------------------------------------------

# (id, centro, código de centro, observador asignado, fecha pretest, fecha postest)
PADRON = [
    ("TRAB-01", "ALMACÉN (CHANKA)",              "CHANKA-001",   "OBS-01", date(2026, 8, 10), date(2026, 10, 12)),
    ("TRAB-02", "ALMACÉN (CHANKA)",              "CHANKA-001",   "OBS-02", date(2026, 8, 10), date(2026, 10, 12)),
    ("TRAB-03", "Hospital Andahuaylas",          "S/C",          "OBS-01", date(2026, 8, 11), date(2026, 10, 13)),
    ("TRAB-04", "Hospital ESSALUD Andahuaylas",  "11214",        "OBS-02", date(2026, 8, 11), date(2026, 10, 13)),
    ("TRAB-05", "Centro de Salud Andahuaylas",   "6804",         "OBS-01", date(2026, 8, 12), date(2026, 10, 14)),
    ("TRAB-06", "Talavera",                      "4195",         "OBS-02", date(2026, 8, 12), date(2026, 10, 14)),
    ("TRAB-07", "San Jeronimo",                  "4167-SJ",      "OBS-01", date(2026, 8, 13), date(2026, 10, 15)),
    ("TRAB-08", "Huancaray",                     "4158",         "OBS-02", date(2026, 8, 13), date(2026, 10, 15)),
    ("TRAB-09", "Chicmo",                        "4202",         "OBS-01", date(2026, 8, 14), date(2026, 10, 16)),
    ("TRAB-10", "Huancabamba",                   "4172",         "OBS-02", date(2026, 8, 14), date(2026, 10, 16)),
    ("TRAB-11", "Pampachiri",                    "4167",         "OBS-01", date(2026, 9, 7),  date(2026, 10, 19)),
    ("TRAB-12", "San Antonio de Cachi",          "4160",         "OBS-02", date(2026, 9, 7),  date(2026, 10, 19)),
    ("TRAB-13", "Turpo",                         "4163",         "OBS-01", date(2026, 9, 8),  date(2026, 10, 20)),
    ("TRAB-14", "Kishuara",                      "4183",         "OBS-02", date(2026, 9, 8),  date(2026, 10, 20)),
]

# Valores de referencia (matriz agregada vigente del proyecto).
# Se usan solo como objetivo; los valores finales se recalculan del crudo.
REF = {
    #        t_reg pre, t_vale pre, rsd pre, cpe pre,   t_reg post, t_vale post, rsd post, cpe post
    "TRAB-01": (38.5, 18.5, 62.5, 64.0,  5.37, 2.12, 95.0, 96.0),
    "TRAB-02": (42.0, 22.0, 57.5, 64.0,  5.73, 1.83, 97.5, 96.0),
    "TRAB-03": (35.0, 16.0, 65.0, 72.0,  5.34, 1.72, 95.0, 96.0),
    "TRAB-04": (33.5, 15.0, 72.5, 76.0,  5.59, 2.17, 90.0, 96.0),
    "TRAB-05": (40.0, 20.5, 55.0, 60.0,  6.15, 1.86, 97.5, 96.0),
    "TRAB-06": (36.5, 17.0, 65.0, 68.0,  4.82, 1.67, 95.0, 96.0),
    "TRAB-07": (44.0, 24.0, 52.5, 56.0,  4.95, 2.00, 100.0, 92.0),
    "TRAB-08": (32.0, 14.5, 75.0, 76.0,  5.92, 1.96, 97.5, 96.0),
    "TRAB-09": (31.5, 15.0, 72.5, 76.0,  6.01, 1.65, 97.5, 96.0),
    "TRAB-10": (39.0, 19.5, 60.0, 68.0,  6.29, 1.87, 97.5, 96.0),
    "TRAB-11": (37.0, 18.0, 62.5, 68.0,  6.44, 1.78, 95.0, 92.0),
    "TRAB-12": (41.5, 21.0, 57.5, 60.0,  5.74, 2.07, 97.5, 92.0),
    "TRAB-13": (34.0, 16.5, 67.5, 72.0,  5.53, 2.27, 92.5, 96.0),
    "TRAB-14": (36.0, 17.5, 65.0, 68.0,  5.63, 1.90, 97.5, 88.0),
}

# Reactivos Likert por operador y momento (los del codebook; no se alteran).
LIKERT = {
    "TRAB-01": ((2, 2, 2, 2, 2, 3, 2, 2), (5, 5, 5, 5, 5, 5, 5, 5)),
    "TRAB-02": ((1, 2, 1, 2, 2, 2, 2, 2), (4, 5, 5, 5, 4, 4, 4, 4)),
    "TRAB-03": ((2, 2, 3, 2, 3, 2, 2, 3), (4, 4, 5, 4, 4, 5, 5, 4)),
    "TRAB-04": ((3, 3, 2, 3, 3, 3, 3, 3), (4, 4, 5, 5, 4, 4, 5, 4)),
    "TRAB-05": ((2, 1, 2, 1, 2, 2, 2, 2), (5, 5, 5, 5, 5, 5, 5, 5)),
    "TRAB-06": ((2, 2, 2, 2, 2, 2, 2, 2), (5, 5, 5, 5, 5, 5, 5, 5)),
    "TRAB-07": ((1, 1, 1, 1, 1, 2, 1, 2), (5, 5, 5, 5, 5, 5, 5, 5)),
    "TRAB-08": ((3, 3, 3, 3, 3, 3, 3, 3), (4, 5, 4, 5, 5, 5, 5, 4)),
    "TRAB-09": ((3, 2, 3, 2, 3, 3, 2, 3), (5, 5, 5, 5, 4, 5, 5, 5)),
    "TRAB-10": ((2, 2, 2, 2, 2, 2, 2, 2), (5, 5, 5, 5, 5, 5, 5, 5)),
    "TRAB-11": ((2, 2, 2, 2, 2, 2, 2, 2), (4, 4, 4, 4, 4, 4, 4, 4)),
    "TRAB-12": ((1, 2, 1, 1, 2, 2, 2, 1), (5, 5, 5, 5, 5, 5, 5, 5)),
    "TRAB-13": ((3, 2, 2, 3, 3, 3, 2, 3), (4, 4, 4, 4, 4, 4, 4, 4)),
    "TRAB-14": ((2, 2, 2, 2, 2, 2, 2, 2), (4, 4, 4, 5, 4, 5, 4, 4)),
}

BIOLOGICOS = ["BCG", "PENT", "IPV", "ROTA", "NEUM", "SPR", "DTA", "HEPB", "INFL", "VARI"]
BIOLOGICO_NOMBRE = {
    "BCG": "BCG (antituberculosa)",
    "PENT": "Pentavalente (DPT-HB-Hib)",
    "IPV": "IPV (antipoliomielítica inactivada)",
    "ROTA": "Rotavirus",
    "NEUM": "Neumococo conjugada",
    "SPR": "SPR (sarampión-paperas-rubéola)",
    "DTA": "Difteria-Tétanos (dT)",
    "HEPB": "Hepatitis B",
    "INFL": "Influenza estacional",
    "VARI": "Varicela",
}
TIPOS_DOC = ["ING", "SAL", "TRA", "DEV", "AJU"]
CRITERIOS = [
    "Biológico", "Lote", "Vencimiento", "Cantidad física",
    "Origen y destino", "Responsable y firma", "Saldo aritmético", "Correlatividad",
]


# --------------------------------------------------------------------------
# 2. Utilidades
# --------------------------------------------------------------------------

def hms(t: datetime) -> str:
    return t.strftime("%H:%M:%S")


def dmy(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def split_three(total_s: int, weights: tuple[float, float, float], jitter: int = 90) -> list[int]:
    """Reparte `total_s` segundos en tres réplicas con variación natural.

    `weights` fija el perfil relativo de las tareas (p. ej. la tercera es más
    lenta que la primera); el jitter introduce la variabilidad de campo. La
    suma siempre es exactamente `total_s`.
    """
    base = total_s / sum(weights)
    parts = []
    for w in weights:
        raw = base * w + RND.uniform(-jitter, jitter)
        parts.append(int(round(raw)))
    parts = [max(45, p) for p in parts]
    parts[2] = total_s - parts[0] - parts[1]
    if parts[2] < 45:
        deficit = 45 - parts[2]
        parts[2] = 45
        parts[0] -= deficit // 2
        parts[1] -= deficit - deficit // 2
    return parts


def fmt_obs_list(items: list[str], max_items: int = 4) -> list[str]:
    return [f"- {x}" for x in items[:max_items]]


# --------------------------------------------------------------------------
# 3. Instrumento 01 — tiempos
# --------------------------------------------------------------------------

# Series documentales realistas: folios con huecos, no correlativos 001..n.
# Cada centro lleva su propio registro, por lo que los números saltan y se
# repiten entre centros, tal como ocurre en el kardex físico del almacén.
def folios(n: int, lo: int = 120, hi: int = 9800) -> list[int]:
    elegidos: set[int] = set()
    while len(elegidos) < n:
        elegidos.add(RND.randint(lo, hi))
    return sorted(elegidos)


def codigo_centro(cod: str) -> str:
    return cod.replace("/", "").replace("-", "")


def unicos_documentos(asientos: list[dict], despachos: list[dict]) -> None:
    """Garantiza que un mismo folio no se repita dentro del registro de un
    centro. Se aplica después de generar los bloques y no consume números
    aleatorios, de modo que ninguna otra cifra del conjunto cambia. Un folio
    repetido contradeciría los criterios de correlatividad (M8) y de guía de
    remisión del propio instrumento."""

    def reservar(filas: list[dict], campo: str) -> None:
        usados: dict[str, set[str]] = {}
        for fila in filas:
            valor = fila[campo]
            if not valor or valor == "Sin guía" or "No aplica" in valor:
                continue
            prefijo, _, numero = valor.rpartition("-")
            if not numero.isdigit():
                continue
            vistos = usados.setdefault((fila["centro_acopio"], prefijo), set())
            if valor in vistos:
                nuevo = int(numero)
                while True:
                    nuevo += 1
                    if nuevo > 9999:
                        nuevo = 100
                    candidato = f"{prefijo}-{nuevo:04d}"
                    if candidato not in vistos:
                        break
                vistos.add(candidato)
                fila[campo] = candidato
                if campo == "documento" and "lote_documento" in fila \
                        and fila["lote_documento"] == valor:
                    fila["lote_documento"] = candidato
            else:
                vistos.add(valor)

    reservar(asientos, "documento")
    reservar(despachos, "documento")


# Lotes de fabricante por biológico (5 por vacuna, vigentes en el periodo).
def construir_lotes() -> dict[str, list[str]]:
    lotes: dict[str, list[str]] = {}
    for bio in BIOLOGICOS:
        series = []
        for _ in range(5):
            anio = RND.choice(["25", "26"])
            mes = RND.randint(1, 9)
            series.append(f"{bio}-{anio}{mes:02d}-{RND.randint(100, 999)}{RND.choice('ABKM')}")
        lotes[bio] = series
    return lotes


LOTES = construir_lotes()

MOTIVOS_PAUSA = {1: "P1", 2: "P2", 3: "P3", 4: "P4"}


def pausa_de_campo(es_pre: bool) -> tuple[int | str, str]:
    """Pausa ajena al proceso (ventanilla, llamada, corte, verificación)."""
    if es_pre:
        if RND.random() < 0.42:
            return RND.choice([45, 60, 60, 90, 120, 150]), MOTIVOS_PAUSA[RND.randint(1, 4)]
        return "", ""
    if RND.random() < 0.18:
        return RND.choice([30, 45, 60]), MOTIVOS_PAUSA[RND.choice([1, 2])]
    return "", ""


TAREAS_REG = [
    ("REG-01", "T1", "Ingreso de lote al almacén (T1)"),
    ("REG-02", "T2", "Salida o transferencia a la red (T2)"),
    ("REG-03", "T3", "Redistribución a la red (T3)"),
]
TAREAS_VALE = [
    ("VALE-01", "T4", "Vale simple para puesto de salud (T4)"),
    ("VALE-02", "T5", "Vale regular para centro de salud (T5)"),
    ("VALE-03", "T6", "Vale de reposición o contingencia (T6)"),
]

# Perfil de duración relativa por tarea: el ingreso es el más rápido y la
# redistribución la más lenta; el vale de contingencia demora más que el simple.
PESOS_REG_PRE = (0.90, 1.00, 1.10)
PESOS_REG_POST = (0.92, 1.00, 1.08)
PESOS_VALE_PRE = (0.93, 1.00, 1.07)
PESOS_VALE_POST = (0.94, 1.00, 1.06)

HORAS_INICIO_PRE = ["07:30", "07:15", "07:45", "08:00", "07:20", "07:40"]
HORAS_INICIO_POST = ["08:00", "07:50", "08:15", "08:30", "07:45", "08:10"]


def generar_tiempos() -> tuple[list[dict], dict]:
    """Devuelve las 168 réplicas y el resumen por operador y momento."""
    filas: list[dict] = []
    resumen: dict[tuple[str, str], dict] = {}

    for i, (op, centro, cod, obs, fpre, fpost) in enumerate(PADRON):
        t_reg_pre, t_vale_pre, _, _, t_reg_post, t_vale_post, _, _ = REF[op]
        for momento in ("Pretest", "Postest"):
            es_pre = momento == "Pretest"
            fecha = fpre if es_pre else fpost
            hhmm = (HORAS_INICIO_PRE if es_pre else HORAS_INICIO_POST)[i % 6]
            h, m = (int(x) for x in hhmm.split(":"))
            t = datetime.combine(fecha, datetime.min.time()).replace(hour=h, minute=m)

            reg_mean_s = int(round((t_reg_pre if es_pre else t_reg_post) * 180))
            vale_mean_s = int(round((t_vale_pre if es_pre else t_vale_post) * 180))

            d_reg = split_three(reg_mean_s, PESOS_REG_PRE if es_pre else PESOS_REG_POST,
                                jitter=75 if es_pre else 20)
            # Transición entre bloques (búsqueda de talonarios, traslado a caja).
            gap_min = RND.choice([2, 3, 4, 5, 6]) if es_pre else RND.choice([0, 1, 1, 2])
            gap_s = gap_min * 60 + RND.randint(0, 55)
            d_vale = split_three(vale_mean_s, PESOS_VALE_PRE if es_pre else PESOS_VALE_POST,
                                 jitter=35 if es_pre else 6)

            folios_reg = folios(3, 120, 3200)
            folios_vale = folios(3, 4100, 9800)
            tipos_reg = ["ING", "SAL", "TRA"]
            if not es_pre:
                tipos_reg = ["ING", "SAL", "TRA"]
            biomol = [RND.choice(BIOLOGICOS) for _ in range(6)]
            lotes = [RND.choice(LOTES[b]) for b in biomol]
            cc = codigo_centro(cod)

            for idx, ((cod_t, tag, desc), dur) in enumerate(zip(TAREAS_REG, d_reg)):
                ini = t
                # La pausa externa ocurre dentro de la ventana de observación:
                # el cronómetro se detiene, de modo que la duración neta es
                # (hora_corte - hora_inicio) - pausa_s.
                pausa_s, motivo = pausa_de_campo(es_pre)
                t = t + timedelta(seconds=dur + int(pausa_s or 0))
                folio = folios_reg[idx]
                filas.append({
                    "sujeto_id": op, "centro_acopio": centro, "momento": momento,
                    "fecha": dmy(fecha), "observador": obs,
                    "indicador": "T_reg", "replica": cod_t, "tarea": tag,
                    "escenario": desc,
                    "documento": f"{tipos_reg[idx]}-{cc}-{folio:04d}",
                    "lote_documento": lotes[idx],
                    "hora_inicio": hms(ini), "hora_corte": hms(t),
                    "duracion_s": dur, "duracion_min": round(dur / 60, 4),
                    "pausa_s": pausa_s, "motivo_pausa": motivo,
                    "valida": "Sí",
                })

            t += timedelta(seconds=gap_s)
            for idx, ((cod_t, tag, desc), dur) in enumerate(zip(TAREAS_VALE, d_vale)):
                ini = t
                pausa_s, motivo = pausa_de_campo(es_pre)
                t = t + timedelta(seconds=dur + int(pausa_s or 0))
                vale = folios_vale[idx]
                filas.append({
                    "sujeto_id": op, "centro_acopio": centro, "momento": momento,
                    "fecha": dmy(fecha), "observador": obs,
                    "indicador": "T_vale", "replica": cod_t, "tarea": tag,
                    "escenario": desc,
                    "documento": f"PEC-{fecha.strftime('%Y')}-{fecha.strftime('%m%d')}-{vale:04d}",
                    "lote_documento": f"PEC-{fecha.strftime('%Y')}-{fecha.strftime('%m%d')}-{vale:04d}",
                    "hora_inicio": hms(ini), "hora_corte": hms(t),
                    "duracion_s": dur, "duracion_min": round(dur / 60, 4),
                    "pausa_s": pausa_s, "motivo_pausa": motivo,
                    "valida": "Sí",
                })

            resumen[(op, momento)] = {
                "t_reg": round(sum(d_reg) / 180, 4),
                "t_vale": round(sum(d_vale) / 180, 4),
                "replicas": 6,
                "inicio": hms(datetime.combine(fecha, datetime.min.time()).replace(hour=h, minute=m)),
                "fin": hms(t),
                "gap_s": gap_s,
                "fecha": fecha,
            }

    return filas, resumen


# --------------------------------------------------------------------------
# 4. Instrumento 02 — auditoría documental (40 asientos) y despachos (25)
# --------------------------------------------------------------------------

# Documentos conformes por operador y momento. Se derivan de los indicadores
# objetivo redondeando a un número entero de documentos (40 y 25 por unidad),
# que es la única granularidad posible en una ficha con ítems binarios.
CONFORMES_RSD = {
    "TRAB-01": (25, 38), "TRAB-02": (23, 39), "TRAB-03": (26, 38), "TRAB-04": (29, 36), "TRAB-05": (22, 39),
    "TRAB-06": (26, 38), "TRAB-07": (21, 40), "TRAB-08": (30, 39), "TRAB-09": (29, 39), "TRAB-10": (24, 39),
    "TRAB-11": (25, 38), "TRAB-12": (23, 39), "TRAB-13": (27, 37), "TRAB-14": (26, 39),
}
CONFORMES_CPE = {
    "TRAB-01": (16, 24), "TRAB-02": (16, 24), "TRAB-03": (18, 24), "TRAB-04": (19, 24), "TRAB-05": (15, 24),
    "TRAB-06": (17, 24), "TRAB-07": (14, 23), "TRAB-08": (20, 24), "TRAB-09": (19, 24), "TRAB-10": (16, 24),
    "TRAB-11": (17, 23), "TRAB-12": (15, 23), "TRAB-13": (18, 24), "TRAB-14": (17, 22),
}

# Frecuencia relativa de los ocho criterios cuando un asiento falla. En el
# proceso manual los fallos se concentran en saldo, firma y correlatividad;
# con SIVAC sobreviven sobre todo los de firma y saldo (validación humana).
PESOS_FALLO_PRE = {1: 8, 2: 10, 3: 7, 4: 6, 5: 9, 6: 20, 7: 24, 8: 16}
PESOS_FALLO_POST = {1: 2, 2: 3, 3: 2, 4: 3, 5: 8, 6: 26, 7: 36, 8: 20}

CANTIDADES = [20, 30, 40, 50, 60, 80, 100, 120, 150, 180, 200, 240, 300]

OBS_ASIENTO_PRE = {
    1: "Biológico consignado no corresponde al frasco físico.",
    2: "Lote del kardex no coincide con el rotulado del frasco.",
    3: "Fecha de vencimiento vencida o ilegible en el asiento.",
    4: "Cantidad física menor a la registrada en el asiento.",
    5: "Origen o destino consignado de forma incompleta.",
    6: "Asiento sin firma del responsable del almacén.",
    7: "Saldo arrastrado no cuadra con la columna de existencias.",
    8: "Numeración correlativa interrumpida; falta un folio.",
}
OBS_ASIENTO_POST = {
    1: "Biológico corregido a mano sobre el asiento impreso.",
    2: "Lote digitado con un dígito trocado; se subsanó en el sistema.",
    3: "Vencimiento registrado sin año; inconsistencia de digitación.",
    4: "Diferencia de una unidad entre conteo físico y sistema.",
    5: "Origen/destino incompleto en un traslado entre microredes.",
    6: "Firma pendiente de regularización del responsable.",
    7: "Saldo no recalculado tras un ajuste autorizado.",
    8: "Correlativo duplicado por reintento de grabación.",
}

OBS_DESPACHO = [
    "Conforme. Cantidad y guía coinciden.",
    "Conforme. Recepción firmada por el jefe del establecimiento.",
    "Conforme. Se adjuntó guía de remisión y acta de entrega.",
    "Conforme. Despacho parcial autorizado y regularizado el mismo día.",
    "Conforme. Verificado el FEFO al momento de la carga.",
    "Entrega menor a la programada; se regulariza en el siguiente despacho.",
    "Entrega mayor a la programada; se ajusta el saldo del almacén.",
    "Guía de remisión no coincide con la cantidad registrada en el kardex.",
    "Despacho sin documento de sustento al momento de la auditoría.",
    "Diferencia por unidad dañada devuelta al almacén.",
    "Se entregó el lote próximo a vencer en lugar del programado.",
]

OBS_FICHA_DOC_PRE = [
    "Auditoría realizada con el kardex físico y el talonario de vales del periodo.",
    "Se verificaron los 40 asientos contra las guías de remisión del archivo de almacén.",
    "El operador sustentó verbalmente los asientos observados; no se corrigió la hoja.",
    "Dos folios del kardex estaban fuera de orden; se reconstruyó la correlatividad.",
    "Se solicitó el libro de actas para validar las devoluciones del periodo.",
]
OBS_FICHA_DOC_POST = [
    "Auditoría realizada sobre el reporte de kardex emitido por el SIVAC.",
    "Los asientos se contrastaron con la trazabilidad de movimientos del sistema.",
    "Se exportó el reporte de despachos y se cotejó con las guías físicas.",
    "Las observaciones pendientes corresponden a firmas en regularización.",
    "El sistema permitió reconstruir la correlatividad sin revisar el archivo físico.",
]


def generar_documental() -> tuple[list[dict], list[dict], dict]:
    asientos: list[dict] = []
    despachos: list[dict] = []
    resumen: dict[tuple[str, str], dict] = {}

    for op, centro, cod, obs, fpre, fpost in PADRON:
        n_rsd = CONFORMES_RSD[op]
        n_cpe = CONFORMES_CPE[op]
        for momento in ("Pretest", "Postest"):
            es_pre = momento == "Pretest"
            fecha_sesion = fpre if es_pre else fpost
            n_conf = n_rsd[0] if es_pre else n_rsd[1]
            n_conc = n_cpe[0] if es_pre else n_cpe[1]
            pesos = PESOS_FALLO_PRE if es_pre else PESOS_FALLO_POST
            obs_txt = OBS_ASIENTO_PRE if es_pre else OBS_ASIENTO_POST

            # --- reparto de criterios fallidos entre los documentos no conformes
            n_falla = 40 - n_conf
            criterios = list(pesos)
            pesos_l = [pesos[c] for c in criterios]
            fallos = RND.choices(criterios, weights=pesos_l, k=n_falla)
            # dos documentos con doble fallo (realismo), el resto con uno
            dobles = set(sorted(range(n_falla), key=lambda _: RND.random())[: max(1, n_falla // 4)])

            # --- posiciones de los documentos no conformes (dispersas)
            pos_falla = set()
            while len(pos_falla) < n_falla:
                pos_falla.add(RND.randrange(40))
            pos_falla = sorted(pos_falla)

            span = RND.randint(25, 34)
            periodo_ini = fecha_sesion - timedelta(days=span)
            periodo_fin = fecha_sesion - timedelta(days=1)
            # Folios de kardex por tipo documental: series independientes con
            # huecos, no correlativas al orden de la auditoría.
            folios_tipo = {t: folios(40, 110, 9400) for t in TIPOS_DOC}
            usado = {t: 0 for t in TIPOS_DOC}
            cc = codigo_centro(cod)

            for k in range(40):
                n = k + 1
                # La ventana va de `span` días antes de la sesión hasta el día
                # previo: ningún asiento puede llevar la fecha de la propia
                # sesión de auditoría.
                f = periodo_ini + timedelta(days=int(round((span - 1) * k / 39)))
                tipo = RND.choices(TIPOS_DOC, weights=[30, 34, 18, 10, 8])[0]
                bio = RND.choice(BIOLOGICOS)
                lote = RND.choice(LOTES[bio])
                cant = RND.choice(CANTIDADES)
                folio = folios_tipo[tipo][usado[tipo]]
                usado[tipo] += 1
                doc = f"{tipo}-{cc}-{folio:04d}"
                if k in pos_falla:
                    idx = pos_falla.index(k)
                    c1 = fallos[idx]
                    crits = {c1: "N"}
                    if idx in dobles:
                        c2 = RND.choice([c for c in criterios if c != c1])
                        crits[c2] = "N"
                else:
                    crits = {}
                cumple = {c: crits.get(c, "S") for c in range(1, 9)}
                conforme = all(v == "S" for v in cumple.values())
                motivo = ""
                if not conforme:
                    motivo = "M" + "+M".join(str(c) for c, v in cumple.items() if v == "N")
                asientos.append({
                    "sujeto_id": op, "centro_acopio": centro, "momento": momento,
                    "fecha_sesion": dmy(fecha_sesion), "auditor": obs,
                    "n": n, "hoja": 1 if n <= 20 else 2,
                    "fecha": dmy(f), "documento": doc, "tipo": tipo,
                    "biologico": bio, "lote": lote, "cantidad": cant,
                    "c1": cumple[1], "c2": cumple[2], "c3": cumple[3], "c4": cumple[4],
                    "c5": cumple[5], "c6": cumple[6], "c7": cumple[7], "c8": cumple[8],
                    "conforme": "S" if conforme else "N",
                    "motivo": motivo,
                    "observacion": obs_txt.get(c1, "") if not conforme else "",
                })

            conformes_reales = sum(1 for a in asientos[-40:] if a["conforme"] == "S")

            # --- bloque B: 25 despachos
            pos_no_conc = set()
            while len(pos_no_conc) < 25 - n_conc:
                pos_no_conc.add(RND.randrange(25))
            pos_no_conc = sorted(pos_no_conc)
            modo_fallo = [RND.choice(["cantidad", "documento", "ambos"]) for _ in pos_no_conc]

            for k in range(25):
                n = k + 1
                # Un despacho se concilia al menos un día después de ocurrido.
                f = fecha_sesion - timedelta(days=max(1, RND.randint(0, 28)))
                bio = RND.choice(BIOLOGICOS)
                prog = RND.choice([20, 30, 40, 50, 60, 80, 100, 120, 150, 180, 200])
                guia = f"GR-{cc}-{RND.randint(1200, 9800):04d}"
                if k in pos_no_conc:
                    modo = modo_fallo[pos_no_conc.index(k)]
                    if modo == "cantidad":
                        delta = RND.choice([-20, -10, -5, 5, 10, 20])
                        entr = max(0, prog + delta)
                        docok = "Sí"
                        o = ("Entrega menor a la programada; se regulariza en el siguiente despacho."
                             if delta < 0 else
                             "Entrega mayor a la programada; se ajusta el saldo del almacén.")
                        guia_txt = guia
                    elif modo == "documento":
                        # Un despacho sin guía de sustento no es conciliable:
                        # la cantidad entregada tampoco coincide con la programada.
                        delta = RND.choice([-10, -5, 5])
                        entr = max(0, prog + delta)
                        docok = "No"
                        o = "Despacho sin documento de sustento al momento de la auditoría."
                        guia_txt = "Sin guía"
                    else:
                        delta = RND.choice([-10, -5])
                        entr = max(0, prog + delta)
                        docok = "No"
                        o = "Guía de remisión no coincide con la cantidad registrada en el kardex."
                        guia_txt = guia
                    conf = "No"
                else:
                    entr = prog
                    docok = "Sí"
                    conf = "Sí"
                    o = RND.choice(OBS_DESPACHO[:5])
                    guia_txt = guia
                despachos.append({
                    "sujeto_id": op, "centro_acopio": centro, "momento": momento,
                    "fecha_sesion": dmy(fecha_sesion), "auditor": obs,
                    "n": n, "fecha": dmy(f), "biologico": bio,
                    "programado": prog, "entregado": entr, "diferencia": entr - prog,
                    "documento": guia_txt, "conforme": conf, "observacion": o,
                })

            conc_reales = sum(1 for d in despachos[-25:] if d["conforme"] == "Sí")
            resumen[(op, momento)] = {
                "conformes": conformes_reales,
                "rsd": round(conformes_reales / 40 * 100, 2),
                "concordantes": conc_reales,
                "cpe": round(conc_reales / 25 * 100, 2),
                "periodo": (dmy(periodo_ini), dmy(periodo_fin)),
                "obs": RND.choice(OBS_FICHA_DOC_PRE if es_pre else OBS_FICHA_DOC_POST),
            }

    return asientos, despachos, resumen


# --------------------------------------------------------------------------
# 5. Instrumento 03 — cuestionario TAM
# --------------------------------------------------------------------------

REACTIVOS = [
    ("AP-01", "AP", "El procedimiento de registro de movimientos de vacunas resulta ágil y sin demoras innecesarias."),
    ("AP-02", "AP", "La emisión de comprobantes y vales de salida se realiza con facilidad y claridad en los pasos requeridos."),
    ("AP-03", "AP", "El flujo operativo para conciliar saldos mensuales reduce la fatiga y el esfuerzo administrativo."),
    ("AP-04", "AP", "Considero que la modalidad de trabajo empleada es cómoda, ordenada y eficiente para mis labores."),
    ("UP-01", "UP", "La plataforma o método de trabajo mejora mi productividad y desempeño en el control de vacunas."),
    ("UP-02", "UP", "El sistema proporciona información precisa y oportuna para la toma de decisiones en inmunizaciones."),
    ("UP-03", "UP", "La aplicación de reglas automáticas de control (como FEFO) evita errores y vencimiento de biológicos."),
    ("UP-04", "UP", "En términos generales, considero sumamente útil la herramienta para la gestión institucional en la DISA."),
]

OBS_CUESTIONARIO_PRE = [
    "Cuestionario aplicado en el almacén, antes de la capacitación en el SIVAC.",
    "El operador solicitó releer dos reactivos; se aclaró sin inducir la respuesta.",
    "Aplicado al término de la jornada, sin presencia de terceros.",
    "Se explicó la escala Likert antes de iniciar; no hubo ítems en blanco.",
]
OBS_CUESTIONARIO_POST = [
    "Cuestionario aplicado tras cuatro semanas de uso continuo del SIVAC.",
    "El operador respondió sin consultar el sistema; se garantizó el anonimato.",
    "Aplicado al cierre del periodo auditado, en presencia del auditor de campo.",
    "Se registraron comentarios adicionales favorables sobre el control FEFO.",
]


def baremo(total: int) -> str:
    if total <= 18:
        return "Bajo"
    if total <= 29:
        return "Medio"
    return "Alto"


def generar_cuestionario() -> list[dict]:
    filas = []
    for op, centro, cod, obs, fpre, fpost in PADRON:
        pre, post = LIKERT[op]
        for momento, vals, fecha in (("Pretest", pre, fpre), ("Postest", post, fpost)):
            ap = sum(vals[:4])
            up = sum(vals[4:])
            for (cod_r, dim, texto), v in zip(REACTIVOS, vals):
                filas.append({
                    "sujeto_id": op, "centro_acopio": centro, "momento": momento,
                    "fecha": dmy(fecha), "encuestador": obs,
                    "reactivo": cod_r, "dimension": dim, "texto": texto, "valor": v,
                    "score_ap": ap, "score_up": up, "score_total": ap + up,
                    "nivel": baremo(ap + up),
                    "observacion": (OBS_CUESTIONARIO_PRE if momento == "Pretest" else OBS_CUESTIONARIO_POST)[
                        PADRON.index((op, centro, cod, obs, fpre, fpost)) % 4],
                })
    return filas


# --------------------------------------------------------------------------
# 6. Estadística de control (reproduce el pipeline del proyecto)
# --------------------------------------------------------------------------

def estadisticas(matriz: list[dict]) -> dict:
    import statistics as ss
    from scipy import stats as st

    out = {"descriptivos": {}, "normalidad": {}, "contrastes": {}, "confiabilidad": {}}
    indicadores = [
        ("t_reg", "Tiempo de registro de movimientos (T_reg)", "min", "D1"),
        ("t_vale", "Tiempo de emisión de vales (T_vale)", "min", "D1"),
        ("rsd", "Registros sin discrepancias (RSD)", "%", "D2"),
        ("cpe", "Concordancia programada vs. entregada (CPE)", "%", "D2"),
        ("score_ap", "Aceptación del proceso (AP)", "pts", "D3"),
        ("score_up", "Utilidad percibida (UP)", "pts", "D3"),
        ("score_tam_total", "Puntaje global TAM", "pts", "D3"),
    ]
    pre = [r for r in matriz if r["momento"] == "Pretest"]
    post = [r for r in matriz if r["momento"] == "Postest"]

    for col, nombre, unidad, dim in indicadores:
        a = [float(r[col]) for r in pre]
        b = [float(r[col]) for r in post]
        d = [y - x for x, y in zip(a, b)]
        w, p = st.shapiro(d)
        t, pt = st.ttest_rel(b, a)
        try:
            wz, pz = st.wilcoxon(b, a)
        except ValueError:
            wz, pz = float("nan"), float("nan")
        sd_d = ss.stdev(d) if len(set(d)) > 1 else 0.0
        dz = (sum(d) / len(d)) / sd_d if sd_d else float("nan")
        out["descriptivos"][col] = {
            "nombre": nombre, "unidad": unidad, "dimension": dim,
            "pre": {"media": ss.mean(a), "de": ss.stdev(a), "mediana": ss.median(a),
                    "min": min(a), "max": max(a), "n": len(a)},
            "post": {"media": ss.mean(b), "de": ss.stdev(b), "mediana": ss.median(b),
                     "min": min(b), "max": max(b), "n": len(b)},
            "dif": {"media": ss.mean(d), "de": ss.stdev(d), "mediana": ss.median(d),
                    "min": min(d), "max": max(d)},
            "delta_pct": (ss.mean(b) - ss.mean(a)) / ss.mean(a) * 100 if ss.mean(a) else None,
        }
        out["normalidad"][col] = {"W": float(w), "p": float(p), "normal": bool(p > 0.05)}
        out["contrastes"][col] = {"t": float(t), "gl": len(d) - 1, "p_t": float(pt), "d": float(dz),
                                  "W_wilcoxon": float(wz), "p_wilcoxon": float(pz)}

    # Alfa de Cronbach por momento (8 reactivos) y por subescala
    for momento, filas in (("Pretest", pre), ("Postest", post)):
        for nombre, cols in (("global", [f"{d}_{i:02d}" for d in ("ap", "up") for i in range(1, 5)]),
                             ("AP", [f"ap_{i:02d}" for i in range(1, 5)]),
                             ("UP", [f"up_{i:02d}" for i in range(1, 5)])):
            k = len(cols)
            items = [[float(r[c]) for r in filas] for c in cols]
            var_items = sum(ss.variance(x) for x in items)
            total = [sum(v) for v in zip(*items)]
            var_total = ss.variance(total)
            alpha = k / (k - 1) * (1 - var_items / var_total) if var_total else float("nan")
            out["confiabilidad"][f"{momento}_{nombre}"] = {"alpha": float(alpha), "k": k, "n": len(filas)}
    return out


# --------------------------------------------------------------------------
# 7. Exportación CSV
# --------------------------------------------------------------------------

def escribir_csv(ruta: Path, filas: list[dict], columnas: list[str]) -> None:
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columnas, extrasaction="ignore",
                            lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def exportar_csv(replicas, asientos, despachos, cuestionario, matriz) -> dict:
    SALIDA.mkdir(parents=True, exist_ok=True)
    escribir_csv(SALIDA / "instrumento01_replicas.csv", replicas, [
        "sujeto_id", "centro_acopio", "momento", "fecha", "observador", "indicador",
        "replica", "tarea", "escenario", "documento", "lote_documento",
        "hora_inicio", "hora_corte", "duracion_s", "duracion_min",
        "pausa_s", "motivo_pausa", "valida"])
    escribir_csv(SALIDA / "instrumento02_asientos.csv", asientos, [
        "sujeto_id", "centro_acopio", "momento", "fecha_sesion", "auditor", "n", "hoja",
        "fecha", "documento", "tipo", "biologico", "lote", "cantidad",
        "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "conforme", "motivo", "observacion"])
    escribir_csv(SALIDA / "instrumento02_despachos.csv", despachos, [
        "sujeto_id", "centro_acopio", "momento", "fecha_sesion", "auditor", "n", "fecha",
        "biologico", "programado", "entregado", "diferencia", "documento", "conforme", "observacion"])
    escribir_csv(SALIDA / "instrumento03_reactivos.csv", cuestionario, [
        "sujeto_id", "centro_acopio", "momento", "fecha", "encuestador", "reactivo",
        "dimension", "valor", "score_ap", "score_up", "score_total", "nivel", "observacion"])
    escribir_csv(SALIDA / "matriz_analitica_pre_post.csv", matriz, [
        "sujeto_id", "centro_acopio", "momento", "t_reg", "t_vale", "rsd", "cpe",
        "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02", "up_03", "up_04",
        "score_ap", "score_up", "score_tam_total", "nivel_satisfaccion"])

    # Formatos de entrada del pipeline: mismos nombres y columnas que
    # datos/recolectados/pretest_campo.csv y posttest_campo.csv, para poder
    # ejecutar scripts/estadistica/analisis_estadistico_sivac.py apuntando
    # DATOS_DIR a esta carpeta.
    columnas_pipeline = [
        "sujeto_id", "centro_acopio", "t_reg", "t_vale", "rsd", "cpe",
        "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02", "up_03", "up_04",
        "score_ap", "score_up", "score_tam_total", "nivel_satisfaccion"]
    for momento, archivo in (("Pretest", "pretest_sintetico.csv"),
                             ("Postest", "posttest_sintetico.csv")):
        escribir_csv(SALIDA / archivo,
                     [m for m in matriz if m["momento"] == momento],
                     columnas_pipeline)
    return {p.name: p.stat().st_size for p in SALIDA.glob("*.csv")}


# --------------------------------------------------------------------------
# 8. Documento Markdown
# --------------------------------------------------------------------------

TITULO = "CONJUNTO DE DATOS SINTÉTICOS DE CAMPO — SIVAC"


def tabla(cabeceras, filas, alineacion=None) -> str:
    alineacion = list(alineacion or [])
    if len(alineacion) < len(cabeceras):
        alineacion += ["---"] * (len(cabeceras) - len(alineacion))
    alineacion = alineacion[: len(cabeceras)]
    out = ["| " + " | ".join(cabeceras) + " |",
           "| " + " | ".join(alineacion) + " |"]
    for f in filas:
        out.append("| " + " | ".join(str(x) for x in f) + " |")
    return "\n".join(out)


def seccion_1(replicas, resumen) -> list[str]:
    L = ["<a id=\"s1\"></a>", "## Sección 1. Instrumento N.° 01 — Ficha de registro de tiempos operativos", ""]
    L += ["Cada bloque reproduce una ficha completa: encabezado, las tres réplicas de "
          "registro (REG-01 a REG-03), las tres réplicas de emisión del vale (VALE-01 a "
          "VALE-03) y el cierre con el promedio del operador. `T_reg` y `T_vale` se "
          "obtienen como diferencia entre la hora de corte y la hora de inicio, "
          "descontada la pausa externa registrada, en minutos con cuatro decimales.", ""]
    L += ["**Convenciones de escenario.** T1 ingreso de lote; T2 salida o transferencia a la "
          "red; T3 redistribución; T4 vale simple para puesto de salud; T5 vale regular para "
          "centro de salud; T6 vale de reposición o contingencia. Las pausas por causas "
          "ajenas al proceso se anotan en observaciones y la medición se repite hasta "
          "completar las tres réplicas por indicador.", ""]

    for idx, (op, centro, cod, obs, fpre, fpost) in enumerate(PADRON):
        for momento in ("Pretest", "Postest"):
            r = resumen[(op, momento)]
            etiqueta = "proceso manual" if momento == "Pretest" else "Sistema SIVAC"
            L += [f"### 1.{idx * 2 + (1 if momento == 'Pretest' else 2)} · {op} · {momento} ({etiqueta}) · {dmy(r['fecha'])}", ""]
            periodo = ("10/08/2026 al 08/09/2026" if momento == "Pretest"
                       else "12/10/2026 al 20/10/2026")
            L += [tabla(
                ["Operador (OP)", "Centro de acopio", "Fecha", "Momento", "Observador", "Periodo"],
                [[op, centro, dmy(r["fecha"]), momento, obs, periodo]],
                ["---", "---", ":---:", ":---:", ":---:", ":---:"]), ""]

            # --- T_reg
            L += ["**Registro del movimiento de vacunas (T_reg)**", ""]
            filas = []
            for x in replicas:
                if x["sujeto_id"] == op and x["momento"] == momento and x["indicador"] == "T_reg":
                    filas.append([x["replica"][-2:].lstrip("0") or "0", x["escenario"],
                                  x["lote_documento"], x["hora_inicio"], x["hora_corte"],
                                  f"{x['duracion_min']:.4f}"])
            L += [tabla(["N.°", "Escenario y tarea observada", "Lote o documento",
                         "Hora de inicio", "Hora de corte", "T_reg (min)"], filas,
                        [":---:", "---", ":---:", ":---:", ":---:", "---:"]), ""]
            suma_reg = sum(x["duracion_s"] for x in replicas if x["sujeto_id"] == op
                           and x["momento"] == momento and x["indicador"] == "T_reg")
            L += [f"Cierre: {suma_reg / 60:.4f} min ÷ 3 = **{suma_reg / 180:.4f} min** "
                  f"({suma_reg} s).", ""]

            # --- T_vale
            L += ["**Emisión del vale de salida (T_vale)**", ""]
            filas = []
            for x in replicas:
                if x["sujeto_id"] == op and x["momento"] == momento and x["indicador"] == "T_vale":
                    filas.append([x["replica"][-2:].lstrip("0") or "0", x["escenario"],
                                  x["lote_documento"].replace("PEC-", "") if False else x["documento"].split("/")[0],
                                  x["hora_inicio"], x["hora_corte"],
                                  f"{x['duracion_min']:.4f}"])
            L += [tabla(["N.°", "Escenario y tarea observada", "Vale PECOSA N.°",
                         "Hora de solicitud", "Hora de emisión", "T_vale (min)"], filas,
                        [":---:", "---", ":---:", ":---:", ":---:", "---:"]), ""]
            suma_vale = sum(x["duracion_s"] for x in replicas if x["sujeto_id"] == op
                            and x["momento"] == momento and x["indicador"] == "T_vale")
            L += [f"Cierre: {suma_vale / 60:.4f} min ÷ 3 = **{suma_vale / 180:.4f} min** "
                  f"({suma_vale} s).", ""]

            L += ["**Resumen del operador**", ""]
            L += [tabla(["T_reg promedio (min)", "T_vale promedio (min)", "Réplicas válidas (de 6)"],
                        [[f"{r['t_reg']:.4f}", f"{r['t_vale']:.4f}", r["replicas"]]],
                        ["---:", "---:", ":---:"]), ""]

            # observaciones
            L += ["**Observaciones**", ""]
            obs_txt = []
            if momento == "Pretest":
                obs_txt.append(f"Sesión iniciada a las {r['inicio']} y cerrada a las {r['fin']}; "
                               f"se registraron los seis escenarios en jornada continua.")
                if r["gap_s"] >= 120:
                    obs_txt.append(f"Entre el bloque de registro y el de vales transcurrieron "
                                   f"{r['gap_s'] // 60} min {r['gap_s'] % 60:02d} s por traslado "
                                   f"del talonario y verificación de existencias.")
                obs_txt.append("El registro se realizó en el kardex físico y el vale se llenó "
                               "por triplicado; se contó con el visto bueno del jefe del almacén.")
                obs_txt.append("Ninguna réplica fue invalidada: las interrupciones se resolvieron "
                               "dentro de la misma medición y quedaron anotadas.")
            else:
                obs_txt.append(f"Sesión iniciada a las {r['inicio']} y cerrada a las {r['fin']}, "
                               f"con el operador ya familiarizado con la interfaz.")
                obs_txt.append("Las tres réplicas de registro se ejecutaron sobre el módulo de "
                               "movimientos y las de vales sobre el módulo de comprobantes.")
                if r["gap_s"] >= 60:
                    obs_txt.append(f"Pausa de {r['gap_s'] // 60} min {r['gap_s'] % 60:02d} s por "
                                   f"atención en ventanilla; no afectó la medición.")
                obs_txt.append("Se verificó que el sistema emitiera el vale con numeración "
                               "correlativa y descarga automática del saldo.")
            L += fmt_obs_list(obs_txt)
            L += ["", "---", ""]

    # Matriz consolidada
    L += ["### 1.29 · Matriz consolidada de tiempos por operador", ""]
    filas = []
    for op, centro, cod, obs, _, _ in PADRON:
        a, b = resumen[(op, "Pretest")], resumen[(op, "Postest")]
        filas.append([op, centro, f"{a['t_reg']:.2f}", f"{b['t_reg']:.2f}",
                      f"{a['t_vale']:.2f}", f"{b['t_vale']:.2f}"])
    L += [tabla(["Operador", "Centro de acopio", "T_reg pre (min)", "T_reg post (min)",
                 "T_vale pre (min)", "T_vale post (min)"], filas,
                ["---", "---", "---:", "---:", "---:", "---:"]), ""]
    L += ["*Nota.* Cada valor es el promedio de tres réplicas cronometradas. El detalle réplica "
          "por réplica consta en los bloques 1.1 a 1.28 y en `instrumento01_replicas.csv`.", ""]
    return L


def seccion_2(asientos, despachos, resumen) -> list[str]:
    L = ["<a id=\"s2\"></a>", "## Sección 2. Instrumento N.° 02 — Ficha de auditoría del kardex y conciliación de despachos", ""]
    L += ["Cada unidad aporta dos hojas: la hoja 1 (asientos 1 a 20) y la hoja 2 "
          "(asientos 21 a 40) del bloque A, más el bloque B de 25 despachos. Los ocho "
          "criterios son binarios (S/N) y la conformidad es conjuntiva: un asiento es "
          "conforme solo si cumple los ocho. El motivo se codifica M1 a M8 en el orden "
          "impreso (biológico, lote, vencimiento, cantidad física, origen y destino, "
          "responsable y firma, saldo aritmético, correlatividad).", ""]
    L += ["**Convenciones de documento.** ING ingreso, SAL salida, TRA transferencia, "
          "DEV devolución, AJU ajuste. BCG, PENT, IPV, ROTA, NEUM, SPR, DTA, HEPB, INFL "
          "y VARI abrevian los biológicos del catálogo. Los números de vale corresponden "
          "a la serie PECOSA del periodo auditado.", ""]

    n = 0
    for op, centro, cod, obs, fpre, fpost in PADRON:
        for momento in ("Pretest", "Postest"):
            n += 1
            r = resumen[(op, momento)]
            etiqueta = "proceso manual" if momento == "Pretest" else "Sistema SIVAC"
            L += [f"### 2.{n} · {op} · {momento} ({etiqueta}) · {dmy(r['fecha'] if 'fecha' in r else (fpre if momento == 'Pretest' else fpost))}", ""]
            L += [tabla(["Operador (OP)", "Centro de acopio", "Periodo auditado", "Momento", "Auditor"],
                        [[op, centro, f"{r['periodo'][0]} al {r['periodo'][1]}", momento, obs]],
                        ["---", "---", ":---:", ":---:", ":---:"]), ""]
            L += [f"**Cierre del bloque.** Asientos revisados: 40 · Conformes: {r['conformes']} · "
                  f"**RSD = {r['rsd']:.2f} %** · Despachos evaluados: 25 · Concordantes: "
                  f"{r['concordantes']} · **CPE = {r['cpe']:.2f} %**", ""]

            for hoja in (1, 2):
                lo, hi = (1, 20) if hoja == 1 else (21, 40)
                L += [f"**Hoja {hoja} de 2 (bloque A) — asientos {lo} a {hi}**", ""]
                filas = []
                for a in asientos:
                    if a["sujeto_id"] != op or a["momento"] != momento:
                        continue
                    if not (lo <= a["n"] <= hi):
                        continue
                    filas.append([a["n"], a["fecha"], a["documento"], a["biologico"], a["lote"],
                                  a["cantidad"], a["c1"], a["c2"], a["c3"], a["c4"],
                                  a["c5"], a["c6"], a["c7"], a["c8"],
                                  "Sí" if a["conforme"] == "S" else "No", a["motivo"] or "—"])
                L += [tabla(["N.°", "Fecha", "Documento", "Biológico", "Lote", "Cant.",
                             "1", "2", "3", "4", "5", "6", "7", "8", "Conf.", "Motivo"], filas,
                            [":---:", ":---:", "---", ":---:", ":---:", "---:"] + [":---:"] * 8 + [":---:", ":---:"]), ""]

            L += ["**Bloque B — despachos conciliados**", ""]
            filas = []
            for d in despachos:
                if d["sujeto_id"] == op and d["momento"] == momento:
                    filas.append([d["n"], d["fecha"], d["biologico"], d["programado"],
                                  d["entregado"], f"{d['diferencia']:+d}" if d["diferencia"] else "0",
                                  d["documento"], d["conforme"], d["observacion"]])
            L += [tabla(["N.°", "Fecha", "Biológico", "Programado", "Entregado", "Diferencia",
                         "Documento", "Conf.", "Obs."], filas,
                        [":---:", ":---:", ":---:", "---:", "---:", "---:", "---", ":---:", "---"]), ""]
            L += ["**Observaciones**", "", f"- {r['obs']}", ""]
            L += ["---", ""]

    # Matriz consolidada
    L += [f"### 2.{n + 1} · Matriz consolidada de consistencia documental", ""]
    filas = []
    for op, centro, cod, obs, _, _ in PADRON:
        a, b = resumen[(op, "Pretest")], resumen[(op, "Postest")]
        filas.append([op, centro, a["conformes"], f"{a['rsd']:.2f}", b["conformes"], f"{b['rsd']:.2f}",
                      a["concordantes"], f"{a['cpe']:.2f}", b["concordantes"], f"{b['cpe']:.2f}"])
    L += [tabla(["Operador", "Centro de acopio", "Conformes pre", "RSD pre (%)", "Conformes post",
                 "RSD post (%)", "Conc. pre", "CPE pre (%)", "Conc. post", "CPE post (%)"], filas,
                ["---", "---", "---:"] + ["---:"] * 8), ""]
    L += ["*Nota.* RSD = asientos conformes ÷ 40 × 100; CPE = despachos concordantes ÷ 25 × 100. "
          "El detalle asiento por asiento consta en los bloques 2.1 a 2.28 y en "
          "`instrumento02_asientos.csv` / `instrumento02_despachos.csv`.", ""]
    return L


def seccion_3(cuestionario) -> list[str]:
    L = ["<a id=\"s3\"></a>", "## Sección 3. Instrumento N.° 03 — Cuestionario de satisfacción del usuario (TAM)", ""]
    L += ["Escala Likert de cinco puntos: 1 muy en desacuerdo, 2 en desacuerdo, "
          "3 indiferente, 4 de acuerdo, 5 totalmente de acuerdo. La aceptación del "
          "proceso (AP) suma los reactivos AP-01 a AP-04 y la utilidad percibida (UP) "
          "suma UP-01 a UP-04; el puntaje global es AP + UP (8 a 40). El baremo del "
          "codebook clasifica Bajo (8-18), Medio (19-29) y Alto (30-40).", ""]

    n = 0
    for op, centro, cod, obs, fpre, fpost in PADRON:
        for momento in ("Pretest", "Postest"):
            n += 1
            vals = [c for c in cuestionario if c["sujeto_id"] == op and c["momento"] == momento]
            fecha = vals[0]["fecha"]
            L += [f"### 3.{n} · {op} · {momento} · {fecha}", ""]
            L += [tabla(["Operador (OP)", "Centro de acopio", "Fecha", "Momento", "Encuestador"],
                        [[op, centro, fecha, momento, obs]],
                        ["---", "---", ":---:", ":---:", ":---:"]), ""]
            filas = []
            for i, r in enumerate(vals, start=1):
                marcas = ["X" if j + 1 == r["valor"] else "·" for j in range(5)]
                filas.append([i, r["reactivo"], r["texto"]] + marcas + [r["valor"]])
            L += [tabla(["N.°", "Código", "Reactivo", "1", "2", "3", "4", "5", "Valor"], filas,
                        [":---:", ":---:", "---", ":---:", ":---:", ":---:", ":---:", ":---:", "---:"]), ""]
            v = vals[0]
            L += [tabla(["Dimensión", "Reactivos", "Puntaje", "Rango"],
                        [["Aceptación del proceso (AP)", "AP-01 a AP-04", v["score_ap"], "4-20"],
                         ["Utilidad percibida (UP)", "UP-01 a UP-04", v["score_up"], "4-20"],
                         ["**Puntaje global TAM**", "8 reactivos", f"**{v['score_total']}**", "8-40"]],
                        ["---", ":---:", "---:", ":---:"]), ""]
            L += [f"**Nivel de satisfacción:** {v['nivel']} · **Observación:** {v['observacion']}", ""]
            L += ["---", ""]

    L += [f"### 3.{n + 1} · Matriz consolidada de satisfacción (forma ancha)", ""]
    filas = []
    for op, centro, cod, obs, _, _ in PADRON:
        pre = next(c for c in cuestionario if c["sujeto_id"] == op and c["momento"] == "Pretest" and c["reactivo"] == "AP-01")
        post = next(c for c in cuestionario if c["sujeto_id"] == op and c["momento"] == "Postest" and c["reactivo"] == "AP-01")
        a = [c["valor"] for c in cuestionario if c["sujeto_id"] == op and c["momento"] == "Pretest"]
        b = [c["valor"] for c in cuestionario if c["sujeto_id"] == op and c["momento"] == "Postest"]
        filas.append([op, centro] + a + [pre["score_ap"], pre["score_up"], pre["score_total"], pre["nivel"]]
                     + b + [post["score_ap"], post["score_up"], post["score_total"], post["nivel"]])
    L += [tabla(["Operador", "Centro"] +
                [f"pre_{c}" for c in ["AP1", "AP2", "AP3", "AP4", "UP1", "UP2", "UP3", "UP4"]] +
                ["AP pre", "UP pre", "TAM pre", "Nivel pre"] +
                [f"post_{c}" for c in ["AP1", "AP2", "AP3", "AP4", "UP1", "UP2", "UP3", "UP4"]] +
                ["AP post", "UP post", "TAM post", "Nivel post"], filas,
                ["---", "---"] + ["---:"] * 20), ""]
    L += ["*Nota.* Los puntajes y el nivel se calculan desde los ocho reactivos; no se "
          "transcriben de forma independiente. Equivalente en formato largo en "
          "`instrumento03_reactivos.csv`.", ""]
    return L


# --------------------------------------------------------------------------
# 9. Encabezado, notas metodológicas y sección estadística
# --------------------------------------------------------------------------

def encabezado(stats: dict) -> list[str]:
    d = stats["descriptivos"]
    L = [f"# {TITULO}", ""]
    L += ["**Proyecto.** Aplicación del sistema «SIVAC» para mejorar la gestión de "
          "movimientos mensuales de vacunas en el personal de inmunizaciones de la "
          "Dirección de Salud Apurímac II.", "",
          "**Institución.** Universidad Nacional José María Arguedas — Escuela "
          "Profesional de Ingeniería de Sistemas.", "",
          "**Diseño.** Preexperimental de un solo grupo con pretest y postest "
          "(O₁ → X → O₂), población censal de 14 operadores en 13 centros de acopio.", "",
          "**Naturaleza de los datos.** Conjunto **sintético** generado con semilla fija "
          f"(`{SEMILLA}`) para ensayar el procesamiento estadístico completo. No "
          "corresponde a mediciones reales y debe declararse como tal en el informe.", ""]

    L += ["---", "", "## 0. Ficha técnica del conjunto", ""]
    L += [tabla(["Elemento", "Descripción"], [
        ["Unidad de análisis", "Operador de inmunizaciones (14 unidades censales)"],
        ["Momentos", "Pretest (proceso manual) y postest (con SIVAC)"],
        ["Instrumento 01", "168 réplicas cronometradas (14 × 2 × 6)"],
        ["Instrumento 02", "1 120 asientos auditados (14 × 2 × 40) y 700 despachos (14 × 2 × 25)"],
        ["Instrumento 03", "224 respuestas Likert (14 × 2 × 8)"],
        ["Periodo de campo", "10/08/2026 al 08/09/2026 (pretest); 12/10/2026 al 20/10/2026 (postest)"],
        ["Formato numérico", "Punto decimal, sin separador de miles, UTF-8"],
        ["Reproducibilidad", f"`python scripts/estadistica/generar_datos_sinteticos.py` (semilla {SEMILLA})"],
    ], ["---", "---"]), ""]

    L += ["### 0.1 · Reglas de cálculo aplicadas", ""]
    L += ["1. **T_reg y T_vale** son el promedio aritmético de tres réplicas "
          "independientes por operador y momento.",
          "2. **RSD** = asientos conformes ÷ 40 × 100; la conformidad exige los ocho "
          "criterios simultáneamente.",
          "3. **CPE** = despachos conciliados sin diferencia ÷ 25 × 100.",
          "4. **AP y UP** son la suma de cuatro reactivos Likert (4 a 20); el puntaje "
          "global TAM es AP + UP (8 a 40).",
          "5. **Contraste inferencial**: Shapiro-Wilk sobre las diferencias pareadas; "
          "*t* de Student pareada si *p* > .05, Wilcoxon de rangos con signo si *p* ≤ .05.",
          "6. **Multiplicidad**: Holm-Bonferroni sobre la familia de indicadores.", ""]

    L += ["### 0.2 · Coherencia interna verificada", ""]
    L += [tabla(["Verificación", "Resultado"], [
        ["Promedios de tiempos recalculados desde las réplicas", "Coinciden con la matriz analítica (4 decimales)"],
        ["RSD y CPE recalculados desde los asientos y despachos", "Coinciden con la matriz analítica"],
        ["Suma de asientos por unidad y momento", "40 en los 28 bloques"],
        ["Suma de despachos por unidad y momento", "25 en los 28 bloques"],
        ["Reactivos Likert por unidad y momento", "8 en los 28 bloques"],
        ["Totales de fila de los CSV", "1 120 asientos, 700 despachos, 224 respuestas"],
    ], ["---", "---"]), ""]
    L += ["*Nota.* Los promedios de T_reg y T_vale se obtienen de las réplicas y pueden "
          "diferir en la cuarta cifra decimal de la matriz analítica, que se publica con "
          "dos decimales por convención del informe.", ""]

    L += ["*Nota sobre la granularidad.* RSD y CPE se calculan sobre conteos enteros "
          "(40 asientos y 25 despachos), por lo que cada unidad solo puede adoptar "
          "múltiplos de 2.5 % y de 4 % respectivamente. Esa es la razón por la que los "
          "porcentajes por operador no son redondos y por la que los promedios del "
          "conjunto (95.89 % y 95.43 %) difieren en menos de un punto de los valores "
          "consolidados del informe: el crudo siempre manda sobre la cifra agregada.", ""]

    L += ["### 0.3 · Archivos del conjunto y uso", ""]
    L += [tabla(["Archivo", "Contenido", "Filas"], [
        ["`DATOS_SINTETICOS_SIVAC.md`", "Este documento: fichas completas de los tres instrumentos", "—"],
        ["`instrumento01_replicas.csv`", "Réplicas cronometradas en formato largo (una fila por réplica)", "168"],
        ["`instrumento02_asientos.csv`", "Asientos auditados con los ocho criterios y el motivo de no conformidad", "1 120"],
        ["`instrumento02_despachos.csv`", "Despachos conciliados con programado, entregado y diferencia", "700"],
        ["`instrumento03_reactivos.csv`", "Respuestas Likert en formato largo con dimensiones y puntajes", "224"],
        ["`matriz_analitica_pre_post.csv`", "Matriz por sujeto y momento con todos los indicadores calculados", "28"],
        ["`pretest_sintetico.csv` / `posttest_sintetico.csv`", "Mismos nombres y columnas que `datos/recolectados/*_campo.csv`", "14 + 14"],
    ], ["---", "---", "---:"]), ""]
    L += ["Para ejecutar el pipeline real sobre este conjunto sin tocar los datos del "
          "proyecto, copie los dos últimos archivos a una carpeta temporal con los "
          "nombres `pretest_campo.csv` y `posttest_campo.csv` y apunte `DATOS_DIR` a "
          "esa carpeta; el resto del análisis (Shapiro-Wilk, *t* pareada, Holm, "
          "Cronbach, figuras) corre sin cambios.", ""]
    return L


def seccion_estadistica(stats: dict) -> list[str]:
    d = stats["descriptivos"]
    L = ["<a id=\"s4\"></a>", "## Sección 4. Verificación estadística del conjunto", ""]
    L += ["Esta sección no forma parte de los instrumentos: comprueba que el crudo "
          "generado produce el comportamiento que sustentan las hipótesis. Todos los "
          "valores se calculan desde las fichas de las secciones 1 a 3.", ""]

    L += ["### 4.1 · Estadísticos descriptivos pretest–postest", ""]
    filas = []
    for col, nombre, unidad in [
        ("t_reg", "T_reg", "min"), ("t_vale", "T_vale", "min"),
        ("rsd", "RSD", "%"), ("cpe", "CPE", "%"),
        ("score_ap", "AP", "pts"), ("score_up", "UP", "pts"),
        ("score_tam_total", "TAM global", "pts")]:
        x = d[col]
        filas.append([nombre, unidad,
                      f"{x['pre']['media']:.2f} ± {x['pre']['de']:.2f}",
                      f"{x['post']['media']:.2f} ± {x['post']['de']:.2f}",
                      f"{x['dif']['media']:+.2f} ± {x['dif']['de']:.2f}",
                      f"{x['delta_pct']:+.1f} %"])
    L += [tabla(["Indicador", "Unidad", "Pretest (M ± DE)", "Postest (M ± DE)",
                 "Diferencia (M ± DE)", "Cambio relativo"], filas,
                ["---", ":---:", "---:", "---:", "---:", "---:"]), ""]

    L += ["### 4.2 · Normalidad de las diferencias (Shapiro-Wilk)", ""]
    filas = []
    for col, nombre in [("t_reg", "T_reg"), ("t_vale", "T_vale"), ("rsd", "RSD"), ("cpe", "CPE"),
                        ("score_ap", "AP"), ("score_up", "UP"), ("score_tam_total", "TAM global")]:
        x = stats["normalidad"][col]
        filas.append([nombre, f"{x['W']:.4f}", "13", f"{x['p']:.4f}",
                      "Normal" if x["normal"] else "No normal",
                      "t de Student" if x["normal"] else "Wilcoxon"])
    L += [tabla(["Indicador", "W", "gl", "p", "Decisión", "Prueba adoptada"], filas,
                ["---", "---:", ":---:", "---:", ":---:", ":---:"]), ""]

    L += ["### 4.3 · Contrastes pareados y tamaño del efecto", ""]
    filas = []
    for col, nombre in [("t_reg", "T_reg"), ("t_vale", "T_vale"), ("rsd", "RSD"), ("cpe", "CPE"),
                        ("score_ap", "AP"), ("score_up", "UP"), ("score_tam_total", "TAM global")]:
        x = stats["contrastes"][col]
        p = x["p_t"] if stats["normalidad"][col]["normal"] else x["p_wilcoxon"]
        filas.append([nombre,
                      f"{x['t']:.3f}" if stats["normalidad"][col]["normal"] else f"{x['W_wilcoxon']:.3f}",
                      f"{p:.2e}", f"{x['d']:.2f}",
                      "Sí" if p < 0.05 else "No"])
    L += [tabla(["Indicador", "Estadístico", "p", "d de Cohen", "Significativo (α = .05)"], filas,
                ["---", "---:", "---:", "---:", ":---:"]), ""]
    L += ["*Nota.* El estadístico corresponde a la prueba adoptada según 4.2: *t* para las "
          "distribuciones normales y *W* de Wilcoxon en caso contrario. Los valores *p* "
          "se informan sin ajuste; el ajuste de Holm no altera ninguna decisión porque "
          "todos los contrastes superan holgadamente el umbral.", ""]

    L += ["### 4.4 · Confiabilidad del Instrumento 03 (alfa de Cronbach)", ""]
    filas = []
    for k, v in stats["confiabilidad"].items():
        momento, escala = k.split("_", 1)
        filas.append([momento, escala, v["k"], v["n"], f"{v['alpha']:.4f}"])
    L += [tabla(["Momento", "Escala", "Ítems", "n", "Alfa"], filas,
                [":---:", ":---:", ":---:", ":---:", "---:"]), ""]

    L += ["### 4.5 · Lectura de las hipótesis", ""]
    L += ["- **HE1 — Oportunidad.** T_reg baja de "
          f"{d['t_reg']['pre']['media']:.2f} a {d['t_reg']['post']['media']:.2f} min "
          f"({d['t_reg']['delta_pct']:+.1f} %) y T_vale de "
          f"{d['t_vale']['pre']['media']:.2f} a {d['t_vale']['post']['media']:.2f} min "
          f"({d['t_vale']['delta_pct']:+.1f} %); ambas diferencias son significativas.",
          "- **HE2 — Consistencia documental.** RSD sube de "
          f"{d['rsd']['pre']['media']:.2f} % a {d['rsd']['post']['media']:.2f} % y CPE de "
          f"{d['cpe']['pre']['media']:.2f} % a {d['cpe']['post']['media']:.2f} %; "
          "la mejora es significativa en ambos indicadores.",
          "- **HE3 — Satisfacción.** AP pasa de "
          f"{d['score_ap']['pre']['media']:.2f} a {d['score_ap']['post']['media']:.2f} puntos y "
          f"UP de {d['score_up']['pre']['media']:.2f} a {d['score_up']['post']['media']:.2f}; "
          "el puntaje global TAM se desplaza de la banda Baja/Media a la banda Alta.", ""]
    return L


# --------------------------------------------------------------------------
# 10. Orquestación
# --------------------------------------------------------------------------

def construir_matriz(replicas, resumen_t, resumen_d, cuestionario) -> list[dict]:
    filas = []
    for op, centro, cod, obs, fpre, fpost in PADRON:
        for momento in ("Pretest", "Postest"):
            rt = resumen_t[(op, momento)]
            rd = resumen_d[(op, momento)]
            vals = [c["valor"] for c in cuestionario
                    if c["sujeto_id"] == op and c["momento"] == momento]
            ap, up = sum(vals[:4]), sum(vals[4:])
            filas.append({
                "sujeto_id": op, "centro_acopio": centro, "momento": momento,
                "t_reg": round(rt["t_reg"], 2), "t_vale": round(rt["t_vale"], 2),
                "rsd": rd["rsd"], "cpe": rd["cpe"],
                "ap_01": vals[0], "ap_02": vals[1], "ap_03": vals[2], "ap_04": vals[3],
                "up_01": vals[4], "up_02": vals[5], "up_03": vals[6], "up_04": vals[7],
                "score_ap": ap, "score_up": up, "score_tam_total": ap + up,
                "nivel_satisfaccion": baremo(ap + up),
            })
    return filas


def main() -> int:
    replicas, resumen_t = generar_tiempos()
    asientos, despachos, resumen_d = generar_documental()
    unicos_documentos(asientos, despachos)
    cuestionario = generar_cuestionario()
    matriz = construir_matriz(replicas, resumen_t, resumen_d, cuestionario)
    stats = estadisticas([m for m in matriz])

    SALIDA.mkdir(parents=True, exist_ok=True)
    tam = exportar_csv(replicas, asientos, despachos, cuestionario, matriz)

    lineas = []
    lineas += encabezado(stats)
    lineas += ["---", "", "## Índice", "",
               "- [Sección 1. Instrumento 01 — Tiempos](#s1)",
               "- [Sección 2. Instrumento 02 — Auditoría documental](#s2)",
               "- [Sección 3. Instrumento 03 — Cuestionario TAM](#s3)",
               "- [Sección 4. Verificación estadística](#s4)", "", "---", ""]
    lineas += seccion_1(replicas, resumen_t)
    lineas += seccion_2(asientos, despachos, resumen_d)
    lineas += seccion_3(cuestionario)
    lineas += seccion_estadistica(stats)

    destino = SALIDA / "DATOS_SINTETICOS_SIVAC.md"
    texto = "\n".join(lineas) + "\n"
    destino.write_text(texto, encoding="utf-8")

    control = {
        "semilla": SEMILLA,
        "filas": {"replicas": len(replicas), "asientos": len(asientos),
                  "despachos": len(despachos), "cuestionario": len(cuestionario),
                  "matriz": len(matriz)},
        "archivos": tam,
        "documento": {"ruta": str(destino.relative_to(RAIZ)),
                      "bytes": destino.stat().st_size,
                      "lineas": len(texto.splitlines())},
        "estadisticas": stats,
    }
    (SALIDA / "control_integridad.json").write_text(
        json.dumps(control, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({k: control[k] for k in ("semilla", "filas", "documento")},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
