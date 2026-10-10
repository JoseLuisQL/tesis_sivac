#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditoría integral DEC-007 y correspondencia de citas 1:1 para informe_final_v01.docx
"""
import re
import docx

doc = docx.Document('salidas/documentos/informe_final_v01.docx')
text = '\n'.join([p.text for p in doc.paragraphs])
tables_text = '\n'.join([' '.join([c.text for c in row.cells]) for t in doc.tables for row in t.rows])
full_text = text + '\n' + tables_text

dims = [
    'Oportunidad de procesamiento',
    'Consistencia documental',
    'Satisfacción del usuario'
]

indicators = [
    'Tiempo de registro de movimiento',
    'Tiempo de emisión de comprobante',
    'registros sin discrepancias',
    'Concordancia de cantidad programada',
    'Aceptación del proceso',
    'Utilidad percibida'
]

print('=== AUDITORIA DIMENSIONES DEC-007 ===')
for d in dims:
    count = full_text.count(d)
    print(f'Dimensión "{d}": {count} menciones')

print('\n=== AUDITORIA INDICADORES ===')
for ind in indicators:
    count = full_text.count(ind)
    print(f'Indicador "{ind}": {count} menciones')

foreign_dims = ['fiabilidad del inventario', 'eficiencia del sistema', 'confiabilidad global']
print('\n=== VERIFICACION DE NO CONTAMINACION / DIMENSIONES AJENAS ===')
for fd in foreign_dims:
    count = full_text.count(fd)
    print(f'Dimensión ajena "{fd}": {count} menciones')

paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
ref_start = next(i for i, p in enumerate(paras) if p.upper() == 'REFERENCIAS BIBLIOGRÁFICAS')
anexo_start = next(i for i in range(ref_start + 1, len(paras)) if paras[i].upper() == 'ANEXOS')
ref_paras = paras[ref_start+1:anexo_start]

print(f'\n=== LISTA OFICIAL DE REFERENCIAS (Total: {len(ref_paras)}) ===')
print('Nuevas 6 fuentes:')
nuevas_fuentes = [
    'Gilbert',
    'Gutiérrez-Aguado',
    'Hussain',
    'Inarotul Huda',
    'Kokol',
    'Mamani-Pari'
]
for nf in nuevas_fuentes:
    found = [r for r in ref_paras if nf.lower() in r.lower()]
    print(f'  - {nf}: {"ENCONTRADA (" + str(len(found)) + ")" if found else "NO ENCONTRADA"}')

print('\n=== EXPERTOS DE VALIDACIÓN EPIS-UNAJMA EN ANEXO 3 ===')
expertos = [
    'Iván Edgard Soria Quispe',
    'Daniel Minaya Gómez',
    'Javier Arturo Ramos Cárdenas',
    'Iván Soria Solís',
    'Daniel Minaya Gutiérrez',
    'Javier Ramos Gonzales'
]
for exp in expertos:
    if exp in full_text:
        print(f'  - Experto "{exp}": PRESENTE en documento')
    else:
        print(f'  - Experto "{exp}": no detectado con nombre exacto')
