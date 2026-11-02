# -*- coding: utf-8 -*-
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

a = json.load(open('_audit_tmp.json', encoding='utf-8'))
DF = a['defectos']; R = a['resumen']; M = a['meta']
tm = json.load(open('_tblmap.json', encoding='utf-8'))
tpage = {x['t']: x['page'] for x in tm}; tpage[0] = 2

doc = Document(M['documento'])
tstats = []
for i, t in enumerate([c for c in doc.element.body.iterchildren() if c.tag == qn('w:tbl')]):
    ws = [int(gc.get(qn('w:w'))) for gc in t.find(qn('w:tblGrid')).findall(qn('w:gridCol'))]
    tstats.append({"t": i, "rows": len(t.findall(qn('w:tr'))), "cols": len(ws),
                   "grid": sum(ws), "min": min(ws), "mean": sum(ws)//len(ws),
                   "page": tpage.get(i)})
json.dump(tstats, open('_tstats.json', 'w', encoding='utf-8'), ensure_ascii=False)

L = []
def w(s=''): L.append(s)

w('## 5. Defectos por tipo')
w('')
w('| Tipo | Cantidad | Páginas afectadas |')
w('|---|---|---|')
for tipo, n in sorted(R['defectos_por_tipo'].items(), key=lambda kv: (-kv[1], kv[0])):
    pgs = sorted({d['pagina'] for d in DF if d['tipo'] == tipo})
    txt = ', '.join(str(p) for p in pgs[:14]) + (', ...' if len(pgs) > 14 else '')
    w('| %s | %d | %s |' % (tipo, n, txt))
w('')
w('## 6. Defectos críticos')
w('')
w('Se registran %d defectos de severidad crítica. Ninguno de ellos es un error de redacción: son fallas que impiden la impresión oficial del documento o inducen a error al lector.' % R['defectos_por_severidad'].get('critica', 0))
w('')
for d in [x for x in DF if x['severidad'] == 'critica']:
    w('- **p%d, %s%s** (%s): %s' % (d['pagina'], d['elemento'],
      (' n.º %d' % d['indice_docx']) if d['indice_docx'] is not None else '',
      d['tipo'], d['descripcion']))
    w('  - Corrección: %s' % d['correccion_sugerida'])
w('')
w('## 7. Geometría de las tablas')
w('')
w('La rejilla se midió directamente sobre `w:tblGrid`. Se consideran desbordadas las tablas cuya suma de columnas excede la caja útil; se separa el exceso significativo (más de 25 dxa, es decir, más de 0.04 cm) del desajuste de redondeo.')
w('')
w('| Tabla | Filas | Cols. | Rejilla dxa | Exceso dxa | Ancho medio | Col. mínima |')
w('|---|---|---|---|---|---|---|')
for s in sorted([x for x in tstats if x['grid'] > 8790], key=lambda x: -x['grid']):
    lim = 13697 if s['t'] == 44 else 8765
    w('| T%02d | %d | %d | %d | %+d | %d | %d |' % (
        s['t'], s['rows'], s['cols'], s['grid'], s['grid'] - lim, s['mean'], s['min']))
w('')
w('Catorce tablas más presentan un exceso de 19 a 25 dxa (0.03 a 0.04 cm), atribuible al redondeo de Word al declarar el ancho de tabla: T00, T01, T02, T03, T04, T07, T13, T29, T30, T31, T32, T33, T34 y T45. Ese desajuste no recorta texto, pero conviene normalizarlo a 8 765 dxa en la misma cirugía.')
w('')
w('### 7.1 Tablas de 10 columnas (T36, T37, T38)')
w('')
w('Las tres tablas de la Dimensión 1 y 2 comparten la misma rejilla de 8 981 dxa con 10 columnas. El exceso de 216 dxa se reparte 0.19 cm por lado y en el PDF se materializa en un desplazamiento de 6 pt sobre el margen izquierdo y 5.5 pt sobre el derecho. La columna más comprometida es la de tamaño muestral: 682 dxa en T36, 411 dxa en T37 y 634 dxa en T38. Con 411 dxa (0.72 cm) el texto se fractura a media palabra (Momen to, Variació n, Median a, 1 4).')
w('')
w('### 7.2 Tablas de 8 y 9 columnas (T39 a T43)')
w('')
w('T39 (8 columnas), T40, T41 y T42 (9 columnas) y T43 (8 columnas) repiten la rejilla de 8 981 dxa. Las columnas de decisión estadística caen por debajo de 800 dxa y los encabezados se parten en tres líneas: p-valor Ajusta do Holm, Decisió n sobre H0,1, Hipótesi s de Investigació n. En T41 la columna más estrecha mide 635 dxa y en T40, 791 dxa.')
w('')
w('### 7.3 Matriz de consistencia en horizontal (T44)')
w('')
w('La Tabla A1.1 mide 14 000 dxa exactos (24.69 cm) sobre una caja útil de 13 697 dxa. El exceso de 303 dxa (0.53 cm) hace que la tabla sobresalga 8.25 pt por la izquierda y 7.7 pt por la derecha del área imprimible. Ninguna celda desborda su propia columna, pero el conjunto invade los márgenes laterales de la sección horizontal.')
w('')
w('### 7.4 Matrices de datos de 18 columnas (T52 y T53)')
w('')
w('Las matrices del pretest y del postest son el punto más débil del documento. Con 18 columnas sobre 8 981 dxa, el ancho medio es de 499 dxa (0.88 cm) y el mínimo de 363 dxa (0.64 cm) en T52 y 400 dxa (0.71 cm) en T53. Las etiquetas de centro de acopio ocupan tres líneas, las cifras se separan del entero (3 8. 5 0) y las cabeceras quedan ilegibles (suj eto_id, centr o_aco pio, nivel_s atisfaccion). La tabla arranca en x = 107.1 pt, muy lejos del margen, porque Word centra el excedente.')
w('')
open('_md_part2.md', 'w', encoding='utf-8').write('\n'.join(L))
print('part2', len(L), 'lines')
