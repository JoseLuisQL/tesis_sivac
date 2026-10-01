---
name: ingreso-fuentes-bibliograficas
description: Ingreso verificado de una fuente nueva por DOI: valida metadatos en Crossref, descarga el PDF de acceso abierto, comprueba que es el documento correcto, lo archiva en la bóveda, lo indexa y crea su ficha @citekey en Obsidian, dejando el registro en Zotero listo. Usar al incorporar cualquier fuente que no esté ya en la colección.
---

# INGRESO DE FUENTES BIBLIOGRÁFICAS — SIVAC-THESIS-LAB

Intérprete: `$PY` = `C:/MisInvestigaciones/tesis/sivac/.venv/Scripts/python.exe`, desde la raíz del repositorio.

## 1. Orden obligatorio
1. **Verificar sin descargar nada:** `$PY scripts/fuentes/descargar_fuente.py verificar <DOI> --json`. Si Crossref responde 404 la fuente **no existe verificada**: no se cita.
2. **Si solo hay título:** `… titulo "título aproximado"` lista candidatos **sin elegir ninguno**; el DOI correcto lo decide una persona y luego se usa `verificar`.
3. **Ingresar:** `… doi <DOI>` (o `… lote --archivo dois.txt`, UTF-8 con o sin BOM o UTF-16; otra codificación se rechaza con mensaje claro, exit 2).

## 2. Qué hace `doi`
- Normaliza el DOI y consulta Crossref (título, autores, año, revista, volumen, páginas).
- Localiza PDF de acceso abierto (OpenAlex; Unpaywall solo si existe `UNPAYWALL_EMAIL`).
- **Valida el PDF descargado:** empieza por `%PDF-`, abre con PyMuPDF, no está cifrado y su contenido coincide con el título de Crossref. Si no coincide **se descarta**; no se guarda un PDF equivocado.
- Guarda en `04_LITERATURA_Y_FUENTES/PDFs_articulos/PDFs_SIVAC/` como `Apellido - año - título-corto.pdf`, sin duplicar por SHA-256.
- Indexa con `ingesta_pdf` (habilita `citacion-exacta-pdf`).
- Crea `04_LITERATURA_Y_FUENTES/notas_fuentes_zotero/@citekey.md` con frontmatter YAML (`tipo`, `citekey`, `doi`, `anio`, `autores`, `verificado`, `pdf_local`, `sha256`, `paginas`, `fecha_ingreso`), referencia APA 7 y enlaces a `[[MOC_01_TESIS_SIVAC]]`. **Nunca sobrescribe** una ficha existente.
- Devuelve `zotero_payload`.

## 3. Registro en Zotero (lo hace el agente, no el script)
Con el MCP de Zotero: `zotero_add_item(source="<DOI>", collections=["4XAQ6D3D"], if_exists="file")`. Comprobar antes con `GET http://127.0.0.1:23119/connector/ping` sin proxy. Si Zotero no responde, dejar el `zotero_payload` en el handoff; no inventar la clave de Zotero.

## 4. Sin PDF de acceso abierto
La ficha queda con `pdf_local: null` y la nota «PDF no disponible en acceso abierto: solicitar al tesista». No se buscan copias en sitios no oficiales.

## 5. Después
Completar «Hallazgos citables» con `citacion-exacta-pdf`, y vincular la ficha a la dimensión DEC-007 que sustenta (Oportunidad, Consistencia documental o Satisfacción). Registrar handoff con `scripts/agentes/curador_cerebro.py registrar-handoff`.
