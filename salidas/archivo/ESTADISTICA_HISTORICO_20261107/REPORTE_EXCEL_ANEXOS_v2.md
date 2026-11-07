# REPORTE DE CONSTRUCCIÓN DEL LIBRO DE TABLAS DE ANEXOS v2

**Proyecto:** SIVAC-THESIS-LAB — Universidad Nacional José María Arguedas (UNAJMA)  
**Agente:** analista-estadistico (Squad D — Bioestadística e Inferencia)  
**Fase:** F8_INTEGRACION_EDITORIAL  
**Fecha:** 2026-10-21  
**Libro generado:** `salidas/estadistica/TABLAS_ANEXOS_SIVAC_v2.xlsx`  
**Estado de los datos:** Datos provisionales. Serán sustituidos por los registros definitivos de campo antes de la sustentación.

## 1. Hojas creadas

| Hoja | Contenido | Filas totales | Columnas | Filas de datos |
|---|---|---:|---:|---:|
| `00_PORTADA` | Portada e índice | 43 | 6 | 0 |
| `01_TABLA_44_CONSISTENCIA` | Tabla 44. Matriz de consistencia metodológica del estudio SIVAC | 11 | 5 | 4 |
| `02_TABLA_45_OPERACIONALIZACION` | Tabla 45. Matriz de operacionalización de las variables de investigación | 11 | 6 | 4 |
| `03_TABLA_46_INSTRUMENTO_01` | Tabla 46. Instrumento N.° 01: Ficha de Registro Cronométrico de Tiempos Operativos | 10 | 4 | 3 |
| `04_TABLA_47_INSTRUMENTO_02` | Tabla 47. Instrumento N.° 02: Ficha de Auditoría y Cotejo Documental de Lotes | 10 | 4 | 3 |
| `05_TABLA_48_INSTRUMENTO_03_TAM` | Tabla 48. Instrumento N.° 03: Cuestionario TAM de Satisfacción del Usuario (Modalidad A) | 15 | 4 | 8 |
| `06_TABLA_49_PRETEST` | Tabla 49. Matriz de datos recolectados en el Pretest (Gestión manual basal, n = 14) | 21 | 18 | 14 |
| `07_TABLA_50_POSTTEST` | Tabla 50. Matriz de datos recolectados en el Posttest (Operación con sistema SIVAC, n = 14) | 21 | 18 | 14 |
| `08_TABLA_51_HISTORIAS_XP` | Tabla 51. Matriz de Historias de Usuario desarrolladas e implementadas en SIVAC bajo XP | 12 | 5 | 5 |
| `09_DESCRIPTIVOS` | Tablas 36, 37 y 38 | 44 | 12 | 21 |
| `10_CONFIABILIDAD` | Tabla 35 | 13 | 8 | 6 |
| `11_NORMALIDAD` | Tabla 39 | 14 | 8 | 7 |
| `12_CONTRASTES` | Tablas 40 a 43 | 49 | 11 | 18 |
| `13_SPSS_SINTAXIS` | Sintaxis SPSS | 248 | 1 | 246 |
| `14_SPSS_SALIDAS` | Salidas SPSS | 260 | 4 | 256 |
| `15_NOTAS_TRAZABILIDAD` | Trazabilidad | 26 | 5 | 19 |

## 2. Correcciones frente a la versión anterior

1. **Rótulos corregidos:** la versión anterior rotulaba las hojas `03_ANEXO5_PRETEST` y `04_ANEXO5_POSTEST` como «Tabla 52» y «Tabla 53». Esos números eran el índice de `python-docx`, no el rótulo visible. En esta versión se rotulan correctamente como **Tabla 49** y **Tabla 50**.
2. **Tablas faltantes incorporadas:** se añadieron la Tabla 46 (Instrumento N.° 01), la Tabla 47 (Instrumento N.° 02), la Tabla 48 (Cuestionario TAM) y la Tabla 51 (Historias de Usuario XP), todas en formato tabular.
3. **Historias de Usuario actualizadas al DOCX v10:** la versión anterior asignaba a HU-06 la «Iteración 2 (Movimientos)». El DOCX v10 registra «Iteración 3 (Núcleo Transaccional y Despacho)». Se transcribió el valor del DOCX vigente.
4. **Fuente actualizada:** las notas de la versión anterior remitían a `informe_final_v04.docx`. Esta versión remite a `informe_final_v10.docx`.
5. **Certificados de validación:** los índices `python-docx` 46, 47 y 48 corresponden a los certificados de los jueces 1, 2 y 3, que no llevan rótulo de tabla. Por indicación del Director no se incorporan como hojas tabulares; las Tablas 46, 47 y 48 visibles son los instrumentos, que sí se incorporaron.

## 3. Verificación de contenido frente al DOCX

- Comparación celda a celda de las tablas 44, 45, 46, 47, 48 y 51: **0 discrepancias** en 153 celdas comparadas.
- Comparación de las matrices de pretest y postest (14 filas × 18 columnas por momento, 504 celdas): **0 discrepancias** entre el DOCX y los CSV.
- Las matrices 49 y 50 se construyeron desde los CSV y se compararon contra las tablas 52 y 53 de `python-docx`; los valores numéricos, identificadores, centros de acopio y niveles coinciden.
- Los encabezados de las matrices se normalizaron a etiquetas legibles (por ejemplo, `AP-01` en lugar de `ap_\n01`), sin alterar los valores.

## 4. Verificación de cifras frente al informe

Se compararon 228 valores estadísticos (descriptivos, variación, normalidad, confiabilidad y contrastes) contra `reporte_estadistico_completo.json`: **0 discrepancias**.

| Bloque | Cifras verificadas | Resultado |
|---|---:|---|
| Descriptivos (media, DE, mediana, RIC, mínimo, máximo) | 126 | Coinciden con el JSON y con las Tablas 36-38 del DOCX |
| Variación porcentual pretest-postest | 7 | Coincide con el JSON |
| Alfa de Cronbach e IC 95 % de Feldt (α, límite inferior, límite superior) | 18 | Coinciden con el JSON y con la Tabla 35 del DOCX |
| Shapiro-Wilk (W y p) | 14 | Coinciden con el JSON y con la Tabla 39 del DOCX |
| t pareada (t, gl, p, d_z) | 28 | Coinciden con el JSON y con las Tablas 40-42 del DOCX |
| Wilcoxon (W, Z, p, r) | 28 | W, Z y p recalculados y coincidentes con el JSON; r recalculado como |Z| / sqrt(N) y trazado al Z de origen en las Tablas 40-42 |
| Holm-Bonferroni (p ajustado) | 7 | Recalculado sobre los siete p adoptados; coincide con el JSON |

**Cifras clave verificadas:**

- T_reg: M pretest = 37.18 min, M postest = 7.18 min; t(13) = -38.944, p < .001, d_z = -10.408.
- T_vale: M pretest = 18.21 min, M postest = 3.04 min; t(13) = -24.509, p < .001, d_z = -6.550.
- RSD: M pretest = 63.57 %, M postest = 96.00 %; t(13) = 26.628, p < .001, d_z = 7.117.
- CPE: M pretest = 67.61 %, M postest = 95.39 %; t(13) = 28.147, p < .001, d_z = 7.523.
- AP: M pretest = 8.07, M postest = 17.71; t(13) = 33.352, p < .001, d_z = 8.914.
- UP: M pretest = 9.00, M postest = 18.50; t(13) = 34.881, p < .001, d_z = 9.322.
- TAM total: M pretest = 17.07, M postest = 36.21; t(13) = 44.477, p < .001, d_z = 11.887.
- Wilcoxon: W = 0.000, Z = -3.296, r = |Z| / sqrt(14) = 0.881 en los siete indicadores; p de Wilcoxon entre 1.2207E-04 y 9.7588E-04.
- Alfa de Cronbach global: pretest = 0.939 [0.874, 0.977]; postest = 0.915 [0.826, 0.968].

## 5. Diseño editorial aplicado

- Encabezados en azul marino `#1F3864` con texto blanco en negrita; bandas alternas `#F2F2F2` y `#FFFFFF`; filas de total en negrita con relleno `#D9E2F3`.
- Bordes finos solo horizontales, sin líneas verticales; sin colores fuera de la paleta institucional.
- Filas de encabezado congeladas, autofiltro en las hojas de una sola tabla, anchos ajustados y ajuste de texto.
- En `09_DESCRIPTIVOS` y `12_CONTRASTES`, que agrupan varias tablas por hoja, no se congelaron encabezados para no mostrar un rótulo ajeno al desplazarse; el autofiltro se aplica solo al bloque final de resumen (Tabla 43).
- Formato numérico: dos decimales para medias, DE y porcentajes; tres decimales para α, W, Z, p y tamaños del efecto; porcentajes con signo `%`.
- Impresión A4 horizontal, escalada a una página de ancho, márgenes de 1.5 cm y filas de encabezado repetidas.

## 6. Marcas de estado y trazabilidad

- La marca `Datos provisionales. Serán sustituidos por los registros definitivos de campo antes de la sustentación.` aparece en la portada, en las matrices 49 y 50 y en todas las hojas estadísticas (09 a 14).
- Las tablas 44 a 48 y 51 son transcripciones metodológicas y no llevan la marca porque no contienen cifras empíricas.
- La hoja `15_NOTAS_TRAZABILIDAD` registra una fila por tabla con rótulo, hoja, rango de celdas, fuente y nota APA.

## 7. Limitaciones y pendientes

- Las bases `pretest_campo.csv` y `posttest_campo.csv` corresponden a registros provisionales; al reemplazarlas por mediciones definitivas debe regenerarse el libro.
- El intervalo de confianza del alfa se calculó por el método de Feldt y se verificó numéricamente contra el JSON; no se reporta como intervalo bootstrap.
- Los certificados de validación por jueces no se tabularon por no llevar rótulo de tabla; si el tesista desea incorporarlos, deben abrirse como hojas independientes sin numeración de tabla.
- `[VERIFICAR]` La asignación de iteración de HU-06 se tomó del DOCX v10; confirmar con el expediente XP si la numeración de iteraciones es la definitiva.
- El r de Rosenthal se calcula como |Z| / sqrt(N), con N = 14 pares válidos, conforme a la convención adoptada. El valor corregido es 0.881 en los siete indicadores (magnitud grande, r >= 0.50); el valor previo 0.62 procedía de un denominador duplicado y quedó sustituido.

## 8. Reproducibilidad

```bash
C:/MisInvestigaciones/tesis/sivac/.venv/Scripts/python.exe \
  C:/MisInvestigaciones/tesis/sivac/scripts/estadistica/build_tablas_anexos_v2.py
```

El script lee únicamente el DOCX, los CSV y el JSON; no los modifica. Vuelve a generar el libro y este reporte de forma idéntica.
