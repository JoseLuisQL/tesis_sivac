import json, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open(r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04\_structure.json", encoding="utf-8"))
def norm(s): return re.sub(r"\s+", " ", s).strip().lower()
ps = [(it["idx"], it["text"].strip()) for it in d["items"] if it["kind"]=="p"]
print("== DUPLICADOS EXACTOS CONSECUTIVOS ==")
for i in range(1,len(ps)):
    a,b = ps[i-1][1], ps[i][1]
    if len(norm(a))>25 and norm(a)==norm(b):
        print(f"P{ps[i-1][0]} == P{ps[i][0]} :: {a[:90]}")
print("== DUPLICADOS EN VENTANA 3 ==")
for i in range(len(ps)):
    for j in range(i+1, min(i+4, len(ps))):
        if len(norm(ps[i][1]))>60 and norm(ps[i][1])==norm(ps[j][1]):
            print(f"P{ps[i][0]} ~ P{ps[j][0]} :: {ps[i][1][:90]}")
print("== FRASES SOSPECHOSAS (final truncado) ==")
conn = (" y"," de"," que"," con"," en"," para"," por"," la"," el"," los"," las"," a"," del"," al"," se"," su")
for idx,t in ps:
    if len(t)<40: continue
    tt=t.rstrip()
    if tt.endswith("..."):
        print(f"P{idx} [SUSPENSIVOS] {tt[-70:]}")
    elif tt.endswith(conn):
        print(f"P{idx} [CONECTOR COLGANTE] ...{tt[-70:]}")
    elif not tt.endswith(('.',':',';','?','!',')','”','"','%')) and len(tt)>60:
        print(f"P{idx} [SIN PUNTO FINAL] ...{tt[-70:]}")
