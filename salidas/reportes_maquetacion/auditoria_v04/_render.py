import pymupdf, os, json
pdf = r"C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v04.pdf"
outdir = r"C:\MisInvestigaciones\tesis\sivac\salidas\reportes_maquetacion\auditoria_v04"
doc = pymupdf.open(pdf)
meta = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=110)
    fn = os.path.join(outdir, "p%03d.png" % (i+1))
    pix.save(fn)
    r = page.rect
    txt = page.get_text()
    meta.append({"page": i+1, "w": round(r.width,1), "h": round(r.height,1),
                 "rotate": page.rotation, "landscape": r.width > r.height,
                 "nwords": len(txt.split()), "chars": len(txt)})
with open(os.path.join(outdir,"_pagemeta.json"),"w",encoding="utf-8") as f:
    json.dump(meta,f,ensure_ascii=False)
print("pages", len(doc))
