import pymupdf, json, re, unicodedata
pdf = r"C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v04.pdf"
outdir = r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04"
doc = pymupdf.open(pdf)
pages = []
for i,page in enumerate(doc):
    txt = page.get_text("text")
    pages.append(txt)

# page dims in points
dims = [(round(p.rect.width,1), round(p.rect.height,1)) for p in doc]

def norm(s):
    return re.sub(r"\s+"," ", s).strip()

# find folios: last non-empty line / first line near top
folio_report=[]
for i,page in enumerate(doc):
    blocks = page.get_text("dict")["blocks"]
    top=[]; bot=[]
    H=page.rect.height; W=page.rect.width
    for b in blocks:
        if b.get("type")!=0: continue
        for l in b["lines"]:
            s="".join(sp["text"] for sp in l["spans"]).strip()
            if not s: continue
            y=l["bbox"][1]; x0=l["bbox"][0]; x1=l["bbox"][2]
            if y < 95: top.append((round(y,1),round(x0,1),round(x1,1),s))
            if y > H-95: bot.append((round(y,1),round(x0,1),round(x1,1),s))
    folio_report.append({"page":i+1,"w":W,"h":H,"top":top[:3],"bot":bot[-3:]})

with open(outdir+r"\_folios.json","w",encoding="utf-8") as f:
    json.dump(folio_report,f,ensure_ascii=False,indent=0)

# ---- detect emoji
emoji_re = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u2B00-\u2BFF]")
emoji_pages=[]
for i,t in enumerate(pages):
    ms = emoji_re.findall(t)
    if ms: emoji_pages.append((i+1,ms))
json.dump([{"page":a,"chars":[hex(ord(c)) for c in b]} for a,b in emoji_pages], open(outdir+r"\_emoji.json","w",encoding="utf-8"), ensure_ascii=False); print("EMOJI pages:", [a for a,b in emoji_pages])

# ---- out of margin text
# A4 595.3x841.9 ; margins L 85 (3cm), R 70.9, T 70.9, B 70.9
oob=[]
for i,page in enumerate(doc):
    W,H=page.rect.width,page.rect.height
    lim_l, lim_r, lim_t, lim_b = 80, W-65, 60, H-60
    bad=[]
    for b in page.get_text("dict")["blocks"]:
        if b.get("type")!=0: continue
        x0,y0,x1,y1=b["bbox"]
        if x0 < lim_l-6 or x1 > lim_r+6 or y0 < lim_t-6 or y1 > lim_b+6:
            s=" ".join("".join(sp["text"] for sp in l["spans"]) for l in b["lines"])[:90]
            bad.append({"bbox":[round(v,1) for v in b["bbox"]],"txt":s})
    if bad: oob.append({"page":i+1,"W":round(W,1),"items":bad[:6]})
print("OUT-OF-BOX pages:", len(oob), [o["page"] for o in oob])
with open(outdir+r"\_oob.json","w",encoding="utf-8") as f:
    json.dump(oob,f,ensure_ascii=False,indent=0)

# ---- blank / sparse pages
sparse=[(i+1,len(pages[i].split())) for i in range(len(pages)) if len(pages[i].split())<25]
print("SPARSE:", sparse)

with open(outdir+r"\_pagetext.json","w",encoding="utf-8") as f:
    json.dump(pages,f,ensure_ascii=False)
