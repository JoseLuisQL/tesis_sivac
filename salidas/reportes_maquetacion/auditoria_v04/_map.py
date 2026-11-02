import json, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open(r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04\_structure.json", encoding="utf-8"))
pages = json.load(open(r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04\_pagetext.json", encoding="utf-8"))
def norm(s): return re.sub(r"\s+", " ", s).strip().lower()
pn = [norm(p) for p in pages]
cursor = 0
mapping = []
items = d["items"]
for k,it in enumerate(items):
    if it["kind"] != "p": continue
    t = it["text"].strip()
    if not re.match(r"^(Tabla|Figura|ANEXO)", t): continue
    key = norm(t)[:45]
    if len(key) < 8: continue
    found = None
    for j in range(cursor, len(pn)):
        if key in pn[j]:
            found = j+1; cursor = j; break
    mapping.append({"p_idx": it["idx"], "text": t[:80], "page": found})
for m in mapping: print(m["p_idx"], m["page"], m["text"][:70])
