# Instrumentos de recolección de datos (v22)

| Archivo | Contenido | Hojas |
| --- | --- | --- |
| 01_CARTA_AUTORIZACION | Carta de autorización institucional firmada y sellada | 2 |
| 03_INSTRUMENTO_01_TIEMPOS | Ficha de registro de tiempos: pausa, motivo, documento y lote separados, validez | 1 |
| 04_INSTRUMENTO_02_DOCUMENTAL | Auditoría del kardex (2 hojas, 20 asientos cada una, con tipo y observación) y conciliación de 25 despachos | 3 |
| 05_INSTRUMENTO_03_CUESTIONARIO | Cuestionario de aceptación y utilidad percibida, 8 reactivos Likert, con encuestador y observaciones | 1 |
| 06_HOJA_DE_OBSERVACIONES | Réplicas de reemplazo y anotaciones de la sesión | 1 |
| 00_PAQUETE_COMPLETO | Los cinco documentos en orden de uso | 8 |

Fuera de `01_IMPRIMIBLES`:

| Carpeta | Contenido |
| --- | --- |
| 02_EDITABLES | Los cuatro documentos en DOCX, para corregir la maqueta |
| 03_FUENTES | El compilador que genera el paquete |
| 04_CONTROL_VISUAL | Una imagen por página, para revisar la maqueta sin abrir el PDF |
| 05_GUIA | Guía de llenado y control de la sesión (9 páginas) |
| 07_CAPTURA | LIBRO_DE_CAPTURA_v22.xlsx: una fila por registro previsto, claves escritas y mediciones en blanco |

El libro de captura no se consolida a mano: `scripts/estadistica/
consolidar_libro_captura.py` lee sus cuatro hojas, recalcula la aritmética de
cada ficha y escribe `datos/recolectados/pretest_campo.csv` y
`posttest_campo.csv`. Sin `--escribir` solo audita y enumera lo que falta; con
`--escribir` exige las veintiocho sesiones completas.

La v21 no admitía el registro real: no tenía pausa ni motivo, unía documento y
lote en una celda, no declaraba el tipo de asiento, no tenía columna de validez
y no dejaba anotar la observación de cada fila. La v22 conserva la maqueta
aprobada (Times New Roman 12 pt, A4, márgenes 3 / 2,5 / 2,5 / 2,5 cm) y añade
esos campos.

Los conteos coinciden con la tesis y con la base de datos: seis operaciones
cronometradas (tres de registro y tres de emisión del vale), cuarenta asientos
de kardex por operador y momento (veinte por hoja), veinticinco despachos,
ocho criterios de conformidad y ocho reactivos AP/UP.

El paquete no incluye consentimiento informado: el permiso formal es la Carta
de Autorización, que la tesis reproduce en el Anexo 8.
