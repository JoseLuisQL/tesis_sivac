# Paquete de instrumentos definitivos v06

**Tesis:** Aplicación del sistema SIVAC para mejorar la gestión de movimientos mensuales de vacunas en el personal de inmunizaciones de la Dirección de Salud Apurímac II.

**Fecha de compilación:** 2026-11-03. **Estado:** borrador para revisión del tesista; no sustituye la aprobación del tesista.

## Contenido del paquete

| Carpeta | Contenido |
|---|---|
| `01_IMPRIMIBLES` | Los seis documentos en PDF, listos para impresión en A4. |
| `02_EDITABLES` | Los seis documentos en DOCX, con estilos nativos y geometría OpenXML. |
| `03_FUENTES` | Las seis fichas de especificación y el manifiesto técnico con las huellas SHA-256. |
| `04_CONTROL_VISUAL` | Una imagen PNG por página generada y, en `antes_v06`, las páginas de la versión anterior para comparar. |

## Índice de documentos

| Orden | Documento | Imprimible | Editable | Páginas |
|---|---|---|---|---|
| 00 | Guía de aplicación de los instrumentos | `01_IMPRIMIBLES/00_GUIA_DE_APLICACION_v06.pdf` | `02_EDITABLES/00_GUIA_DE_APLICACION_v06.docx` | 1 |
| 01 | Ficha de tiempos | `01_IMPRIMIBLES/01_FICHA_TIEMPOS_v06.pdf` | `02_EDITABLES/01_FICHA_TIEMPOS_v06.docx` | 1 |
| 02 | Ficha documental | `01_IMPRIMIBLES/02_FICHA_DOCUMENTAL_v06.pdf` | `02_EDITABLES/02_FICHA_DOCUMENTAL_v06.docx` | 3 |
| 03 | Cuestionario de satisfacción del usuario | `01_IMPRIMIBLES/03_CUESTIONARIO_SATISFACCION_v06.pdf` | `02_EDITABLES/03_CUESTIONARIO_SATISFACCION_v06.docx` | 1 |
| 04 | Consentimiento informado | `01_IMPRIMIBLES/04_CONSENTIMIENTO_INFORMADO_v06.pdf` | `02_EDITABLES/04_CONSENTIMIENTO_INFORMADO_v06.docx` | 1 |
| 05 | Certificado de validación de contenido | `01_IMPRIMIBLES/05_CERTIFICADO_VALIDACION_v06.pdf` | `02_EDITABLES/05_CERTIFICADO_VALIDACION_v06.docx` | 2 |

## Secuencia de aplicación en campo

1. **Antes del trabajo de campo:** los tres jueces firman el certificado de validación (05). Un ejemplar por juez; no se entrega a los participantes.
2. **Antes de la primera medición:** cada participante firma el consentimiento informado (04) por duplicado.
3. **Pretest:** se aplican la ficha de tiempos (01), la ficha documental (02) y el cuestionario (03), en ese orden.
4. **Intervención:** operación del sistema SIVAC. No se usa ningún formulario.
5. **Postest:** se aplican 01, 02 y 03 en el mismo orden del pretest.

## Qué se imprime

| Documento | Copias |
|---|---|
| 01. Ficha de tiempos | Una hoja por participante y por momento (pretest y postest). |
| 02. Ficha documental | Una hoja por participante y por momento, sobre los documentos del periodo revisado. |
| 03. Cuestionario | Una hoja por participante y por momento. |
| 04. Consentimiento | Dos ejemplares por participante, firmados una sola vez antes de la primera medición. |
| 05. Certificado | Un ejemplar por juez validador, de un solo uso, firmado antes del trabajo de campo. |
| 00. Guía | Un ejemplar para el investigador. |

## Reglas de impresión

A4 vertical, sin escala. Márgenes: izquierdo 3.0 cm, superior 3.0 cm, derecho e inferior 2.5 cm. Times New Roman 10 pt en el cuerpo y 9.5 pt en las tablas. Las tablas de captura llevan contorno y separadores horizontales, con línea vertical solo en las columnas que se marcan: los ocho criterios y Conf. en la ficha documental, Prog./Entr./Dif./Conforme en los despachos, la escala 1 a 5 del cuestionario y los Sí/No de la matriz de validación. Los campos de texto quedan abiertos para escribir de corrido. El encabezado va sombreado en gris claro y, en los listados de 20, 25 o 40 renglones, la columna de numeración va sombreada como carril de lectura. No se imprime ninguna nota de producción.

## Reproducibilidad

El paquete se regenera con:

```
python scripts/compiladores/instrumentos_recoleccion_v06_builder.py
python scripts/compiladores/concordancia_v06_builder.py
python scripts/compiladores/verificar_instrumentos_v06.py
```

Dos corridas seguidas producen archivos idénticos byte a byte: el DOCX se reescribe con fechas de entrada fijas en el ZIP, el PDF se normaliza (fecha fija e identificador derivado del contenido) y el manifiesto usa `SOURCE_DATE_EPOCH` o, en su defecto, el instante cero de la fecha de la versión.
