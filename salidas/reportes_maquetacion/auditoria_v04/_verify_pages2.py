import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = json.load(open('_folios.json', encoding='utf-8'))
pt = json.load(open('_pagetext.json', encoding='utf-8'))
print('pagetext type', type(pt), (list(pt.keys())[:5] if isinstance(pt, dict) else len(pt)))
for p in f:
    tops = p['top']; bots = p['bot']
    folio = None
    for y0,y1,x1,t in tops:
        if re.fullmatch(r'[ivxlcdm]+|\d+', t.strip(), flags=re.I) and y0 < 60:
            folio = t.strip()
    orient = 'L' if p['w'] > p['h'] else 'P'
    key = str(p['page'])
    txt = ''
    if isinstance(pt, dict):
        txt = pt.get(key, '') or ''
        if isinstance(txt, dict): txt = txt.get('text','')
    body = ' '.join(t for y0,y1,x1,t in tops if not (re.fullmatch(r'[ivxlcdm]+|\d+', t.strip(), flags=re.I) and y0<60))[:70]
    if p['page'] >= 128:
        print(f"p{p['page']:03d} {orient} folio={folio!r} chars={len(txt)!s:>5} | {body}")
