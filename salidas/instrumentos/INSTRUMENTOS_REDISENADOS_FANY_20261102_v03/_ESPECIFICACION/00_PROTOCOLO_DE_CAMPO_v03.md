---
tipo: instrumento
fase: F8
agente: especialista-instrumentos
estado: borrador
fecha: 2026-11-02
---

# Protocolo de campo de los Instrumentos 1 y 2
## Sistema SIVAC, versión v03

### 1. Objetivo

Regula la aplicación de la Ficha de tiempos (Instrumento 1) y de la Ficha de auditoría documental (Instrumento 2), destinadas a medir la Variable Dependiente "Gestión de movimientos mensuales de vacunas" (DEC-027) en la DISA Apurímac II. El Instrumento 3 se rige por su propio instructivo.

### 2. Diseño, población y códigos

Diseño preexperimental de un solo grupo, con pretest y postest (O1 → X → O2). Población censal: N = n = 14 trabajadores de inmunizaciones en 13 centros de acopio.

- Fases: "Antes de SIVAC (pretest)" y "Con SIVAC (postest)", con los mismos escenarios y la misma carga fija.
- Códigos: participantes P01 a P14; centros C01 a C13.
- La lista maestra que vincula códigos y nombres la custodia el investigador, separada de las fichas.

### 3. Dimensiones e indicadores

1. Oportunidad de procesamiento: T_reg (tiempo de registro de movimientos) y T_vale (tiempo de emisión del vale), en minutos decimales.
2. Consistencia documental: RSD (documentos sin discrepancias) y CPE (despachos concordantes), en porcentaje.
3. Satisfacción del usuario: AP (aceptación del proceso) y UP (utilidad percibida), en puntos.

Cada dimensión se mide con su propio instrumento y ningún indicador se sustituye ni se estima a partir de otro.

En este protocolo, registro documental equivale al documento de movimiento auditado, y despacho equivale a la entrega efectuada al establecimiento destino.

### 4. Tareas cronometradas, carga fija y disparadores

Se cronometran seis tareas: tres de registro (REG-01, REG-02 y REG-03) y tres de emisión de vale (VALE-01, VALE-02 y VALE-03). Cada tarea se ejecuta una vez por fase y produce una observación destinada a su indicador.

| Código | Escenario | Carga fija | Inicio | Fin |
|---|---|---|---|---|
| REG-01 | Ingreso de lote | 1 biológico, 1 lote, 20 frascos | Recibe el lote y abre el kardex o el formulario | Cierra y firma el asiento, o confirma el guardado |
| REG-02 | Salida o transferencia a microred | 3 biológicos, 3 lotes, 30 frascos (10 por biológico) | Recibe la orden de salida y abre el registro | Cierra y firma el asiento, o confirma el guardado |
| REG-03 | Redistribución entre centros de acopio | 2 biológicos, 2 lotes, 20 frascos (10 por biológico) | Recibe la orden de redistribución y abre el registro | Cierra y firma el asiento, o confirma el guardado |
| VALE-01 | Vale de salida regular | 3 biológicos, 30 frascos | Recibe la solicitud de despacho | Genera y confirma el vale impreso o digital |
| VALE-02 | Vale de reposición urgente por contingencia de cadena de frío | 1 biológico, 10 frascos | Recibe la solicitud urgente | Genera y confirma el vale impreso o digital |
| VALE-03 | Vale de transferencia entre centros de acopio | 2 biológicos, 20 frascos | Recibe la solicitud de transferencia | Genera y confirma el vale impreso o digital |

La carga es fija. La carga real se verifica con el número de biológicos y de frascos; solo en REG-01 a REG-03 se verifica además el número de lotes. Si la carga real difiere de la fija, la tarea no es válida.

### 5. Repeticiones de tareas no válidas

Una tarea se anula si no se completó, si la carga real no fue la fijada o si medió una interrupción no registrada. La repetición se asienta en el registro de repeticiones de la página 2 de la Ficha 1, con el mismo código de escenario y el motivo.

De cada escenario se conserva el primer tiempo válido. Las repeticiones posteriores no se promedian, no se suman y no sustituyen a un tiempo ya válido.

### 6. Duración, pausa y validez

- Duración: minutos decimales, calculada como fin menos inicio. Conversión: minutos = horas × 60 + minutos + segundos ÷ 60. Anote el resultado con dos decimales.
- Pausa: interrupción no atribuible al procedimiento (atención a terceros, corte de energía o fuerza mayor). Se anota en minutos y se resta.
- Tiempo válido: duración menos pausa, con dos cifras decimales.
- Una interrupción externa que no impide completar la tarea se registra como pausa y se resta; una interrupción atribuible al procedimiento no se resta.
- Una tarea con tiempo válido igual o menor que cero se anula y se repite.

### 7. Criterios de conformidad documental (RSD)

Un documento es conforme solo si los ocho criterios están en Sí.

1. Biológico: nombre y presentación coinciden con el producto físico y el documento de origen.
2. Lote: el número asentado es idéntico al rotulado y al del documento de origen.
3. Vencimiento: mes y año coinciden con el rotulado.
4. Cantidad: dosis o frascos coinciden con el conteo físico.
5. Centro: código y denominación del establecimiento coinciden con el documento que autoriza.
6. Responsable: nombre, cargo y firma o sello de quien entrega y de quien recibe, legibles.
7. Saldo: saldo final = saldo inicial + ingresos − salidas, sin diferencia.
8. Correlatividad: fecha y hora del asiento son coherentes con el documento que autoriza y con el asiento previo.

Un solo No hace no conforme el documento. El motivo se consigna como el primer criterio marcado No.

### 8. Concordancia de despachos (CPE)

E es la cantidad entregada; P, la cantidad programada; D = E − P. El despacho es concordante solo si D = 0 y existe el documento que autoriza el despacho. Toda diferencia distinta de cero, por exceso o por defecto, es no concordante, y un despacho sin documento que autoriza también es no concordante aunque las cantidades coincidan. No existe diferencia autorizada ni compensación entre despachos. Si las unidades difieren, se convierten a dosis y se anota la equivalencia en Observación.

### 9. Ventana documental y corpus

- La ventana documental es de 30 días calendario, común a todas las fichas de auditoría de una misma fase.
- El corpus es de 40 a 60 entregas por ventana, distribuidas entre los 14 participantes según los movimientos que cada uno registró.
- La ficha de auditoría es por participante: el código P del encabezado atribuye todas las filas de la hoja.
- La suma de las filas auditadas de los 14 participantes debe situarse entre 40 y 60. El investigador verifica esta suma antes de cerrar la fase.
- Si un participante no registró entregas en la ventana, su CPE queda "no calculable" y no se imputa valor.

La página A audita los documentos que respaldan los movimientos de la misma ventana; la página B audita los despachos que integran el corpus.

### 10. Fórmulas y unidades

- T_reg = media aritmética de los tres tiempos válidos de REG-01, REG-02 y REG-03, en minutos decimales.
- T_vale = media aritmética de los tres tiempos válidos de VALE-01, VALE-02 y VALE-03, en minutos decimales.
- RSD = documentos conformes / documentos auditados × 100, en porcentaje.
- CPE = despachos concordantes / despachos auditados × 100, en porcentaje.
- AP = suma de AP-01 a AP-04, de 4 a 20 puntos.
- UP = suma de UP-01 a UP-04, de 4 a 20 puntos.

Cada participante recibe un valor por indicador. No se agrega un valor por indicador a partir de participantes con datos faltantes.

### 11. Reglas de incidencia

- Tarea no realizada: se anota "No realizada", no se imputa tiempo y se reprograma. Si un escenario queda sin tiempo válido, el indicador se informa como sin dato.
- Documento faltante: si no se ubica el asiento, se anota "No ubicado" y no se cuenta como auditado; si falta un respaldo de un asiento existente, se marcan No los criterios que no puedan verificarse.
- Despacho sin documento que autoriza: se audita y es no concordante aunque las cantidades coincidan; se anota "sin documento".
- Participante sin entregas en la ventana: CPE "no calculable", sin imputación.
- Ningún campo se completa con valores supuestos, promedios ni copias.

### 12. Orden de aplicación

1. Consentimiento informado.
2. Ficha de tiempos, durante la ejecución de las seis tareas.
3. Ficha de auditoría, sobre la ventana documental de 30 días.
4. Cuestionario de satisfacción, al cierre.

### 13. Anonimato y uso académico

Las fichas no llevan nombres, documentos de identidad ni datos clínicos; solo emplean los códigos P y C. La lista maestra se guarda aparte y se destruye al terminar el informe. Los datos se usan solo para esta investigación.

### 14. Nota de producción

Los dos instrumentos se imprimen en A4 vertical, sin páginas horizontales. Márgenes: izquierdo 3.0 cm; superior, derecho e inferior 2.5 cm; ancho útil 15.5 cm. Times New Roman 10 pt en el cuerpo y 9.5 pt en las tablas, sin fuente menor a 9.5 pt. Rejilla visible en los formularios. Encabezado con dos logotipos simétricos. No se admiten ecuaciones OMML dentro de celdas ni la reducción de columnas, criterios o contenido para ajustar el formato (DEC-026).

### Pendientes de alineación del informe

1. El informe v20 (p. 95) describe tres escenarios; la v03 fija seis tareas agrupadas en dos indicadores, conforme a DEC-021. La sección debe actualizarse en la etapa siguiente.
2. La Tabla 47 del informe define la CPE como cantidad entregada sobre cantidad programada; la v03 emplea despachos concordantes sobre despachos auditados, conforme a la Ecuación 4 y a DEC-021. La tabla y su nota deben corregirse.
3. La Tabla 48 del informe parafrasea los reactivos AP y UP; la v03 conserva los ocho literales de DEC-019. Los enunciados deben restituirse literalmente.
4. El informe v20 exige ICC(2,1) y kappa de Cohen para las Fichas 1 y 2; DEC-023 autoriza la revisión de contenido de las hojas D1 y D2. La vía de acreditación debe armonizarse en el informe.
5. La ventana de 30 días y el corpus de 40 a 60 entregas quedan fijados por DEC-021 y no son materia de decisión del investigador. El informe debe eliminar toda formulación que los presente como pendientes.
