# -*- coding: utf-8 -*-
"""
Constructor Quirúrgico OpenXML de Anexos 3 y 4 para el Informe Final de Tesis SIVAC (UNAJMA).
Lee y procesa salidas/documentos/anexos_instrumentos_validacion.json generando los bloques nativos
compatibles con scripts.utilidades.docx_quirurgico.construir_docx_openxml.

Anexo 3: Certificados de Validación por Juicio de Expertos (Modelo Fany 2024 / DEC-015 / DEC-020).
Anexo 4: Instrumentos de Recolección de Datos (Ficha Tiempos, Ficha Cotejo, Cuestionario TAM).
"""
import json
from pathlib import Path
from typing import Any, Dict, List

RAIZ = Path(__file__).resolve().parents[2]
RUTA_JSON = RAIZ / "salidas" / "documentos" / "anexos_instrumentos_validacion.json"


def cargar_datos_anexos() -> Dict[str, Any]:
    """Carga los datos estructurados desde el JSON canónico."""
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def generar_bloques_anexo_3(datos: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Genera los bloques OpenXML correspondientes al Anexo 3: Juicio de Expertos."""
    if datos is None:
        datos = cargar_datos_anexos()

    anexo3 = datos["anexo_3_validacion_juicio_expertos"]
    meta = datos["metadata"]
    bloques: List[Dict[str, Any]] = []

    # Título principal del Anexo 3
    bloques.append({"tipo": "h1", "texto": anexo3["identificador"] + ": " + anexo3["titulo"]})
    bloques.append({
        "tipo": "parrafo",
        "alineacion": "both",
        "sangria_primera_linea": True,
        "texto": (
            f"El presente anexo contiene los certificados individuales de validación de contenido emitidos bajo el "
            f"modelo institucional de la Universidad Nacional José María Arguedas (UNAJMA), correspondiente a la tesis "
            f"titulada “{meta['titulo_oficial_tesis']}”, presentada por el {meta['tesista']} bajo la asesoría de la "
            f"{meta['asesora']}. Conforme a las decisiones metodológicas DEC-007, DEC-015, DEC-016 y DEC-020, se sometió "
            f"a evaluación pericial el conjunto de elementos estructurados que componen la medición de la Variable Dependiente "
            f"(Gestión de movimientos mensuales de vacunas) en sus tres dimensiones: Oportunidad de procesamiento, Consistencia "
            f"documental y Satisfacción del usuario."
        )
    })
    bloques.append({
        "tipo": "parrafo",
        "alineacion": "both",
        "sangria_primera_linea": True,
        "texto": (
            "La validación fue conducida mediante un panel multidisciplinario conformado por tres (3) jueces expertos independientes "
            "con grado de Magíster: un especialista en Ingeniería de Sistemas y Software (Experto 1), una especialista en Salud Pública, "
            "Inmunizaciones y Cadena de Frío (Experto 2), y un especialista en Gestión Pública, Bioestadística y Metodología (Experto 3). "
            "Cada experto evaluó los doce (12) elementos operacionales en los criterios dicotómicos de Pertinencia, Relevancia y Claridad, "
            "consignando su opinión global sobre la aplicabilidad y suficiencia de los instrumentos para la contrastación de las hipótesis."
        )
    })

    # Detalle de cada uno de los 3 expertos
    for exp in anexo3["certificados_individuales"]:
        perfil = exp["perfil_profesional"]
        ident = exp["campos_identificacion"]
        decl = exp["declaracion_aplicabilidad"]
        firma = exp["placeholders_firma_y_sello"]

        bloques.append({"tipo": "h2", "texto": f"Certificado N.° 0{exp['numero']}: Validación por Juicio de Expertos — {perfil['titulo_academico']}"})
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "negrita": True,
            "texto": f"I. DATOS DEL JUEZ VALIDADOR (EXPERTO {exp['numero']}):"
        })
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "texto": (
                f"• Apellidos y Nombres: {ident['apellidos_y_nombres']}\n"
                f"• Documento Nacional de Identidad (DNI): {ident['dni']}\n"
                f"• Grado Académico y Título: {ident['grado_y_titulo']}\n"
                f"• Especialidad Profesional: {perfil['especialidad']}\n"
                f"• Rol Pericial: {perfil['rol_pericial']}\n"
                f"• Institución Laboral / Adscripción: {ident['institucion_laboral']}\n"
                f"• Registro de Colegio Profesional: {ident['registro_profesional']}\n"
                f"• Fecha de Evaluación Pericial: {ident['fecha_evaluacion']}"
            )
        })

        # Tabla de los 12 ítems evaluados
        filas_eval = []
        for it in anexo3["inventario_12_items_evaluados"]:
            filas_eval.append([
                str(it["item_numero"]),
                it["instrumento"],
                it["indicador_codigo"],
                it["elemento_evaluado"],
                "[ ] Sí  [ ] No",
                "[ ] Sí  [ ] No",
                "[ ] Sí  [ ] No",
                ""
            ])

        bloques.append({
            "tipo": "tabla_apa7",
            "numero": f"Tabla 3.{exp['numero']}",
            "titulo": f"Matriz Pericial de Evaluación de Ítems según Criterios Dicotómicos UNAJMA — Experto {exp['numero']}",
            "encabezados": ["N.°", "Instrumento", "Indicador", "Elemento Operacional Evaluado", "Pertinencia", "Relevancia", "Claridad", "Sugerencias"],
            "filas": filas_eval,
            "ancho_total_dxa": 8788,
            "nota": "Formato institucional Fany 2024 emitido en blanco conforme a DEC-016. Notas al pie: (1) Pertinencia: El ítem corresponde al concepto teórico. (2) Relevancia: El ítem representa adecuadamente la dimensión. (3) Claridad: El enunciado es conciso, exacto y comprensible."
        })

        # Cuadro de Calificación Cuantitativa
        cuadro_cuant = exp["cuadro_calificacion_cuantitativa"]
        filas_cuant = []
        for fc in cuadro_cuant["filas"]:
            filas_cuant.append([
                fc["dimension"],
                fc["items"],
                fc["pertinencia"],
                fc["relevancia"],
                fc["claridad"],
                fc.get("v_aiken", fc.get("v_aiken_global", "[ EN BLANCO ]")),
                fc["veredicto"]
            ])

        bloques.append({
            "tipo": "tabla_apa7",
            "numero": f"Tabla 3.{exp['numero']}B",
            "titulo": f"Cuadro de Calificación Cuantitativa (V de Aiken e IVC) — Experto {exp['numero']}",
            "encabezados": cuadro_cuant["columnas"],
            "filas": filas_cuant,
            "ancho_total_dxa": 8788,
            "nota": "Coeficiente V de Aiken calculado mediante V = S / n para escala dicotómica (Aiken, 1985). Umbral mínimo de validez: V >= 0.80 e IVC >= 0.80."
        })

        # Declaración de aplicabilidad y placeholders de firma
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "negrita": True,
            "texto": "II. OPINIÓN DE APLICABILIDAD Y SUFICIENCIA DEL INSTRUMENTO:"
        })
        opciones_txt = "\n".join(f"   {op}" for op in decl["opinion_global_instrumentos"])
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "texto": f"1. Opinión global sobre el conjunto de instrumentos:\n{opciones_txt}"
        })
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "texto": f"2. {decl['suficiencia_elementos']}"
        })
        obs_txt = "\n".join(decl["observaciones_y_recomendaciones"])
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "texto": f"3. Observaciones y recomendaciones generales:\n{obs_txt}"
        })
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "center",
            "sangria_primera_linea": False,
            "texto": (
                f"\n\n{firma['linea_firma']}\n"
                f"{firma['texto_firma']}\n"
                f"{firma['linea_post_firma']}\n"
                f"{firma['placeholder_sello']}\n"
            )
        })

    return bloques


def generar_bloques_anexo_4(datos: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Genera los bloques OpenXML correspondientes al Anexo 4: Instrumentos de Recolección."""
    if datos is None:
        datos = cargar_datos_anexos()

    anexo4 = datos["anexo_4_instrumentos_recoleccion_datos"]
    bloques: List[Dict[str, Any]] = []

    # Título principal del Anexo 4
    bloques.append({"tipo": "h1", "texto": anexo4["identificador"] + ": " + anexo4["titulo"]})
    bloques.append({
        "tipo": "parrafo",
        "alineacion": "both",
        "sangria_primera_linea": True,
        "texto": (
            "El presente anexo documenta en su totalidad los tres (3) instrumentos oficiales e inmutables de recolección de datos "
            "empleados en la investigación para la contrastación empírica en pretest (O1) y postest (O2). Cada instrumento responde "
            "estrictamente a una de las tres dimensiones fijadas por la decisión institucional DEC-007: Oportunidad de procesamiento "
            "(Instrumento 01), Consistencia documental (Instrumento 02) y Satisfacción del usuario (Instrumento 03). Los instrumentos "
            "incorporan sus respectivos protocolos estandarizados de medición, reglas de agregación intrasujeto anti-pseudorreplicación, "
            "criterios de conformidad y baremos psicométricos."
        )
    })

    for inst in anexo4["instrumentos"]:
        bloques.append({"tipo": "h2", "texto": f"{inst['codigo']}: {inst['nombre']}"})
        bloques.append({
            "tipo": "parrafo",
            "alineacion": "both",
            "sangria_primera_linea": False,
            "texto": (
                f"• Variable Dependiente: {inst['variable_dependiente']}\n"
                f"• Dimensión Evaluada: {inst['dimension']}\n"
                f"• Técnica de Recolección: {inst['tecnica']}\n"
                f"• Población Objetivo: {inst['poblacion_objetivo']}"
            )
        })

        secs = inst["secciones"]

        # INSTRUMENTO 01
        if inst["instrumento_id"] == "INST-01":
            # Protocolo
            proto = secs["seccion_2_protocolo_pmmv"]
            bloques.append({"tipo": "h3", "texto": proto["titulo"]})
            for r in proto["reglas"]:
                bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": f"• {r}"})

            # Tabla Treg
            treg = secs["seccion_3_tabla_treg"]
            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.1A", "titulo": treg["titulo"], "encabezados": treg["encabezados"], "filas": treg["filas"], "ancho_total_dxa": 8788, "nota": f"Fórmula: {treg['formula']}. {treg['consolidados']['mediana_intrasujeto_principal']} | {treg['consolidados']['promedio_descriptivo']}."})

            # Tabla Tvale
            tvale = secs["seccion_4_tabla_tvale"]
            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.1B", "titulo": tvale["titulo"], "encabezados": tvale["encabezados"], "filas": tvale["filas"], "ancho_total_dxa": 8788, "nota": f"Fórmula: {tvale['formula']}. {tvale['consolidados']['mediana_intrasujeto_principal']} | {tvale['consolidados']['promedio_descriptivo']}."})

            # Declaración y firmas
            dec = secs["seccion_5_declaracion_y_firmas"]
            bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": f"{dec['declaracion']}\n\n{dec['firma_evaluador']}\n{dec['firma_operador']}"})

        # INSTRUMENTO 02
        elif inst["instrumento_id"] == "INST-02":
            # 8 Criterios
            crit_sec = secs["seccion_2_regla_8_criterios_rsd"]
            bloques.append({"tipo": "h3", "texto": crit_sec["titulo"]})
            bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": crit_sec["descripcion"]})
            for c in crit_sec["criterios"]:
                bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": f"  - {c}"})

            # Matriz RSD
            rsd = secs["seccion_3_matriz_rsd"]
            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.2A", "titulo": rsd["titulo"], "encabezados": rsd["encabezados"], "filas": rsd["filas_muestra"], "ancho_total_dxa": 8788, "nota": f"Fórmula: {rsd['formula']}. {rsd['consolidado_rsd']['porcentaje_rsd_operador']}."})

            # Matriz CPE
            cpe = secs["seccion_4_matriz_cpe"]
            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.2B", "titulo": cpe["titulo"], "encabezados": cpe["encabezados"], "filas": cpe["filas_muestra"], "ancho_total_dxa": 8788, "nota": f"Fórmula: {cpe['formula']}. Regla: {cpe['regla_concordancia']}. {cpe['consolidado_cpe']['porcentaje_cpe_operador']}."})

            # Declaración y firmas
            dec = secs["seccion_5_declaracion_y_firmas"]
            bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": f"{dec['declaracion']}\n\n{dec['firma_auditor']}\n{dec['firma_responsable_acopio']}"})

        # INSTRUMENTO 03
        elif inst["instrumento_id"] == "INST-03":
            # Escala Likert
            instruc = secs["seccion_1_instrucciones_y_escala"]
            bloques.append({"tipo": "h3", "texto": instruc["titulo"]})
            bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": instruc["texto_instrucciones"]})
            filas_likert = [[str(niv["puntos"]), niv["etiqueta"], niv["descripcion"]] for niv in instruc["escala_likert_5_niveles"]]
            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.3A", "titulo": "Escala Likert de 5 Puntos y Criterios Operativos de Calificación", "encabezados": ["Puntos", "Categoría Verbal", "Significado Operativo en Cadena de Frío"], "filas": filas_likert, "ancho_total_dxa": 8788, "nota": "Escala psicométrica autoadministrada bajo código de anonimato (TRAB-01 a TRAB-14)." })

            # Modalidad A
            moda = secs["seccion_3_modalidad_a_tabla"]
            filas_moda = []
            for sub in moda["reactivos"]:
                for it in sub["items"]:
                    filas_moda.append([it["codigo"], it["enunciado"], "[ ]", "[ ]", "[ ]", "[ ]", "[ ]"])

            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.3B", "titulo": moda["titulo"], "encabezados": moda["encabezados"], "filas": filas_moda, "ancho_total_dxa": 8788, "nota": f"Modalidad A oficial para HE3 (8 reactivos, 8 a 40 puntos). {moda['calificacion_sumativa']['puntaje_global_modalidad_a']}."})

            # Baremo
            bare = secs["seccion_4_baremo_terciles"]
            filas_bare = [[b["nivel"], b["rango_global"], b["rango_subescala"], b["porcentaje"], b["interpretacion"]] for b in bare["tabla"]]
            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.3C", "titulo": bare["titulo"], "encabezados": ["Nivel de Satisfacción", "Rango Global (8 Ítems)", "Rango Subescala (4 Ítems)", "% Escalar", "Interpretación Psicométrica UNAJMA"], "filas": filas_bare, "ancho_total_dxa": 8788, "nota": "Baremo teórico por terciles simétricos normalizados de 11 unidades de amplitud (DEC-019)." })

            # Modalidad B
            modb = secs["seccion_5_modalidad_b_anexo"]
            filas_modb = []
            for sub in modb["reactivos"]:
                for it in sub["items"]:
                    filas_modb.append([it["codigo"], it["enunciado"], "[ ]", "[ ]", "[ ]", "[ ]", "[ ]"])

            bloques.append({"tipo": "tabla_apa7", "numero": "Tabla 4.3D", "titulo": modb["titulo"], "encabezados": modb["encabezados"], "filas": filas_modb, "ancho_total_dxa": 8788, "nota": "Módulo complementario postest según ISO/IEC 25010:2023. No se barema ni se suma a la variable dependiente."})

            # Declaración y firmas
            dec = secs["seccion_6_declaracion_y_firmas"]
            bloques.append({"tipo": "parrafo", "alineacion": "both", "sangria_primera_linea": False, "texto": f"{dec['declaracion']}\n\n{dec['firma_participante']}\n{dec['firma_encuestador']}"})

    return bloques


if __name__ == "__main__":
    datos = cargar_datos_anexos()
    b3 = generar_bloques_anexo_3(datos)
    b4 = generar_bloques_anexo_4(datos)
    print(f"[OK] Anexo 3 generado con {len(b3)} bloques OpenXML.")
    print(f"[OK] Anexo 4 generado con {len(b4)} bloques OpenXML.")
