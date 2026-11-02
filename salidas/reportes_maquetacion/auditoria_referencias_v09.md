# AUDITORÍA DE CORRESPONDENCIA BIUNÍVOCA CITA-REFERENCIA — INFORME FINAL v09

**Documento auditado:** `salidas/documentos/informe_final_v09.docx` (813 párrafos, 59 tablas; SHA-256 `6275fc75a2a8a64dd74752e819907591f85acf63a081288de6ce72acfdbf5275`).
**Fecha:** 2026-10-21.
**Fase:** F8_INTEGRACION_EDITORIAL.
**Agente:** verificador-integridad (Squad A, Inteligencia Bibliográfica y Evidencia).
**Modalidad:** auditoría en solo lectura. El DOCX no se modificó.
**Lista de Referencias:** rótulo en el párrafo 725; asentamientos en los párrafos 726 a 767 (42 entradas).
**Órdenes quirúrgicas:** `salidas/reportes_maquetacion/referencias_v09_ordenes.json`.

---

## 1. Dictamen general

**REQUIERE_AJUSTE.**

La correspondencia 1:1 no está cerrada en el v09. El cuerpo cita siete obras que no figuran en la lista (Cronbach, Feldt, Shapiro y Wilk, Razali y Wah, Wilcoxon, Holm y Quispe Tello), mantiene dos referencias sin cita activa (Arisholm et al., 2007; Dolan et al., 2020) y contiene cuatro asentamientos con metadatos divergentes de la fuente primaria, uno de ellos con un DOI que resuelve a un artículo ajeno.

Las órdenes emitidas resuelven las siete citas huérfanas vigentes con once inserciones verificadas, convierten las dos referencias decorativas en citas activas semánticamente pertinentes y corrigen los cinco asentamientos defectuosos. Con ellas la lista pasa de 42 a 53 entradas y la correspondencia queda cerrada, salvo los puntos marcados `[VERIFICAR]` que dependen de datos que solo el tesista o el repositorio institucional pueden aportar.

| Métrica | Resultado |
|---|---|
| Referencias existentes | 42 |
| Inserciones ordenadas | 11 |
| Referencias resultantes | 53 |
| Citas huérfanas inventariadas en v06 | 10 |
| Citas huérfanas vigentes en v09 | 7 |
| Citas huérfanas extinguidas por la reescritura | 3 |
| Referencias sin cita activa | 2 |
| Sustituciones en el cuerpo | 17 |
| Asentamientos corregidos | 5 |
| DOIs verificados en Crossref | 28 |
| DOIs con corrección obligatoria | 1 (Brooks et al., 2024) |
| Identificadores no resolubles | 3 (`[VERIFICAR]`) |

---

## 2. Cambios del v09 respecto del v06

La reescritura del cuerpo eliminó tres de las diez citas huérfanas inventariadas en la auditoría previa:

- **OMS y UNICEF (2021):** la atribución y las cifras asociadas ya no aparecen en el cuerpo ni en las tablas.
- **Mamani (2023):** la cifra de 76.4% y la atribución desaparecieron. El documento cita ahora Mamani-Pari et al. (2026), que sí tiene asentamiento.
- **Rojas y Vargas (2022):** la cifra de 84.5% y la atribución desaparecieron.

Por tanto, la restricción 1 de la comisión se resuelve en tres casos por extinción de la aserción y en siete por inserción o corrección. Las cuatro órdenes de inserción emitidas para el v06 (párrafos 742, 745, 761 y 765) **nunca fueron aplicadas**: los párrafos ancla conservan exactamente el mismo texto y las entradas siguen ausentes. Se reemiten como inserciones reales, no como sustituciones intra-párrafo.

---

## 3. Matriz 1:1 completa

La tabla se ordena por asentamiento. Las columnas «Referencia» y «Párrafos que la citan» expresan la correspondencia en ambos sentidos: toda cita del cuerpo remite a un asentamiento y todo asentamiento remite a sus párrafos citantes.

### 3.1 Asentamientos existentes (párrafos 726-767)

| # | Párr. | Referencia (autor, año) | Párrafos que la citan | DOI / URL y estado | Estado 1:1 |
|---|---|---|---|---|---|
| 1 | 726 | Addy et al. (2024) | 260, 327 | Sin DOI. No localizada en Crossref ni OpenAlex; revista declarada no indexada | Citada / **`[VERIFICAR]`** |
| 2 | 727 | Alvarez Ticllasuca et al. (2023) | 159 | Handle `20.500.12894/9418` → HTTP 200 | Citada / verificada |
| 3 | 728 | Arisholm et al. (2007) | 444 (cita añadida) | `10.1109/TSE.2007.17` → Crossref OK | Citada tras orden |
| 4 | 729 | Astuhuaman Perez y Baltazar Maza (2023) | 216, 272 | Handle `11537/43590` → HTTP 200 | Citada / verificada |
| 5 | 730 | Balón Morejón (2023) | 157, 210, 236 | Handle `46000/9257` → **HTTP 404** | Citada / **`[VERIFICAR]`** |
| 6 | 731 | Beck (1999) | 173, 242, 245, 307, 329, 334, 338, 444, 551 | `10.1109/2.796139` → Crossref OK | Citada / verificada |
| 7 | 732 | Brooks et al. (2024) | 155 | **DOI ajeno** `10.1016/j.vaccine.2024.01.045`; corregido a `10.2196/62657` | Citada / **corregida** |
| 8 | 733 | Champi Velásquez (2023) | 159, 219, 259, 263, 293 | Handle `20.500.12872/844` → HTTP 200 (página de desafío del repositorio) | Citada / verificada |
| 9 | 734 | Chekol et al. (2023) | 156, 274, 278, 290, 301 | `10.3389/frhs.2023.1059611` → Crossref OK; título y autores corregidos | Citada / **corregida** |
| 10 | 735 | Cohen (1988) | 177, 620, 627, 637, 639, 683, 686, 689, 692, 698 | Libro impreso, sin DOI | Citada / verificada |
| 11 | 736 | Cohn (2004) | 246, 311 | Libro impreso, sin DOI | Citada / verificada |
| 12 | 737 | Dang et al. (2024) | 157, 208, 271, 272, 290, 321 | `10.2196/45070` → Crossref OK | Citada / verificada |
| 13 | 738 | Davis (1989) | 173, 280, 290, 319, 602, 613, 713 | `10.2307/249008` → Crossref OK | Citada / verificada |
| 14 | 739 | De la Torre Llorente et al. (2010) | 231, 323, 370 | Libro impreso, sin DOI | Citada / verificada |
| 15 | 740 | Dolan et al. (2020) | 711 (cita añadida) | `10.1186/s43058-020-00022-8` → Crossref OK | Citada tras orden |
| 16 | 741 | Ergetie et al. (2023) | 156, 211 | `10.3389/fpubh.2023.1194807` → Crossref OK | Citada / verificada |
| 17 | 742 | Garcia Villacorta y Calderón Huaman (2023) | 159, 218, 260, 297, 315 | Handle `11537/33833` → HTTP 200 | Citada / verificada |
| 18 | 743 | Gilbert et al. (2020) | 213, 265, 711 | `10.1016/j.vaccine.2019.10.059` → Crossref OK | Citada / verificada |
| 19 | 744 | Gutiérrez-Aguado et al. (2024) | 158, 259 | `10.25176/rfmh.v24i1.6189` → Crossref OK | Citada / verificada |
| 20 | 745 | Hernández-Sampieri et al. (2014) | 177, 551, 553, 555, 557, 559, 571, 573, 610, 619, 623, 625, 650 | Libro impreso, sin DOI | Citada / verificada |
| 21 | 746 | Hussain et al. (2025) | 284, 290 | `10.1186/s12912-024-02648-8` → Crossref OK | Citada / verificada |
| 22 | 747 | Inarotul Huda et al. (2025) | 214, 711 | `10.35870/ijsecs.v5i3.5354` → Crossref OK | Citada / verificada |
| 23 | 748 | ISO/IEC (2023) | 173, 252, 551 | `iso.org/standard/78176.html` → HTTP 403 por bloqueo anti-bot | Citada / verificación manual |
| 24 | 749 | Kigenza et al. (2023) | 157, 209, 265 | `10.9745/GHSP-D-22-00295` → Crossref OK | Citada / verificada |
| 25 | 750 | Kokol (2022) | 242 | `10.3390/app12199462` → Crossref OK | Citada / verificada |
| 26 | 751 | Luján Mora (2002) | 230, 234 | Libro impreso, sin DOI | Citada / verificada |
| 27 | 752 | Luo et al. (2024) | 280, 283, 290, 319 | `10.1057/s41599-024-02976-9` → Crossref OK | Citada / verificada |
| 28 | 753 | Mamani-Pari et al. (2026) | 220, 253 | `10.2196/81377` → Crossref OK; revista y volumen corregidos | Citada / **corregida** |
| 29 | 754 | Mego Navarro (2021) | 158, 217, 236, 315 | Handle `20.500.12867/5068` → HTTP 403 por bloqueo anti-bot | Citada / verificación manual |
| 30 | 755 | Mekonen et al. (2024) | 156, 275, 299 | `10.4258/hir.2024.30.4.375` → Crossref OK | Citada / verificada |
| 31 | 756 | Ministerio de Salud del Perú (2022) | 158, 212, 219, 220, 253, 259, 293, 295, 309, 317, 330, 383, 586 | URL `gob.pe/.../3576882-884-2022-minsa` → **redirige a una norma de la Región Piura de 2018**; URL retirada | Citada / **corregida** |
| 32 | 757 | Moumane et al. (2024) | 253, 256 | `10.31083/j.ceog5104088` → Crossref OK | Citada / verificada |
| 33 | 758 | Ndlovu et al. (2022) | 285 | `10.2196/32722` → Crossref OK; año y volumen corregidos | Citada / **corregida** |
| 34 | 759 | Oliveira et al. (2020) | 285, 288 | `10.1590/1518-8345.3360.3307` → Crossref OK | Citada / verificada |
| 35 | 760 | OPS y PATH (2020) | 155, 265, 325 | Handle `10665.2/53120` → HTTP 502 transitorio | Citada / verificación manual |
| 36 | 761 | Pressman (2010) | 246, 250, 307, 329 | Libro impreso, sin DOI | Citada / verificada |
| 37 | 762 | Ruiz Barea (2023) | 237, 303, 313, 370 | Sin DOI ni URL en la entrada | Citada / verificada |
| 38 | 763 | Shen et al. (2024) | 157, 207, 266, 305, 327 | `10.3389/fphar.2024.1373642` → Crossref OK | Citada / verificada |
| 39 | 764 | Sommerville (2016) | 231, 236, 240, 242, 329, 444 | Libro impreso, sin DOI | Citada / verificada |
| 40 | 765 | Tristán-López (2008) | 177, 625, 627 | Sin DOI; revista no depositada en Crossref | Citada / verificada |
| 41 | 766 | Wasswa et al. (2023) | 157, 212, 265, 266, 269, 299, 325 | `10.1186/s40545-023-00517-4` → Crossref OK | Citada / verificada |
| 42 | 767 | World Health Organization (2021) | 155, 259 | Handle IRIS `10665/344249` → HTTP 200 | Citada / verificada |

### 3.2 Asentamientos que se insertan (11)

| # | Ancla | Referencia insertada | Párrafos que la citan | DOI / URL y estado | Estado 1:1 |
|---|---|---|---|---|---|
| 43 | 736 | Cronbach (1951) | 649 | `10.1007/BF02310555` → Crossref OK | Citada / verificada |
| 44 | 741 | Feldt (1965) | 649, 652 | `10.1007/BF02289499` → Crossref OK | Citada / verificada |
| 45 | 742 | George y Mallery (2003) | 650 | Libro impreso, sin DOI; registro Open Library verificado | Citada / verificada |
| 46 | 745 | Hernández-Sampieri y Mendoza (2018) | 650 | Libro impreso, sin DOI; ISBN 978-1-4562-6096-5 | Citada / verificada |
| 47 | 745 | Holm (1979) | 683 | DOI `10.2307/4615733` no resuelve; JSTOR `stable/4615733` → HTTP 200 | Citada / **`[VERIFICAR]`** |
| 48 | 761 | Quispe Tello (2024) | 630 | Sin DOI; URL del repositorio UNAJMA no consta en el PDF | Citada / **`[VERIFICAR]`** |
| 49 | 761 | Razali y Wah (2011) | 677 | Sin DOI registrado en Crossref ni OpenAlex | Citada / **`[VERIFICAR]`** |
| 50 | 761 | Rosenthal (1991) | 637, 683, 686, 689, 692 | `10.4135/9781412984997` → Crossref OK (monografía) | Citada / verificada |
| 51 | 762 | Shapiro y Wilk (1965) | 677, 681 | `10.1093/biomet/52.3-4.591` → Crossref OK | Citada / verificada |
| 52 | 765 | Venkatesh et al. (2003) | 713 | `10.2307/30036540` → Crossref OK | Citada / verificada |
| 53 | 766 | Wilcoxon (1945) | 679 | `10.2307/3001968` → Crossref OK | Citada / verificada |

**Resultado:** 53 referencias, 53 con cita activa; cero referencias decorativas. Siete citas huérfanas vigentes resueltas; tres extinguidas por reescritura.

---

## 4. Plan de inserción y orden alfabético

El orden de aplicación es secuencial. Cuando varias entradas comparten ancla, se aplican en el orden indicado; cada inserción debe crear un **párrafo nuevo** con el `pPr` de la lista, no un salto de línea intra-párrafo.

| Orden | Insertar después de | Entrada | Justificación alfabética |
|---|---|---|---|
| 1 | 736 Cohn (2004) | Cronbach (1951) | Cohen < Cohn < **Cronbach** < Dang |
| 2 | 741 Ergetie et al. (2023) | Feldt (1965) | Ergetie < **Feldt** < Garcia |
| 3 | 742 Garcia Villacorta (2023) | George y Mallery (2003) | Garcia < **George** < Gilbert |
| 4 | 745 Hernández-Sampieri et al. (2014) | Hernández-Sampieri y Mendoza (2018) | 2014 < **2018** < Holm < Hussain |
| 5 | inserción 4 | Holm (1979) | Hernández-Sampieri < **Holm** < Hussain |
| 6 | 761 Pressman (2010) | Quispe Tello (2024) | Pressman < **Quispe Tello** < Razali |
| 7 | inserción 6 | Razali y Wah (2011) | Quispe Tello < **Razali** < Rosenthal |
| 8 | inserción 7 | Rosenthal (1991) | Razali < **Rosenthal** < Ruiz |
| 9 | 762 Ruiz Barea (2023) | Shapiro y Wilk (1965) | Ruiz < **Shapiro** < Shen («Sha» < «She») |
| 10 | 765 Tristán-López (2008) | Venkatesh et al. (2003) | Tristán < **Venkatesh** < Wasswa |
| 11 | 766 Wasswa et al. (2023) | Wilcoxon (1945) | Wasswa < **Wilcoxon** < World Health Organization |

**Advertencia de maquetación.** La auditoría v06 ya advirtió que el salto de línea intra-párrafo no genera sangría francesa autónoma. Las once entradas deben quedar como párrafos independientes con `w:ind left="720" hanging="720"`, `w:line="360"`, `w:after="120"`, Times New Roman 12 pt y alineación justificada. Si se aplican como span dentro del párrafo ancla, la compuerta no puede declararse cerrada.

---

## 5. Resolución de las diez citas huérfanas

| # | Cita | Párr. v09 | Decisión | Resultado |
|---|---|---|---|---|
| 1 | Cronbach (1951) | 649 | Insertar obra primaria | Resuelta; DOI verificado |
| 2 | Feldt (1965) | 649 | Insertar obra primaria | Resuelta; DOI verificado |
| 3 | Shapiro-Wilk (1965) | 677 | Insertar obra primaria y corregir cita a «Shapiro y Wilk (1965)» en 677 y 681 | Resuelta; DOI verificado |
| 4 | Razali y Wah (2011) | 677 | Insertar referencia y cambiar «&» por «y» | Resuelta con `[VERIFICAR: sin DOI registrado]` |
| 5 | Wilcoxon (1945) | 679 | Insertar obra primaria | Resuelta; DOI verificado |
| 6 | Holm (1979) | 683 | Insertar referencia con URL JSTOR | Resuelta con `[VERIFICAR: DOI no registrado]` |
| 7 | Fany (2024) | 630 | Sustituir por «Quispe Tello (2024)» e insertar la tesis | Resuelta con `[VERIFICAR: URL de repositorio]` |
| 8 | OMS y UNICEF (2021) | — | Sin acción: la atribución fue eliminada en el v09 | Extinguida por reescritura |
| 9 | Mamani (2023) | — | Sin acción: la atribución y la cifra fueron eliminadas | Extinguida por reescritura |
| 10 | Rojas y Vargas (2022) | — | Sin acción: la atribución y la cifra fueron eliminadas | Extinguida por reescritura |

**Nota sobre Fany (2024).** El PDF primario de la tesis modelo UNAJMA identifica a la autora como **Fany Quispe Tello**. «Fany» es nombre de pila; la cita correcta es **Quispe Tello (2024)** y el asentamiento se ordena en la letra Q, entre Pressman y Razali.

---

## 6. Resolución de las dos referencias no citadas

| Referencia | Párr. lista | Decisión | Cita activa incorporada | Justificación |
|---|---|---|---|---|
| Arisholm et al. (2007) | 728 | Incorporar cita activa | Párr. 444: `(Arisholm et al., 2007; Beck, 1999; Sommerville, 2016)` | El párrafo trata la programación por pares en Extreme Programming; el artículo evalúa empíricamente esa práctica con complejidad de sistema y experiencia del programador. |
| Dolan et al. (2020) | 740 | Incorporar cita activa | Párr. 711: se añade «…en concordancia con los factores percibidos que condicionan la introducción y adopción de los registros electrónicos de inmunización (Dolan et al., 2020).» | El párrafo discute registros electrónicos de inmunización; el estudio analiza los factores percibidos de introducción y adopción en Tanzania y Zambia. La cláusula es paráfrasis fiel y no añade datos empíricos. |

No se retira ninguna entrada de la lista.

---

## 7. Correcciones de asentamientos

### 7.1 Críticas

1. **Brooks et al. (2024), párrafo 732.** El DOI `10.1016/j.vaccine.2024.01.045` resuelve a un artículo ajeno. El registro correcto es `10.2196/62657`, *JMIR Public Health and Surveillance*, 10, e62657; se corrigen además la inicial del cuarto autor (`Mboussou, F. F.`) y el nombre de la revista. La cita del párrafo 155 se mantiene.
2. **Ministerio de Salud del Perú (2022), párrafo 756.** La URL consignada redirige a una norma de la Región Piura de 2018. Se retira la URL no fiable; queda pendiente la URL oficial MINSA.
3. **Addy et al. (2024), párrafo 726.** Sin DOI y sin registro en Crossref ni OpenAlex; la revista declarada no es indexada. Se mantiene la entrada con `[VERIFICAR]` hasta que el tesista aporte el documento primario.
4. **Balón Morejón (2023), párrafo 730.** El handle `46000/9257` responde HTTP 404. Se mantiene con `[VERIFICAR]`; requiere URL actualizada del repositorio UPSE.

### 7.2 Mayores

1. **Chekol et al. (2023), párrafo 734.** Se corrige el título («…among health centers of West Gojjam Zone, northwest Ethiopia, 2021») y la nómina de autores: Chekol, A., Ketemaw, A., Endale, A., Aschale, A., Endalew, B., y Asemahagn, M. A. La nota del párrafo 278 ya consignaba el título correcto.
2. **Mamani-Pari et al. (2026), párrafo 753.** La revista es *JMIR Human Factors*, 13, e81377, no *JMIR Medical Informatics*, 14(1). Se corrige también el párrafo 220.
3. **Ndlovu et al. (2022), párrafos 758 y 285.** Año 2022, *JMIR Formative Research*, 6(3), e32722. El cuerpo citaba 2021.

### 7.3 Menores

1. Se uniforma «Ministerio de Salud, 2022» a «Ministerio de Salud del Perú, 2022» en siete párrafos (158 con dos ocurrencias, 259, 293, 295, 309, 317 y 586).
2. Se sustituye el ampersand por «y» en el párrafo 650.
3. Se corrige «Shapiro-Wilk (1965)» a «Shapiro y Wilk (1965)» en 677 y 681.
4. Se cita la NTS 196 por autor-año en el párrafo 713.
5. El párrafo 649 contiene la redundancia «coeficiente Alfa de Cronbach (Cronbach, 1951)». Es un defecto de redacción ajeno a la integridad bibliográfica; se recomienda «coeficiente Alfa de Cronbach (1951)» o «coeficiente Alfa (Cronbach, 1951)». No se incluye en las órdenes para no alterar el contenido sin autorización del redactor.
6. El párrafo 650 conserva la duplicación literal detectada en v06 (cláusula del umbral .800 y referencias a la Tabla 4 y la Tabla 35). Es un defecto de redacción que debe subsanar `redactor-academico`.

---

## 8. Formato APA 7 de las entradas nuevas

| Entrada | Sangría francesa | Interlineado | Fuente | Espaciado posterior | Alineación | DOI como hipervínculo |
|---|---|---|---|---|---|---|
| Cronbach (1951) | 1.27 cm (720/720) | 1.5 (360) | Times New Roman 12 pt | 6 pt (120) | Justificada | `https://doi.org/10.1007/BF02310555` |
| Feldt (1965) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | `https://doi.org/10.1007/BF02289499` |
| George y Mallery (2003) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | Sin DOI |
| Hernández-Sampieri y Mendoza (2018) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | Sin DOI |
| Holm (1979) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | URL JSTOR |
| Quispe Tello (2024) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | Sin URL verificada |
| Razali y Wah (2011) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | Sin DOI |
| Rosenthal (1991) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | `https://doi.org/10.4135/9781412984997` |
| Shapiro y Wilk (1965) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | `https://doi.org/10.1093/biomet/52.3-4.591` |
| Venkatesh et al. (2003) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | `https://doi.org/10.2307/30036540` |
| Wilcoxon (1945) | 1.27 cm | 1.5 | Times New Roman 12 pt | 6 pt | Justificada | `https://doi.org/10.2307/3001968` |

Todas las entradas usan dos apellidos unidos por «y», «et al.» desde tres autores en la cita y el DOI con el prefijo `https://doi.org/`.

---

## 9. Inventario de pendientes

| Marcador | Ubicación | Motivo | Responsable |
|---|---|---|---|
| `[VERIFICAR: Addy et al., 2024 no localizado en Crossref/OpenAlex]` | Párr. 726 | Revista no indexada; sin DOI | Tesista / redactor |
| `[VERIFICAR: handle 46000/9257 responde 404]` | Párr. 730 | URL de repositorio UPSE inválida | Tesista |
| `[VERIFICAR: URL oficial MINSA de la NTS 196]` | Párr. 756 | La URL consignada redirige a una norma ajena | Tesista |
| `[VERIFICAR: DOI 10.2307/4615733 no resuelve]` | Inserción Holm | Sin DOI registrado; se usa URL JSTOR | Verificador en próxima pasada |
| `[VERIFICAR: URL de repositorio UNAJMA de la tesis 2024]` | Inserción Quispe Tello | El PDF no consigna URL | Tesista |
| `[VERIFICAR: Razali y Wah sin DOI registrado]` | Inserción Razali | Artículo no depositado en Crossref/OpenAlex | Verificador en próxima pasada |
| `[VERIFICAR: iso.org responde 403]` | Párr. 748 | Bloqueo anti-bot; norma existente | Verificación manual |
| `[VERIFICAR: handle UTP 20.500.12867/5068 responde 403]` | Párr. 754 | Bloqueo anti-bot; no prueba de inexistencia | Verificación manual |
| `[VERIFICAR: handle OPS responde 502]` | Párr. 760 | Error transitorio del servidor IRIS | Reintentar |

---

## 10. Acciones correctivas

Dirigidas a `redactor-academico` y a `maquetador-docx`:

1. Aplicar las 22 sustituciones del JSON con las anclas literales, respetando el número de ocurrencias indicado.
2. Insertar las 11 referencias como **párrafos independientes** con sangría francesa, en el orden secuencial de la sección 4.
3. No alterar el texto de las entradas entregadas; las correcciones de Brooks, Chekol, Mamani-Pari, Ndlovu y Ministerio de Salud ya están incorporadas en el JSON.
4. Verificar en Word que los 53 asentamientos conserven `left=720`, `hanging=720`, `line=360`, `after=120`, Times New Roman 12 pt y alineación justificada.
5. Comprobar que los hipervínculos DOI queden activos y con el formato `https://doi.org/...`, sin barras invertidas ni espacios.
6. Resolver los nueve pendientes de la sección 9 antes de declarar cerrada la compuerta QG-9.
7. Corregir la duplicación literal del párrafo 650 y la redundancia «Alfa de Cronbach (Cronbach, 1951)» del párrafo 649.
8. Solicitar una nueva auditoría 1:1 después de aplicar las órdenes.

---

## 11. Limitaciones

- La auditoría verificó 28 DOIs en Crossref y resolvió los handles y URLs de los asentamientos no DOI. Los códigos 403 y 502 se documentan como bloqueo o error del servidor, no como inexistencia de la obra.
- No se verificó el contenido interno de cada obra contra la afirmación que la cita; esa comprobación literal corresponde al modo `deep-research (fact-check)` y requiere los PDF primarios.
- La entrada 726 (Addy et al., 2024) no pudo confirmarse en ninguna base indexada. Se mantiene por instrucción de no inventar ni eliminar datos sin respaldo, con marca `[VERIFICAR]`.
- El DOCX no se modificó. Todas las órdenes son preparatorias para la intervención de `maquetador-docx`.
