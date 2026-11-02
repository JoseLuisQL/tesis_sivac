import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
st = json.load(open('_structure.json', encoding='utf-8'))
paras = {it['idx']:it for it in st['items'] if it['kind']=='p'}
for rng in [(19,32),(60,66),(615,626),(700,712),(750,760),(794,810)]:
    print(f"===== P{rng[0]}..P{rng[1]-1} =====")
    for i in range(*rng):
        p=paras.get(i)
        if p: print(f"P{i:04d} [{p['style']}] {(p['text'] or '').strip()[:300]!r}")
