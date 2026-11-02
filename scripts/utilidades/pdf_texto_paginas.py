# -*- coding: utf-8 -*-
"""pdf_texto_paginas.py - Extraccion de texto por pagina fisica y render de paginas (SOLO LECTURA)."""
import json, sys, hashlib, os
import pymupdf

def run(pdf, outdir, tag, render_to=0, dpi=110):
    doc = pymupdf.open(pdf)
    pages = []
    for i, p in enumerate(doc):
        t = p.get_text("text")
        pages.append({"page": i + 1, "chars": len(t), "scanned_no_text": len(t.strip()) < 40, "text": t})
    h = hashlib.sha256(open(pdf, "rb").read()).hexdigest()
    out = {"source_pdf": os.path.abspath(pdf), "sha256_pdf": h, "page_count": len(doc), "pages": pages}
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "PDF_TEXTO_%s.json" % tag), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    if render_to:
        rend = os.path.join(outdir, "paginas_%s_%03d" % (tag, render_to))
        os.makedirs(rend, exist_ok=True)
        for i in range(min(render_to, len(doc))):
            doc[i].get_pixmap(dpi=dpi).save(os.path.join(rend, "%s_p%03d.png" % (tag.lower(), i + 1)))
        print("rendered", rend)
    print("pages", len(doc), "scanned", sum(1 for x in pages if x["scanned_no_text"]))
    return out

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 0,
        int(sys.argv[5]) if len(sys.argv) > 5 else 110)
