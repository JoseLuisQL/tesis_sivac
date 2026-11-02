import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = json.load(open('_folios.json', encoding='utf-8'))
print(type(f))
if isinstance(f, dict):
    print(list(f.keys())[:10])
    for k in list(f.keys())[:3]:
        print(k, json.dumps(f[k], ensure_ascii=False)[:400])
elif isinstance(f, list):
    print(len(f)); print(json.dumps(f[:3], ensure_ascii=False)[:800])
