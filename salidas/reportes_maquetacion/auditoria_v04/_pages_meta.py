import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = json.load(open('_folios.json', encoding='utf-8'))
pt = json.load(open('_pagetext.json', encoding='utf-8'))
print('pt sample:', json.dumps(pt[:2], ensure_ascii=False)[:500])
out=[]
for p in f:
    folio=None
    body=[]
    for y0,y1,x1,t in p['top']:
        if re.fullmatch(r'[ivxlcdm]+|\d+', t.strip(), flags=re.I) and y0 < 60:
            folio = t.strip()
        else:
            body.append(t)
    orient = 'horizontal' if p['w'] > p['h'] else 'vertical'
    txt = pt[p['page']-1] if isinstance(pt, list) and len(pt)>=p['page'] else ''
    if isinstance(txt, dict): txt = txt.get('text','')
    out.append({'pagina':p['page'],'folio':folio,'orientacion':orient,'lead':' '.join(body)[:90],'chars':len(txt or '')})
json.dump(out, open('_pages_meta.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
for r in out:
    print(f"{r['pagina']:3d} {r['orientacion'][0].upper()} folio={str(r['folio']):>4} chars={r['chars']:>5} | {r['lead'][:80]}")
