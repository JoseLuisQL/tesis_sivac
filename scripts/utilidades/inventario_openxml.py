# -*- coding: utf-8 -*-
"""inventario_openxml.py - Inspeccion OpenXML permanente y SOLO LECTURA."""
import argparse, hashlib, json, os, re, struct, zipfile
from datetime import datetime, timezone
from lxml import etree

NS = {
 'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
 'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
 'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
 'wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
 'pic':'http://schemas.openxmlformats.org/drawingml/2006/picture',
 'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
 'v':'urn:schemas-microsoft-com:vml',
}
W='{%s}'%NS['w']; R='{%s}'%NS['r']; WP='{%s}'%NS['wp']; A='{%s}'%NS['a']
TW=566.929; EMU=360000.0; PORT=8788

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def qn(tag):
    p,l=tag.split(':'); return '{%s}%s'%(NS[p],l)

def val(el,attr='w:val'):
    return None if el is None else el.get(qn(attr))

def onoff(el):
    if el is None: return None
    v=el.get(qn('w:val'))
    return True if v is None else v.lower() not in ('0','false','off')

def read_rpr(rpr):
    out={}
    if rpr is None: return out
    f=rpr.find(qn('w:rFonts'))
    if f is not None:
        out['font_ascii']=f.get(qn('w:ascii')) or f.get(qn('w:hAnsi'))
        out['font_hansi']=f.get(qn('w:hAnsi')); out['font_cs']=f.get(qn('w:cs'))
    for tag,key in (('w:sz','size_pt'),('w:szCs','size_cs_pt')):
        el=rpr.find(qn(tag))
        if el is not None:
            try: out[key]=int(val(el))/2.0
            except (TypeError,ValueError): pass
    for tag,key in (('w:b','bold'),('w:i','italic'),('w:caps','caps'),('w:smallCaps','small_caps'),('w:strike','strike')):
        el=rpr.find(qn(tag))
        if el is not None: out[key]=onoff(el)
    for tag,key in (('w:u','underline'),('w:color','color')):
        el=rpr.find(qn(tag))
        if el is not None: out[key]=val(el)
    va=rpr.find(qn('w:vertAlign'))
    if va is not None: out['vert_align']=val(va)
    return out

def read_ppr(ppr):
    out={}
    if ppr is None: return out
    for tag,key in (('w:pStyle','pStyle'),('w:jc','jc')):
        el=ppr.find(qn(tag))
        if el is not None: out[key]=val(el)
    ind=ppr.find(qn('w:ind'))
    if ind is not None:
        for a in ('left','right','firstLine','hanging','start','end'):
            v=ind.get(qn('w:'+a))
            if v is not None: out['ind_'+a]=int(v)
    sp=ppr.find(qn('w:spacing'))
    if sp is not None:
        for a in ('line','lineRule','before','after','beforeLines','afterLines'):
            v=sp.get(qn('w:'+a))
            if v is not None: out['spacing_'+a]=v if a=='lineRule' else int(v)
    ol=ppr.find(qn('w:outlineLvl'))
    if ol is not None: out['outline_lvl']=int(val(ol))
    for tag,key in (('w:keepNext','keep_next'),('w:pageBreakBefore','page_break_before')):
        el=ppr.find(qn(tag))
        if el is not None: out[key]=onoff(el)
    num=ppr.find(qn('w:numPr'))
    if num is not None:
        out['num_id']=val(num.find(qn('w:numId'))); out['ilvl']=val(num.find(qn('w:ilvl')))
    return out

def effective(base,direct):
    d=dict(base or {}); d.update({k:v for k,v in (direct or {}).items() if v is not None}); return d

def para_text(p):
    parts=[]
    for node in p.iter():
        if node.tag==W+'t': parts.append(node.text or '')
        elif node.tag==W+'tab': parts.append('\t')
        elif node.tag in (W+'br',W+'cr'): parts.append('\n')
        elif node.tag==W+'noBreakHyphen': parts.append('-')
    return ''.join(parts)

def collect_fields(p,pid):
    out=[]
    for fs in p.iter(W+'fldSimple'):
        out.append({'paragraph':pid,'instr':fs.get(qn('w:instr')),'simple':True})
    for it in p.iter(W+'instrText'):
        if it.text and it.text.strip():
            s=it.text.strip()
            if not any((f.get('instr') or '').strip()==s for f in out):
                out.append({'paragraph':pid,'instr':s,'simple':False})
    return out

def collect_drawings(p,pid,rels):
    out=[]
    for dr in p.iter():
        if dr.tag in (WP+'inline',WP+'anchor'):
            kind='inline' if dr.tag==WP+'inline' else 'anchor'
            ext=dr.find(WP+'extent'); geom=None
            if ext is not None:
                try: geom={'width_cm':round(int(ext.get('cx'))/EMU,2),'height_cm':round(int(ext.get('cy'))/EMU,2)}
                except (TypeError,ValueError): pass
            for b in dr.iter(A+'blip'):
                rid=b.get(R+'embed')
                if not rid: continue
                info={'paragraph':pid,'kind':kind,'rel_id':rid,'geometry':geom}
                info.update(rels.get(rid,{})); out.append(info)
    for img in p.iter('{%s}imagedata'%NS['v']):
        rid=img.get(R+'id')
        info={'paragraph':pid,'kind':'vml','rel_id':rid,'geometry':None}
        info.update(rels.get(rid,{})); out.append(info)
    return out

def image_dims(data):
    try:
        if data[:8]==b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II',data[16:24])
        if data[:2]==b'\xff\xd8':
            i=2
            while i<len(data)-9:
                if data[i]!=0xFF: i+=1; continue
                m=data[i+1]
                if m in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF):
                    return int.from_bytes(data[i+7:i+9],'big'),int.from_bytes(data[i+5:i+7],'big')
                if m in (0xD8,0xD9) or 0xD0<=m<=0xD7: i+=2
                else: i+=2+int.from_bytes(data[i+2:i+4],'big')
            return None
        if data[:6] in (b'GIF87a',b'GIF89a'):
            return int.from_bytes(data[6:8],'little'),int.from_bytes(data[8:10],'little')
        if data[:2]==b'BM':
            return int.from_bytes(data[18:22],'little'),int.from_bytes(data[22:26],'little')
    except Exception: pass
    return None

def read_rels(z,part):
    rp=os.path.dirname(part)+'/_rels/'+os.path.basename(part)+'.rels'
    out={}
    if rp in z.namelist():
        root=etree.fromstring(z.read(rp))
        for rel in root:
            out[rel.get('Id')]={'rel_type':rel.get('Type').split('/')[-1],'target':rel.get('Target'),'external':rel.get('TargetMode')=='External'}
    return out

def read_sectpr(pr,rels):
    out={}
    if pr is None: return out
    pg=pr.find(qn('w:pgSz'))
    if pg is not None:
        try:
            w=int(pg.get(qn('w:w'))); h=int(pg.get(qn('w:h')))
            out.update(page_w_dxa=w,page_h_dxa=h,orientation=pg.get(qn('w:orient')) or ('landscape' if w>h else 'portrait'),page_w_cm=round(w/TW,2),page_h_cm=round(h/TW,2))
        except (TypeError,ValueError): pass
    mar=pr.find(qn('w:pgMar'))
    if mar is not None:
        for a in ('top','right','bottom','left','header','footer','gutter'):
            v=mar.get(qn('w:'+a))
            if v is not None:
                try: out[a+'_dxa']=int(v); out[a+'_cm']=round(int(v)/TW,2)
                except ValueError: pass
    pn=pr.find(qn('w:pgNumType'))
    if pn is not None:
        out['pg_num_fmt']=pn.get(qn('w:fmt')); out['pg_num_start']=pn.get(qn('w:start'))
    tp=pr.find(qn('w:titlePg'))
    if tp is not None: out['title_pg']=onoff(tp)
    refs=[]
    for kind in ('headerReference','footerReference'):
        for el in pr.findall(qn('w:'+kind)):
            rid=el.get(R+'id')
            refs.append({'kind':kind.replace('Reference',''),'type':el.get(qn('w:type')) or 'default','rel_id':rid,'target':rels.get(rid,{}).get('target')})
    out['refs']=refs
    return out

def parse_styles(z):
    if 'word/styles.xml' not in z.namelist(): return {}, {}
    root=etree.fromstring(z.read('word/styles.xml'))
    dd={'rPr':{},'pPr':{}}
    ddel=root.find(qn('w:docDefaults'))
    if ddel is not None:
        rpr=ddel.find('.//'+qn('w:rPrDefault')+'/'+qn('w:rPr')); ppr=ddel.find('.//'+qn('w:pPrDefault')+'/'+qn('w:pPr'))
        if rpr is not None: dd['rPr']=read_rpr(rpr)
        if ppr is not None: dd['pPr']=read_ppr(ppr)
    styles={}
    for st in root.findall(qn('w:style')):
        sid=st.get(qn('w:styleId'))
        styles[sid]={'id':sid,'type':st.get(qn('w:type')),'name':val(st.find(qn('w:name'))),'basedOn':val(st.find(qn('w:basedOn'))),'rPr':read_rpr(st.find(qn('w:rPr'))),'pPr':read_ppr(st.find(qn('w:pPr')))}
    def resolve(sid,seen=None):
        seen=seen or set()
        if sid not in styles or sid in seen: return {'rPr':{},'pPr':{}}
        seen.add(sid); st=styles[sid]
        base=resolve(st.get('basedOn'),seen) if st.get('basedOn') else {'rPr':{},'pPr':{}}
        return {'rPr':{**base['rPr'],**st['rPr']},'pPr':{**base['pPr'],**st['pPr']}}
    return styles, {'docDefaults':dd,'resolved':{sid:resolve(sid) for sid in styles}}

def part_text(z,target):
    name='word/'+target.lstrip('/')
    if name not in z.namelist(): return None
    root=etree.fromstring(z.read(name)); lines=[]
    for p in root.iter(W+'p'):
        t=para_text(p).strip()
        if t: lines.append(t)
    return '\n'.join(lines)

def slug(path):
    return re.sub(r'[^A-Za-z0-9_-]+','_',os.path.splitext(os.path.basename(path))[0])

def build(docx_path,outdir,pdf_path=None):
    os.makedirs(outdir,exist_ok=True)
    src_sha=sha256_file(docx_path)
    z=zipfile.ZipFile(docx_path)
    root=etree.fromstring(z.read('word/document.xml'))
    body=root.find(qn('w:body'))
    rels=read_rels(z,'word/document.xml')
    styles,styles_ctx=parse_styles(z)
    media={}
    for name in z.namelist():
        if name.startswith('word/media/'):
            data=z.read(name); d=image_dims(data)
            media[name.replace('word/','')]={'bytes':len(data),'px_w':d[0] if d else None,'px_h':d[1] if d else None}
    for rid,r in rels.items():
        tgt=(r.get('target') or '').lstrip('/')
        if tgt.startswith('media/') and tgt in media: r.update(media[tgt])
        r['dpi_effective']=None
    paragraphs=[]; tables=[]; sections=[]; fields_all=[]; images_all=[]
    st={'para':0,'tbl':0,'sect':0}

    def new_para(p,container='body',cell_ref=None):
        pid='P%04d'%(st['para']+1)
        ppr=p.find(qn('w:pPr')); direct=read_ppr(ppr); sid=direct.get('pStyle')
        resolved=styles_ctx['resolved'].get(sid,{'pPr':{},'rPr':{}}) if sid else {'pPr':{},'rPr':{}}
        eff=effective(styles_ctx['docDefaults']['pPr'],resolved.get('pPr',{})); eff=effective(eff,direct)
        runs=[]
        for r in p.findall(qn('w:r')):
            rpr=read_rpr(r.find(qn('w:rPr'))); txt=para_text(r)
            if txt or rpr: runs.append({'text':txt,'rPr':rpr})
        rec={'idx0':st['para'],'id':pid,'container':container,'cell_ref':cell_ref,'section':st['sect']+1,'style_id':sid,'style_name':styles.get(sid,{}).get('name'),'text':para_text(p),'chars':len(para_text(p)),'direct_pPr':direct,'effective_pPr':eff,'runs':runs,'run_signatures':sorted({json.dumps({k:x['rPr'].get(k) for k in ('font_ascii','size_pt','bold','italic','caps') if k in x['rPr']},sort_keys=True) for x in runs})}
        if ppr is not None and ppr.find(qn('w:sectPr')) is not None:
            sp=read_sectpr(ppr.find(qn('w:sectPr')),rels); sp['after_paragraph']=pid; sections.append(sp); st['sect']+=1; rec['section']=st['sect']+1
        rec['fields']=collect_fields(p,pid); rec['drawings']=collect_drawings(p,pid,rels)
        paragraphs.append(rec); fields_all.extend(rec['fields']); images_all.extend(rec['drawings']); st['para']+=1
        return rec

    def walk(parent,container='body',tid=None,row=None,col=None):
        for ch in parent:
            if ch.tag==W+'p': new_para(ch,container,f'{tid}.{row}.{col}' if tid else None)
            elif ch.tag==W+'sdt':
                c=ch.find(qn('w:sdtContent'))
                if c is not None: walk(c,container,tid,row,col)

    for ch in body:
        if ch.tag==W+'p': new_para(ch)
        elif ch.tag==W+'tbl':
            tid='T%03d'%st['tbl']; tblpr=ch.find(qn('w:tblPr'))
            grid=[int(g.get(qn('w:w'))) for g in ch.findall(qn('w:tblGrid')+'/'+qn('w:gridCol')) if g.get(qn('w:w'))]
            rows=ch.findall(qn('w:tr')); cells=[]; rows_meta=[]
            for ri,tr in enumerate(rows):
                trpr=tr.find(qn('w:trPr'))
                rows_meta.append({'row':ri,'cantSplit':onoff(trpr.find(qn('w:cantSplit'))) if trpr is not None else None,'tblHeader':onoff(trpr.find(qn('w:tblHeader'))) if trpr is not None else None,'height':val(trpr.find(qn('w:trHeight'))) if trpr is not None else None})
                for ci,tc in enumerate(tr.findall(qn('w:tc'))):
                    tcpr=tc.find(qn('w:tcPr')); tcw=None; span=1; vm=None
                    if tcpr is not None:
                        tw=tcpr.find(qn('w:tcW'))
                        if tw is not None and tw.get(qn('w:type')) in (None,'dxa'):
                            try: tcw=int(tw.get(qn('w:w')))
                            except (TypeError,ValueError): pass
                        gs=tcpr.find(qn('w:gridSpan'))
                        if gs is not None:
                            try: span=int(val(gs))
                            except (TypeError,ValueError): pass
                        vme=tcpr.find(qn('w:vMerge'))
                        if vme is not None: vm=vme.get(qn('w:val')) or 'continue'
                    start=st['para']; walk(tc,'table_cell',tid,ri,ci)
                    txt='\n'.join(x['text'] for x in paragraphs[start:] if x['text'])
                    cells.append({'table':tid,'row':ri,'col':ci,'cell_id':f'{tid}.{ri}.{ci}','text':txt,'chars':len(txt),'width_dxa':tcw,'gridSpan':span,'vMerge':vm,'paragraph_ids':[x['id'] for x in paragraphs[start:]]})
            tblw=None; borders={}; floating=False; overlap=None; layout=None
            if tblpr is not None:
                tw=tblpr.find(qn('w:tblW'))
                if tw is not None and tw.get(qn('w:type')) in (None,'dxa'):
                    try: tblw=int(tw.get(qn('w:w')))
                    except (TypeError,ValueError): pass
                b=tblpr.find(qn('w:tblBorders'))
                if b is not None:
                    for e in b: borders[etree.QName(e).localname]=e.get(qn('w:val'))
                floating=tblpr.find(qn('w:tblpPr')) is not None
                ov=tblpr.find(qn('w:tblOverlap')); overlap=val(ov) if ov is not None else None
                lay=tblpr.find(qn('w:tblLayout')); layout=lay.get(qn('w:type')) if lay is not None else None
            gs=sum(grid) if grid else None; total=tblw or gs
            tables.append({'idx0':st['tbl'],'id':tid,'style_id':val(tblpr.find(qn('w:tblStyle'))) if tblpr is not None else None,'rows':len(rows),'cols':max((len(r.findall(qn('w:tc'))) for r in rows),default=0),'grid_dxa':grid,'grid_sum_dxa':gs,'tblW_dxa':tblw,'total_width_dxa':total,'over_print_width':(total>PORT) if total else None,'printable_limit_dxa':PORT,'floating':floating,'tblOverlap':overlap,'layout':layout,'borders':borders,'borders_horizontal_count':sum(1 for k,v in borders.items() if v not in (None,'none','nil') and k in ('top','bottom','insideH')),'borders_vertical_count':sum(1 for k,v in borders.items() if v not in (None,'none','nil') and k in ('left','right','insideV')),'rows_meta':rows_meta,'cells':cells})
            st['tbl']+=1
        elif ch.tag==W+'sdt':
            c=ch.find(qn('w:sdtContent'))
            if c is not None: walk(c)

    bs=body.find(qn('w:sectPr'))
    if bs is not None:
        sp=read_sectpr(bs,rels); sp['after_paragraph']=None; sections.append(sp)
    for i,s in enumerate(sections):
        s['index']=i+1; s['headers_footers']=[]
        for ref in s.get('refs',[]):
            info=dict(ref)
            if info.get('target'):
                info['text']=part_text(z,info['target']); info['images']=[]
                hr=read_rels(z,'word/'+info['target'].lstrip('/'))
                for rid,rr in hr.items():
                    if rr.get('rel_type')=='image': info['images'].append(rr)
            s['headers_footers'].append(info)

    fk={}
    for f in fields_all:
        instr=(f.get('instr') or '').strip(); k=instr.split()[0].upper() if instr else 'UNKNOWN'
        fk[k]=fk.get(k,0)+1

    pdf_info=None; anchors=None
    if pdf_path and os.path.exists(pdf_path):
        try:
            import pymupdf
            doc=pymupdf.open(pdf_path); pages=[]; pnorm=[]
            norm=lambda s: re.sub(r'\s+',' ',s).strip().lower()
            for i,pg in enumerate(doc):
                t=pg.get_text('text'); pages.append({'page':i+1,'chars':len(t),'text':t}); pnorm.append(norm(t))
            anchors=[]; cur=0
            for rec in paragraphs:
                txt=norm(rec['text'])
                if len(txt)<20:
                    anchors.append({'paragraph':rec['id'],'page':None,'method':'skipped_short'}); continue
                probe=txt[:60]; found=None
                for j in range(cur,len(pnorm)):
                    if probe in pnorm[j]: found=j+1; break
                if found is None:
                    for j in range(len(pnorm)):
                        if probe in pnorm[j]: found=j+1; break
                if found:
                    cur=found-1; rec['pdf_page']=found; anchors.append({'paragraph':rec['id'],'page':found,'method':'text_probe'})
                else:
                    anchors.append({'paragraph':rec['id'],'page':None,'method':'not_found'})
            pdf_info={'source_pdf':os.path.abspath(pdf_path),'sha256_pdf':sha256_file(pdf_path),'page_count':len(doc),'pages':pages}
            with open(os.path.join(outdir,'PDF_TEXTO_%s.json'%slug(docx_path)),'w',encoding='utf-8') as f:
                json.dump(pdf_info,f,ensure_ascii=False,indent=1)
            with open(os.path.join(outdir,'ANCLAS_%s.json'%slug(docx_path)),'w',encoding='utf-8') as f:
                json.dump({'source_docx':os.path.abspath(docx_path),'source_sha256':src_sha,'source_pdf_sha256':pdf_info['sha256_pdf'],'anchors':anchors},f,ensure_ascii=False,indent=1)
        except Exception as e:
            pdf_info={'error':str(e)}

    inv={'meta':{'tool':'inventario_openxml.py','version':'1.0','generated_at':datetime.now(timezone.utc).isoformat(),'source_docx':os.path.abspath(docx_path),'sha256_docx':src_sha,'bytes_docx':os.path.getsize(docx_path),'read_only':True,'pdf':{k:pdf_info[k] for k in ('source_pdf','sha256_pdf','page_count')} if pdf_info and 'error' not in pdf_info else pdf_info},'summary':{'paragraphs':len(paragraphs),'body_paragraphs':sum(1 for p in paragraphs if p['container']=='body'),'table_paragraphs':sum(1 for p in paragraphs if p['container']=='table_cell'),'tables':len(tables),'table_cells':sum(len(t['cells']) for t in tables),'sections':len(sections),'images':len(images_all),'unique_media':len(media),'fields':len(fields_all),'field_kinds':fk,'floating_tables':sum(1 for t in tables if t['floating']),'tables_over_print_width':sum(1 for t in tables if t['over_print_width']),'rows_without_cantSplit':sum(1 for t in tables for r in t['rows_meta'] if r['cantSplit'] is not True)},'sections':sections,'tables':tables,'paragraphs':paragraphs,'fields':fields_all,'images':images_all,'media':media,'styles_used':sorted({p['style_id'] for p in paragraphs if p['style_id']})}
    jp=os.path.join(outdir,'INVENTARIO_%s.json'%slug(docx_path))
    with open(jp,'w',encoding='utf-8') as f: json.dump(inv,f,ensure_ascii=False,indent=1)
    mp=os.path.join(outdir,'INVENTARIO_%s.md'%slug(docx_path))
    with open(mp,'w',encoding='utf-8') as f:
        f.write('# INVENTARIO OPENXML - %s\n\n- SHA-256: `%s`\n- Generado: %s\n- Solo lectura: si\n\n'%(os.path.basename(docx_path),src_sha,inv['meta']['generated_at']))
        f.write('## Resumen\n\n```json\n%s\n```\n\n'%json.dumps(inv['summary'],ensure_ascii=False,indent=1))
        f.write('## Secciones\n\n')
        for s in sections:
            f.write('- S%02d: %s %sx%s cm; margenes sup/inf/izq/der=%s/%s/%s/%s cm; pgNum=%s start=%s\n'%(s['index'],s.get('orientation'),s.get('page_w_cm'),s.get('page_h_cm'),s.get('top_cm'),s.get('bottom_cm'),s.get('left_cm'),s.get('right_cm'),s.get('pg_num_fmt'),s.get('pg_num_start')))
        f.write('\n## Prosa por parrafo\n\n')
        for p in paragraphs:
            if not p['text'].strip(): continue
            f.write('### %s [%s] %s - %s\n'%(p['id'],p['container'],p.get('style_name') or p.get('style_id') or '-',('p.%d'%p['pdf_page']) if p.get('pdf_page') else 's/p'))
            f.write('%s\n\n'%p['text'].replace('\n',' '))
        f.write('\n## Tablas\n\n')
        for t in tables:
            f.write('### %s - %dx%d ancho=%s dxa flotante=%s\n\n'%(t['id'],t['rows'],t['cols'],t['total_width_dxa'],t['floating']))
            f.write('| celda | texto | ancho dxa |\n|---|---|---|\n')
            for c in t['cells']:
                f.write('| %s | %s | %s |\n'%(c['cell_id'],c['text'].replace('\n',' / ').replace('|','\\|'),c['width_dxa']))
            f.write('\n')
    return jp,mp

def main():
    ap=argparse.ArgumentParser(description='Inventario OpenXML de solo lectura')
    ap.add_argument('docx'); ap.add_argument('--outdir',required=True); ap.add_argument('--pdf',default=None)
    a=ap.parse_args(); j,m=build(a.docx,a.outdir,a.pdf); print(j); print(m)

if __name__=='__main__': main()
