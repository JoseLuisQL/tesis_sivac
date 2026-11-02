import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
st = json.load(open('_structure.json', encoding='utf-8'))
paras=[it for it in st['items'] if it['kind']=='p']
for p in paras:
    t=(p['text'] or '').strip()
    if 610 <= p['idx'] <= 700 or 95 <= p['idx'] <= 120:
        for m in re.finditer(r'(Tabla|Figura)\s+(A?\d+(?:\.\d+)?)', t):
            ctx = t[max(0,m.start()-70):m.end()+30].replace('\n',' ')
            print(f"P{p['idx']:04d} :: ...{ctx}...")
