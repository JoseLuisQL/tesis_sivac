# -*- coding: utf-8 -*-
"""
Generador del Certificado Único de Validación por Juicio de Expertos (Modelo Fany 2024 - DEC-015).
Produce salidas/documentos/anexos_fany/ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx (.pdf)
y los 3 certificados individuales de expertos en salidas/instrumentos/formatos_validacion/
totalmente en blanco conforme a DEC-016, DEC-019 y DEC-020.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts.comun import rutas, seguridad
from scripts.utilidades.docx_quirurgico import construir_docx_openxml, construir_pdf_nativo

REACTIVOS_MODALIDAD_A = [
    ("AP-01", "Agilidad percibida (AP)", "El procedimiento actual para asentar los movimientos diarios y cierres de mes es ágil y no demanda un esfuerzo mental o físico excesivo."),
    ("AP-02", "Agilidad percibida (AP)", "El flujo de trabajo requerido para emitir comprobantes de salida y vales de entrega es fluido y está libre de demoras o trabas burocráticas."),
    ("AP-03", "Agilidad percibida (AP)", "El método empleado me permite conciliar los saldos de inventario con las microredes generando tranquilidad y reduciendo el estrés laboral."),
    ("AP-04", "Agilidad percibida (AP)", "El tiempo que dedico al registro administrativo de vacunas es equilibrado y me deja disponibilidad para mis labores sanitarias y asistenciales."),
    ("UP-01", "Utilidad percibida (UP)", "El mecanismo de registro utilizado me permite disponer de información fidedigna y en tiempo real del stock de vacunas y jeringas."),
    ("UP-02", "Utilidad percibida (UP)", "El control de números de lote y fechas de vencimiento que brinda el proceso previene oportunamente mermas o pérdidas de biológicos."),
    ("UP-03", "Utilidad percibida (UP)", "La metodología de gestión facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico versus registrado."),
    ("UP-04", "Utilidad percibida (UP)", "En general, considero que el procedimiento empleado es una herramienta altamente eficaz para garantizar el abastecimiento oportuno de vacunas."),
]

REACTIVOS_MODALIDAD_B = [
    ("AP-01", "Agilidad percibida (AP)", "El sistema web SIVAC permite asentar los movimientos diarios y cierres de mes de manera ágil y sin demandar un esfuerzo mental o físico excesivo."),
    ("AP-02", "Agilidad percibida (AP)", "El flujo automatizado del sistema web SIVAC para emitir comprobantes de salida y vales de entrega es fluido y elimina las trabas burocráticas."),
    ("AP-03", "Agilidad percibida (AP)", "El sistema web SIVAC me permite conciliar los saldos de inventario con las microredes generando tranquilidad y reduciendo el estrés laboral."),
    ("AP-04", "Agilidad percibida (AP)", "El tiempo que dedico al registro administrativo en el sistema web SIVAC es equilibrado y amplía mi disponibilidad para labores sanitarias."),
    ("UP-01", "Utilidad percibida (UP)", "El sistema web SIVAC me permite disponer de información fidedigna y en tiempo real del stock de vacunas y jeringas."),
    ("UP-02", "Utilidad percibida (UP)", "El control automatizado de lotes y alertas FEFO de vencimiento en el sistema web SIVAC previene oportunamente mermas o pérdidas de biológicos."),
    ("UP-03", "Utilidad percibida (UP)", "El sistema web SIVAC facilita la detección inmediata y rectificación de cualquier descuadre de inventario físico versus registrado."),
    ("UP-04", "Utilidad percibida (UP)", "En general, considero que el sistema web SIVAC es una herramienta altamente eficaz para garantizar el abastecimiento oportuno de vacunas."),
]


def _bloques_certificado_fany(etiqueta_juez: str = "Experto Validador (En Blanco — DEC-016)") -> list:
    filas_matriz = [
        [cod, ind, enunciado, "[  ] Sí   [  ] No", "[  ] Sí   [  ] No", "[  ] Sí   [  ] No", ""]
        for cod, ind, enunciado in REACTIVOS_MODALIDAD_A
    ]
    return [
        {
            "tipo": "titulo_portada",
            "lineas": [
                {"texto": "UNIVERSIDAD NACIONAL JOSÉ MARÍA ARGUEDAS", "negrita": True, "pt": 14},
                {"texto": "FACULTAD DE INGENIERÍA — ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS", "negrita": True, "pt": 11},
                {"texto": "CERTIFICADO ÚNICO DE VALIDEZ DE CONTENIDO POR JUICIO DE EXPERTOS (MODELO FANY 2024)", "negrita": True, "pt": 12},
            ],
        },
        {"tipo": "h2", "texto": "I. DATOS GENERALES DEL PROYECTO E INSTRUMENTO"},
        {
            "tipo": "parrafo",
            "sangria_primera_linea": False,
            "texto": f"Título de la Tesis: {rutas.TITULO_OFICIAL}. Tesista: {rutas.TESISTA}. Asesora: {rutas.ASESORA}.",
        },
        {
            "tipo": "parrafo",
            "sangria_primera_linea": False,
            "texto": (
                f"Instrumento Evaluado: Instrumento N.° 03 — Cuestionario de Satisfacción del Usuario sobre el Proceso de "
                f"Gestión de Movimientos Mensuales de Vacunas (Escala Likert 1–5, 8 reactivos, Dimensión 3 DEC-007). "
                f"Validador: {etiqueta_juez}."
            ),
        },
        {
            "tipo": "tabla_apa7",
            "numero": "Tabla 1",
            "titulo": "Matriz de Evaluación por Juicio de Expertos según Criterios Dicotómicos del Modelo Fany 2024 (DEC-015 / DEC-020)",
            "encabezados": ["Ítem", "Indicador", "Reactivo (Modalidad A — Pretest / Análogo Modalidad B)", "Pertinencia", "Relevancia", "Claridad", "Observaciones"],
            "filas": filas_matriz,
            "nota": "Formato emitido 100% en blanco para llenado de puño y letra o firma digital del juez experto conforme a DEC-016.",
        },
        {"tipo": "h2", "texto": "II. OPINIÓN DE APLICABILIDAD Y FIRMA DEL EXPERTO (EN BLANCO — DEC-016)"},
        {
            "tipo": "parrafo",
            "sangria_primera_linea": False,
            "texto": "Opinión de aplicabilidad:   [   ] Aplicable       [   ] Aplicable después de corregir       [   ] No aplicable",
        },
        {
            "tipo": "parrafo",
            "sangria_primera_linea": False,
            "texto": "Apellidos y Nombres del Juez Experto: ____________________________________________________________________",
        },
        {
            "tipo": "parrafo",
            "sangria_primera_linea": False,
            "texto": "DNI: ______________________   Grado Académico: ___________________________   CIP/COP/CMP: ________________",
        },
        {
            "tipo": "parrafo",
            "sangria_primera_linea": False,
            "texto": "Fecha: ____ / ____ / 2026      Firma y Sello del Experto: ________________________________________________",
        },
    ]


def generar_todos_formatos_fany() -> dict:
    destino_anexo2_docx = (
        rutas.SALIDAS_DOCUMENTOS
        / "anexos_fany"
        / "ANEXO_2_VALIDACION_FANY_INST03_MODALIDAD_A_VACIO.docx"
    )
    destino_anexo2_pdf = destino_anexo2_docx.with_suffix(".pdf")
    bloques = _bloques_certificado_fany("Certificado Único Consolidado (3 Jueces Expertos — En Blanco)")
    construir_docx_openxml(destino_anexo2_docx, "Anexo 2 — Certificado Único de Validación Fany 2024", bloques)

    lineas_pdf = [
        [
            "ANEXO 2: CERTIFICADO UNICO DE VALIDACION POR JUICIO DE EXPERTOS (MODELO FANY 2024)",
            f"Tesis: {rutas.TITULO_OFICIAL}",
            f"Tesista: {rutas.TESISTA} | Asesora: {rutas.ASESORA}",
            "Instrumento Evaluado: Instrumento 03 - Cuestionario TAM (Dim. 3: Satisfaccion del Usuario)",
            "Normativa: DEC-007 (3 Dimensiones), DEC-015 (Fany 2024), DEC-016 (En Blanco), DEC-020 (Exencion Inst 01 y 02)",
            "",
            "MATRIZ DE VALIDACION DICOTOMICA (PERTINENCIA / RELEVANCIA / CLARIDAD):",
        ]
        + [f"  {cod} ({ind}): {enun} -> Pert:[ ] Rel:[ ] Clar:[ ]" for cod, ind, enun in REACTIVOS_MODALIDAD_A]
        + [
            "",
            "DICTAMEN DE APLICABILIDAD (EN BLANCO PARA EL EXPERTO):",
            "  [  ] Aplicable     [  ] Aplicable tras corregir     [  ] No aplicable",
            "  Nombre del Experto: ___________________________________ DNI: ___________________",
            "  Grado Academico: ______________________________________ Firma: _________________",
        ]
    ]
    construir_pdf_nativo(destino_anexo2_pdf, "Anexo 2 - Validacion Fany 2024", lineas_pdf)

    generados = [str(destino_anexo2_docx), str(destino_anexo2_pdf)]
    dir_val = rutas.SALIDAS_INSTRUMENTOS / "formatos_validacion"
    for num_juez in (1, 2, 3):
        p_docx = dir_val / f"CERTIFICADO_FANY_2024_JUEZ_0{num_juez}_VACIO.docx"
        p_pdf = dir_val / f"CERTIFICADO_FANY_2024_JUEZ_0{num_juez}_VACIO.pdf"
        construir_docx_openxml(
            p_docx,
            f"Certificado de Validación Fany 2024 — Juez Experto 0{num_juez} (En Blanco)",
            _bloques_certificado_fany(f"Juez Experto 0{num_juez} (En Blanco — DEC-016)"),
        )
        construir_pdf_nativo(p_pdf, f"Certificado Fany 2024 - Juez 0{num_juez}", lineas_pdf)
        generados.extend([str(p_docx), str(p_pdf)])

    return {"estado": "completado", "archivos_generados": generados}


def main() -> int:
    seguridad.configurar_utf8()
    res = generar_todos_formatos_fany()
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
