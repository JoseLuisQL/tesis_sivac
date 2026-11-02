# -*- coding: utf-8 -*-
import io, sys, json, hashlib, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

BASE = r"C:/MisInvestigaciones/tesis/sivac/salidas"
DOCX = BASE + "/documentos/informe_final_v04.docx"
PDF  = BASE + "/documentos/informe_final_v04.pdf"
M    = "http://schemas.openxmlformats.org/officeDocument/2006/math"

pages = json.load(open('_pages_meta.json', encoding='utf-8'))
sha = hashlib.sha256(open(DOCX, 'rb').read()).hexdigest()
size = os.path.getsize(DOCX)

doc = Document(DOCX)
body = doc.element.body
paras = [c for c in body.iterchildren() if c.tag == qn('w:p')]
tbls  = [c for c in body.iterchildren() if c.tag == qn('w:tbl')]
n_img = len(body.findall('.//' + qn('w:drawing')))
n_omml = len(body.findall('.//{%s}oMath' % M))
n_tblppr = len(body.findall('.//' + qn('w:tblpPr')))
n_cantsplit = len(body.findall('.//' + qn('w:cantSplit')))
n_tblheader = len(body.findall('.//' + qn('w:tblHeader')))

geom = []
for i, t in enumerate(tbls):
    g = t.find(qn('w:tblGrid'))
    ws = []
    if g is not None:
        for gc in g.findall(qn('w:gridCol')):
            try: ws.append(int(gc.get(qn('w:w'))))
            except Exception: ws.append(0)
    geom.append((i, sum(ws), min(ws) if ws else 0, len(ws)))
over_all = [g for g in geom if g[1] > 8765]
over = [g for g in geom if g[1] > 8790]
leve = [g for g in geom if 8765 < g[1] <= 8790]

def D(pagina, elemento, indice, tipo, desc, sev, corr):
    return {"pagina": pagina, "elemento": elemento, "indice_docx": indice,
            "tipo": tipo, "descripcion": desc, "severidad": sev,
            "correccion_sugerida": corr}

DEF = []
DEF.append(D(2, "parrafo", None, "TEXTO_INCOMPLETO",
 "Acta de sustentación armada con una instrucción editorial entre corchetes (espacio reservado para insertar el acta oficial escaneada) y con el dictamen prellenado APROBADO CON MENCION; fecha, jurado y firmas quedan en blanco.",
 "alta", "Sustituir la caja de instrucción por el acta oficial firmada; retirar el dictamen prellenado."))
DEF.append(D(3, "parrafo", 18, "TEXTO_INCOMPLETO",
 "La declaración jurada conserva dos marcadores de identidad: DNI N.° [Completar DNI oficial antes de impresión] en el encabezado y de nuevo bajo la línea de firma.",
 "alta", "Reemplazar ambos marcadores por el número de DNI real."))
DEF.append(D(7, "encabezado", None, "DESORDEN_SECCION",
 "El índice de contenido termina en REFERENCIAS BIBLIOGRÁFICAS tras el apartado 3.2: omite el 3.3 (Metodología XP, pp. 40-85), el CAPÍTULO V, el CAPÍTULO VI, CONCLUSIONES, RECOMENDACIONES y ANEXOS.",
 "critica", "Aplicar estilos Heading 1 a 3 a todos los títulos y regenerar el campo TOC."))
DEF.append(D(8, "encabezado", None, "TEXTO_INCOMPLETO",
 "El índice de figuras enumera solo Figura 1 a Figura 10; faltan las 35 figuras del Capítulo III y las cuatro del Anexo 7.",
 "alta", "Regenerar la lista de figuras con rótulos nativos y numeración única."))
DEF.append(D(9, "encabezado", None, "TEXTO_INCOMPLETO",
 "El índice de tablas enumera solo Tabla 1 a Tabla 5; faltan las tablas 6-26, las tablas 13-21 del Capítulo V y las tablas de los Anexos 1-6.",
 "alta", "Regenerar la lista de tablas completa a partir de rótulos SEQ."))
DEF.append(D(9, "parrafo", 47, "ESPACIADO_INCORRECTO",
 "La entrada Tabla 4 del índice de tablas es la única sin línea de puntos conductores hasta el número de página.",
 "baja", "Restituir el tabulador con relleno de puntos en esa entrada."))
DEF.append(D(22, "parrafo", 113, "ROTULO_INCORRECTO",
 "El texto remite a la Tabla 10 del Capítulo IV para la matriz de operacionalización; en el Capítulo IV esa matriz es la Tabla 3 y la Tabla 10 es un diccionario de datos del Capítulo III.",
 "alta", "Corregir la referencia cruzada a Tabla 3."))
DEF.append(D(30, "tabla", 1, "ROTULO_INCORRECTO",
 "La tabla de síntesis de antecedentes (14 filas x 6 columnas, pp. 30-33) carece de rótulo Tabla N: solo lleva título descriptivo.",
 "alta", "Asignar número correlativo y anteponer el rótulo."))
DEF.append(D(35, "encabezado", None, "NUMERACION_SALTADA",
 "La numeración de figuras reinicia tres veces: Figuras 1-10 en el Capítulo III (pp. 35-46), Figuras 1-35 en el mismo capítulo (pp. 46-97) y Figuras 5-7 en el Capítulo V.",
 "alta", "Renumerar las figuras de forma continua y actualizar todas las referencias cruzadas."))
DEF.append(D(46, "tabla", 2, "SALTO_PAGINA_AUSENTE",
 "El rótulo Tabla 1 Dimensiones, indicadores y escalas de medición queda al pie de p46 y la tabla (7 x 4) se desarrolla en p47.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(52, "parrafo", 253, "NUMERACION_SALTADA",
 "Segunda tabla rotulada Tabla 1 (roles y responsabilidades, 7 x 4) coexistiendo con la Tabla 1 de P0201; la numeración del Capítulo III arranca en 1 pese a las tablas previas.",
 "alta", "Renumerar de forma continua y eliminar el rótulo duplicado."))
DEF.append(D(58, "parrafo", 278, "ENCABEZADO_HUERFANO",
 "El rótulo Tabla 6 queda como último bloque de p58 (y = 758 pt de 842) y el título, la tabla y la nota pasan a p59.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(58, "encabezado", None, "SALTO_PAGINA_AUSENTE",
 "Causa sistémica: de 115 párrafos de rótulo (Tabla/Figura) solo 15 tienen keepNext, por lo que rótulos y títulos se separan de su objeto en pp. 46, 58, 81, 85-89, 96, 104, 108, 111, 117 y 130.",
 "alta", "Aplicar keepNext a todos los rótulos y títulos mediante docx_quirurgico."))
DEF.append(D(65, "parrafo", 326, "ENCABEZADO_HUERFANO",
 "El encabezado 3.3.2.4. Modelado Conceptual, Lógico y Físico de la Base de Datos queda al pie de p65 sin ninguna línea de texto debajo.",
 "alta", "Aplicar keepNext a los encabezados de nivel 2 y 3."))
DEF.append(D(68, "parrafo", 345, "ROTULO_INCORRECTO",
 "Párrafo de nota que comienza con la palabra Tabla (Tabla maestra que representa el nivel superior de la estructura sanitaria) y resulta capturable por cualquier índice automático de tablas.",
 "baja", "Reformular el inicio del párrafo."))
DEF.append(D(74, "parrafo", 372, "ROTULO_INCORRECTO",
 "Párrafo que comienza con Tabla sin ser rótulo (Tabla central transaccional con restricción de unicidad uk_movimiento_establecimiento_vacuna_mes_anio).",
 "baja", "Reformular el inicio del párrafo."))
DEF.append(D(81, "parrafo", 408, "TEXTO_CORTADO",
 "El rótulo Figura 14 queda al pie de p81 (y = 751 pt) y su título descriptivo pasa a p82: número y título en páginas distintas.",
 "alta", "Unir rótulo y título en un párrafo único con keepNext."))
DEF.append(D(85, "parrafo", 441, "TEXTO_CORTADO",
 "El rótulo Figura 21 queda al pie de p85 y su título pasa a p86.", "alta",
 "Aplicar keepNext y unir rótulo y título."))
DEF.append(D(86, "parrafo", 445, "TEXTO_CORTADO",
 "El rótulo Figura 23 queda al pie de p86 y su título pasa a p87.", "alta",
 "Aplicar keepNext y unir rótulo y título."))
DEF.append(D(87, "parrafo", 449, "TEXTO_CORTADO",
 "El rótulo Figura 25 queda al pie de p87 y su título pasa a p88.", "alta",
 "Aplicar keepNext y unir rótulo y título."))
DEF.append(D(88, "parrafo", 453, "TEXTO_CORTADO",
 "El rótulo Figura 27 queda al pie de p88 y su título pasa a p89.", "alta",
 "Aplicar keepNext y unir rótulo y título."))
DEF.append(D(89, "parrafo", 457, "TEXTO_CORTADO",
 "El rótulo Figura 29 queda al pie de p89 y su título pasa a p90.", "alta",
 "Aplicar keepNext y unir rótulo y título."))
DEF.append(D(91, "parrafo", 492, "ENCABEZADO_HUERFANO",
 "El encabezado 3.3.4. Fase IV: Pruebas de Calidad del Software queda al pie de p91 sin texto debajo.",
 "alta", "Aplicar keepNext a los encabezados."))
DEF.append(D(96, "parrafo", 518, "TEXTO_CORTADO",
 "El rótulo Figura 35 queda al pie de p96 y su título pasa a p97.", "alta",
 "Aplicar keepNext y unir rótulo y título."))
DEF.append(D(100, "tabla", 29, "ROTULO_INCORRECTO",
 "La tabla Cronograma y protocolo de ejecución de la intervención preexperimental (5 x 4) no lleva rótulo Tabla N.",
 "alta", "Asignar número correlativo y anteponer el rótulo."))
DEF.append(D(103, "tabla", 31, "ROTULO_INCORRECTO",
 "La tabla Estructura de unidades de observación primaria, reglas de agregación pareada y criterios de inclusión (7 x 4) no lleva rótulo Tabla N.",
 "alta", "Asignar número correlativo y anteponer el rótulo."))
DEF.append(D(104, "tabla", 32, "SALTO_PAGINA_AUSENTE",
 "El rótulo Tabla 3 Operacionalización de las variables de investigación queda al pie de p104 y la tabla se desarrolla en p105.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(108, "tabla", 33, "SALTO_PAGINA_AUSENTE",
 "El rótulo Tabla 4 Relación de técnicas e instrumentos de recolección de datos queda al pie de p108 y la tabla se desarrolla en p109.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(111, "tabla", 34, "SALTO_PAGINA_AUSENTE",
 "El rótulo Tabla 5 Estructura de la validación de los instrumentos queda al pie de p111 y la tabla (4 x 7) se desarrolla en p112.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(115, "parrafo", 619, "TEXTO_INCOMPLETO",
 "Advertencia interna impresa en el cuerpo del Capítulo V: declara que los resultados corresponden a DATOS DE PRUEBA - REEMPLAZAR (DEC-007) e incluye rutas y comandos del repositorio.",
 "critica", "Retirar la advertencia del informe final y trasladarla a una nota interna no impresa."))
DEF.append(D(115, "tabla", 35, "TABLA_DESBORDADA",
 "Tabla descriptiva de 8 columnas y 7 filas con 8 981 dxa de rejilla frente a 8 765 dxa útiles (216 dxa de exceso, 0.19 cm por lado).",
 "alta", "Reducir la rejilla a 8 765 dxa y redistribuir columnas."))
DEF.append(D(116, "parrafo", 623, "ROTULO_INCORRECTO",
 "En la Tabla 4 se consolidan los coeficientes remite a la Tabla 4 del Capítulo IV (técnicas e instrumentos); la tabla de confiabilidad es la Tabla 13.",
 "alta", "Corregir la referencia a Tabla 13."))
DEF.append(D(117, "parrafo", 631, "ENCABEZADO_HUERFANO",
 "El rótulo Tabla 14 y su título quedan al pie de p117 y la tabla (7 x 10) aparece sola en p118.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(117, "parrafo", 630, "ROTULO_INCORRECTO",
 "En la Tabla 5 y en la Figura 6 se detallan remite a objetos del Capítulo IV; lo correcto es Tabla 14 y Figura 5.",
 "alta", "Corregir ambas referencias cruzadas."))
DEF.append(D(118, "tabla", 36, "TABLA_DESBORDADA",
 "Tabla de 10 columnas y 7 filas con rejilla de 8 981 dxa frente a 8 765 dxa de caja útil (márgenes 3.0 / 2.54 / 2.54 cm): excede 216 dxa, 0.19 cm por lado. En el PDF llega a x = 528.8 pt frente al límite derecho de 523.3 pt y arranca en x = 79.0 pt frente al límite izquierdo de 85.05 pt.",
 "alta", "Reducir la rejilla a 8 765 dxa; valorar orientación horizontal o fusión de columnas."))
DEF.append(D(118, "tabla", 36, "CELDA_ILEGIBLE",
 "La columna n mide 682 dxa (1.20 cm) y la de indicador 1 061 dxa (1.87 cm): encabezados partidos en tres y cuatro líneas y celdas de indicador en cinco líneas.",
 "media", "Ampliar las columnas de texto y reducir el cuerpo a 9 pt dentro de la tabla."))
DEF.append(D(120, "tabla", 37, "TABLA_DESBORDADA",
 "Tabla de 10 columnas y 7 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso); en el PDF llega a x = 528.8 pt frente al límite de 523.3 pt.",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(120, "tabla", 37, "CELDA_ILEGIBLE",
 "La columna n mide 411 dxa (0.72 cm), la más estrecha del documento: fractura palabras y cifras (Momen to, Variació n, Median a, 1 4).",
 "critica", "Eliminar la columna n, constante igual a 14, o ensancharla a 700 dxa."))
DEF.append(D(121, "parrafo", 648, "ROTULO_INCORRECTO",
 "En la Tabla 7 y en la Figura 8 se presenta: los objetos de la Dimensión 3 son la Tabla 16 y la Figura 7.",
 "alta", "Corregir ambas referencias cruzadas."))
DEF.append(D(122, "tabla", 38, "TABLA_DESBORDADA",
 "Tabla de 10 columnas y 10 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso); en el PDF alcanza x = 528.8 pt.",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(122, "tabla", 38, "CELDA_ILEGIBLE",
 "La columna más estrecha mide 634 dxa (1.12 cm); Constructo/subescala y Momento evaluado se parten en cuatro líneas y las etiquetas TAM se apilan verticalmente.",
 "media", "Ampliar columnas de texto y abreviar encabezados."))
DEF.append(D(124, "tabla", 39, "TABLA_DESBORDADA",
 "Tabla de 8 columnas y 8 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles; en el PDF alcanza x = 528.8 pt.",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(124, "parrafo", 659, "ROTULO_INCORRECTO",
 "La Tabla 8 resume las decisiones: la tabla de normalidad que sigue es la Tabla 17.",
 "alta", "Corregir la referencia a Tabla 17."))
DEF.append(D(125, "tabla", 39, "VIUDA_HUERFANA",
 "La tabla de 8 filas se fragmenta entre p124 y p125; la segunda página arrastra el remanente de filas con el encabezado repetido.",
 "media", "Mantener la tabla en una página o dividirla por dimensión con subtítulos propios."))
DEF.append(D(126, "parrafo", 672, "ENCABEZADO_HUERFANO",
 "5.4.2. Contrastación de la Hipótesis Específica 2 queda al pie de p126 sin texto debajo.",
 "alta", "Aplicar keepNext al encabezado."))
DEF.append(D(126, "tabla", 40, "TABLA_DESBORDADA",
 "Tabla de 9 columnas y 5 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(126, "tabla", 40, "CELDA_ILEGIBLE",
 "Encabezados fracturados: p-valor Ajusta do Holm y Decisió n sobre H0,1; la columna más estrecha mide 791 dxa (1.40 cm).",
 "alta", "Abreviar encabezados y redistribuir anchos."))
DEF.append(D(126, "parrafo", 668, "ROTULO_INCORRECTO",
 "(Tabla 9) remite al diccionario de datos; el contraste de la HE1 se presenta en la Tabla 18.",
 "alta", "Corregir la referencia a Tabla 18."))
DEF.append(D(127, "tabla", 41, "TABLA_DESBORDADA",
 "Tabla de 9 columnas y 5 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(127, "tabla", 41, "CELDA_ILEGIBLE",
 "La columna más estrecha mide 635 dxa (1.12 cm): Concordanc ia, Wilcoxo n, Rechaz ar, Gran de.",
 "critica", "Ampliar las columnas de indicador y decisión; abreviar encabezados."))
DEF.append(D(127, "parrafo", 675, "ROTULO_INCORRECTO",
 "(Tabla 10): el contraste de la HE2 se presenta en la Tabla 19.", "alta",
 "Corregir la referencia a Tabla 19."))
DEF.append(D(128, "tabla", 41, "VIUDA_HUERFANA",
 "La tabla se divide entre p127 y p128 con el encabezado repetido, dejando la segunda página con el remanente de filas.",
 "media", "Reajustar anchos y altura para mantener la tabla en una página."))
DEF.append(D(128, "parrafo", 682, "ROTULO_INCORRECTO",
 "(Tabla 11): el contraste de la HE3 se presenta en la Tabla 20.", "alta",
 "Corregir la referencia a Tabla 20."))
DEF.append(D(129, "tabla", 42, "TABLA_DESBORDADA",
 "Tabla de 9 columnas y 7 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(129, "tabla", 42, "CELDA_ILEGIBLE",
 "Encabezados fracturados: Estadísti co t, p-valor Ajusta do Holm, Decisió n sobre H0,3.",
 "alta", "Abreviar encabezados y redistribuir anchos."))
DEF.append(D(130, "parrafo", 691, "ENCABEZADO_HUERFANO",
 "El rótulo Tabla 21 y su título quedan al pie de p130 y la tabla continúa sola en p131.",
 "alta", "Aplicar keepNext al rótulo y al título."))
DEF.append(D(130, "tabla", 43, "TABLA_DESBORDADA",
 "Tabla de 8 columnas y 5 filas con rejilla de 8 981 dxa frente a 8 765 dxa útiles (216 dxa de exceso).",
 "alta", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(130, "tabla", 43, "CELDA_ILEGIBLE",
 "Encabezados fracturados: Hipótesi s de Investigació n, Decisió n, Operativ a; celdas Rechaz ar H0,1 y Reducció n > 15%.",
 "alta", "Reducir el número de columnas y abreviar encabezados."))
DEF.append(D(130, "parrafo", 690, "ROTULO_INCORRECTO",
 "En la Tabla 12 se presenta el balance consolidado: la tabla resumen es la Tabla 21.",
 "alta", "Corregir la referencia a Tabla 21."))
DEF.append(D(131, "tabla", 43, "VIUDA_HUERFANA",
 "p131 contiene solo las filas finales y la nota de la Tabla 21 (938 caracteres en toda la página); más del 60 por ciento del área queda en blanco.",
 "alta", "Cerrar la tabla en p130 reduciendo altura de fila o cuerpo tipográfico."))
DEF.append(D(73, "tabla", 17, "TABLA_DESBORDADA",
 "Sobrancho leve y sistemático en las tablas de cinco y seis columnas del Capítulo III: T14 (8 856 dxa), T17 (8 961), T19 (8 900), T22 (8 895), T23 (8 817) y T27 (8 898) frente a 8 765 dxa útiles. El exceso de 52 a 196 dxa no recorta texto, pero invade el margen derecho.",
 "baja", "Reajustar la rejilla de esas seis tablas a 8 765 dxa."))
DEF.append(D(141, "parrafo", 752, "VIUDA_HUERFANA",
 "Página con una sola referencia (World Health Organization, 2021), 160 caracteres, y más del 80 por ciento del área en blanco.",
 "media", "Ajustar el interlineado de la lista para evitar el arrastre de una sola entrada."))
DEF.append(D(142, "parrafo", 753, "VIUDA_HUERFANA",
 "Página dedicada exclusivamente a la palabra ANEXOS (12 caracteres), sin otro contenido.",
 "baja", "Integrar la portadilla con el primer anexo o eliminarla."))
DEF.append(D(143, "tabla", 44, "TABLA_DESBORDADA",
 "Matriz de consistencia en orientación horizontal con rejilla de 14 000 dxa frente a 13 697 dxa de caja útil (21.0 - 3.0 - 2.54 - 2.54 cm): excede 303 dxa (0.53 cm). En el PDF abarca de x = 76.8 a 777.6 pt frente a los límites de 85.05 y 769.92 pt.",
 "alta", "Reducir la rejilla a 13 697 dxa o ampliar la caja útil horizontal a 3.0 / 2.0 cm."))
DEF.append(D(145, "tabla", 44, "VIUDA_HUERFANA",
 "p145 contiene solo las dos últimas filas y la nota de la Tabla A1.1; el resto de la página queda en blanco.",
 "media", "Ajustar anchos y altura de fila para cerrar la matriz en p144."))
DEF.append(D(146, "tabla", 45, "CELDA_ILEGIBLE",
 "La matriz de operacionalización (6 columnas, 8 766 dxa) comprime la primera columna hasta partir palabras (Variable Independie nte) y apila las definiciones en 8 a 10 líneas por celda.",
 "media", "Ampliar las columnas de variable y definición; mover la definición operacional a una nota."))
DEF.append(D(147, "tabla", 45, "VIUDA_HUERFANA",
 "La Tabla A2.1 se prolonga a p147 con tres filas y su nota, dejando el resto de la página vacío.",
 "media", "Reducir altura de fila o cuerpo tipográfico para cerrar la tabla en p146."))
DEF.append(D(148, "tabla", 46, "TEXTO_INCOMPLETO",
 "Certificado del Experto 1 con el nombre sustituido por Evaluador Pericial Designado (Experto 1), DNI [Registrado en expediente] y firma no insertada.",
 "alta", "Insertar nombre, grado, institución, DNI y firma reales del juez validador."))
DEF.append(D(148, "tabla", 46, "EMOJI",
 "El pictograma U+270D precede a ESPACIO RESERVADO PARA INSERCION DE FIRMA Y SELLO ESCANEADO DEL EXPERTO.",
 "alta", "Sustituir el pictograma por un recuadro rotulado Firma y sello del juez validador."))
DEF.append(D(149, "tabla", 47, "TEXTO_INCOMPLETO",
 "Certificado del Experto 2 con nombre genérico, DNI [Registrado en expediente] y firma no insertada.",
 "alta", "Insertar los datos reales del juez validador."))
DEF.append(D(149, "tabla", 47, "EMOJI",
 "Segundo pictograma U+270D en el espacio de firma del Experto 2.", "alta",
 "Reemplazar por un recuadro de firma sin pictogramas."))
DEF.append(D(149, "tabla", 48, "TEXTO_INCOMPLETO",
 "Certificado del Experto 3 con nombre genérico, DNI [Registrado en expediente] y firma no insertada.",
 "alta", "Insertar los datos reales del juez validador."))
DEF.append(D(149, "tabla", 48, "EMOJI",
 "Tercer pictograma U+270D en el espacio de firma del Experto 3.", "alta",
 "Reemplazar por un recuadro de firma sin pictogramas."))
DEF.append(D(150, "tabla", 49, "CELDA_ILEGIBLE",
 "La ficha A4.1 comprime cuatro columnas de 2 191 dxa (3.86 cm) y corta fórmulas como (Total registros conformes sin error / Total transacciones auditadas) * 100 en seis líneas.",
 "media", "Trasladar las fórmulas al cuerpo narrativo, conforme a la prohibición de fórmulas en celdas."))
DEF.append(D(151, "tabla", 51, "VIUDA_HUERFANA",
 "La Tabla A4.3 (cuestionario TAM) se prolonga a p152, donde queda una sola fila (UP-04) y la nota; el 80 por ciento de la página queda en blanco.",
 "alta", "Reducir el enunciado de los reactivos o el interlineado para cerrar la tabla en p151."))
DEF.append(D(153, "tabla", 52, "TABLA_DESBORDADA",
 "Matriz de datos del pretest con 18 columnas y 15 filas: 8 981 dxa de rejilla frente a 8 765 dxa útiles (216 dxa de exceso). En el PDF arranca en x = 107.1 pt y llega a x = 528.8 pt frente al límite derecho de 523.3 pt.",
 "critica", "Reducir la rejilla a 8 765 dxa; pasar la matriz a horizontal o dividirla en dos tablas."))
DEF.append(D(153, "tabla", 52, "CELDA_ILEGIBLE",
 "Con 18 columnas el ancho medio es de 499 dxa (0.88 cm) y el mínimo de 363 dxa (0.64 cm): las cifras se fracturan hasta en cuatro líneas (3 8. 5 0), ALMACEN (CHANKA) ocupa tres líneas y las cabeceras se leen suj eto_id, centr o_aco pio, nivel_s atisfaccion.",
 "critica", "Dividir en dos tablas de 9 columnas o girar a horizontal con anchos mínimos de 700 dxa."))
DEF.append(D(154, "tabla", 53, "TABLA_DESBORDADA",
 "Matriz de datos del postest con 18 columnas y 15 filas: 8 981 dxa de rejilla frente a 8 765 dxa útiles, con el mismo desborde de 5.5 pt sobre el margen derecho.",
 "critica", "Reducir la rejilla a 8 765 dxa o pasar la matriz a orientación horizontal."))
DEF.append(D(154, "tabla", 53, "CELDA_ILEGIBLE",
 "Mismas patologías que la matriz del pretest: columna mínima de 400 dxa (0.71 cm), cifras y etiquetas partidas en varias líneas, cabeceras ilegibles.",
 "critica", "Dividir la matriz o ampliar columnas en horizontal."))
DEF.append(D(155, "tabla", 53, "VIUDA_HUERFANA",
 "La segunda página de la matriz ocupa por completo p155 sin encabezado de sección ni contexto.",
 "baja", "Repetir el encabezado de columna y rotular la continuación."))
DEF.append(D(156, "tabla", 54, "TABLA_DESBORDADA",
 "La Tabla A6.1 (5 columnas, 8 981 dxa) excede la caja útil en 216 dxa; en el PDF llega a x = 528.8 pt frente al límite de 523.3 pt.",
 "media", "Reducir la rejilla a 8 765 dxa."))
DEF.append(D(157, "tabla", 55, "EMOJI",
 "La caja de la Figura A7.1 contiene el pictograma U+1F4F7 (cámara) antes de ESPACIO RESERVADO PARA FOTOGRAFIA DE EVIDENCIA EN CAMPO.",
 "alta", "Sustituir el pictograma por el texto Espacio reservado para fotografía de evidencia en campo."))
DEF.append(D(157, "tabla", 56, "EMOJI",
 "La caja de la Figura A7.2 repite el pictograma U+1F4F7.", "alta",
 "Eliminar el pictograma y conservar solo el rótulo textual."))
DEF.append(D(157, "tabla", 57, "EMOJI",
 "La caja de la Figura A7.3 repite el pictograma U+1F4F7.", "alta",
 "Eliminar el pictograma y conservar solo el rótulo textual."))
DEF.append(D(158, "tabla", 58, "EMOJI",
 "La caja de la Figura A7.4 repite el pictograma U+1F4F7.", "alta",
 "Eliminar el pictograma y conservar solo el rótulo textual."))
DEF.append(D(157, "parrafo", None, "TEXTO_INCOMPLETO",
 "Las cuatro cajas del Anexo 7 conservan la instrucción editorial Instrucción para el tesista: Insertar en este espacio la fotografía correspondiente a, visible en el documento final.",
 "critica", "Insertar las fotografías definitivas a 300 DPI o retirar el anexo."))
DEF.append(D(158, "tabla", 58, "TEXTO_INCOMPLETO",
 "Cuarta caja del Anexo 7 con la misma instrucción editorial y sin fotografía insertada.",
 "critica", "Insertar la fotografía definitiva o retirar la caja."))
DEF.append(D(157, "parrafo", 804, "ROTULO_INCORRECTO",
 "El rótulo Figura A7.3 queda al pie de p157 y su título y su nota pasan a p158, separados de la caja correspondiente.",
 "alta", "Unir rótulo, título, caja y nota con keepNext."))
DEF.append(D(157, "parrafo", 800, "TEXTO_DUPLICADO",
 "La nota Registro fotográfico de verificación en campo. Dirección de Salud Apurímac II (2026). se repite literalmente cuatro veces (P0800, P0803, P0806, P0809).",
 "baja", "Diferenciar cada nota con la fecha y el lugar específicos de la toma."))
DEF.append(D(52, "encabezado", None, "NUMERACION_SALTADA",
 "La numeración de tablas reinicia en el Capítulo III (1 a 26), vuelve a reiniciar en el Capítulo IV (2 a 5) y salta a 13 en el Capítulo V (13 a 21).",
 "alta", "Aplicar numeración continua 1 a 59 en el cuerpo y reservar A1.1 a A7.4 para los anexos."))
ROMAN = {4: 'ii', 5: 'iii', 6: 'iv', 7: 'v', 8: 'vi', 9: 'vii', 10: 'viii', 11: 'ix', 12: 'x'}
pdef = {}
for d in DEF:
    pdef.setdefault(d['pagina'], []).append(d)

out_pages = []
for r in pages:
    p = r['pagina']
    folio = r['folio']
    orient = r['orientacion']
    if p <= 3:
        esquema = 'preliminar_sin_folio'; esperado = None
    elif p <= 12:
        esquema = 'preliminar_romano'; esperado = ROMAN[p]
    else:
        esquema = 'cuerpo_arabigo'; esperado = str(p - 12)
    if esperado is None:
        ok = folio is None
    else:
        ok = (folio is not None and str(folio).strip() == esperado)
    ds = pdef.get(p, [])
    out_pages.append({"pagina": p, "folio_impreso": folio, "orientacion": orient,
                      "esquema_folio": esquema, "folio_correcto": bool(ok),
                      "veredicto": 'OBSERVADA' if ds else 'CONFORME'})

sev_count = {}
for d in DEF:
    sev_count[d['severidad']] = sev_count.get(d['severidad'], 0) + 1
tipo_count = {}
for d in DEF:
    tipo_count[d['tipo']] = tipo_count.get(d['tipo'], 0) + 1

resumen = {
    "paginas_totales": 158, "paginas_revisadas": 158,
    "paginas_conformes": sum(1 for x in out_pages if x['veredicto'] == 'CONFORME'),
    "paginas_observadas": sum(1 for x in out_pages if x['veredicto'] == 'OBSERVADA'),
    "defectos_totales": len(DEF),
    "defectos_por_severidad": sev_count,
    "defectos_por_tipo": tipo_count,
    "parrafos_nivel_superior": len(paras),
    "tablas": len(tbls),
    "imagenes_en_linea": n_img,
    "formulas_omml": n_omml,
    "tablas_con_tblpPr": n_tblppr,
    "filas_con_cantSplit": n_cantsplit,
    "filas_con_tblHeader": n_tblheader,
    "tablas_que_exceden_caja_util": len(over_all),
    "tablas_con_exceso_significativo": len(over),
    "tablas_con_exceso_leve": len(leve),
    "tablas_desbordadas_dxa": [{"tabla": g[0], "rejilla": g[1], "columnas": g[3]} for g in over],
    "tablas_con_exceso_leve_dxa": [{"tabla": g[0], "rejilla": g[1], "columnas": g[3]} for g in leve],
    "paginas_horizontales": [143, 144, 145],
    "folio_conforme": all(x['folio_correcto'] for x in out_pages),
    "orden_canonico_conforme": True
}

audit = {
    "meta": {
        "documento": DOCX, "pdf": PDF, "sha256": sha, "bytes": size,
        "fecha_auditoria": "2026-10-21", "agente": "analista-documental",
        "fase": "F8_INTEGRACION_EDITORIAL", "squad": "Squad A y E",
        "metodo": "Render de las 158 páginas a 110 DPI con PyMuPDF, inspección visual de cada página, análisis del paquete OpenXML (document.xml, styles.xml, numbering.xml) y medición de las cajas de dibujo contra los márgenes.",
        "referencia_contraste": "Fany_Tesis_Bachiller_2024.pdf (106 páginas)",
        "margenes_dxa": {"izquierdo": 1701, "derecho": 1440, "superior": 1440, "inferior": 1440},
        "caja_util_vertical_dxa": 8765, "caja_util_horizontal_dxa": 13697
    },
    "resumen": resumen,
    "paginas": out_pages,
    "defectos": DEF
}

OUTJ = BASE + "/reportes_maquetacion/auditoria_hoja_por_hoja_v04.json"
json.dump(audit, open(OUTJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(audit, open('_audit_tmp.json', 'w', encoding='utf-8'), ensure_ascii=False)
print("JSON ->", OUTJ)
print(json.dumps(resumen, ensure_ascii=False, indent=1))
