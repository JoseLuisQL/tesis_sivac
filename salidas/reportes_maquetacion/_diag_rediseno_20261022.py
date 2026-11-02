import json, hashlib, re, sys, os, zipfile
from xml.etree import ElementTree as ET
from docx import Document
import pdfplumber
from pypdf import PdfReader

BASE = r"C:\MisInvestigaciones\tesis\sivac"
V01 = os.path.join(BASE, "salidas", "instrumentos", "INSTRUMENTOS_REDISENADOS_FANY_20261022_v01")
RECTOR = os.path.join(BASE, "salidas", "evidencias", "instrumentos_aplicados", "EXPEDIENTE_VALIDACION_JUICIO_EXPERTOS_MODELO_FANY.docx")
ACT = os.path.join(BASE, "salidas", "instrumentos", "PAQUETE_CAMPO_14_20261022", "_MAESTROS_DOCX", "TRAB-01")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def norm(s):
    s = (s or "").replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

def rows_of(doc):
    out = []
    for t in doc.tables:
        for r in t.rows:
            cells = []
            for c in r.cells:
                if not cells or c.text != cells[-1]:
                    cells.append(c.text)
            out.append(" | ".join(cells))
    return out

def reactivos(doc):
    d = {}
    for r in rows_of(doc):
        m = re.match(r"\s*((?:AP|UP|PU|PE)-\d{2})\s*\|(.*)", r, re.S)
        if m:
            d[m.group(1)] = norm(m.group(2))
    return d

def docx_xml(p):
    z = zipfile.ZipFile(p)
    xml = z.read("word/document.xml").decode("utf-8")
    return xml

def geom(p):
    xml = docx_xml(p)
    root = ET.fromstring(xml)
    tabs = root.iter(W + "tbl")
    widths, grids, rows, cs, th, fl, om = [], [], 0, 0, 0, 0, 0
    for t in root.iter(W + "tbl"):
        pr = t.find(W + "tblPr")
        if pr is not None:
            tw = pr.find(W + "tblW")
            if tw is not None:
                widths.append(tw.get(W + "w"))
            if pr.find(W + "tblpPr") is not None:
                fl += 1
        g = t.find(W + "tblGrid")
        if g is not None:
            grids.append(sum(int(c.get(W + "w") or 0) for c in g.findall(W + "gridCol")))
        for r in t.findall(W + "tr"):
            rows += 1
            trp = r.find(W + "trPr")
            if trp is not None:
                if trp.find(W + "cantSplit") is not None:
                    cs += 1
                if trp.find(W + "tblHeader") is not None:
                    th += 1
    for t in root.iter(W + "tbl"):
        for tc in t.iter(W + "tc"):
            if tc.find(".//" + M + "oMath") is not None:
                om += 1
    sec = root.find(".//" + W + "sectPr")
    mar = {}
    if sec is not None:
        pg = sec.find(W + "pgMar")
        if pg is not None:
            mar = {k.split("}")[-1]: pg.get(W + k) for k in ("top", "bottom", "left", "right")}
    return {"tblW": sorted(set(widths)), "grid_suma": sorted(set(grids)), "filas": rows,
            "cantSplit": cs, "tblHeader": th, "tblpPr": fl, "oMath_en_celdas": om, "margenes": mar}

def txt_pdf(p):
    with pdfplumber.open(p) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages), len(pdf.pages)

def alltext(doc):
    parts = [x.text for x in doc.paragraphs]
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                parts.append(c.text)
    return "\n".join(parts)

out = {"hashes": {}, "reactivos": {}, "geom": {}, "pdf": {}, "campos": {}, "conjunto": {}, "cont": {}, "reglas": {}, "rector": {}}
man = json.load(open(os.path.join(V01, "MANIFIESTO.json"), encoding="utf-8"))
com = json.load(open(os.path.join(BASE, "salidas", "reportes_maquetacion", "comision_rediseno_instrumentos_fany_20261022.json"), encoding="utf-8"))

# hashes de salida contra manifiesto
man_by_docx = {}
for e in man.get("documentos", []):
    if isinstance(e, dict):
        man_by_docx[os.path.basename(e.get("docx", ""))] = e
for f in sorted(os.listdir(V01)):
    p = os.path.join(V01, f)
    if f.lower().endswith((".docx", ".pdf")):
        h = sha(p)
        e = man_by_docx.get(f if f.endswith(".docx") else "")
        declared = None
        for k, v in man_by_docx.items():
            if v.get("pdf") and os.path.basename(v["pdf"]) == f:
                declared = v.get("sha256_pdf")
            if k == f:
                declared = v.get("sha256_docx")
        out["hashes"][f] = {"sha256": h, "manifiesto": declared, "coincide": (declared == h) if declared else None}

# huellas de fuentes
out["fuentes"] = {}
for k, v in (man.get("fuentes_preservadas_sha256") or {}).items():
    p = os.path.join(BASE, k.replace("/", os.sep))
    out["fuentes"][k] = {"declarado": v, "actual": sha(p) if os.path.exists(p) else None}
out["fuentes_comision_iguales"] = (com.get("fuentes_preservadas_sha256") == man.get("fuentes_preservadas_sha256"))

# reactivos
rd = Document(RECTOR)
rr = reactivos(rd)
out["rector"]["codigos"] = sorted(rr)
out["rector"]["total"] = len(rr)
A = Document(os.path.join(V01, "03_CUESTIONARIO_SATISFACCION_A.docx"))
B = Document(os.path.join(V01, "04_MODULO_COMPLEMENTARIO_B_POST.docx"))
ra, rb = reactivos(A), reactivos(B)
out["reactivos"]["A_codigos"] = sorted(ra)
out["reactivos"]["B_codigos"] = sorted(rb)
out["reactivos"]["A_faltan"] = sorted(set(ra) - set(rr))
out["reactivos"]["B_faltan"] = sorted(set(rb) - set(rr))
out["reactivos"]["A_distintos"] = [k for k in ra if k in rr and ra[k] != rr[k]]
out["reactivos"]["B_distintos"] = [k for k in rb if k in rr and rb[k] != rr[k]]
for k in out["reactivos"]["A_distintos"][:2]:
    out["reactivos"].setdefault("muestra", []).append({"cod": k, "rector": rr[k][:200], "docx": ra[k][:200]})

# reactivos en PDF
for f in ("03_CUESTIONARIO_SATISFACCION_A.pdf", "04_MODULO_COMPLEMENTARIO_B_POST.pdf"):
    tx, n = txt_pdf(os.path.join(V01, f))
    src = ra if f.startswith("03") else rb
    out["pdf"][f] = {"paginas": n, "codigos": sorted(re.findall(r"\b(?:AP|UP|PU|PE)-\d{2}\b", tx)),
                     "faltantes": sorted(set(src) - set(re.findall(r"\b(?:AP|UP|PU|PE)-\d{2}\b", tx))),
                     "escala_1_5": all(x in tx for x in ["1", "2", "3", "4", "5"])}

# geometria
for f in sorted(x for x in os.listdir(V01) if x.endswith(".docx")):
    out["geom"][f] = geom(os.path.join(V01, f))

# paginas de todos los PDF
for f in sorted(x for x in os.listdir(V01) if x.endswith(".pdf")):
    out["pdf"].setdefault(f, {})["paginas"] = len(PdfReader(os.path.join(V01, f)).pages)

# campos vacios y microcabeceras
def fieldcheck(doc):
    res = {}
    for t in doc.tables[:3]:
        for r in t.rows:
            cs = [c.text.strip() for c in r.cells]
            if cs and cs[0]:
                res.setdefault(cs[0][:40], cs[1][:30] if len(cs) > 1 else "")
    return res
out["campos"]["A"] = fieldcheck(A)
out["campos"]["B"] = fieldcheck(B)

# conjunto vs separados
C = Document(os.path.join(V01, "00_INSTRUMENTOS_RECOLECCION_SIVAC.docx"))
ct = norm(alltext(C))
for f, d in (("01", Document(os.path.join(V01, "01_FICHA_TIEMPOS.docx"))), ("02", Document(os.path.join(V01, "02_FICHA_AUDITORIA_DOCUMENTAL.docx"))), ("03", A), ("04", B)):
    lines = [norm(x) for x in alltext(d).split("\n") if len(norm(x)) > 25]
    missing = [x for x in lines if x not in ct]
    out["conjunto"][f] = {"lineas": len(lines), "ausentes": len(missing), "muestra_ausente": missing[:3]}

# continuaciones y reglas
t02 = alltext(Document(os.path.join(V01, "02_FICHA_AUDITORIA_DOCUMENTAL.docx")))
out["cont"]["RSD"] = [m for m in re.findall(r"RSD[^\n]{0,80}", t02)][:4]
out["cont"]["CPE"] = [m for m in re.findall(r"CPE[^\n]{0,80}", t02)][:4]
out["cont"]["incidencias"] = "incidencia" in norm(t02)
out["cont"]["D06"] = "D-06" in t02
out["cont"]["continua"] = "continuaci" in norm(t02)

# reglas RSD/CPE frente al formulario actual
cur = alltext(Document(os.path.join(ACT, "01_PRE_03_FICHA_02_AUDITORIA_PRE.docx")))
def rules(t):
    return [norm(x) for x in re.split(r"(?<=\.)\s+", t) if ("conforme" in norm(x) or "concordancia" in norm(x)) and len(norm(x)) > 60]
r_new, r_old = rules(t02), rules(cur)
out["reglas"]["nuevas"] = r_new[:4]
out["reglas"]["actuales"] = r_old[:4]
out["reglas"]["iguales_exactas"] = all(x in " ".join(r_old) for x in r_new) if r_new else None

# 04 no cuarto instrumento
out["doc04"] = {"titulo": [p.text for p in B.paragraphs if p.text.strip()][:2],
                "menciona_variable_nueva": bool(re.search(r"variable independiente|nueva dimensi", norm(alltext(B)))),
                "menciona_complement": "complementar" in norm(alltext(B))}

print(json.dumps(out, ensure_ascii=False, indent=1))


# ---------- FASE 2: controles focalizados ----------
out2 = {}
Araw = reactivos(A); Braw = reactivos(B)
def clean(s):
    s = re.sub(r"\|\s*\[\s*\]", "", s)
    s = re.sub(r"\b[1-5]\b", " ", s)
    return norm(s)
out2["reactivos_iguales_limpios"] = {
    "A": [k for k in Araw if k in rr and clean(Araw[k]) != clean(rr[k])],
    "B": [k for k in Braw if k in rr and clean(Braw[k]) != clean(rr[k])]
}
out2["reactivos_secuencia_rector"] = sorted(rr)[:16]

def blocks(t, keys):
    out = {}
    for k in keys:
        idx = [m.start() for m in re.finditer(k, norm(t))]
        out[k] = [norm(t)[i:i+260] for i in idx[:2]]
    return out
t01 = alltext(Document(os.path.join(V01, "01_FICHA_TIEMPOS.docx")))
out2["continuaciones"] = {
    "02_contin": [x for x in re.split(r"\n", t02) if "continu" in norm(x)][:6],
    "02_D": sorted(set(re.findall(r"\b[DE]-\d{2}\b", t02)))[:12],
    "01_incid": [x for x in re.split(r"\n", t01) if "incidencia" in norm(x)][:4],
    "01_D": sorted(set(re.findall(r"\b[DE]-\d{2}\b", t01)))[:12],
    "apoyos": sorted(os.listdir(os.path.join(V01, "APOYOS_INVESTIGADOR")))
}
ap = os.path.join(V01, "APOYOS_INVESTIGADOR")
out2["apoyos_pdf"] = {}
for f in sorted(os.listdir(ap)):
    if f.lower().endswith(".pdf"):
        out2["apoyos_pdf"][f] = len(PdfReader(os.path.join(ap, f)).pages)

def ruletext(t, key):
    n = norm(t)
    i = n.find(key)
    return n[i:i+400] if i >= 0 else None
out2["reglas_exactas"] = {
    "conformidad_igual": ruletext(t02, "un documento es conforme") == ruletext(cur, "un documento es conforme"),
    "conformidad_nueva": ruletext(t02, "un documento es conforme"),
    "concordancia_nueva": ruletext(t02, "concordancia entre cantidad programada") or ruletext(t02, "regla de concordancia"),
    "concordancia_actual": ruletext(cur, "concordancia entre cantidad programada")
}
def meta_rows(doc):
    rows = []
    for t in doc.tables[:3]:
        for r in t.rows:
            cs = [c.text.strip() for c in r.cells]
            if len(cs) >= 2 and cs[0] and len(cs[0]) < 45:
                rows.append(cs[0] + " = " + cs[1][:22])
    return rows
out2["metadatos"] = {"01": meta_rows(Document(os.path.join(V01, "01_FICHA_TIEMPOS.docx"))),
                     "02": meta_rows(Document(os.path.join(V01, "02_FICHA_AUDITORIA_DOCUMENTAL.docx"))),
                     "A": meta_rows(A), "B": meta_rows(B)}
claims = ["validez", "validado", "confiabilidad", "comprensi", "juicio de experto", "aprobado por"]
for f, d in (("01", Document(os.path.join(V01, "01_FICHA_TIEMPOS.docx"))), ("02", Document(os.path.join(V01, "02_FICHA_AUDITORIA_DOCUMENTAL.docx"))), ("03", A), ("04", B)):
    tx = norm(alltext(d))
    out2.setdefault("afirmaciones", {})[f] = [c for c in claims if c in tx]
out2["firmas"] = {"02_nueva": [x for x in re.split(r"\n", t02) if "firma" in norm(x)][:3],
                  "02_actual": [x for x in re.split(r"\n", cur) if "firma" in norm(x)][:3]}
out2["correspondencia"] = {"total": len(man.get("correspondencia_campos", [])),
                           "sin_destino_visible": []}
allnew = norm(alltext(C))
for e in man.get("correspondencia_campos", []):
    d = e.get("destino", "")
    if d and len(d) > 8:
        key = norm(d)[:40]
        if key not in allnew:
            out2["correspondencia"]["sin_destino_visible"].append(d[:60])
print("FASE2")
print(json.dumps(out2, ensure_ascii=False, indent=1))

# ---------- FASE 3: equivalencia estricta y soportes ----------
out3 = {}
def longcell(txt):
    cs = [c.strip() for c in txt.split("|") if c.strip()]
    cs = [c for c in cs if not re.fullmatch(r"\[?\s*\]?|[1-5]", c)]
    return max(cs, key=len) if cs else ""
def key(s):
    s = norm(s)
    s = re.sub(r"[^a-z0-9áéíóúñü ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()
cmpA = {k: {"rector": key(longcell(v)), "docx": key(longcell(Araw[k]))} for k, v in rr.items() if k in Araw}
cmpB = {k: {"rector": key(longcell(v)), "docx": key(longcell(Braw[k]))} for k, v in rr.items() if k in Braw}
out3["estricto_A_ok"] = [k for k, v in cmpA.items() if v["rector"] == v["docx"]]
out3["estricto_A_diff"] = {k: v for k, v in cmpA.items() if v["rector"] != v["docx"]}
out3["estricto_B_ok"] = [k for k, v in cmpB.items() if v["rector"] == v["docx"]]
out3["estricto_B_diff"] = {k: v for k, v in cmpB.items() if v["rector"] != v["docx"]}

for f, d in (("03", A), ("04", B)):
    tx = alltext(d)
    out3.setdefault("fase", {})[f] = [x.strip() for x in tx.split("\n") if "fase" in norm(x)][:4]

apd = Document(os.path.join(ap, "05_APOYOS_INVESTIGADOR_INSTRUCCIONES_CIERRE_CONTINUACIONES.docx"))
apt = alltext(apd)
out3["apoyos"] = {c: (c in apt) for c in ["D-06", "E-13", "H-05", "RSD", "CPE", "cierre", "puntuaci"]}
out3["apoyos_paginas_docx"] = len(apd.sections)

old01 = alltext(Document(os.path.join(ACT, "01_PRE_02_FICHA_01_TIEMPOS_PRE.docx")))
prot_new = [x.strip() for x in t01.split("\n") if "cron" in norm(x) or "protocolo" in norm(x)]
prot_old = [x.strip() for x in old01.split("\n") if "cron" in norm(x) or "protocolo" in norm(x)]
out3["protocolo"] = {"nuevo": prot_new[:3], "actual": prot_old[:3],
                     "mismo_inicio": key(prot_new[0])[:80] == key(prot_old[0])[:80] if prot_new and prot_old else None}
conf = [x.strip() for x in t02.split("\n") if "conforme" in norm(x)]
out3["conformidad_nueva"] = conf[:3]
out3["conformidad_actual"] = [x.strip() for x in cur.split("\n") if "conforme" in norm(x)][:3]
out3["PE_contexto"] = [x.strip()[:160] for x in alltext(B).split("\n") if "comprensi" in norm(x)]
print("FASE3")
print(json.dumps(out3, ensure_ascii=False, indent=1))
