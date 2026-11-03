---
tipo: instrumento
fase: F8
agente: especialista-forms
estado: borrador
fecha: 2026-11-02
---

# Diccionario de datos de los instrumentos SIVAC

## 1. Alcance

Este diccionario define la estructura tabular con la que se registran las respuestas de los tres instrumentos de recolección: la Ficha de tiempos, la Ficha de auditoría documental y el Cuestionario de satisfacción. Su finalidad es asegurar que la captura, la validación y el análisis posterior utilicen los mismos nombres, tipos y reglas de ausencia. El diccionario no contiene datos: todas las celdas de captura se emiten vacías.

## 2. Reglas de codificación

1. Una celda vacía significa que el dato no se realizó o no es aplicable. No se usan 0 ni 99 como códigos de ausencia.
2. No se imputan valores, promedios, valores de la fase opuesta ni datos supuestos.
3. RSD y CPE solo se calculan cuando el denominador correspondiente es mayor que cero.
4. AP y UP solo se calculan cuando los cuatro reactivos de la subescala están completos.
5. El valor 0 solo se admite cuando la medición efectiva sea cero; el valor 99 no se admite en ninguna variable.
6. Las fechas se registran en formato AAAA-MM-DD y los minutos en decimales con dos cifras.

## 3. Variables

| Variable | Etiqueta | Tipo | Unidad o escala | Valores admitidos | Fuente | Observaciones |
|---|---|---|---|---|---|---|
| id_participante | Código del participante | Texto | Código | P01 a P14 | Hoja de control de aplicación | Identifica al trabajador sin revelar su nombre. |
| centro | Código del centro de acopio | Texto | Código | C01 a C13 | Hoja de control de aplicación | Identifica el centro donde se aplica el instrumento. |
| fase | Momento de aplicación | Entero | Código | 1 = pretest; 2 = postest | Hoja de control de aplicación | Permite separar las dos mediciones del mismo participante. |
| fecha | Fecha de aplicación | Fecha | AAAA-MM-DD | Fecha calendario válida; vacía si no se aplicó | Ficha 1 y Ficha 2 | No se completa si la medición no se realizó. |
| reg_01 | Tiempo de registro de REG-01 | Decimal | Minutos | Mayor o igual que 0; vacía si no se realizó | Ficha 1 (tiempos) | Tiempo válido de la tarea REG-01, ingreso de lote. |
| reg_02 | Tiempo de registro de REG-02 | Decimal | Minutos | Mayor o igual que 0; vacía si no se realizó | Ficha 1 (tiempos) | Tiempo válido de la tarea REG-02, salida o transferencia a microred. |
| reg_03 | Tiempo de registro de REG-03 | Decimal | Minutos | Mayor o igual que 0; vacía si no se realizó | Ficha 1 (tiempos) | Tiempo válido de la tarea REG-03, redistribución entre centros de acopio. |
| vale_01 | Tiempo de emisión de VALE-01 | Decimal | Minutos | Mayor o igual que 0; vacía si no se realizó | Ficha 1 (tiempos) | Tiempo válido de la tarea VALE-01, vale de salida regular. |
| vale_02 | Tiempo de emisión de VALE-02 | Decimal | Minutos | Mayor o igual que 0; vacía si no se realizó | Ficha 1 (tiempos) | Tiempo válido de la tarea VALE-02, reposición urgente por contingencia. |
| vale_03 | Tiempo de emisión de VALE-03 | Decimal | Minutos | Mayor o igual que 0; vacía si no se realizó | Ficha 1 (tiempos) | Tiempo válido de la tarea VALE-03, transferencia entre centros de acopio. |
| t_reg | Tiempo medio de registro | Decimal | Minutos | Mayor o igual que 0; vacía si falta alguna observación | Derivada | Requiere reg_01, reg_02 y reg_03. |
| t_vale | Tiempo medio de emisión del vale | Decimal | Minutos | Mayor o igual que 0; vacía si falta alguna observación | Derivada | Requiere vale_01, vale_02 y vale_03. |
| doc_auditados | Documentos auditados | Entero | Conteo | Mayor o igual que 0; vacía si no se auditó | Ficha 2 (auditoría) | No incluye documentos no ubicados. |
| doc_conformes | Documentos conformes | Entero | Conteo | De 0 a doc_auditados; vacía si no se auditó | Ficha 2 (auditoría) | Solo cuenta documentos con los ocho criterios en Sí. |
| rsd | Registros sin discrepancias | Decimal | Porcentaje | De 0 a 100; vacía si doc_auditados es 0 | Derivada | Se informa como porcentaje. |
| desp_auditados | Despachos auditados | Entero | Conteo | Mayor o igual que 0; vacía si no se auditó | Ficha 2 (auditoría) | Incluye los despachos sin documento que autoriza, que se registran como no concordantes. |
| desp_concordantes | Despachos concordantes | Entero | Conteo | De 0 a desp_auditados; vacía si no se auditó | Ficha 2 (auditoría) | Solo cuenta despachos con diferencia igual a cero y documento que autoriza. |
| cpe | Concordancia programada frente a entregada | Decimal | Porcentaje | De 0 a 100; vacía si desp_auditados es 0 | Derivada | Se informa como porcentaje. |
| ap_01 | Aceptación del proceso, reactivo 1 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal AP-01 de DEC-019. |
| ap_02 | Aceptación del proceso, reactivo 2 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal AP-02 de DEC-019. |
| ap_03 | Aceptación del proceso, reactivo 3 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal AP-03 de DEC-019. |
| ap_04 | Aceptación del proceso, reactivo 4 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal AP-04 de DEC-019. |
| up_01 | Utilidad percibida, reactivo 1 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal UP-01 de DEC-019. |
| up_02 | Utilidad percibida, reactivo 2 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal UP-02 de DEC-019. |
| up_03 | Utilidad percibida, reactivo 3 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal UP-03 de DEC-019. |
| up_04 | Utilidad percibida, reactivo 4 | Entero | Likert 1 a 5 | 1, 2, 3, 4 o 5; vacía si no se respondió | Instrumento 3 | Enunciado literal UP-04 de DEC-019. |
| ap | Puntaje de aceptación del proceso | Entero | Puntos | De 4 a 20; vacía si falta algún reactivo AP | Derivada | Suma de los cuatro reactivos AP. |
| up | Puntaje de utilidad percibida | Entero | Puntos | De 4 a 20; vacía si falta algún reactivo UP | Derivada | Suma de los cuatro reactivos UP. |
| observaciones | Observaciones de la aplicación | Texto | Texto libre | Texto; vacía si no hay incidencia | Hoja de control de aplicación | Registra incidencias, repeticiones y motivos de anulación. |

## 4. Fórmulas

Las fórmulas se expresan con texto y no con objetos OMML. Se ubican fuera de la tabla para no alterar su estructura.

- T_reg = (reg_01 + reg_02 + reg_03) / 3.
- T_vale = (vale_01 + vale_02 + vale_03) / 3.
- RSD = doc_conformes / doc_auditados × 100.
- CPE = desp_concordantes / desp_auditados × 100.
- AP = ap_01 + ap_02 + ap_03 + ap_04.
- UP = up_01 + up_02 + up_03 + up_04.

## 5. Control de calidad

Antes de cerrar la base de datos se verifica lo siguiente:

1. Que las tres observaciones de cada indicador existan cuando se reporte T_reg o T_vale; si falta una, el promedio no se calcula.
2. Que el denominador de RSD y de CPE sea mayor que cero antes de calcular el porcentaje.
3. Que los valores Likert de ap_01 a ap_04 y de up_01 a up_04 estén entre 1 y 5.
4. Que no haya celdas con 0 o 99 usadas como código de ausencia.
5. Que doc_conformes no exceda doc_auditados y que desp_concordantes no exceda desp_auditados.
6. Que id_participante pertenezca al rango P01 a P14 y centro al rango C01 a C13.
7. Que cada participante tenga como máximo un registro por fase.

---

**Nota de producción.** Documento interno de especificación. Formato A4 vertical, margen izquierdo de 3.0 cm y márgenes superior, derecho e inferior de 2.5 cm, Times New Roman de 9.5 a 10 pt, tabla de 15.5 cm de ancho útil; si la tabla no cabe en una página, continúa en páginas sucesivas. Prohibido el A4 horizontal y la fuente menor a 9.5 pt. La tabla de variables no contiene fórmulas ni objetos OMML.
