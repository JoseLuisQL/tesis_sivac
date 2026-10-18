# GENERADORES RETIRADOS DE LA RUTA OFICIAL

Cuarentena, no destrucción. Los tres programas de la tabla están retirados de la ruta oficial y
deben trasladarse a esta carpeta con `python scripts/utilidades/cuarentenar_generadores_apocrifos.py`.
No deben ejecutarse ni citarse como fuente de resultados; se conservan íntegros para trazabilidad.

| Archivo | Qué emitía | Decisión que lo retira |
|---|---|---|
| `generar_expedientes_e_instrumentos.py` | Expediente de validación con coeficientes prefabricados para 32 ítems (V = 0.98 y 0.97; IVC = 1.00; "Excelente (>=0.90)"; "VÁLIDO"; "APROBADO"). Sus fichas declaraban una arquitectura Laravel/MySQL, ya sustituida por el stack real. | **DEC-014**: los coeficientes atribuidos a jueces que no evaluaron son aritméticamente inalcanzables y quedan prohibidos como resultado. |
| `generar_matriz_ivc_excel.py` | Libro Excel de IVC con un diccionario de calificaciones precargadas presentado como "asignadas por los jueces expertos reales". | **DEC-014**: ninguna calificación puede existir antes de que un juez real firme el certificado. |
| `generar_formatos_validacion.py` | Formatos de validación del modelo Cóndor Tinoco: cinco criterios, escala ordinal de 1 a 4 y 32 ítems. | **DEC-015**: el modelo vigente es el Anexo 2 de Fany 2024, con criterios dicotómicos Sí/No de Pertinencia, Relevancia y Claridad. |

Generador vigente: `scripts/compiladores/generar_anexo2_validacion_fany.py`. Su único modo de
escritura es `--generar`; sin argumentos no escribe nada y `--verificar` solo audita la
estructura en memoria. Emite un certificado en blanco del Instrumento N.° 03 (DEC-016, DEC-019,
DEC-020), que los jueces reales llenan a mano.

Los coeficientes solo se calculan después, con `scripts/agentes/validez_contenido.py`, sobre las
actas realmente suscritas.
