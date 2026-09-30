---
name: formato-instrumentos-validacion
description: Plantillas y procedimientos para diseño de instrumentos y validación por juicio de expertos según modelos reales de UNAJMA.
---

# Formato de Instrumentos y Validación por Juicio de Expertos

Esta habilidad estandariza los instrumentos y la carpeta de validación de SIVAC según los modelos en `ejemplo_validacion/`.

## 1. Instrumentos de Recolección de Datos
1. **Fichas de Observación / Registro de Tiempos y Errores (Dimensiones 1, 2 y 3):**
   - *Oportunidad:* Registro de fecha/hora inicio y fecha/hora fin de registro de movimiento.
   - *Fiabilidad:* Lista de cotejo de concordancia física vs digital de existencias.
   - *Concordancia documental:* Matriz de verificación de vales físicos vs registros en base de datos.
2. **Cuestionario de Satisfacción del Usuario (Dimensión 4):**
   - Escala tipo Likert de 5 puntos (Totalmente en desacuerdo a Totalmente de acuerdo).
   - Items orientados a la utilidad percibida y facilidad de uso (Modelo TAM adaptado a SIVAC).

## 2. Paquete de Validación por Juicio de Expertos
Para cada uno de los expertos evaluadores (mínimo 3 ingenieros de sistemas/especialistas):
1. **Carta de presentación y solicitud de validación:** Dirigida al experto con título de tesis y objetivos.
2. **Ficha de definición de variables e indicadores:** Cuadro resumen para guiar al evaluador.
3. **Matriz de validación por ítem:** Criterios de claridad, pertinencia y relevancia (escala 1 a 5 o binaria según formato UNAJMA).
4. **Certificado de validez de contenido:** Con la opinión final (Aplicable / Requiere modificación / No aplicable) y firma del experto.
5. **Cálculo de Coeficiente V de Aiken o IVC:** Script y plantilla Excel para verificar que cada ítem y el instrumento global superen el umbral crítico ($V \ge 0.80$, $p < 0.05$).
