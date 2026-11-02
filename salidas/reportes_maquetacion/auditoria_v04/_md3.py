# -*- coding: utf-8 -*-
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

a = json.load(open('_audit_tmp.json', encoding='utf-8'))
DF = a['defectos']; R = a['resumen']; P = a['paginas']
byd = {}
for d in DF: byd.setdefault(d['pagina'], []).append(d)

L = []
def w(s=''): L.append(s)

w('## 8. Pictogramas y marcadores de plantilla')
w('')
w('| Clase | Unicode | Cantidad | Ubicación |')
w('|---|---|---|---|')
w('| Cámara | U+1F4F7 | 4 | Tablas de las cajas A7.1 a A7.4, páginas 157-158 |')
w('| Mano escribiendo | U+270D | 3 | Certificados de los expertos 1, 2 y 3, páginas 148-149 |')
w('')
w('Los siete pictogramas son ajenos al registro editorial institucional. El reemplazo textual sobrio ya está redactado en el JSON de auditoría: «Espacio reservado para fotografía de evidencia en campo» y «Firma y sello del juez validador».')
w('')
w('Marcadores de plantilla pendientes: acta de sustentación con instrucción de inserción y dictamen prellenado (p2); DNI del autor con doble marcador (p3); advertencia DATOS DE PRUEBA - REEMPLAZAR (DEC-007) impresa en el cuerpo del Capítulo V (p115); nombre, DNI y firma de los tres jueces (pp. 148-149); instrucción para el tesista en las cuatro cajas del Anexo 7 (pp. 157-158).')
w('')
w('## 9. Fichas por página observada')
w('')
for x in P:
    if x['veredicto'] != 'OBSERVADA':
        continue
    ds = byd[x['pagina']]
    w('### Página %d (folio %s, %s) — OBSERVADA' % (x['pagina'], x['folio_impreso'] or 'sin folio', x['orientacion']))
    w('')
    for d in ds:
        ref = ('P%04d' % d['indice_docx']) if d['elemento'] == 'parrafo' and d['indice_docx'] is not None else \
              ('TABLA %d' % d['indice_docx']) if d['indice_docx'] is not None else d['elemento']
        w('- `%s` · **%s** (%s): %s' % (ref, d['tipo'], d['severidad'], d['descripcion']))
        w('  - Corrección: %s' % d['correccion_sugerida'])
    w('')
w('## 10. Control de inmutabilidad')
w('')
w('Los archivos de referencia y el documento auditado se abrieron en modo de solo lectura. No se ejecutó ninguna escritura sobre `informe_final_v04.docx` ni sobre `informe_final_v04.pdf`: la huella SHA-256 registrada en el apartado 1 corresponde al estado previo y posterior a la auditoría. Los únicos archivos creados son los PNG de render, los auxiliares de medición y este informe, todos bajo `salidas/reportes_maquetacion/`.')
w('')
w('## 11. Recomendaciones priorizadas')
w('')
w('1. **Cirugía de rejilla (bloqueante).** Llevar a 8 765 dxa las diecinueve tablas con exceso significativo y a 13 697 dxa la Tabla A1.1. En T37 eliminar la columna n, constante igual a 14, y redistribuir su ancho entre las columnas de texto.')
w('2. **Matrices de 18 columnas (bloqueante).** Dividir T52 y T53 en dos tablas de 9 columnas (identificación y puntajes) o trasladarlas a una sección horizontal con anchos mínimos de 700 dxa. Con la rejilla actual el dato no es legible en papel.')
w('3. **Control de rótulos (bloqueante para QG-9).** Aplicar keepNext a los 115 párrafos de rótulo y a todos los encabezados de nivel 2 y 3; unir número y título de figura en un párrafo único. Esto resuelve las diecisiete separaciones detectadas entre páginas 46 y 130 y en el Anexo 7.')
w('4. **Renumeración única.** Asignar numeración continua a tablas (1 a 59) y figuras (1 a 52), actualizar las once referencias cruzadas erróneas del Capítulo V y regenerar los índices de figuras y de tablas a partir de campos SEQ.')
w('5. **Regeneración del índice de contenido.** Aplicar Heading 1 a 3 a todas las secciones; hoy el índice omite el 3.3, el Capítulo V, el Capítulo VI, Conclusiones, Recomendaciones y Anexos.')
w('6. **Limpieza editorial.** Retirar la advertencia de datos de prueba, sustituir los siete pictogramas, completar los datos de los certificados y del acta, e insertar las fotografías del Anexo 7 o retirar las cajas.')
w('7. **Control de viudas.** Ajustar interlineado y altura de fila en pp. 131, 141, 145, 147, 151 y 155 para evitar páginas con menos del 20 por ciento de ocupación.')
w('')
w('---')
w('')
w('## Anexo A. Inventario completo de tablas')
w('')
ts = json.load(open('_tstats.json', encoding='utf-8'))
w('| Tabla | Filas | Cols. | Rejilla dxa | Exceso sobre caja útil |')
w('|---|---|---|---|---|')
for s in ts:
    lim = 13697 if s['t'] == 44 else 8765
    w('| T%02d | %d | %d | %d | %+d |' % (s['t'], s['rows'], s['cols'], s['grid'], s['grid'] - lim))
w('')
w('## Anexo B. Correspondencia con el JSON')
w('')
w('El registro estructurado `auditoria_hoja_por_hoja_v04.json` contiene los 158 veredictos de página, los 90 defectos con la estructura exigida (`pagina`, `elemento`, `indice_docx`, `tipo`, `descripcion`, `severidad`, `correccion_sugerida`) y las mediciones agregadas. Los índices `indice_docx` de párrafo corresponden a la numeración P del volcado `informe_final_v04_texto_plano.md`; los de tabla corresponden a la numeración TABLA del mismo volcado.')
w('')
open('_md_part3.md', 'w', encoding='utf-8').write('\n'.join(L))
print('part3', len(L), 'lines')
