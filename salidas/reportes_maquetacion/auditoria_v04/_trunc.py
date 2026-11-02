import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
st = json.load(open('_structure.json', encoding='utf-8'))
paras = [it for it in st['items'] if it['kind']=='p']
conn = {'y','o','u','e','de','del','en','que','con','por','para','la','el','los','las','un','una','unos','unas','al','se','como','entre','sin','sobre','desde','hasta','su','sus','ni','pero','sino','aunque','mientras','donde','cuando','porque','pues','si','no'}
out=[]
for p in paras:
    t = (p['text'] or '').strip()
    if len(t) < 60: continue
    if re.fullmatch(r'[A-ZÁÉÍÓÚÑ0-9 .,:;\-–—()\[\]“”"°%/]+', t) and t.endswith('.'): continue
    last = re.sub(r'[^\wáéíóúñü]', '', t.split()[-1].lower())
    if t[-1] not in '.):;!?»"' and last in conn:
        out.append((p['idx'], p['style'], t[-120:]))
print('TRUNCAMIENTOS CANDIDATOS:', len(out))
for i,s,t in out:
    print(f"P{i:04d} [{s}] ...{t}")
json.dump(out, open('_trunc.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
