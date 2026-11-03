# -*- coding: utf-8 -*-
"""Verificación numérica del paquete de instrumentos v06.

Comprueba que los formularios v06, aplicados a los datos de campo, reproducen
exactamente las cifras publicadas en el informe:

* AP, UP y total con los ocho reactivos 1-4 (AP-01…AP-04) y 5-8 (UP-01…UP-04).
* Alfa de Cronbach global y por subescala.
* RSD con los ocho criterios y la regla conjuntiva.
* CPE con igualdad exacta (entregado = programado).

Fuentes:
    datos/recolectados/pretest_campo.csv
    datos/recolectados/posttest_campo.csv
    datos/recolectados/SIVAC_DATOS_CAMPO.md   (registro por bloque)

Uso:
    python scripts/compiladores/verificar_instrumentos_v06.py
    python scripts/compiladores/verificar_instrumentos_v06.py --json salida.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics as st
from pathlib import Path
from typing import Any, Dict, List

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "datos" / "recolectados"
PRETEST = DATOS / "pretest_campo.csv"
POSTEST = DATOS / "posttest_campo.csv"
REGISTRO = DATOS / "SIVAC_DATOS_CAMPO.md"

# Cifras publicadas en el informe final (Tablas 35 y siguientes).
PUBLICADO = {
    "pretest": {"ap": (8.07, 2.27), "up": (9.00, 1.88), "total": (17.07, 4.08),
                "alpha": 0.939, "alpha_ap": 0.877, "alpha_up": 0.874,
                "rsd": (63.57, 12.31), "cpe": (67.71, 11.26)},
    "postest": {"ap": (17.71, 1.64), "up": (18.50, 1.56),
                "total": (36.21, 3.09), "alpha": 0.915, "alpha_ap": 0.831,
                "alpha_up": 0.841, "rsd": (91.96, 4.72), "cpe": (88.57, 5.63)},
}


def _filas(ruta: Path) -> List[Dict[str, str]]:
    with ruta.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _alfa(items: List[List[int]]) -> float:
    k = len(items[0])
    var_items = sum(st.variance([it[j] for it in items]) for j in range(k))
    var_total = st.variance([sum(it) for it in items])
    return k / (k - 1) * (1 - var_items / var_total)


def _cuestionario(ruta: Path) -> Dict[str, Any]:
    """AP = ítems 1-4 del formulario; UP = ítems 5-8."""
    filas = _filas(ruta)
    items = [[int(f[f"ap_0{i}"]) for i in range(1, 5)] +
             [int(f[f"up_0{i}"]) for i in range(1, 5)] for f in filas]
    ap = [sum(it[:4]) for it in items]
    up = [sum(it[4:]) for it in items]
    total = [a + u for a, u in zip(ap, up)]
    return {
        "n": len(filas),
        "ap": (round(st.mean(ap), 2), round(st.stdev(ap), 2)),
        "up": (round(st.mean(up), 2), round(st.stdev(up), 2)),
        "total": (round(st.mean(total), 2), round(st.stdev(total), 2)),
        "alpha": round(_alfa(items), 3),
        "alpha_ap": round(_alfa([it[:4] for it in items]), 3),
        "alpha_up": round(_alfa([it[4:] for it in items]), 3),
        "rango_ap": (min(ap), max(ap)),
        "rango_up": (min(up), max(up)),
        "rango_total": (min(total), max(total)),
    }


def _tabla_bloque(texto: str) -> List[List[str]]:
    filas: List[List[str]] = []
    empezado = False
    for linea in texto.split("\n"):
        if linea.startswith("| :---:"):
            empezado = True
            continue
        if not empezado:
            continue
        if not linea.startswith("|"):
            break
        filas.append([c.strip() for c in linea.strip().strip("|").split("|")])
    return filas


def _documental() -> Dict[str, Any]:
    """RSD (ocho criterios, conjuntiva) y CPE (igualdad exacta) por bloque."""
    texto = REGISTRO.read_text(encoding="utf-8")
    seccion = texto[texto.find('<a id="parte-4">'):texto.find('<a id="parte-5">')]
    bloques = re.split(r"### Bloque ", seccion)[1:]
    acumulado = {"pretest": {"rsd": [], "cpe": []},
                 "postest": {"rsd": [], "cpe": []}}
    incidencias: List[str] = []
    for bloque in bloques:
        cabecera = bloque.split("\n")[0]
        fase = "pretest" if "Pretest" in cabecera else "postest"
        codigo = re.search(r"TRAB-\d+", cabecera)
        declarado_doc = re.search(
            r"Documentos auditados: (\d+) · Conformes: (\d+)", bloque)
        declarado_des = re.search(
            r"Entregas conciliadas: (\d+) · Concordantes: (\d+)", bloque)
        partes = bloque.split("**Entregas conciliadas")
        docs = _tabla_bloque(partes[0])
        despachos = _tabla_bloque(partes[1]) if len(partes) > 1 else []

        conformes_8 = sum(1 for r in docs if all(c == "S" for c in r[5:13]))
        conformes_col = sum(1 for r in docs if len(r) > 13 and r[13] == "S")
        if conformes_8 != conformes_col:
            incidencias.append(f"{codigo}: criterios y columna Conforme difieren")
        if conformes_8 != int(declarado_doc.group(2)):
            incidencias.append(f"{codigo}: conformes declarados no coinciden")
        if len(docs) != int(declarado_doc.group(1)):
            incidencias.append(f"{codigo}: asientos declarados no coinciden")

        exactos = sum(1 for r in despachos if r[4] == r[5])
        if exactos != int(declarado_des.group(2)):
            incidencias.append(
                f"{codigo}: concordantes declarados no coinciden con la "
                f"igualdad exacta")
        if len(despachos) != int(declarado_des.group(1)):
            incidencias.append(f"{codigo}: despachos declarados no coinciden")

        acumulado[fase]["rsd"].append(100 * conformes_8 / len(docs))
        acumulado[fase]["cpe"].append(100 * exactos / len(despachos))

    resumen = {fase: {
        "n": len(datos["rsd"]),
        "rsd": (round(st.mean(datos["rsd"]), 2),
                round(st.stdev(datos["rsd"]), 2)),
        "cpe": (round(st.mean(datos["cpe"]), 2),
                round(st.stdev(datos["cpe"]), 2)),
    } for fase, datos in acumulado.items()}
    return {"bloques": len(bloques), "resumen": resumen,
            "incidencias": incidencias}


def _comparar(obtenido: Any, esperado: Any, etiqueta: str,
              tolerancia: float = 0.011) -> Dict[str, Any]:
    if isinstance(esperado, tuple):
        ok = all(abs(o - e) <= tolerancia for o, e in zip(obtenido, esperado))
    else:
        ok = abs(obtenido - esperado) <= tolerancia
    return {"indicador": etiqueta, "obtenido": obtenido, "publicado": esperado,
            "concuerda": ok}


def verificar() -> Dict[str, Any]:
    documento = _documental()
    chequeos: List[Dict[str, Any]] = []
    salida: Dict[str, Any] = {"cuestionario": {}, "documental": documento,
                              "chequeos": chequeos}
    for fase, ruta in (("pretest", PRETEST), ("postest", POSTEST)):
        datos = _cuestionario(ruta)
        salida["cuestionario"][fase] = datos
        esperado = PUBLICADO[fase]
        for clave, etiqueta in (("ap", "AP (4 ítems)"),
                                ("up", "UP (4 ítems)"),
                                ("total", "Total (8 ítems)")):
            chequeos.append(_comparar(datos[clave], esperado[clave],
                                      f"{etiqueta} {fase}"))
        for clave, etiqueta in (("alpha", "Alfa total"),
                                ("alpha_ap", "Alfa AP"),
                                ("alpha_up", "Alfa UP")):
            chequeos.append(_comparar(datos[clave], esperado[clave],
                                      f"{etiqueta} {fase}", 0.0011))
        for clave, etiqueta in (("rsd", "RSD (8 criterios)"),
                                ("cpe", "CPE (exacto)")):
            chequeos.append(_comparar(documento["resumen"][fase][clave],
                                      esperado[clave], f"{etiqueta} {fase}"))
    salida["todo_concuerda"] = (all(c["concuerda"] for c in chequeos)
                                and not documento["incidencias"])
    return salida


def _imprimir(resultado: Dict[str, Any]) -> None:
    print("Cuestionario (8 reactivos, escala 1-5)")
    for fase, datos in resultado["cuestionario"].items():
        print(f"  {fase:8s} n={datos['n']}  AP {datos['ap'][0]:.2f}±"
              f"{datos['ap'][1]:.2f}  UP {datos['up'][0]:.2f}±"
              f"{datos['up'][1]:.2f}  Total {datos['total'][0]:.2f}±"
              f"{datos['total'][1]:.2f}  α {datos['alpha']:.3f} "
              f"(AP {datos['alpha_ap']:.3f} / UP {datos['alpha_up']:.3f})")
    print("Ficha documental (bloques de campo)")
    for fase, datos in resultado["documental"]["resumen"].items():
        print(f"  {fase:8s} n={datos['n']}  RSD {datos['rsd'][0]:.2f}±"
              f"{datos['rsd'][1]:.2f}  CPE {datos['cpe'][0]:.2f}±"
              f"{datos['cpe'][1]:.2f}")
    print(f"Bloques revisados: {resultado['documental']['bloques']}")
    fallos = [c for c in resultado["chequeos"] if not c["concuerda"]]
    print(f"Chequeos: {len(resultado['chequeos'])} · fallos: {len(fallos)}")
    for fallo in fallos:
        print(f"  FALLO {fallo['indicador']}: obtenido {fallo['obtenido']} "
              f"≠ publicado {fallo['publicado']}")
    for incidencia in resultado["documental"]["incidencias"]:
        print(f"  INCIDENCIA {incidencia}")
    print("RESULTADO:", "TODO CONCUERDA" if resultado["todo_concuerda"]
          else "HAY DIFERENCIAS")


def main() -> int:
    analizador = argparse.ArgumentParser(
        description="Verifica que los instrumentos v06 reproducen las cifras "
                    "publicadas.")
    analizador.add_argument("--json", default=None,
                            help="ruta del JSON de resultados")
    argumentos = analizador.parse_args()
    resultado = verificar()
    _imprimir(resultado)
    if argumentos.json:
        Path(argumentos.json).write_text(
            json.dumps(resultado, ensure_ascii=False, indent=2),
            encoding="utf-8")
        print(f"[v06] resultados: {argumentos.json}")
    return 0 if resultado["todo_concuerda"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
