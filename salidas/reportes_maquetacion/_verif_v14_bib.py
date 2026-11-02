# -*- coding: utf-8 -*-
"""Verificacion read-only de anclas bibliograficas contra v14. No modifica nada."""
import sys
from docx import Document

RUTA = r"C:\MisInvestigaciones\tesis\sivac\salidas\documentos\informe_final_v14.docx"
doc = Document(RUTA)
p = doc.paragraphs
print("PARRAFOS:", len(p))
print("TABLAS:", len(doc.tables))

INDICES = [177, 260, 265, 325, 327, 625, 630, 726, 730, 753, 761, 765, 767]
for i in INDICES:
    t = p[i].text if i < len(p) else "<FUERA DE RANGO>"
    print("\n=== P%d ===" % i)
    print(repr(t))

print("\n=== TABLA 3 fila 3 ===")
t3 = doc.tables[3]
for j, c in enumerate(t3.rows[3].cells):
    print(j, repr(c.text))

print("\n=== CONTEO DE PATRONES EN TODO EL DOCUMENTO ===")
todo = "\n".join(x.text for x in p)
patrones = [
    "Addy et al., 2024",
    "Addy, 2023",
    "Organización Panamericana de la Salud y PATH, 2020",
    "Organización Panamericana de la Salud y PATH, 2019",
    "Fany (2024)",
    "Quispe Tello",
    "10665.2/53120",
    "10665.2/50482",
    "3576882-884-2022-minsa",
    "3642636-884-2022-minsa",
    "46000/9257",
    "Standardization, y International",
    "20.500.14168/854",
]
for q in patrones:
    print("%-60s -> %d" % (q, todo.count(q)))

print("\n=== ENCABEZADOS T52/T53 (repeticion de guion bajo) ===")
for idx in (52, 53):
    fila0 = doc.tables[idx].rows[0]
    print(idx, [repr(c.text) for c in fila0.cells])
