---
name: validacion-psicometrica
description: Algoritmos psicométricos (V de Aiken e IVC de Tristán-López) aplicables solo al certificado Fany 2024 del Instrumento N.° 03 llenado por jueces reales, con criterios dicotómicos Sí/No (DEC-015, DEC-020).
---

# VALIDACIÓN PSICOMÉTRICA DE INSTRUMENTOS: UNAJMA (EPIS)

> ## AVISO DE VIGENCIA: 2026-10-18
>
> **Esta skill calcula coeficientes; no autoriza a inventarlos.**
>
> Por **DEC-014**, el bloque psicométrico del proyecto fue declarado nulo: los tres jueces no
> evaluaron los instrumentos y los valores 0.987, 1.00 y [0.899, 0.999] son aritméticamente
> inalcanzables. Los generadores que los producían
> (`generar_expedientes_e_instrumentos.py` y `generar_matriz_ivc_excel.py`) están bloqueados.
>
> **Regla operativa:** las fórmulas de las secciones 2 a 5 solo pueden aplicarse sobre el
> certificado Fany 2024 del Instrumento N.° 03, Modalidad A, llenado a mano por jueces reales.
> Mientras no exista ese documento firmado, el cálculo permanece
> `BLOQUEADO: esperando juicio real`.
>
> **Nota de estructura:** el modelo vigente es dicotómico (Sí/No). Cada criterio tiene
> exactamente dos categorías, de modo que la V de Aiken se calcula con `c = 2` y su
> interpretación cambia respecto del modelo archivado.

---

## 0. Alcance del Juicio de Contenido (DEC-020)

El juicio de expertos se aplica a **un solo instrumento**: el Instrumento N.° 03, Cuestionario
de Satisfacción del Usuario, Modalidad A, con sus ocho reactivos (AP-01 a AP-04 y UP-01 a
UP-04). Los otros instrumentos no se someten a juicio de contenido y se acreditan por vía
propia:

| Instrumento | Vía de acreditación | Criterio |
|---|---|---|
| Instrumento N.° 01, Ficha de observación cronométrica | Protocolo de medición de movimientos de vacunas (PMMV) y acuerdo interobservador | ICC(2,1) >= 0.75 |
| Instrumento N.° 02, Ficha de registro y cotejo documental | Protocolo de medición de movimientos de vacunas (PMMV) y concordancia interauditor | Kappa de Cohen >= 0.80 |
| Instrumento N.° 03, Modalidad A (8 reactivos) | Juicio de contenido, certificado único Fany 2024 | V de Aiken >= 0.80 e IVC >= 0.80 |
| Instrumento N.° 03, Modalidad B (8 reactivos) | Módulo anexo de postest, sin baremación ni contraste | No recibe certificado |

---

## 1. Modelo de Contenido Vigente: Fany 2024 (DEC-015)

### 1.1. Los Tres Criterios Dicotómicos por Ítem
Cada juez experto evalúa cada uno de los ocho reactivos bajo tres criterios, y registra una
sola marca por criterio:

1. **Pertinencia:** El ítem corresponde al concepto teórico formulado.
2. **Relevancia:** El ítem es apropiado para representar al componente o dimensión específica
   del constructo.
3. **Claridad:** Se entiende sin dificultad alguna el enunciado del ítem, es conciso, exacto y
   directo.

### 1.2. Registro de la Respuesta
El certificado no admite grados intermedios. Cada celda se marca con `Sí` o `No`, sin casillas
de puntuación numérica y sin escala ordinal. Para el cálculo se codifica:

- `Sí` = 1 (acuerdo favorable)
- `No` = 0 (acuerdo desfavorable)

### 1.3. Ausencia de Dicotomización Posterior
No existe una calificación ordinal previa que deba dicotomizarse. El juez emite directamente
la categoría binaria, de modo que la matriz de cálculo no transforma puntajes: solo transcribe
las marcas Sí/No del certificado firmado.

**Nota sobre el modelo archivado:** el protocolo Cóndor Tinoco quedó superado por DEC-015. El
material se conserva en `salidas/instrumentos/formatos_validacion/_archivo_condor_no_usar/` y
no debe citarse como vigente. El script de cálculo conserva un perfil heredado para leer
matrices históricas, pero ese perfil nunca se usa para la captura del certificado actual.

---

## 2. Fórmulas del Índice de Validez de Contenido (IVC)

Sea `c_ijk` la marca binaria del juez `j` (`j = 1, ..., N`) al ítem `i` (`i = 1, ..., M`) en el
criterio `k` (`k = 1, 2, 3`, correspondientes a Pertinencia, Relevancia y Claridad).

### 2.1. IVC por Criterio en cada Ítem (IVC_ik)
$$IVC_{ik} = \frac{\sum_{j=1}^{N} c_{ijk}}{N}$$

Para un panel de N = 3 jueces, los valores posibles son 0/3 = 0.00, 1/3 = 0.33, 2/3 = 0.67 y
3/3 = 1.00.

### 2.2. IVC Promedio del Ítem (IVC_i)
El índice de cada reactivo es la media aritmética de los tres criterios:
$$IVC_i = \frac{1}{3} \sum_{k=1}^{3} IVC_{ik} = \frac{IVC_{i,\text{Per}} + IVC_{i,\text{Rel}} + IVC_{i,\text{Cla}}}{3}$$

### 2.3. IVC Global del Instrumento (IVC_total)
El índice global es el promedio de los IVC_i de los M = 8 reactivos de la Modalidad A:
$$IVC_{total} = \frac{1}{8} \sum_{i=1}^{8} IVC_i$$

---

## 3. Criterios de Decisión y Baremos

Para un panel de N = 3 jueces:

- **Umbral por ítem (Tristán-López, 2008):** IVC_i >= 0.58. Como los valores posibles son
  {0.00, 0.33, 0.67, 1.00}, el umbral exige que al menos 2 de los 3 jueces marquen Sí en el
  promedio de los tres criterios.
- **Regla por ítem:**
  - IVC_i >= 0.80: validez suficiente. Se mantiene el reactivo.
  - 0.58 <= IVC_i < 0.80: aceptable con ajustes de redacción sugeridos por los jueces.
  - IVC_i < 0.58: el reactivo se descarta o se reformula íntegramente.
- **Regla global:**
  - IVC_total >= 0.90: validez excelente.
  - 0.80 <= IVC_total < 0.90: validez buena, aplicable con ajustes menores.
  - IVC_total < 0.80: validez insuficiente, exige reformulación del instrumento.

**Advertencia de granularidad:** con N = 3 y tres criterios dicotómicos, cada IVC_ik solo puede
tomar cuatro valores. Toda decisión debe reportarse con el cociente exacto y no con decimales
redondeados que sugieran una precisión inexistente.

---

## 4. Matriz de Captura de Calificaciones Reales

La matriz se construye únicamente transcribiendo un certificado ya firmado. Su estructura
mínima es de formato largo, con una fila por combinación de juez, ítem y criterio:

| Columna | Contenido |
|---|---|
| `juez` | Identificador del experto (J1, J2, J3) |
| `item` | Código literal del reactivo (AP-01 a AP-04, UP-01 a UP-04) |
| `criterio` | `pertinencia`, `relevancia` o `claridad` |
| `puntaje` | 1 = Sí, 0 = No |

Reglas de integridad:

1. No se admiten celdas vacías ni valores distintos de 0 y 1.
2. No se admiten filas duplicadas para una misma combinación de juez, ítem y criterio.
3. El número de filas es 3 jueces x 8 ítems x 3 criterios = 72.
4. La matriz se deriva del certificado firmado; jamás se rellena por estimación.

El comando `scripts/agentes/validez_contenido.py plantilla` genera la captura vacía y
`calcular` procesa el archivo con calificaciones reales.

---

## 5. Coeficiente V de Aiken para Criterios Dicotómicos

Con criterios dicotómicos, el coeficiente se reduce a la proporción de jueces que marcan Sí:
$$V = \frac{S}{n}$$
donde `S` es el número de jueces que marcaron Sí y `n` es el número de jueces evaluadores.

- Rango de V: [0, 1].
- Valores alcanzables con n = 3: 0.000, 0.333, 0.667 y 1.000.
- **Consecuencia del umbral:** V >= 0.80 solo se alcanza con V = 1.000, es decir, con
  unanimidad perfecta de los tres jueces. Un solo voto negativo deja el ítem en 0.667 e
  incumple el umbral.
- **Intervalo de confianza al 95 % (Penfield y Giacobbi, 2004), con k = 1:**
  $$L = \frac{2nV + z^2 - 1 - z\sqrt{z^2 - 2 - \frac{1}{n} + 4nV(1 - V)}}{2(n + z^2)}$$
  donde `z` es el cuantil normal estándar para el nivel de confianza elegido.
- **Límite de significancia estadística:** con n = 3 y categorías equiprobables, la
  probabilidad exacta de obtener unanimidad bajo la hipótesis nula es 1/8 = 0.125, de modo que
  ningún valor de V puede alcanzar p < .05 con tres jueces. La decisión se sustenta en el
  coeficiente y en el juicio del panel, y esta limitación debe declararse expresamente en el
  informe.

---

## 6. Confiabilidad Psicométrica: Alfa de Cronbach

La consistencia interna se estima sobre los ocho reactivos de la Modalidad A (DEC-019): cuatro
de Aceptación del Proceso (AP-01 a AP-04) y cuatro de Utilidad Percibida (UP-01 a UP-04). Cada
subescala suma de 4 a 20 puntos y el total de la Modalidad A de 8 a 40 puntos; la Modalidad B no
se suma ni se barema.
$$\alpha = \frac{K}{K - 1} \left( 1 - \frac{\sum_{i=1}^{K} s_i^2}{s_t^2} \right)$$
donde K = 8 (número de reactivos), `s_i^2` es la varianza de las puntuaciones en el ítem `i` y
`s_t^2` es la varianza del puntaje total del cuestionario.

**Advertencia de potencia muestral:** con la población censal N = n = 14 la razón sujetos por
reactivo es 14 / 8 = 1.75, muy por debajo de la proporción 5:1 a 10:1 que suele exigirse para
estimar consistencia interna. El alfa debe reportarse con su intervalo de confianza al 95 % por
el método de Feldt, Woodruff y Salih, no como un valor puntual, y su magnitud no autoriza a
declarar de forma unívoca la fiabilidad del instrumento.

**Omega de McDonald:** no es estimable con n = 14 y 8 reactivos, porque el modelo factorial que
lo sustenta no es identificable de forma estable. No debe reportarse ningún valor de omega y su
ausencia debe constar expresamente en el informe, con la razón muestral que la motiva.

### Baremo de Confiabilidad (George y Mallery, 2003)
- Alfa >= 0.90: excelente.
- 0.80 <= Alfa < 0.90: buena (estándar meta para SIVAC).
- 0.70 <= Alfa < 0.80: aceptable.
- 0.60 <= Alfa < 0.70: cuestionable.
- Alfa < 0.60: inaceptable.
