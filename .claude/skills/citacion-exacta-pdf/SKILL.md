---
name: citacion-exacta-pdf
description: Localiza en los PDFs de la bóveda el párrafo y la página exactos que sustentan una afirmación, verifica citas textuales palabra por palabra y arma la cita APA 7 con la página impresa. Usar SIEMPRE antes de escribir una cita con página, una cifra atribuida a un autor o una paráfrasis de una fuente indexada.
---

# CITACIÓN EXACTA DESDE PDF — SIVAC-THESIS-LAB

> **Regla de oro:** una página, cifra o frase atribuida a un autor solo se escribe si el buscador la encontró en el PDF. Si no la encontró, se escribe `[VERIFICAR: motivo]`. Nunca se adivina.

Intérprete obligatorio: `C:/MisInvestigaciones/tesis/sivac/.venv/Scripts/python.exe` (abreviado `$PY`). Ejecutar desde la raíz `C:/MisInvestigaciones/tesis/sivac`.

## 1. Dos números de página distintos

| Campo | Significado | Uso |
|---|---|---|
| `pagina_fisica` | Posición de la hoja en el PDF (1 = primera) | Localizar en el visor; **no se cita** |
| `etiqueta_impresa` | Número impreso en la página o etiqueta lógica del PDF | **Es la que se cita en APA** (`p. 45`) |

Existen desfases reales: Pressman 32 páginas, *Metodología de la investigación* 33, *User Stories Applied* 23. Si `etiqueta_impresa` es `null` (9 PDFs, p. ej. los artículos JMIR capturados de la web), la cita sale como `p. [VERIFICAR: página impresa no determinada; pág. PDF N]`.

## 2. Flujo de trabajo

1. **Indexar** (una vez por PDF; se regenera solo si cambia su SHA-256). Los 30 PDFs de `PDFs_SIVAC` ya están indexados en `04_LITERATURA_Y_FUENTES/indices_pdf/`.
   ```
   $PY scripts/fuentes/ingesta_pdf.py --todos
   $PY scripts/fuentes/ingesta_pdf.py "ruta/al.pdf" --forzar
   ```
2. **Buscar** la afirmación:
   ```
   $PY scripts/fuentes/buscador_citas.py buscar "texto o idea" --pdf "parte del nombre" --k 5 --autores "Beck,Fowler" --anio 1999 --tipo parafrasis [--parrafo] [--json]
   ```
   Devuelve PDF, página física, página impresa, número de párrafo, texto del párrafo, contexto, `score` (0-100) y `tipo` (`literal` o `aproximada`). Si el mejor `score` < 60 responde «sin coincidencia confiable»: **no forzar** un resultado.
3. **Verificar una cita textual** (entre comillas):
   ```
   $PY scripts/fuentes/buscador_citas.py verificar "fragmento exacto" --pdf "parte del nombre" --json
   ```
   `verificada: true` solo si es literal o similitud ≥ 97 y no hay palabras ni cifras alteradas. Una palabra cambiada que invierte el sentido NO se acepta.
4. **Citar** con el formato que devuelve `--autores/--anio/--tipo`: `(Apellido, año, p. X)`; tres o más autores → `et al.` desde la primera mención (APA 7); normas sin páginas → `párr. N` con `--parrafo`.
5. **Registrar** en la ficha `@citekey.md` de la fuente, sección «Hallazgos citables», el fragmento, la página impresa y el párrafo, para no repetir la búsqueda.

## 3. Prohibiciones

- No citar con número de página sin haber ejecutado `buscar` o `verificar`.
- No usar `pagina_fisica` como página APA.
- No traducir una cita textual entre comillas: parafrasear o citar en el idioma original.
- No tratar `tipo: aproximada` como literal: es paráfrasis cercana; revisar el párrafo completo antes de atribuirla.
- No inferir texto de páginas con `sin_capa_texto: true`: requieren OCR (Tesseract **no está instalado**; `content.pdf` y `u5uRux…pdf` tienen 14 y 8 páginas así). Declarar «requiere OCR» y pedir decisión al tesista.

## 4. Verificación cruzada
Antes de entregar un capítulo, `$PY scripts/agentes/verificador_integridad.py capitulo.md --md` comprueba correspondencia citas/referencias, DOIs en Crossref y, para las fuentes indexadas, las citas textuales.
