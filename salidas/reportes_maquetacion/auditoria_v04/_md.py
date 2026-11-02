# -*- coding: utf-8 -*-
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

a = json.load(open('_audit_tmp.json', encoding='utf-8'))
P = a['paginas']; DF = a['defectos']; R = a['resumen']; M = a['meta']
byd = {}
for d in DF: byd.setdefault(d['pagina'], []).append(d)

doc = Document(M['documento'])
tstats = []
for i, t in enumerate([c for c in doc.element.body.iterchildren() if c.tag == qn('w:tbl')]):
    ws = [int(gc.get(qn('w:w'))) for gc in t.find(qn('w:tblGrid')).findall(qn('w:gridCol'))]
    tstats.append((i, len(t.findall(qn('w:tr'))), len(ws), sum(ws), min(ws), sum(ws)//len(ws)))

L = []
def w(s=''): L.append(s)

w('# Auditoría hoja por hoja del Informe Final v04')
w('')
w('**Documento auditado:** `salidas/documentos/informe_final_v04.docx` y su render `informe_final_v04.pdf`  ')
w('**Agente:** analista-documental (Squad A y E)  ')
w('**Fase:** F8_INTEGRACION_EDITORIAL  ')
w('**Fecha:** 2026-10-21  ')
w('**Referencia de contraste:** Fany_Tesis_Bachiller_2024.pdf (106 páginas)')
w('')
w('---')
w('')
w('## 1. Identificación y huella del documento')
w('')
w('| Atributo | Valor |')
w('|---|---|')
w('| SHA-256 del DOCX | `%s` |' % M['sha256'])
w('| Tamaño | %d bytes (%.2f MB) |' % (M['bytes'], M['bytes']/1048576))
w('| Páginas del PDF | 158 |')
w('| Párrafos de nivel superior | %d |' % R['parrafos_nivel_superior'])
w('| Tablas | %d |' % R['tablas'])
w('| Imágenes en línea | %d |' % R['imagenes_en_linea'])
w('| Ecuaciones OMML | %d |' % R['formulas_omml'])
w('| Tablas flotantes (w:tblpPr) | %d |' % R['tablas_con_tblpPr'])
w('| Filas con cantSplit | %d |' % R['filas_con_cantSplit'])
w('| Filas con tblHeader | %d |' % R['filas_con_tblHeader'])
w('| Secciones | 5 (la 3.ª horizontal) |')
w('| Páginas horizontales | 143, 144 y 145 |')
w('')
w('## 2. Método')
w('')
w('Se renderizaron las 158 páginas del PDF a 110 DPI con PyMuPDF (`salidas/reportes_maquetacion/auditoria_v04/p001.png` a `p158.png`), se inspeccionó cada página y se cruzó el resultado visual con el paquete OpenXML (`document.xml`, `styles.xml`, `numbering.xml`). La geometría se midió sobre la rejilla real de cada tabla (`w:tblGrid/w:gridCol`) y sobre las cajas de dibujo del PDF, comparándolas con la caja útil impresa:')
w('')
w('- Márgenes declarados: izquierdo 1 701 dxa (3.0 cm), derecho, superior e inferior 1 440 dxa (2.54 cm).')
w('- Caja útil vertical: 11 906 - 1 701 - 1 440 = **8 765 dxa** (15.46 cm).')
w('- Caja útil horizontal: 16 838 - 1 701 - 1 440 = **13 697 dxa** (24.16 cm).')
w('- En el PDF: límite izquierdo x = 85.05 pt, límite derecho x = 523.3 pt (vertical) y x = 769.92 pt (horizontal).')
w('')
w('Esquema de folios contrastado: páginas 1-3 sin folio (portada, acta, declaración); páginas 4-12 en romanos minúsculas ii-x; páginas 13-158 en arábigos 1-146, reiniciados en la Introducción y continuos hasta el final.')
w('')
w('## 3. Veredicto global')
w('')
w('| Métrica | Valor |')
w('|---|---|')
w('| Páginas revisadas | 158 |')
w('| Páginas CONFORMES | %d |' % R['paginas_conformes'])
w('| Páginas OBSERVADAS | %d |' % R['paginas_observadas'])
w('| Defectos registrados | %d |' % R['defectos_totales'])
w('| Críticos | %d |' % R['defectos_por_severidad'].get('critica', 0))
w('| Altos | %d |' % R['defectos_por_severidad'].get('alta', 0))
w('| Medios | %d |' % R['defectos_por_severidad'].get('media', 0))
w('| Bajos | %d |' % R['defectos_por_severidad'].get('baja', 0))
w('| Esquema de folios | %s |' % ('CONFORME en las 158 páginas' if R['folio_conforme'] else 'CON OBSERVACIONES'))
w('| Orden canónico de secciones | CONFORME |')
w('')
w('El orden canónico de la tesis se cumple sin inversiones: Portada, Acta, Declaración jurada, Dedicatoria, Agradecimientos, Índice de contenido, Índice de figuras, Índice de tablas, Resumen, Abstract, Chumasqa, Introducción, Capítulos I a VI, Conclusiones, Recomendaciones, Referencias y Anexos 1 a 7. Las deficiencias detectadas son de rotulación, numeración, geometría tabular y control de viudas, no de arquitectura capitular.')
w('')
w('## 4. Registro página por página')
w('')
w('| Pág. | Folio | Orientación | Esquema | Folio correcto | Defectos | Veredicto |')
w('|---|---|---|---|---|---|---|')
for x in P:
    n = len(byd.get(x['pagina'], []))
    w('| %d | %s | %s | %s | %s | %d | %s |' % (
        x['pagina'], x['folio_impreso'] or '-', x['orientacion'],
        'romano' if 'romano' in x['esquema_folio'] else ('sin folio' if 'sin_folio' in x['esquema_folio'] else 'arábigo'),
        'sí' if x['folio_correcto'] else 'no', n, x['veredicto']))
w('')
open('_md_part1.md', 'w', encoding='utf-8').write('\n'.join(L))
print('part1', len(L), 'lines')
