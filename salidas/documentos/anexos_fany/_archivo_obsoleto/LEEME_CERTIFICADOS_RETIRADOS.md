# CERTIFICADOS RETIRADOS DE LA RUTA OFICIAL

**Proyecto:** APLICACIÓN DEL SISTEMA “SIVAC” PARA MEJORAR LA GESTIÓN DE MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA DIRECCIÓN DE SALUD APURÍMAC II
**Tesista:** Bach. José Luis Quispe León
**Retiro registrado:** 2026-10-18
**Responsable del retiro:** agente `especialista-instrumentos` (Squad B)

---

## 1. Objeto de esta carpeta

Esta carpeta conserva, con fines exclusivamente históricos y de auditoría, los certificados de validez de contenido que estuvieron disponibles en la ruta oficial `salidas/documentos/anexos_fany/` y que fueron retirados por presentar defectos de construcción. Ningún archivo fue eliminado: todos se conservan íntegros y sin edición en esta ubicación.

La estructura definitiva de los certificados no se ha resuelto. Por esa razón no se ha generado ningún certificado sustituto y el generador que produjo estos documentos se encuentra bloqueado.

---

## 2. Primer conjunto: certificados de la variable dependiente (VD)

Archivos: `ANEXO_2_VALIDACION_FANY_VD_EXPERTO_1_VACIO.docx`, `ANEXO_2_VALIDACION_FANY_VD_EXPERTO_2_VACIO.docx` y `ANEXO_2_VALIDACION_FANY_VD_EXPERTO_3_VACIO.docx`.

Cada certificado presenta tres dimensiones con cuatro ítems por dimensión, doce en total. El conjunto se retiró por las razones siguientes.

- Los ítems de la dimensión 1 no traducen los indicadores del Instrumento 01. El ítem 3 mide un “tiempo total” y el ítem 4 mide la “atención de la demanda”; ninguna de esas dos magnitudes se registra en la ficha cronométrica, que consigna únicamente el tiempo de registro y el tiempo de emisión del vale.
- El ítem 2 de la dimensión 2 es un meta-ítem sobre la propia regla de auditoría de ocho criterios, no un reactivo sobre el atributo medido.
- Los ítems de la dimensión 3 son paráfrasis de aceptación del proceso y de utilidad percibida, no los enunciados literales del cuestionario TAM.
- Los Instrumentos 01 y 02 son fichas de registro, no escalas. El formato institucional con criterios dicotómicos Sí/No es aplicable a ítems de cuestionario, no a fichas de observación ni de cotejo documental.

---

## 3. Segundo conjunto: certificados de la variable independiente (VI)

Archivos: `ANEXO_2_VALIDACION_FANY_VI_EXPERTO_1_VACIO.docx`, `ANEXO_2_VALIDACION_FANY_VI_EXPERTO_2_VACIO.docx` y `ANEXO_2_VALIDACION_FANY_VI_EXPERTO_3_VACIO.docx`.

Cada certificado distribuye doce ítems entre adecuación funcional, eficiencia de desempeño, usabilidad y seguridad. El conjunto se retiró por las razones siguientes.

- No existe instrumento de recolección que respalde esos ítems. Ninguno de los tres instrumentos oficiales del proyecto los contiene y no se ha definido un cuarto instrumento.
- El paréntesis “(sin el sistema/tras la implantación del sistema SIVAC)”, aplicado a la variable independiente, produce una pregunta lógicamente irrespondible: indaga si SIVAC cumple sus funciones sin SIVAC.
- La variable independiente está definida como intervención dicotómica, sin dimensiones analíticas, de modo que no admite una matriz de ítems por dimensión.
- La norma ISO/IEC 25010:2023 no se acredita mediante juicio de contenido. Su verificación técnica, con métricas y evidencias, ya consta en la Tabla 8 del Capítulo III.

---

## 4. Tercer conjunto: archivos de una iteración anterior

Archivos: `ANEXO_2_VALIDACION_FANY_EXPERTO_1_VACIO.docx`, `ANEXO_2_VALIDACION_FANY_EXPERTO_2_VACIO.docx` y `ANEXO_2_VALIDACION_FANY_EXPERTO_3_VACIO.docx`.

Corresponden a una versión previa del generador, sin sufijo de variable en el nombre. Fueron retirados con anterioridad y arrastran los mismos defectos de contenido descritos en las secciones 2 y 3. Se conservan por trazabilidad documental.

---

## 5. Estado real de la validación por juicio de expertos

- La validación por juicio de expertos **no se ha ejecutado**. No existe acta, dictamen, calificación ni firma de ningún juez.
- La compuerta de calidad **QG-5 permanece abierta**.
- La fase **F6 permanece bloqueada** en tanto QG-5 no se cierre.
- No se han calculado coeficientes de validez de contenido sobre estos formatos, y no corresponde calcularlos: no hay evaluación real que procesar.
- El generador `scripts/compiladores/generar_anexo2_validacion_fany.py` produce hoy exactamente el contenido defectuoso aquí descrito. Su uso está bloqueado hasta que se resuelva la estructura definitiva.

---

## 6. Instrucción operativa

Los archivos de esta carpeta **no deben imprimirse, circular ni presentarse a ningún juez experto**, bajo ninguna circunstancia y con ningún propósito, incluidos el piloto, la prueba de formato o la demostración de avance.

Toda consulta sobre el contenido de estos archivos debe remitirse a esta nota. Toda decisión sobre la estructura sustituta corresponde al tesista, previa coordinación con el agente `guardian-consistencia`.
