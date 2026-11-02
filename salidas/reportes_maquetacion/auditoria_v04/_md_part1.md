# Auditoría hoja por hoja del Informe Final v04

**Documento auditado:** `salidas/documentos/informe_final_v04.docx` y su render `informe_final_v04.pdf`  
**Agente:** analista-documental (Squad A y E)  
**Fase:** F8_INTEGRACION_EDITORIAL  
**Fecha:** 2026-10-21  
**Referencia de contraste:** Fany_Tesis_Bachiller_2024.pdf (106 páginas)

---

## 1. Identificación y huella del documento

| Atributo | Valor |
|---|---|
| SHA-256 del DOCX | `134c0ecad628432356f121662adb7b41462d4e32117074a111a9fe0398094887` |
| Tamaño | 15229744 bytes (14.52 MB) |
| Páginas del PDF | 158 |
| Párrafos de nivel superior | 810 |
| Tablas | 59 |
| Imágenes en línea | 49 |
| Ecuaciones OMML | 12 |
| Tablas flotantes (w:tblpPr) | 0 |
| Filas con cantSplit | 462 |
| Filas con tblHeader | 54 |
| Secciones | 5 (la 3.ª horizontal) |
| Páginas horizontales | 143, 144 y 145 |

## 2. Método

Se renderizaron las 158 páginas del PDF a 110 DPI con PyMuPDF (`salidas/reportes_maquetacion/auditoria_v04/p001.png` a `p158.png`), se inspeccionó cada página y se cruzó el resultado visual con el paquete OpenXML (`document.xml`, `styles.xml`, `numbering.xml`). La geometría se midió sobre la rejilla real de cada tabla (`w:tblGrid/w:gridCol`) y sobre las cajas de dibujo del PDF, comparándolas con la caja útil impresa:

- Márgenes declarados: izquierdo 1 701 dxa (3.0 cm), derecho, superior e inferior 1 440 dxa (2.54 cm).
- Caja útil vertical: 11 906 - 1 701 - 1 440 = **8 765 dxa** (15.46 cm).
- Caja útil horizontal: 16 838 - 1 701 - 1 440 = **13 697 dxa** (24.16 cm).
- En el PDF: límite izquierdo x = 85.05 pt, límite derecho x = 523.3 pt (vertical) y x = 769.92 pt (horizontal).

Esquema de folios contrastado: páginas 1-3 sin folio (portada, acta, declaración); páginas 4-12 en romanos minúsculas ii-x; páginas 13-158 en arábigos 1-146, reiniciados en la Introducción y continuos hasta el final.

## 3. Veredicto global

| Métrica | Valor |
|---|---|
| Páginas revisadas | 158 |
| Páginas CONFORMES | 99 |
| Páginas OBSERVADAS | 59 |
| Defectos registrados | 90 |
| Críticos | 10 |
| Altos | 63 |
| Medios | 10 |
| Bajos | 7 |
| Esquema de folios | CONFORME en las 158 páginas |
| Orden canónico de secciones | CONFORME |

El orden canónico de la tesis se cumple sin inversiones: Portada, Acta, Declaración jurada, Dedicatoria, Agradecimientos, Índice de contenido, Índice de figuras, Índice de tablas, Resumen, Abstract, Chumasqa, Introducción, Capítulos I a VI, Conclusiones, Recomendaciones, Referencias y Anexos 1 a 7. Las deficiencias detectadas son de rotulación, numeración, geometría tabular y control de viudas, no de arquitectura capitular.

## 4. Registro página por página

| Pág. | Folio | Orientación | Esquema | Folio correcto | Defectos | Veredicto |
|---|---|---|---|---|---|---|
| 1 | - | vertical | sin folio | sí | 0 | CONFORME |
| 2 | - | vertical | sin folio | sí | 1 | OBSERVADA |
| 3 | - | vertical | sin folio | sí | 1 | OBSERVADA |
| 4 | ii | vertical | romano | sí | 0 | CONFORME |
| 5 | iii | vertical | romano | sí | 0 | CONFORME |
| 6 | iv | vertical | romano | sí | 0 | CONFORME |
| 7 | v | vertical | romano | sí | 1 | OBSERVADA |
| 8 | vi | vertical | romano | sí | 1 | OBSERVADA |
| 9 | vii | vertical | romano | sí | 2 | OBSERVADA |
| 10 | viii | vertical | romano | sí | 0 | CONFORME |
| 11 | ix | vertical | romano | sí | 0 | CONFORME |
| 12 | x | vertical | romano | sí | 0 | CONFORME |
| 13 | 1 | vertical | arábigo | sí | 0 | CONFORME |
| 14 | 2 | vertical | arábigo | sí | 0 | CONFORME |
| 15 | 3 | vertical | arábigo | sí | 0 | CONFORME |
| 16 | 4 | vertical | arábigo | sí | 0 | CONFORME |
| 17 | 5 | vertical | arábigo | sí | 0 | CONFORME |
| 18 | 6 | vertical | arábigo | sí | 0 | CONFORME |
| 19 | 7 | vertical | arábigo | sí | 0 | CONFORME |
| 20 | 8 | vertical | arábigo | sí | 0 | CONFORME |
| 21 | 9 | vertical | arábigo | sí | 0 | CONFORME |
| 22 | 10 | vertical | arábigo | sí | 1 | OBSERVADA |
| 23 | 11 | vertical | arábigo | sí | 0 | CONFORME |
| 24 | 12 | vertical | arábigo | sí | 0 | CONFORME |
| 25 | 13 | vertical | arábigo | sí | 0 | CONFORME |
| 26 | 14 | vertical | arábigo | sí | 0 | CONFORME |
| 27 | 15 | vertical | arábigo | sí | 0 | CONFORME |
| 28 | 16 | vertical | arábigo | sí | 0 | CONFORME |
| 29 | 17 | vertical | arábigo | sí | 0 | CONFORME |
| 30 | 18 | vertical | arábigo | sí | 1 | OBSERVADA |
| 31 | 19 | vertical | arábigo | sí | 0 | CONFORME |
| 32 | 20 | vertical | arábigo | sí | 0 | CONFORME |
| 33 | 21 | vertical | arábigo | sí | 0 | CONFORME |
| 34 | 22 | vertical | arábigo | sí | 0 | CONFORME |
| 35 | 23 | vertical | arábigo | sí | 1 | OBSERVADA |
| 36 | 24 | vertical | arábigo | sí | 0 | CONFORME |
| 37 | 25 | vertical | arábigo | sí | 0 | CONFORME |
| 38 | 26 | vertical | arábigo | sí | 0 | CONFORME |
| 39 | 27 | vertical | arábigo | sí | 0 | CONFORME |
| 40 | 28 | vertical | arábigo | sí | 0 | CONFORME |
| 41 | 29 | vertical | arábigo | sí | 0 | CONFORME |
| 42 | 30 | vertical | arábigo | sí | 0 | CONFORME |
| 43 | 31 | vertical | arábigo | sí | 0 | CONFORME |
| 44 | 32 | vertical | arábigo | sí | 0 | CONFORME |
| 45 | 33 | vertical | arábigo | sí | 0 | CONFORME |
| 46 | 34 | vertical | arábigo | sí | 1 | OBSERVADA |
| 47 | 35 | vertical | arábigo | sí | 0 | CONFORME |
| 48 | 36 | vertical | arábigo | sí | 0 | CONFORME |
| 49 | 37 | vertical | arábigo | sí | 0 | CONFORME |
| 50 | 38 | vertical | arábigo | sí | 0 | CONFORME |
| 51 | 39 | vertical | arábigo | sí | 0 | CONFORME |
| 52 | 40 | vertical | arábigo | sí | 2 | OBSERVADA |
| 53 | 41 | vertical | arábigo | sí | 0 | CONFORME |
| 54 | 42 | vertical | arábigo | sí | 0 | CONFORME |
| 55 | 43 | vertical | arábigo | sí | 0 | CONFORME |
| 56 | 44 | vertical | arábigo | sí | 0 | CONFORME |
| 57 | 45 | vertical | arábigo | sí | 0 | CONFORME |
| 58 | 46 | vertical | arábigo | sí | 2 | OBSERVADA |
| 59 | 47 | vertical | arábigo | sí | 0 | CONFORME |
| 60 | 48 | vertical | arábigo | sí | 0 | CONFORME |
| 61 | 49 | vertical | arábigo | sí | 0 | CONFORME |
| 62 | 50 | vertical | arábigo | sí | 0 | CONFORME |
| 63 | 51 | vertical | arábigo | sí | 0 | CONFORME |
| 64 | 52 | vertical | arábigo | sí | 0 | CONFORME |
| 65 | 53 | vertical | arábigo | sí | 1 | OBSERVADA |
| 66 | 54 | vertical | arábigo | sí | 0 | CONFORME |
| 67 | 55 | vertical | arábigo | sí | 0 | CONFORME |
| 68 | 56 | vertical | arábigo | sí | 1 | OBSERVADA |
| 69 | 57 | vertical | arábigo | sí | 0 | CONFORME |
| 70 | 58 | vertical | arábigo | sí | 0 | CONFORME |
| 71 | 59 | vertical | arábigo | sí | 0 | CONFORME |
| 72 | 60 | vertical | arábigo | sí | 0 | CONFORME |
| 73 | 61 | vertical | arábigo | sí | 1 | OBSERVADA |
| 74 | 62 | vertical | arábigo | sí | 1 | OBSERVADA |
| 75 | 63 | vertical | arábigo | sí | 0 | CONFORME |
| 76 | 64 | vertical | arábigo | sí | 0 | CONFORME |
| 77 | 65 | vertical | arábigo | sí | 0 | CONFORME |
| 78 | 66 | vertical | arábigo | sí | 0 | CONFORME |
| 79 | 67 | vertical | arábigo | sí | 0 | CONFORME |
| 80 | 68 | vertical | arábigo | sí | 0 | CONFORME |
| 81 | 69 | vertical | arábigo | sí | 1 | OBSERVADA |
| 82 | 70 | vertical | arábigo | sí | 0 | CONFORME |
| 83 | 71 | vertical | arábigo | sí | 0 | CONFORME |
| 84 | 72 | vertical | arábigo | sí | 0 | CONFORME |
| 85 | 73 | vertical | arábigo | sí | 1 | OBSERVADA |
| 86 | 74 | vertical | arábigo | sí | 1 | OBSERVADA |
| 87 | 75 | vertical | arábigo | sí | 1 | OBSERVADA |
| 88 | 76 | vertical | arábigo | sí | 1 | OBSERVADA |
| 89 | 77 | vertical | arábigo | sí | 1 | OBSERVADA |
| 90 | 78 | vertical | arábigo | sí | 0 | CONFORME |
| 91 | 79 | vertical | arábigo | sí | 1 | OBSERVADA |
| 92 | 80 | vertical | arábigo | sí | 0 | CONFORME |
| 93 | 81 | vertical | arábigo | sí | 0 | CONFORME |
| 94 | 82 | vertical | arábigo | sí | 0 | CONFORME |
| 95 | 83 | vertical | arábigo | sí | 0 | CONFORME |
| 96 | 84 | vertical | arábigo | sí | 1 | OBSERVADA |
| 97 | 85 | vertical | arábigo | sí | 0 | CONFORME |
| 98 | 86 | vertical | arábigo | sí | 0 | CONFORME |
| 99 | 87 | vertical | arábigo | sí | 0 | CONFORME |
| 100 | 88 | vertical | arábigo | sí | 1 | OBSERVADA |
| 101 | 89 | vertical | arábigo | sí | 0 | CONFORME |
| 102 | 90 | vertical | arábigo | sí | 0 | CONFORME |
| 103 | 91 | vertical | arábigo | sí | 1 | OBSERVADA |
| 104 | 92 | vertical | arábigo | sí | 1 | OBSERVADA |
| 105 | 93 | vertical | arábigo | sí | 0 | CONFORME |
| 106 | 94 | vertical | arábigo | sí | 0 | CONFORME |
| 107 | 95 | vertical | arábigo | sí | 0 | CONFORME |
| 108 | 96 | vertical | arábigo | sí | 1 | OBSERVADA |
| 109 | 97 | vertical | arábigo | sí | 0 | CONFORME |
| 110 | 98 | vertical | arábigo | sí | 0 | CONFORME |
| 111 | 99 | vertical | arábigo | sí | 1 | OBSERVADA |
| 112 | 100 | vertical | arábigo | sí | 0 | CONFORME |
| 113 | 101 | vertical | arábigo | sí | 0 | CONFORME |
| 114 | 102 | vertical | arábigo | sí | 0 | CONFORME |
| 115 | 103 | vertical | arábigo | sí | 2 | OBSERVADA |
| 116 | 104 | vertical | arábigo | sí | 1 | OBSERVADA |
| 117 | 105 | vertical | arábigo | sí | 2 | OBSERVADA |
| 118 | 106 | vertical | arábigo | sí | 2 | OBSERVADA |
| 119 | 107 | vertical | arábigo | sí | 0 | CONFORME |
| 120 | 108 | vertical | arábigo | sí | 2 | OBSERVADA |
| 121 | 109 | vertical | arábigo | sí | 1 | OBSERVADA |
| 122 | 110 | vertical | arábigo | sí | 2 | OBSERVADA |
| 123 | 111 | vertical | arábigo | sí | 0 | CONFORME |
| 124 | 112 | vertical | arábigo | sí | 2 | OBSERVADA |
| 125 | 113 | vertical | arábigo | sí | 1 | OBSERVADA |
| 126 | 114 | vertical | arábigo | sí | 4 | OBSERVADA |
| 127 | 115 | vertical | arábigo | sí | 3 | OBSERVADA |
| 128 | 116 | vertical | arábigo | sí | 2 | OBSERVADA |
| 129 | 117 | vertical | arábigo | sí | 2 | OBSERVADA |
| 130 | 118 | vertical | arábigo | sí | 4 | OBSERVADA |
| 131 | 119 | vertical | arábigo | sí | 1 | OBSERVADA |
| 132 | 120 | vertical | arábigo | sí | 0 | CONFORME |
| 133 | 121 | vertical | arábigo | sí | 0 | CONFORME |
| 134 | 122 | vertical | arábigo | sí | 0 | CONFORME |
| 135 | 123 | vertical | arábigo | sí | 0 | CONFORME |
| 136 | 124 | vertical | arábigo | sí | 0 | CONFORME |
| 137 | 125 | vertical | arábigo | sí | 0 | CONFORME |
| 138 | 126 | vertical | arábigo | sí | 0 | CONFORME |
| 139 | 127 | vertical | arábigo | sí | 0 | CONFORME |
| 140 | 128 | vertical | arábigo | sí | 0 | CONFORME |
| 141 | 129 | vertical | arábigo | sí | 1 | OBSERVADA |
| 142 | 130 | vertical | arábigo | sí | 1 | OBSERVADA |
| 143 | 131 | horizontal | arábigo | sí | 1 | OBSERVADA |
| 144 | 132 | horizontal | arábigo | sí | 0 | CONFORME |
| 145 | 133 | horizontal | arábigo | sí | 1 | OBSERVADA |
| 146 | 134 | vertical | arábigo | sí | 1 | OBSERVADA |
| 147 | 135 | vertical | arábigo | sí | 1 | OBSERVADA |
| 148 | 136 | vertical | arábigo | sí | 2 | OBSERVADA |
| 149 | 137 | vertical | arábigo | sí | 4 | OBSERVADA |
| 150 | 138 | vertical | arábigo | sí | 1 | OBSERVADA |
| 151 | 139 | vertical | arábigo | sí | 1 | OBSERVADA |
| 152 | 140 | vertical | arábigo | sí | 0 | CONFORME |
| 153 | 141 | vertical | arábigo | sí | 2 | OBSERVADA |
| 154 | 142 | vertical | arábigo | sí | 2 | OBSERVADA |
| 155 | 143 | vertical | arábigo | sí | 1 | OBSERVADA |
| 156 | 144 | vertical | arábigo | sí | 1 | OBSERVADA |
| 157 | 145 | vertical | arábigo | sí | 6 | OBSERVADA |
| 158 | 146 | vertical | arábigo | sí | 2 | OBSERVADA |
