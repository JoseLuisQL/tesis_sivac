import io, sys, json, re, unicodedata
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pymupdf
PDF = r"C:/MisInvestigaciones/tesis/sivac/salidas/documentos/informe_final_v04.pdf"
st = json.load(open('_structure.json', encoding='utf-8'))
paras = {it['idx']:it for it in st['items'] if it['kind']=='p'}
pdf = pymupdf.open(PDF)
def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]', '', s.lower())
pages = [norm(pdf[i].get_text()) for i in range(pdf.page_count)]
targets = [10,18,113,134,201,253,326,345,372,408,441,445,449,453,457,492,518,541,547,553,560,589,601,619,623,624,630,631,639,640,648,649,659,660,668,669,672,675,676,682,683,690,691,752,753,796,797,798,800,804,757,775,778,781,786,789,794]
res={}
cursor=0
for i in sorted(targets):
    t = (paras[i]['text'] or '').strip()
    key = norm(t)[:70]
    found=None
    if len(key)>=12:
        for p in range(cursor, len(pages)):
            if key in pages[p]:
                found=p+1; cursor=p; break
    res[i]=found
for i in sorted(res):
    print(f"P{i:04d} -> p{res[i]} :: {(paras[i]['text'] or '')[:70]!r}")
json.dump(res, open('_pmap.json','w',encoding='utf-8'))
