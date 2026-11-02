import json, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
st = json.load(open('_structure.json', encoding='utf-8'))
paras = [it for it in st['items'] if it['kind']=='p']
print('TOTAL paras', len(paras))
pats = [r'^Tabla\s', r'^Figura\s', r'Completar', r'registrado en expediente', r'Instrucción para el tesista', r'DATOS DE PRUEBA', r'ADVERTENCIA', r'^\d+\.\d+\.', r'^CAPÍTULO', r'^ANEXO', r'^CONCLUSIONES', r'^RECOMENDACIONES', r'^REFERENCIAS', r'^ANEXOS', r'^\[?\s*X\s*\]', r'ESPACIO RESERVADO']
for p in paras:
    t=(p['text'] or '').strip()
    if not t: continue
    for pat in pats:
        if re.search(pat, t[:80]):
            print(f"P{p['idx']:04d} [{p['style']}] {t[:150]}")
            break
