# -*- coding: utf-8 -*-
"""Consolida el libro de captura v22 en los dos CSV de campo.

Es el paso que la guía de campo promete y que hasta ahora no existía: lee
`07_CAPTURA/LIBRO_DE_CAPTURA_v22.xlsx` (una fila por registro previsto, con las
mediciones digitadas de las fichas de papel), recalcula los siete indicadores
por operador y fase y escribe `datos/recolectados/pretest_campo.csv` y
`posttest_campo.csv` con las dieciocho columnas del diccionario de variables.

Reglas (idénticas a las de la ficha impresa y a las de
`construir_registro_campo.py`):

    duracion_s   = hora_corte − hora_inicio − pausa_s
    duracion_min = duracion_s ÷ 60
    T_reg        = media de las réplicas válidas de T_reg (tres)
    T_vale       = media de las réplicas válidas de T_vale (tres)
    RSD          = asientos conformes ÷ 40 × 100
    CPE          = despachos conformes ÷ 25 × 100
    AP / UP      = suma de los cuatro reactivos de cada dimensión
    TAM          = AP + UP; nivel según baremo Bajo 8–18, Medio 19–29, Alto 30–40

Un asiento es conforme solo si los ocho criterios están en S; un despacho, solo
si la cantidad entregada iguala la programada. El libro declara las columnas
«conforme», pero el consolidado las recalcula y avisa cuando no coinciden: el
papel manda, la aritmética controla.

Uso:
    python scripts/estadistica/consolidar_libro_captura.py            # audita
    python scripts/estadistica/consolidar_libro_captura.py --escribir  # consolida
    python scripts/estadistica/consolidar_libro_captura.py --borrador --escribir

Sin `--escribir` solo informa qué falta: no toca ningún archivo. Con
`--escribir` exige que las cuatro hojas estén completas para cada fase; si algo
falta, no escribe y enumera los registros ausentes. `--borrador` escribe de
todos modos, pero con el sufijo `_borrador` para que nadie lo confunda con el
consolidado definitivo.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parents[2]
LIBRO = (RAIZ / "salidas" / "instrumentos" / "INSTRUMENTOS_DEFINITIVOS_v22"
         / "07_CAPTURA" / "LIBRO_DE_CAPTURA_v22.xlsx")
RECO = RAIZ / "datos" / "recolectados"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generar_datos_sinteticos as G  # noqa: E402  (padrón y baremo)

COLUMNAS = ["sujeto_id", "centro_acopio", "t_reg", "t_vale", "rsd", "cpe",
            "ap_01", "ap_02", "ap_03", "ap_04", "up_01", "up_02",
            "up_03", "up_04", "score_ap", "score_up", "score_tam_total",
            "nivel_satisfaccion"]

REPLICAS = ("01_replicas", "02_asientos", "02_despachos", "03_reactivos")
ASIENTOS_POR_SESION = 40
DESPACHOS_POR_SESION = 25
REPLICAS_POR_INDICADOR = 3
REACTIVOS = ("AP-01", "AP-02", "AP-03", "AP-04",
             "UP-01", "UP-02", "UP-03", "UP-04")


# --------------------------------------------------------------------------
# Lectura del libro
# --------------------------------------------------------------------------

def _texto(valor) -> str:
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return "Sí" if valor else "No"
    return str(valor).strip()


def _entero(valor) -> int | None:
    texto = _texto(valor).replace(",", ".")
    if not texto:
        return None
    try:
        return int(round(float(texto)))
    except ValueError:
        return None


def _segundos(hora) -> int | None:
    """HH:MM:SS (texto o datetime.time) a segundos desde medianoche."""
    if hora is None:
        return None
    if hasattr(hora, "hour"):
        return hora.hour * 3600 + hora.minute * 60 + hora.second
    texto = _texto(hora)
    partes = texto.split(":")
    if len(partes) not in (2, 3):
        return None
    try:
        valores = [int(p) for p in partes]
    except ValueError:
        return None
    if len(valores) == 2:
        valores.append(0)
    return valores[0] * 3600 + valores[1] * 60 + valores[2]


def _tabla(libro, nombre: str) -> tuple[list[str], list[dict]]:
    hoja = libro[nombre]
    cabecera = [celda.value for celda in hoja[2]]
    cabecera = [c for c in cabecera if c is not None]
    filas = []
    for fila in hoja.iter_rows(min_row=3, max_col=len(cabecera)):
        registro = {cabecera[j]: fila[j].value for j in range(len(cabecera))}
        if not _texto(registro.get("sujeto_id")):
            continue
        filas.append(registro)
    return cabecera, filas


# --------------------------------------------------------------------------
# Cálculo
# --------------------------------------------------------------------------

def _duracion(registro: dict) -> tuple[int | None, str | None]:
    """Segundos netos y aviso cuando la aritmética no cierra."""
    inicio = _segundos(registro.get("hora_inicio"))
    corte = _segundos(registro.get("hora_corte"))
    pausa = _entero(registro.get("pausa_s")) or 0
    declarada = _entero(registro.get("duracion_s"))
    if inicio is not None and corte is not None:
        bruta = corte - inicio
        if bruta < 0:
            bruta += 24 * 3600          # cruce de medianoche
        neta = bruta - pausa
        if declarada is not None and declarada != neta:
            return neta, (f"duracion_s declarada {declarada} s no coincide con "
                          f"la aritmética ({neta} s)")
        return neta, None
    if declarada is not None:
        return declarada, None
    return None, "sin horas ni duración"


def _valida(registro: dict) -> bool:
    return _texto(registro.get("valida")) in ("Sí", "Si", "S", "sí", "si", "")


def _conforme_asiento(registro: dict) -> bool:
    criterios = [_texto(registro.get(f"c{i}")).upper() for i in range(1, 9)]
    return all(c == "S" for c in criterios)


def _conforme_despacho(registro: dict) -> bool:
    programado = _entero(registro.get("programado"))
    entregado = _entero(registro.get("entregado"))
    return programado is not None and programado == entregado


def consolidar(libro_path: Path = LIBRO) -> dict:
    libro = load_workbook(libro_path, data_only=True)
    faltantes = [n for n in REPLICAS if n not in libro.sheetnames]
    if faltantes:
        raise SystemExit(f"El libro no tiene las hojas {faltantes}.")

    _, replicas = _tabla(libro, "01_replicas")
    _, asientos = _tabla(libro, "02_asientos")
    _, despachos = _tabla(libro, "02_despachos")
    _, reactivos = _tabla(libro, "03_reactivos")

    avisos: list[str] = []
    pendientes: dict[tuple[str, str], list[str]] = {}
    filas: list[dict] = []

    for op, centro, _cod, _obs, _pre, _post in G.PADRON:
        for momento in ("Pretest", "Postest"):
            clave = (op, momento)
            pendientes[clave] = []

            # D1 · tiempos: media de las réplicas válidas de cada indicador.
            tiempos = {}
            for indicador in ("T_reg", "T_vale"):
                grupo = [r for r in replicas
                         if _texto(r["sujeto_id"]) == op
                         and _texto(r["momento"]) == momento
                         and _texto(r["indicador"]) == indicador]
                valores = []
                for registro in grupo:
                    segundos, aviso = _duracion(registro)
                    if aviso:
                        avisos.append(f"{op} {momento} {indicador} "
                                      f"{_texto(registro.get('replica'))}: {aviso}")
                    if not _valida(registro):
                        continue
                    if segundos is None:
                        continue
                    valores.append(segundos / 60.0)
                if len(valores) < REPLICAS_POR_INDICADOR:
                    pendientes[clave].append(
                        f"{indicador}: {len(valores)} de "
                        f"{REPLICAS_POR_INDICADOR} réplicas válidas")
                tiempos[indicador] = valores

            # D2 · consistencia documental.
            docs = [r for r in asientos
                    if _texto(r["sujeto_id"]) == op
                    and _texto(r["momento"]) == momento]
            desp = [r for r in despachos
                    if _texto(r["sujeto_id"]) == op
                    and _texto(r["momento"]) == momento]
            conformes = [r for r in docs if _conforme_asiento(r)]
            concordantes = [r for r in desp if _conforme_despacho(r)]

            if len(docs) < ASIENTOS_POR_SESION:
                pendientes[clave].append(
                    f"asientos: {len(docs)} de {ASIENTOS_POR_SESION}")
            if len(desp) < DESPACHOS_POR_SESION:
                pendientes[clave].append(
                    f"despachos: {len(desp)} de {DESPACHOS_POR_SESION}")

            for registro in docs:
                declarado = _texto(registro.get("conforme"))
                real = _conforme_asiento(registro)
                if declarado and (declarado.startswith("S")) != real:
                    avisos.append(
                        f"{op} {momento} asiento {_texto(registro.get('n'))}: "
                        f"«conforme» dice {declarado} y los criterios dan "
                        f"{'Sí' if real else 'No'}")
                if real and not _texto(registro.get("c1")):
                    pendientes[clave].append(
                        f"asiento {_texto(registro.get('n'))} sin criterios")

            for registro in desp:
                programado = _entero(registro.get("programado"))
                entregado = _entero(registro.get("entregado"))
                if programado is None or entregado is None:
                    pendientes[clave].append(
                        f"despacho {_texto(registro.get('n'))} sin cantidades")

            # D3 · cuestionario.
            respuestas = {}
            for registro in reactivos:
                if (_texto(registro["sujeto_id"]) != op
                        or _texto(registro["momento"]) != momento):
                    continue
                codigo = _texto(registro.get("reactivo"))
                valor = _entero(registro.get("valor"))
                if valor is None or not 1 <= valor <= 5:
                    pendientes[clave].append(f"{codigo} sin valor 1 a 5")
                    continue
                respuestas[codigo] = valor
            faltan = [c for c in REACTIVOS if c not in respuestas]

            ap = sum(respuestas.get(c, 0) for c in REACTIVOS[:4])
            up = sum(respuestas.get(c, 0) for c in REACTIVOS[4:])
            tam = ap + up

            filas.append({
                "sujeto_id": op,
                "centro_acopio": centro,
                "t_reg": (round(sum(tiempos["T_reg"])
                                / len(tiempos["T_reg"]), 2)
                          if tiempos["T_reg"] else ""),
                "t_vale": (round(sum(tiempos["T_vale"])
                                 / len(tiempos["T_vale"]), 2)
                           if tiempos["T_vale"] else ""),
                "rsd": (round(len(conformes) / ASIENTOS_POR_SESION * 100, 2)
                        if len(docs) >= ASIENTOS_POR_SESION else ""),
                "cpe": (round(len(concordantes) / DESPACHOS_POR_SESION * 100, 2)
                        if len(desp) >= DESPACHOS_POR_SESION else ""),
                "ap_01": respuestas.get("AP-01", ""),
                "ap_02": respuestas.get("AP-02", ""),
                "ap_03": respuestas.get("AP-03", ""),
                "ap_04": respuestas.get("AP-04", ""),
                "up_01": respuestas.get("UP-01", ""),
                "up_02": respuestas.get("UP-02", ""),
                "up_03": respuestas.get("UP-03", ""),
                "up_04": respuestas.get("UP-04", ""),
                "score_ap": ap if not faltan else "",
                "score_up": up if not faltan else "",
                "score_tam_total": tam if not faltan else "",
                "nivel_satisfaccion": G.baremo(tam) if not faltan else "",
                "_momento": momento,
            })

    return {"filas": filas, "pendientes": pendientes, "avisos": avisos}


# --------------------------------------------------------------------------
# Informe y escritura
# --------------------------------------------------------------------------

def informe(resultado: dict) -> int:
    pendientes = resultado["pendientes"]
    avisos = resultado["avisos"]
    completas = [k for k, v in pendientes.items() if not v]
    incompletas = {k: v for k, v in pendientes.items() if v}

    print(f"Sesiones completas: {len(completas)} de {len(pendientes)}")
    for (op, momento), faltas in incompletas.items():
        print(f"  · {op} {momento}: " + "; ".join(faltas))
    if avisos:
        print(f"\nAvisos de aritmética o de conformidad ({len(avisos)}):")
        for aviso in avisos[:40]:
            print("  · " + aviso)
        if len(avisos) > 40:
            print(f"  … y {len(avisos) - 40} más")
    return len(incompletas)


def escribir(resultado: dict, borrador: bool = False) -> list[Path]:
    destinos = []
    sufijo = "_borrador" if borrador else ""
    for momento, nombre in (("Pretest", "pretest_campo"),
                            ("Postest", "posttest_campo")):
        destino = RECO / f"{nombre}{sufijo}.csv"
        with destino.open("w", encoding="utf-8", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=COLUMNAS,
                                      lineterminator="\n")
            escritor.writeheader()
            for fila in resultado["filas"]:
                if fila["_momento"] == momento:
                    escritor.writerow({c: fila[c] for c in COLUMNAS})
        destinos.append(destino)
    return destinos


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Consolida el libro de captura v22 en los CSV de campo.")
    parser.add_argument("libro", nargs="?", default=str(LIBRO),
                        help="ruta del LIBRO_DE_CAPTURA_v22.xlsx")
    parser.add_argument("--escribir", action="store_true",
                        help="escribe los CSV; sin esta bandera solo audita")
    parser.add_argument("--borrador", action="store_true",
                        help="escribe aunque falten registros, con sufijo _borrador")
    opciones = parser.parse_args(argv)

    libro = Path(opciones.libro)
    if not libro.exists():
        raise SystemExit(f"No existe el libro: {libro}")

    resultado = consolidar(libro)
    incompletas = informe(resultado)

    if not opciones.escribir:
        print("\nModo auditoría: no se escribió ningún archivo. "
              "Añada --escribir para consolidar.")
        return 0
    if incompletas and not opciones.borrador:
        print("\nNo se escribe: hay sesiones incompletas. Corrija el libro o "
              "use --borrador para un ensayo.")
        return 2

    for destino in escribir(resultado, borrador=opciones.borrador):
        print(f"Consolidado: {destino}")
    if opciones.borrador:
        print("Borrador: no reemplaza los CSV definitivos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
