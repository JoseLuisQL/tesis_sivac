# -*- coding: utf-8 -*-
import io, sys, hashlib, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table

DOCX = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.docx"
OUT  = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04_texto_plano.md"

sha = hashlib.sha256(open(DOCX,'rb').read()).hexdigest()
size = os.path.getsize(DOCX)
doc = Document(DOCX)

def ptext(p):
    parts=[]
    for node in p.iter():
        tag=node.tag
        if tag==qn('w:t'):
            parts.append(node.text or '')
        elif tag==qn('w:tab'):
            parts.append('\t')
        elif tag in (qn('w:br'), qn('w:cr')):
            parts.append('\n')
    return ''.join(parts)

body = doc.element.body
children = list(body.iterchildren())
paras=[]; tables=[]
for ch in children:
    if ch.tag==qn('w:p'): paras.append((len(paras),ch))
    elif ch.tag==qn('w:tbl'): tables.append((len(tables),ch))

allp=[x[1] for x in paras]
def has_img(p):
    return p.find('.//'+qn('w:drawing')) is not None or p.find('.//'+qn('w:pict')) is not None
def caption_label(i):
    for j in range(i+1, min(i+4, len(allp))):
        t = ptext(allp[j]).strip()
        if t:
            m = re.match(r'^(Figura\s+A?\d+(?:\.\d+)?)', t)
            return m.group(1) if m else None
    return None

lines=[]
lines.append("# VOLCADO INTEGRO DE TEXTO - informe_final_v04.docx")
lines.append("")
lines.append("Documento auditado (solo lectura): `salidas/documentos/informe_final_v04.docx`")
lines.append("")
lines.append("- SHA-256: `%s`" % sha)
lines.append("- Tamano: %d bytes" % size)
lines.append("- Parrafos de nivel superior: %d (indices P0000-P%04d)" % (len(paras), len(paras)-1))
lines.append("- Tablas: %d (indices TABLA 0 a TABLA %d)" % (len(tables), len(tables)-1))
lines.append("- Imagenes en linea: 49")
lines.append("")
lines.append("## Convenciones")
lines.append("")
lines.append("- `[Pnnnn]`: parrafo de nivel superior con su indice exacto, en orden de documento, base 0. El texto sigue al rotulo; los tabuladores y saltos internos se conservan.")
lines.append("- `[TABLA n]`: posicion de la tabla n (base 0, misma numeracion que el informe de auditoria). Debajo se transcriben todas las celdas, fila por fila, separadas por ` | `.")
lines.append("- `[FIGURA n]`: posicion de una imagen en linea (orden de aparicion). Si existe rotulo del documento en los tres parrafos siguientes, se indica con `rotulo_documento=`.")
lines.append("- `[TOC]`: entradas del indice de contenido, alojadas en un bloque de contenido estructurado (w:sdt) que no forma parte de la numeracion P.")
lines.append("- El volcado reproduce el texto tal como esta almacenado: no corrige faltas, no normaliza espacios y no omite ningun parrafo, incluidos los vacios.")
lines.append("")
lines.append("---")
lines.append("")

def table_block(tb, idx):
    out=[]
    nrows=len(tb.rows); ncols=len(tb.columns)
    grid = tb._tbl.tblGrid
    widths=[]
    if grid is not None:
        for gc in grid.findall(qn('w:gridCol')):
            try: widths.append(int(gc.get(qn('w:w'))))
            except Exception: widths.append(0)
    out.append("[TABLA %d] %d filas x %d columnas; ancho de rejilla %d dxa" % (idx, nrows, ncols, sum(widths)))
    for r in tb.rows:
        cells=[]; seen=set()
        for c in r.cells:
            if id(c._tc) in seen: continue
            seen.add(id(c._tc))
            txt=' / '.join(ptext(p).strip() for p in c._tc.findall(qn('w:p')))
            cells.append(txt.replace('\n',' '))
        out.append("  " + " | ".join(cells))
    out.append("")
    return out

pidx={el:i for i,el in paras}
tidx={el:i for i,el in tables}
img_count=0
for ch in children:
    if ch.tag==qn('w:p'):
        i=pidx[ch]; t=ptext(ch)
        if has_img(ch):
            img_count+=1
            lab=caption_label(i)
            extra=(" rotulo_documento=%s" % lab) if lab else ""
            lines.append("[FIGURA %d]%s" % (img_count, extra))
            lines.append("[P%04d]" % i)
            if t.strip(): lines.append(t)
        elif t.strip()=='':
            lines.append("[P%04d]" % i)
        else:
            lines.append("[P%04d] %s" % (i, t))
    elif ch.tag==qn('w:tbl'):
        lines.extend(table_block(Table(ch, doc), tidx[ch]))
    elif ch.tag==qn('w:sdt'):
        ps=ch.findall('.//'+qn('w:p'))
        if ps:
            lines.append("[TOC] Entradas del indice de contenido (bloque w:sdt; campo TOC de niveles 1 a 3):")
            for p in ps:
                tt=ptext(p).replace('\n',' ').strip()
                if tt: lines.append("  [TOC] %s" % tt)
            lines.append("")

txt="\n".join(lines)+"\n"
open(OUT,'w',encoding='utf-8').write(txt)
print("written", OUT, len(txt), "chars")
print("paras", len(paras), "tables", len(tables), "images", img_count)
