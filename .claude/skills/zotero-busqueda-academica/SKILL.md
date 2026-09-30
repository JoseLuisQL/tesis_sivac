---
name: zotero-busqueda-academica
description: Protocolos quirúrgicos para consultar la colección de Zotero, recuperar metadatos, verificar DOIs, vincular PDFs locales y realizar búsquedas académicas de respaldo vía Firecrawl y You.com para SIVAC-THESIS-LAB.
---

# BÚSQUEDA Y GESTIÓN BIBLIOGRÁFICA EN ZOTERO — SIVAC

> **Principio Innegociable:** Cero alucinaciones. Toda afirmación fáctica o teórica en la tesis debe poseer respaldo verificado en Zotero (`@citekey`), DOI activo verificado o URL de repositorio institucional (RENATI/ALICIA/SUNEDU).

---

## 1. Repositorio Maestro en Zotero

- **Nombre de la Colección:** `TESIS_SIVAC_BIBLIOGRAFIA_ZOTERO`
- **Key de la Colección en Zotero:** `4XAQ6D3D`
- **Total de Fuentes Curadas:** 26 fuentes primarias (artículos Scopus/WoS/PubMed, libros normativos y tesis de repositorios).
- **Ubicación de PDFs Locales en Obsidian:** `C:\MisInvestigaciones\obsidian_vault\02-LITERATURA-ZOTERO\PDFs_SIVAC\`
- **Catálogo Detallado en Obsidian:** `04_LITERATURA/CATALOGO_MAESTRO_FUENTES_ZOTERO_SIVAC.md`
- **Lista APA 7 Maestra:** `04_LITERATURA/REFERENCIAS_SIVAC.md`

---

## 2. Protocolo de Consulta con MCP Zotero

Cuando un agente requiera sustentar una sección teórica, metodológica o de discusión:

### 2.1. Búsqueda por Subcadena de Autor o Año
```json
{
  "query": "Astuhuaman 2024",
  "qmode": "titleCreatorYear",
  "limit": 5
}
```
*Herramienta:* `mcp__zotero__zotero_search_items`.

### 2.2. Obtención de Metadatos y Abstract Completo
```json
{
  "item_key": "AXV7ZDMC",
  "format": "markdown",
  "include_abstract": true
}
```
*Herramienta:* `mcp__zotero__zotero_get_item_metadata`.

### 2.3. Exportación de Referencia en Formato APA 7 o BibTeX
```json
{
  "item_keys": ["AXV7ZDMC", "8DGREDL4"],
  "style": "apa",
  "export_format": "bib"
}
```
*Herramienta:* `mcp__zotero__zotero_export_bibliography`.

### 2.4. Localización de Archivo PDF Físico
```json
{
  "item_key": "AXV7ZDMC"
}
```
*Herramienta:* `mcp__zotero__zotero_get_attachment_path`.
Si se opera en entorno de archivos locales, consultar directamente en `C:\MisInvestigaciones\obsidian_vault\02-LITERATURA-ZOTERO\PDFs_SIVAC\`.

---

## 3. Matriz de Mapeo Rápido: Indicadores SIVAC vs Citekeys Zotero

| Variable / Dimensión SIVAC | Indicador Específico | Fuentes Primarias en Zotero | Citekey | Aporte Clave a la Tesis |
|---|---|---|---|---|
| **VI: Sistema Web SIVAC** | Metodología Extreme Programming (XP) | Beck (1999), Cohn (2004), Pressman (2010), Sommerville (2016), Mego (2021) | `@beck1999`, `@cohn2004`, `@pressman2010`, `@sommerville2016`, `@mego2021` | Fases de XP (Exploración, Planificación, Iteraciones, Puesta en producción) y 15 Historias de Usuario. |
| **VI: Calidad del Software** | Adecuación funcional y usabilidad | ISO/IEC (2023), Moumane et al. (2024), Ruiz Barea (2023), Luján Mora (2002) | `@iso25010_2023`, `@moumane2024`, `@ruizbarea2023`, `@lujanmora2002` | Evaluación del producto de software bajo ISO/IEC 25010:2023 y seguridad de APIs REST con JWT. |
| **VD-D1: Oportunidad** | Tiempo de registro ($T_{reg}$) / Tiempo emisión vales ($T_{vale}$) | Balón (2023), Astuhuaman & Baltazar (2024), Dang et al. (2024), Wasswa et al. (2023) | `@balon2023`, `@astuhuaman2024`, `@dang2024`, `@wasswa2023` | Balón redujo tiempos de 3-4 días a 6 segundos; Dang redujo tiempos de 36.1 a 11.7 días; Astuhuaman mejoró citas en Apurímac en un 83%. |
| **VD-D2: Consistencia** | % Registros sin discrepancias ($RSD$) / % Concordancia ($CPE$) | Shen et al. (2024), Kigenza et al. (2023), Chekol et al. (2023), Garcia & Calderón (2023) | `@shen2024`, `@kigenza2023`, `@chekol2023`, `@garcia2023` | Shen redujo tasa de errores de 0.425‰ a 0.025‰; Kigenza elevó la concordancia de inventario del 25% al 85%; Chekol documentó causas de subregistro. |
| **VD-D3: Satisfacción** | Aceptación del proceso ($AP$) / Utilidad percibida ($UP$) | Davis (1989), Ndlovu et al. (2021), Duong et al. (2021), Brooks et al. (2024) | `@ndlovu2021`, `@duong2021`, `@brooks2024` | Modelo TAM en personal de salud; Ndlovu demostró 87% de aceptación en trabajadores sanitarios; Duong evaluó adopción en Vietnam. |
| **Marco Sanitario** | Cadena de frío y movimientos de vacunas | MINSA (2022), OPS/PATH (2020), Champi (2023), Ergetie et al. (2023) | `@minsa2022`, `@opspath2020`, `@champi2023`, `@ergetie2023` | NTS N° 196-MINSA/DGIESP-2022; lineamientos de la OPS para digitalización e-LMIS en inmunizaciones. |
| **Metodología y Estadística** | Diseño preexperimental, muestreo, normalidad, Wilcoxon | Hernández-Sampieri et al. (2014), George & Mallery (2003) | `@sampieri2014`, `@georgemallery2003` | Diseño preexperimental $O_1 \to X \to O_2$, confiabilidad Alfa de Cronbach y baremos psicométricos. |

---

## 4. Protocolo de Búsqueda Externa (Respaldo en Firecrawl y You.com)

Si se requiere localizar un antecedente o norma complementaria no presente en la colección inicial:

1. **Búsqueda Académica con Firecrawl:**
   - Usar `mcp__firecrawl__firecrawl_search` con `categories: ["research"]` o `categories: ["developer"]`.
   - Incluir términos específicos: `"cadena de frio" AND vacunas AND "sistema web" AND (Peru OR Apurimac)`.
2. **Búsqueda con You.com:**
   - Usar `mcp__ydc-server__you-search` para localizar artículos indexados en SciELO, Redalyc, Dialnet o repositorios universitarios RENATI.
   - Usar `mcp__ydc-server__you-contents` para extraer el texto completo y verificar el DOI antes de redactar.
3. **Ingreso a Zotero:**
   - Una vez comprobada la validez de la nueva fuente, se registra en Zotero mediante `mcp__zotero__zotero_add_item(source=DOI, collections=['4XAQ6D3D'])`.
   - Se crea su ficha en `C:\MisInvestigaciones\obsidian_vault\04_LITERATURA_Y_FUENTES\notas_fuentes_zotero\@citekey.md`.

---

## 5. Lista de Verificación Anti-Alucinaciones
Antes de incorporar una cita en cualquier borrador:
- [ ] ¿Existe el `@citekey` en `CATALOGO_MAESTRO_FUENTES_ZOTERO_SIVAC.md`?
- [ ] ¿Los autores y el año coinciden con la fuente original (sin invertir orden ni alterar grafías)?
- [ ] ¿Si es cita textual, se dispone del número exacto de página verificado en el PDF?
- [ ] ¿Si es paráfrasis, refleja con fidelidad el hallazgo cuantitativo o conceptual del autor original?
- [ ] ¿Si no se cuenta con el PDF o DOI verificado, se colocó la marca explícita `[VERIFICAR: motivo]`?
