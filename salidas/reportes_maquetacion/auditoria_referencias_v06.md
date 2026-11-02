# AUDITORÍA DE CORRESPONDENCIA CITA-REFERENCIA - INFORME FINAL v06

**Documento auditado:** `salidas/documentos/informe_final_v06.docx` (813 párrafos, 59 tablas).  
**Fecha:** 2026-10-21.  
**Fase:** F8_INTEGRACION_EDITORIAL.  
**Agente:** verificador-integridad (Squad A, Inteligencia Bibliográfica y Evidencia).  
**Modalidad:** lectura del DOCX y emisión de órdenes. El documento no se modificó.  
**Insumos:** lista de Referencias del cuerpo (párrafos 726 a 767), cuerpo narrativo y tablas (párrafos 0 a 724), cuatro fuentes previamente verificadas por el Director General.

---

## 1. Dictamen general

**REQUIERE_AJUSTE.**

La lista de Referencias contiene 42 asentamientos. El cuerpo cita cuatro obras que no figuran en ella: Venkatesh et al. (2003), Rosenthal (1991), George y Mallery (2003) y Hernández-Sampieri y Mendoza (2018). Las cuatro están efectivamente citadas, por lo que procede su inserción. Con las cuatro inserciones la lista pasaría a 46 asentamientos.

Subsisten, además, diez citas en el texto sin asentamiento bibliográfico y dos referencias que nunca se citan en el cuerpo. Ninguna de las cuatro fuentes nuevas se inserta dos veces: se verificó que no existieran ya bajo otra grafía.

| Métrica | Resultado |
|---|---|
| Referencias existentes antes de la inserción | 42 |
| Inserciones ordenadas | 4 |
| Referencias después de la inserción | 46 |
| Citas en el texto sin referencia (huérfanas) | 10 |
| Referencias sin cita en el texto | 2 |
| Correspondencia 1:1 tras la inserción | 44 de 46 referencias citadas; 10 citas distintas sin asentamiento |

---

## 2. Estructura de la lista de Referencias

- El rótulo `REFERENCIAS BIBLIOGRÁFICAS` ocupa el párrafo 725.
- Los asentamientos ocupan los párrafos 726 a 767, uno por párrafo, en orden alfabético.
- Todos los asentamientos revisados usan el estilo `Normal` con `w:ind left="720" hanging="720"`, `w:line="360"`, `w:after="120"`, alineación justificada y Times New Roman de 12 pt.
- El último asentamiento de la lista es World Health Organization (2021), en el párrafo 767.

---

## 3. Órdenes de inserción

Las órdenes completas, con ancla literal y texto nuevo, están en `salidas/reportes_maquetacion/referencias_v06_ordenes.json`.

| # | Entrada nueva | Párrafo ancla | Posición alfabética | Cita que la exige |
|---|---|---|---|---|
| 1 | George, D., y Mallery, P. (2003) | 742 | Entre Garcia Villacorta (2023) y Gilbert et al. (2020) | (George & Mallery, 2003), párrafo 650 |
| 2 | Hernández-Sampieri, R., y Mendoza, C. P. (2018) | 745 | Después de Hernández-Sampieri et al. (2014) y antes de Hussain et al. (2025) | (Hernández-Sampieri & Mendoza, 2018), párrafo 650 |
| 3 | Rosenthal, R. (1991) | 761 | Entre Pressman (2010) y Ruiz Barea (2023) | (Rosenthal, 1991), párrafo 637; usos de r de Rosenthal en 683, 686, 689 y 692 |
| 4 | Venkatesh, V., Morris, M. G., Davis, G. B., y Davis, F. D. (2003) | 765 | Entre Tristán-López (2008) y Wasswa et al. (2023) | (Venkatesh et al., 2003), párrafo 713 |

**Advertencia de maquetación.** El aplicador sustituye spans dentro de párrafos existentes. El salto de línea intra-párrafo no crea un párrafo nuevo: la segunda entrada comparte el `pPr` del ancla y su primera línea no recibe el tratamiento de sangría francesa como párrafo independiente. Se recomienda que `maquetador-docx` convierta el salto en un párrafo nuevo con el mismo `pPr` (left 720, hanging 720, line 360, after 120) o verifique el resultado en Word antes de dar por cerrada la compuerta. Asimismo, la sustitución del span completo del ancla puede reescribir los runs del asentamiento previo: debe comprobarse que su URL conserve el hipervínculo activo y que el DOI de Rosenthal y el de Venkatesh queden como hipervínculos `https://doi.org/...`.

---

## 4. Matriz de citas auditadas

### 4.1 Referencias existentes

| Párrafo | Referencia | Cita en el cuerpo (párrafos) | Estado |
|---|---|---|---|
| 726 | Addy et al. (2024) | 260, 327 | Citada |
| 727 | Alvarez Ticllasuca et al. (2023) | 159 | Citada |
| 728 | Arisholm et al. (2007) | Ninguna | **No citada** |
| 729 | Astuhuaman Perez y Baltazar Maza (2023) | 216, 272 | Citada |
| 730 | Balón Morejón (2023) | 157, 210, 236 | Citada |
| 731 | Beck (1999) | 173, 242, 245 | Citada |
| 732 | Brooks et al. (2024) | 155 | Citada |
| 733 | Champi Velásquez (2023) | 159, 219, 259 | Citada |
| 734 | Chekol et al. (2023) | 156, 274, 278 | Citada |
| 735 | Cohen (1988) | 177, 620, 637 | Citada |
| 736 | Cohn (2004) | 246, 311 | Citada |
| 737 | Dang et al. (2024) | 157, 208, 271 | Citada |
| 738 | Davis (1989) | 173, 280, 290 | Citada |
| 739 | De la Torre Llorente et al. (2010) | 231, 323 | Citada |
| 740 | Dolan et al. (2020) | Ninguna | **No citada** |
| 741 | Ergetie et al. (2023) | 156, 211 | Citada |
| 742 | Garcia Villacorta y Calderón Huaman (2023) | 159, 218, 260 | Citada |
| 743 | Gilbert et al. (2020) | 213, 265 | Citada |
| 744 | Gutiérrez-Aguado et al. (2024) | 158, 259 | Citada |
| 745 | Hernández-Sampieri et al. (2014) | 177, 551, 553 | Citada |
| 746 | Hussain et al. (2025) | 284, 290 | Citada |
| 747 | Inarotul Huda et al. (2025) | 214 | Citada |
| 748 | ISO/IEC (2023) | 173, 252, 551 | Citada |
| 749 | Kigenza et al. (2023) | 157, 209, 265 | Citada |
| 750 | Kokol (2022) | 242 | Citada |
| 751 | Luján Mora (2002) | 230, 234 | Citada |
| 752 | Luo et al. (2024) | 217, 280, 283 | Citada |
| 753 | Mamani-Pari et al. (2026) | 220, 253 | Citada |
| 754 | Mego Navarro (2021) | 158, 217, 236 | Citada |
| 755 | Mekonen et al. (2024) | 156, 275, 299 | Citada |
| 756 | Ministerio de Salud del Perú (2022) | 158, 212, 219 | Citada |
| 757 | Moumane et al. (2024) | 253, 256 | Citada |
| 758 | Ndlovu et al. (2021) | 285 | Citada |
| 759 | Oliveira et al. (2020) | 285, 288 | Citada |
| 760 | OPS y PATH (2020) | 155, 265, 325 | Citada |
| 761 | Pressman (2010) | 246, 250, 307 | Citada |
| 762 | Ruiz Barea (2023) | 237, 303, 313 | Citada |
| 763 | Shen et al. (2024) | 157, 207, 266 | Citada |
| 764 | Sommerville (2016) | 231, 236, 240 | Citada |
| 765 | Tristán-López (2008) | 177, 625, 627 | Citada |
| 766 | Wasswa et al. (2023) | 157, 212, 265 | Citada |
| 767 | World Health Organization (2021) | 155, 259 | Citada |

### 4.2 Referencias que se insertan

| Párrafo destino | Referencia | Cita en el cuerpo (párrafos) | Estado |
|---|---|---|---|
| 742 | George y Mallery (2003) | 650 | Citada, sin asentamiento |
| 745 | Hernández-Sampieri y Mendoza (2018) | 650 | Citada, sin asentamiento |
| 761 | Rosenthal (1991) | 637, 683, 686, 689, 692 | Citada, sin asentamiento |
| 765 | Venkatesh et al. (2003) | 713 | Citada, sin asentamiento |

---

## 5. Citas en el texto sin referencia (huérfanas)

| # | Cita | Párrafo | Observación |
|---|---|---|---|
| 1 | Cronbach (1951) | 649 | Coeficiente alfa de Cronbach citado con año; no hay asentamiento de Cronbach en la lista. |
| 2 | Feldt (1965) | 649 | Método de intervalo de confianza citado con año; se repite en las notas de los párrafos 650 y 652. |
| 3 | Shapiro-Wilk (1965) | 677 | Prueba de normalidad citada como si fuera obra; se repite en el párrafo 681. |
| 4 | Razali & Wah (2011) | 677 | Afirmación sobre potencia de la prueba sin asentamiento. |
| 5 | Wilcoxon (1945) | 679 | Prueba de rangos con signo citada con año; no hay asentamiento. |
| 6 | Holm (1979) | 683 | Corrección de Holm-Bonferroni citada con año; no hay asentamiento. |
| 7 | Fany (2024) | 630 | Formato institucional de validación atribuido a Fany (2024); no figura en la lista. |
| 8 | OMS y UNICEF (2021) | 711 | Evidencia internacional atribuida conjuntamente a OMS y UNICEF; la lista solo tiene World Health Organization (2021) y ningún asentamiento de UNICEF. |
| 9 | Mamani (2023) | 711 | Estudio de Puno con la cifra de 76.4%; no coincide con Mamani-Pari et al. (2026). Posible confusión de autor y año. |
| 10 | Rojas y Vargas (2022) | 712 | Estudio de Lima con la cifra de 84.5%; no figura en la lista. |

Las citas 1 a 6 corresponden a métodos estadísticos epónimos. Si la tesis no cita las obras originales, debe optarse por una de dos vías: incorporar el asentamiento primario o eliminar el año y tratar el rótulo como nombre de la prueba, sin formato de cita. Las citas 7 a 10 respaldan afirmaciones sustantivas y cifras concretas; su falta de asentamiento es la inconsistencia de mayor riesgo.

---

## 6. Referencias sin cita en el texto

| # | Referencia | Párrafo | Observación |
|---|---|---|---|
| 1 | Arisholm et al. (2007). Evaluating pair programming with respect to system complexity and programmer expertise. IEEE Transactions on Software Engineering, 33(2), 65-86. https://doi.org/10.1109/TSE.2007.17 | 728 | No aparece en el cuerpo ni en tablas. Referencia decorativa. |
| 2 | Dolan et al. (2020). Perceptions of factors influencing the introduction and adoption of electronic immunization registries in Tanzania and Zambia: A mixed methods study. Implementation Science Communications, 1(1), Artículo 38. https://doi.org/10.1186/s43058-020-00022-8 | 740 | No aparece en el cuerpo ni en tablas. Referencia decorativa. |

---

## 7. Clasificación de inconsistencias

### Críticas
1. Citas 8, 9 y 10 de la sección 5: OMS y UNICEF (2021), Mamani (2023) y Rojas y Vargas (2022) sostienen cifras y evidencia internacional sin asentamiento trazable. Constituyen aserciones huérfanas con datos cuantitativos.
2. Cita 7 de la sección 5: Fany (2024) se presenta como fuente normativa del formato de validación sin entrada en Referencias.

### Mayores
1. Cuatro obras citadas sin asentamiento: Venkatesh et al. (2003), Rosenthal (1991), George y Mallery (2003) y Hernández-Sampieri y Mendoza (2018). Se subsanan con las órdenes de la sección 3.
2. Dos referencias sin cita: Arisholm et al. (2007) y Dolan et al. (2020).
3. Citas metodológicas con año sin asentamiento: Cronbach (1951), Feldt (1965), Shapiro-Wilk (1965), Razali & Wah (2011), Wilcoxon (1945) y Holm (1979).

### Menores
1. El cuerpo cita `Ministerio de Salud, 2022` y la lista registra `Ministerio de Salud del Perú (2022)`. Conviene uniformar la primera mención con la denominación completa y la sigla.
2. En el párrafo 713 la NTS N.° 196-MINSA/DGIESP-2022 se cita por número normativo dentro del paréntesis, en lugar del formato autor-año que corresponde a su asentamiento.
3. La entrada de Venkatesh et al. (2003) usa guion simple en el rango de páginas `425-478`; el resto de la lista usa guion largo. Se conservó el texto entregado por el Director.
4. La entrada de Hernández-Sampieri y Mendoza (2018) incluye ISBN, dato que APA 7 no exige. Se conservó el texto entregado.
5. El párrafo 650 contiene una duplicación literal de la cláusula sobre el umbral .800 y las referencias a la Tabla 4 y a la Tabla 35. Es un defecto de redacción ajeno a la lista, pero afecta la lectura de las dos citas nuevas.

---

## 8. Verificación de formato APA 7 de las entradas nuevas

| Párrafo ancla | Sangría francesa | Interlineado | Fuente | Espaciado posterior | Alineación | Hereda formato |
|---|---|---|---|---|---|---|
| 742 | left 720 / hanging 720 (1.27 cm) | 360 (1.5) | Times New Roman 12 pt | 120 (6 pt) | Justificada | Sí |
| 745 | left 720 / hanging 720 (1.27 cm) | 360 (1.5) | Times New Roman 12 pt | 120 (6 pt) | Justificada | Sí |
| 761 | left 720 / hanging 720 (1.27 cm) | 360 (1.5) | Times New Roman 12 pt | 120 (6 pt) | Justificada | Sí |
| 765 | left 720 / hanging 720 (1.27 cm) | 360 (1.5) | Times New Roman 12 pt | 120 (6 pt) | Justificada | Sí |

Los cuatro párrafos ancla cumplen el formato de la regla 03. La salvedad es la indicada en la sección 3: el salto intra-párrafo no genera sangría francesa autónoma para la entrada insertada.

---

## 9. Acciones correctivas

Dirigidas a `redactor-academico`:

1. Aplicar las cuatro inserciones con las anclas literales del JSON. No alterar el texto de las entradas entregadas.
2. Resolver las citas 8, 9 y 10 de la sección 5 antes de cualquier compuerta: aportar el asentamiento verificable de OMS y UNICEF (2021), Mamani (2023) y Rojas y Vargas (2022), o retirar la atribución y la cifra. Si Mamani (2023) es en realidad Mamani-Pari et al. (2026), corregir autor y año en el párrafo 711 y verificar que el dato de 76.4% conste en esa obra.
3. Resolver Fany (2024): incorporarla a Referencias como tesis modelo UNAJMA o reformular la mención como formato institucional sin formato de cita.
4. Para Cronbach (1951), Feldt (1965), Shapiro-Wilk (1965), Razali & Wah (2011), Wilcoxon (1945) y Holm (1979): incorporar las obras primarias o eliminar el año del rótulo metodológico. La decisión debe ser uniforme en todo el documento.
5. Citar Arisholm et al. (2007) en la sección de Extreme Programming (programación por pares) o retirarla de la lista. Citar Dolan et al. (2020) en el marco de adopción de registros electrónicos de inmunización o retirarla.
6. Uniformar `Ministerio de Salud del Perú` y la cita de la NTS en el párrafo 713.
7. Corregir la duplicación literal del párrafo 650.
8. Tras aplicar los cambios, solicitar nueva auditoría 1:1 y la verificación de que cada entrada insertada quedó como párrafo independiente con sangría francesa.

---

## 10. Limitaciones de la auditoría

- Las cuatro fuentes insertadas fueron entregadas como ya verificadas por el Director General; no se repitió su búsqueda.
- No se re-resolvieron en línea los DOI y URL de los 42 asentamientos existentes. La auditoría cubre correspondencia 1:1, grafía autor-año y formato APA 7, no la resolución remota de cada identificador.
- La detección de citas combinó extracción automatizada y revisión manual de las 129 cadenas candidatas, con descarte de falsos positivos por apellidos compuestos (Balón Morejón, Mego Navarro, Champi Velásquez, Garcia Villacorta, Astuhuaman Perez).
- El conteo de referencias se hizo sobre el texto de los párrafos 726 a 767; no se contaron entradas dentro de tablas porque la lista es narrativa.
