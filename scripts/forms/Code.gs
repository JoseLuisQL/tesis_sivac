/**
 * ================================================================================
 * SIVAC-THESIS-LAB — GENERADOR PROFESIONAL DE ECOSISTEMA GOOGLE FORMS
 * Proyecto: APLICACIÓN DEL SISTEMA "SIVAC" PARA MEJORAR LA GESTIÓN DE
 *           MOVIMIENTOS DE VACUNAS EN EL PERSONAL DE INMUNIZACIONES DE LA
 *           DIRECCIÓN DE SALUD APURÍMAC II
 * Modelo espejo: Jhon_Tesis_Bachiller_2026 (223p) — Anexos 3 y 4 + Forms
 * Institución: Universidad Nacional José María Arguedas (UNAJMA) — EPIS
 * Tesista: Bach. José Luis Quispe León (DNI 70519963)
 * Asesora: Dra. Norma Lorena Catacora Flores  |  VD: DEC-007 (3 dimensiones)
 * Diseño: Preexperimental O1 → X → O2, censal N=n=14, validación 3 jueces
 * Fecha de validación formal: 19 de octubre de 2026
 * ================================================================================
 * INSTRUCCIONES DE USO (como en Jhon 2026):
 * 1. Cree un Google Sheet vacío en su Drive institucional (ej. SIVAC_BD_TRABAJO_CAMPO).
 * 2. En el Sheet: Extensiones > Apps Script > pegue íntegro este archivo Code.gs.
 * 3. Ejecute generarEcosistemaFormulariosSIVAC() y autorice permisos.
 * 4. El script crea carpeta SIVAC_RECOLECCION_DATOS_2026 con los 3 Forms vinculados
 *    al Sheet, validaciones de rango y destino automático de respuestas.
 * 5. Obtenga enlaces con obtenerEnlacesFormularios() o desde Drive.
 * ================================================================================
 */

/** Punto de entrada principal — crea los 3 formularios vinculados al Sheet activo. */
function generarEcosistemaFormulariosSIVAC() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const folderName = "SIVAC_RECOLECCION_DATOS_2026";

  const folders = DriveApp.getFoldersByName(folderName);
  let targetFolder;
  if (folders.hasNext()) {
    targetFolder = folders.next();
  } else {
    targetFolder = DriveApp.createFolder(folderName);
  }

  Logger.log("=== SIVAC — Iniciando construcción de ecosistema de formularios ===");
  Logger.log("Sheet destino: " + ss.getName() + " (" + ss.getId() + ")");
  Logger.log("Carpeta Drive: " + targetFolder.getName());

  crearFormularioCronometrico(targetFolder, ss);
  crearFormularioDocumental(targetFolder, ss);
  crearFormularioTAM(targetFolder, ss);

  Logger.log("=== Ecosistema SIVAC generado y vinculado exitosamente ===");
  Logger.log("Ejecute obtenerEnlacesFormularios() para ver los enlaces de edición y respuesta.");
}

/** Devuelve enlaces de edición y respuesta de los 3 Forms del ecosistema. */
function obtenerEnlacesFormularios() {
  const folderName = "SIVAC_RECOLECCION_DATOS_2026";
  const folder = DriveApp.getFoldersByName(folderName);
  if (!folder.hasNext()) {
    Logger.log("No se encontró la carpeta " + folderName + ". Ejecute generarEcosistemaFormulariosSIVAC() primero.");
    return;
  }
  const f = folder.next();
  const files = f.getFilesByType(MimeType.GOOGLE_FORMS);
  while (files.hasNext()) {
    const file = files.next();
    const form = FormApp.openById(file.getId());
    Logger.log("────────────────────────────────────────");
    Logger.log("Formulario: " + form.getTitle());
    Logger.log("  Edición  : " + form.getEditUrl());
    Logger.log("  Respuesta: " + form.getPublishedUrl());
    Logger.log("  ID       : " + form.getId());
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// FORMULARIO 01 — FICHA CRONOMÉTRICA (D1: Oportunidad — T_reg / T_vale)
// ─────────────────────────────────────────────────────────────────────────────
function crearFormularioCronometrico(folder, ss) {
  const form = FormApp.create("SIVAC-INST01: Ficha Cronométrica de Oportunidad de Procesamiento");
  form.setDescription(
    "Instrumento N.º 01 — Medición del tiempo en minutos decimales insumido en el registro de movimientos (T_reg) y en la emisión de vales oficiales (T_vale). "
    + "Comparación Pretest (O1: kardex manual/Excel) vs Postest (O2: sistema web SIVAC). "
    + "Población censal N=n=14 — DISA Apurímac II. Tesista: Bach. José Luis Quispe León (UNAJMA-EPIS)."
  );
  form.setAllowResponseEdits(false);
  form.setIsQuiz(false);
  form.setProgressBar(true);
  form.setConfirmationMessage("Registro cronométrico guardado correctamente. Gracias por su participación.");

  const file = DriveApp.getFileById(form.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  // — Identificación —
  form.addSectionHeaderItem().setTitle("A. IDENTIFICACIÓN DEL OPERADOR CENSAL Y DE LA MEDICIÓN");

  const itemTrab = form.addListItem().setTitle("Código del Trabajador de Salud").setHelpText("Seleccione su código anonimizado asignado (TRAB-01 a TRAB-14).").setRequired(true);
  itemTrab.setChoiceValues(generarCodigosTrabajadores());

  const itemCentro = form.addListItem().setTitle("Centro de Acopio Provincial").setHelpText("Sede donde se realiza la observación.").setRequired(true);
  itemCentro.setChoiceValues(obtenerCentrosAcopio());

  const itemFase = form.addMultipleChoiceItem().setTitle("Fase de Medición").setHelpText("O1 = método manual tradicional | O2 = sistema web SIVAC.").setRequired(true);
  itemFase.setChoiceValues(["PRETEST (O1: Método manual / kardex físico / Excel)", "POSTEST (O2: Sistema web SIVAC)"]);

  form.addDateItem().setTitle("Fecha de la Observación").setHelpText("Fecha real de la medición cronometrada.").setRequired(true);
  form.addTextItem().setTitle("Observador / Evaluador").setHelpText("Nombre del observador (tesista o asistente calibrado).").setRequired(true);

  // — Sección B: T_reg —
  form.addSectionHeaderItem().setTitle("B. TIEMPO DE REGISTRO DE MOVIMIENTOS (T_reg)")
    .setHelpText("T_reg = t_fin_registro − t_inicio_registro. Inicia al tomar el documento fuente o abrir el módulo; finaliza al guardar y balancear el movimiento. Unidad: minutos decimales (precisión 0.01 min).");

  form.addTextItem().setTitle("Batería de tareas ejecutada").setHelpText("Ej. REG-01 ingreso simple, REG-02 despacho regular, REG-03 reajuste multibioplástico.").setRequired(true);

  const itemTreg = form.addTextItem().setTitle("Tiempo Neto de Registro — T_reg (minutos decimales)").setHelpText("Ejemplo: 3.25 = 3 min 15 s. Debe ser mayor a 0.").setRequired(true);
  itemTreg.setValidation(FormApp.createTextValidation().requireNumberGreaterThan(0).setHelpText("Debe ingresar un valor numérico positivo mayor a 0 (ej. 2.50).").build());

  form.addParagraphTextItem().setTitle("Incidencias u Observaciones de Campo en el Registro (opcional)").setHelpText("Cortes de fluido, atención urgente u otras interrupciones pausadas.").setRequired(false);

  // — Sección C: T_vale —
  form.addSectionHeaderItem().setTitle("C. TIEMPO DE EMISIÓN DE VALES OFICIALES (T_vale)")
    .setHelpText("T_vale = t_emisión_documento − t_inicio_solicitud. Culmina al generar/imprimir el PDF foliado con numeración oficial.");

  form.addTextItem().setTitle("Número de Vale Oficial / PECOSA Auditado").setHelpText("Ej. VALE-2026-001 o PECOSA N.º.").setRequired(true);

  const itemCant = form.addTextItem().setTitle("Cantidad de Ítems Biológicos en el Vale").setHelpText("Número entero positivo de vacunas/insumos en el vale.").setRequired(true);
  itemCant.setValidation(FormApp.createTextValidation().requireWholeNumber().requireNumberGreaterThan(0).setHelpText("Debe ser un número entero positivo.").build());

  const itemTvale = form.addTextItem().setTitle("Tiempo Neto de Emisión de Vale — T_vale (minutos decimales)").setHelpText("Ejemplo: 4.75 = 4 min 45 s. Debe ser mayor a 0.").setRequired(true);
  itemTvale.setValidation(FormApp.createTextValidation().requireNumberGreaterThan(0).setHelpText("Debe ingresar un valor numérico positivo mayor a 0.").build());

  form.addMultipleChoiceItem().setTitle("Método utilizado para el registro/emisión").setChoiceValues(["Manual / kardex físico", "Hoja Excel dispersa", "Sistema web SIVAC"]).setRequired(true);

  // Vincular al Sheet (cada Form crea su propia hoja de respuestas)
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  Logger.log("Form 01 Cronométrico creado: " + form.getEditUrl());
  Logger.log("  Respuesta: " + form.getPublishedUrl());
}

// ─────────────────────────────────────────────────────────────────────────────
// FORMULARIO 02 — FICHA DOCUMENTAL (D2: Consistencia — RSD / CPE)
// ─────────────────────────────────────────────────────────────────────────────
function crearFormularioDocumental(folder, ss) {
  const form = FormApp.create("SIVAC-INST02: Ficha de Cotejo Documental de Consistencia");
  form.setDescription(
    "Instrumento N.º 02 — Auditoría física vs registros: % Registros sin discrepancias (RSD) y Concordancia programada vs entregada (CPE). "
    + "Ventana PMMV de 30 días calendario consecutivos por fase. Corpus 40–60 transacciones por ventana — DISA Apurímac II. "
    + "Regla inmutable de 8 criterios simultáneos para RSD. Tesista: Bach. José Luis Quispe León."
  );
  form.setProgressBar(true);
  form.setConfirmationMessage("Auditoría documental registrada correctamente. Gracias.");
  form.setAllowResponseEdits(false);

  const file = DriveApp.getFileById(form.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  // — Identificación —
  form.addSectionHeaderItem().setTitle("A. DATOS DE LA AUDITORÍA DOCUMENTAL");

  form.addListItem().setTitle("Código del Trabajador / Centro Auditado").setChoiceValues(generarCodigosTrabajadores()).setRequired(true);
  form.addListItem().setTitle("Centro de Acopio Provincial").setChoiceValues(obtenerCentrosAcopio()).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Fase de Auditoría").setChoiceValues(["PRETEST (O1: Kardex físico / cuadernos manuales)", "POSTEST (O2: Base de datos SIVAC + vales PDF)"]).setRequired(true);
  form.addDateItem().setTitle("Fecha de Auditoría").setRequired(true);
  form.addTextItem().setTitle("Ventana Temporal Auditada (30 días)").setHelpText("Ej. 01/03/2026 al 30/03/2026.").setRequired(true);

  // — Sección B: RSD —
  form.addSectionHeaderItem().setTitle("B. PORCENTAJE DE REGISTROS SIN DISCREPANCIAS (RSD)")
    .setHelpText("RSD = (N_conformes / N_total_auditados) × 100. Un registro es CONFORME (1) solo si cumple simultáneamente los 8 criterios; si falla 1 → NO CONFORME (0).");

  const itemLotesTot = form.addTextItem().setTitle("Total de Registros / Lotes Auditados en la Ventana (N_total)").setHelpText("Corpus de la ventana: típicamente 40–60 registros.").setRequired(true);
  itemLotesTot.setValidation(FormApp.createTextValidation().requireWholeNumber().requireNumberBetween(1, 200).setHelpText("Debe ser un entero entre 1 y 200.").build());

  const itemLotesConf = form.addTextItem().setTitle("Número de Registros Conformes sin Discrepancia (N_conformes)").setHelpText("Debe ser ≤ N_total. Cumplen los 8 criterios simultáneos.").setRequired(true);
  itemLotesConf.setValidation(FormApp.createTextValidation().requireWholeNumber().requireNumberBetween(0, 200).setHelpText("Debe ser un entero entre 0 y 200, y ≤ N_total.").build());

  const itemRSD = form.addTextItem().setTitle("RSD Calculado (%) — Registros sin discrepancias").setHelpText("Calcule: (N_conformes / N_total) × 100. Ej. 85.00").setRequired(true);
  itemRSD.setValidation(FormApp.createTextValidation().requireNumberBetween(0, 100).setHelpText("Debe estar entre 0 y 100.").build());

  form.addCheckboxItem().setTitle("Tipos de Discrepancias Detectadas en la Muestra (marque todas las que apliquen)").setChoiceValues([
    "Ninguna — Conformidad absoluta (8/8 criterios)",
    "C1: Tipo de movimiento mal clasificado",
    "C2: Denominación del biológico no estandarizada",
    "C3: Número de lote no coincide con frasco físico",
    "C4: Fecha de caducidad omitida o no coincide",
    "C5: Cantidad física no coincide con documento",
    "C6: Origen/Destino sin código RENIPRESS",
    "C7: Responsable sin firma/usuario trazable",
    "C8: Sin documento formal de respaldo (vale/PECOSA/guía)",
    "Descuadre aritmético en saldo final",
    "Omisión de registro de salida o merma"
  ]).setRequired(true);

  // — Sección C: CPE —
  form.addSectionHeaderItem().setTitle("C. CONCORDANCIA PROGRAMADA vs ENTREGADA (CPE)")
    .setHelpText("CPE = (Q_entregada / Q_programada) × 100. Concordante si Q_ent=Q_prog o existe acta/memorando MINSA que justifica variación.");

  const itemProg = form.addTextItem().setTitle("Total de Dosis Programadas en Requerimiento Mensual (Q_prog)").setRequired(true);
  itemProg.setValidation(FormApp.createTextValidation().requireWholeNumber().requireNumberGreaterThan(0).build());

  const itemEnt = form.addTextItem().setTitle("Total de Dosis Efectivamente Entregadas y Sustentadas (Q_ent)").setRequired(true);
  itemEnt.setValidation(FormApp.createTextValidation().requireWholeNumber().requireNumberGreaterThan(0).build());

  const itemCPE = form.addTextItem().setTitle("CPE Calculado (%) — Concordancia programada vs entregada").setHelpText("Calcule: (Q_ent / Q_prog) × 100. Ej. 96.50").setRequired(true);
  itemCPE.setValidation(FormApp.createTextValidation().requireNumberBetween(0, 200).setHelpText("Debe estar entre 0 y 200%.").build());

  form.addMultipleChoiceItem().setTitle("Causa Primaria de No Concordancia (si aplica)").setChoiceValues([
    "Ninguna — Concordancia completa (Q_ent = Q_prog)",
    "Ajuste técnico justificado con acta MINSA (concordante)",
    "Quiebre de stock en almacén central DISA",
    "Descuadre de existencias previo al despacho",
    "Lote vencido/inmovilizado retirado de la remesa",
    "Recorte preventivo por capacidad de cadena de frío receptora"
  ]).setRequired(true);

  form.addParagraphTextItem().setTitle("Observaciones de Auditoría (opcional)").setRequired(false);

  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  Logger.log("Form 02 Documental creado: " + form.getEditUrl());
  Logger.log("  Respuesta: " + form.getPublishedUrl());
}

// ─────────────────────────────────────────────────────────────────────────────
// FORMULARIO 03 — CUESTIONARIO TAM (D3: Satisfacción — AP / UP)
// ─────────────────────────────────────────────────────────────────────────────
function crearFormularioTAM(folder, ss) {
  const form = FormApp.create("SIVAC-INST03: Cuestionario de Satisfacción del Usuario (Modelo TAM)");
  form.setDescription(
    "Instrumento N.º 03 — Satisfacción del usuario bajo Technology Acceptance Model (TAM; Davis, 1989) + ISO/IEC 25010:2023. "
    + "Escala Likert 1 (Totalmente en Desacuerdo) a 5 (Totalmente de Acuerdo). 8 ítems oficiales para HE3 (AP + UP) + 8 anexo clásico SIVAC (PU + PEOU). "
    + "Población censal N=n=14 — DISA Apurímac II. Ley N.º 29733 de Protección de Datos Personales — respuestas anónimas (código TRAB-XX). "
    + "Tesista: Bach. José Luis Quispe León | Asesora: Dra. Norma Lorena Catacora Flores."
  );
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);
  form.setConfirmationMessage("Cuestionario TAM registrado correctamente. ¡Gracias por su participación!");
  form.setIsQuiz(false);

  const file = DriveApp.getFileById(form.getId());
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);

  // — Consentimiento y Datos —
  form.addSectionHeaderItem().setTitle("A. CONSENTIMIENTO INFORMADO Y DATOS DEL PARTICIPANTE")
    .setHelpText("Sus respuestas son anónimas y confidenciales (Ley 29733). Se identifican solo por código TRAB-XX.");

  form.addMultipleChoiceItem().setTitle("¿Confirmo que he leído y firmado el Consentimiento Informado y acepto participar voluntariamente?").setChoiceValues(["SÍ, acepto participar voluntariamente"]).setRequired(true);
  form.addListItem().setTitle("Código Asignado de Participante").setChoiceValues(generarCodigosTrabajadores()).setRequired(true);
  form.addListItem().setTitle("Centro de Acopio Asignado").setChoiceValues(obtenerCentrosAcopio()).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Condición Laboral").setChoiceValues(["Nombrado", "Contratado CAS", "Servicios Tercerizados"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Profesión / Cargo").setChoiceValues(["Lic. en Enfermería", "Técnico en Enfermería", "Otro"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Años de Experiencia en Cadena de Frío").setChoiceValues(["Menos de 2 años", "2 a 5 años", "6 a 10 años", "Más de 10 años"]).setRequired(true);
  form.addMultipleChoiceItem().setTitle("Fase de Evaluación").setChoiceValues(["PRETEST (O1: Proceso manual / kardex y Excel tradicional)", "POSTEST (O2: Proceso informatizado mediante sistema web SIVAC)"]).setRequired(true);

  // — Subdimensión 3.1: AP (4 ítems oficiales HE3) —
  form.addSectionHeaderItem().setTitle("B. SUBDIMENSIÓN 3.1: ACEPTACIÓN DEL PROCESO OPERATIVO (AP)")
    .setHelpText("Marque del 1 al 5 según su experiencia real en la fase evaluada.");

  const itemsAP = [
    "El procedimiento actual para registrar movimientos diarios y cierres no demanda un esfuerzo excesivo.",
    "El flujo de trabajo para emitir vales de entrega es fluido y libre de demoras o trabas burocraticas.",
    "El metodo permite conciliar saldos con las microredes reduciendo el estres y la incertidumbre laboral.",
    "El tiempo dedicado al registro deja disponibilidad para realizar tareas sanitarias y asistenciales del servicio."
  ];
  itemsAP.forEach(function(text) {
    form.addScaleItem().setTitle(text).setBounds(1, 5).setLabels("Totalmente en Desacuerdo", "Totalmente de Acuerdo").setRequired(true);
  });

  // — Subdimensión 3.2: UP (4 ítems oficiales HE3) —
  form.addSectionHeaderItem().setTitle("C. SUBDIMENSIÓN 3.2: UTILIDAD PERCIBIDA PARA LA GESTIÓN (UP)")
    .setHelpText("Marque del 1 al 5 según su experiencia real en la fase evaluada.");

  const itemsUP = [
    "El mecanismo permite disponer de informacion fidedigna y en tiempo real del stock de vacunas.",
    "El control de lotes y vencimientos previene oportunamente mermas y perdidas de biologicos.",
    "Facilita la deteccion inmediata y la rectificacion de cualquier descuadre de inventario fisico.",
    "En general, es una herramienta altamente eficaz para asegurar el abastecimiento de vacunas."
  ];
  itemsUP.forEach(function(text) {
    form.addScaleItem().setTitle(text).setBounds(1, 5).setLabels("Totalmente en Desacuerdo", "Totalmente de Acuerdo").setRequired(true);
  });

  // — Anexo TAM clásico SIVAC — solo Postest (PU + PEOU) —
  form.addSectionHeaderItem().setTitle("D. MÓDULO COMPLEMENTARIO ANEXO: CALIDAD EN USO DEL SOFTWARE SIVAC (solo POSTEST)")
    .setHelpText("Este bloque aplica exclusivamente en POSTEST. En PRETEST déjelo sin responder o marque Neutral (3) según indicación del evaluador. PU = Utilidad Percibida | PEOU = Facilidad de Uso Percibida (Davis, 1989).");

  const itemsPU = [
    "Utilizar SIVAC agiliza notablemente el registro de entradas, salidas y transferencias.",
    "SIVAC permite consultar inmediatamente existencias y saldos por lote y fecha de caducidad.",
    "La generacion automatica de vales oficiales en PDF agiliza sustancialmente el despacho.",
    "SIVAC incrementa la productividad global en el control de la cadena de frio institucional."
  ];
  itemsPU.forEach(function(text) {
    form.addScaleItem().setTitle(text).setBounds(1, 5).setLabels("Totalmente en Desacuerdo", "Totalmente de Acuerdo").setRequired(false);
  });

  const itemsPEOU = [
    "La interfaz grafica de SIVAC es limpia, intuitiva y facil de comprender para el operador.",
    "Aprender a operar los modulos de movimientos y lotes requirio poco tiempo y esfuerzo.",
    "Los mensajes de confirmacion y validacion de stock orientan claramente las acciones.",
    "Es facil lograr que SIVAC realice exactamente las tareas requeridas durante la jornada."
  ];
  itemsPEOU.forEach(function(text) {
    form.addScaleItem().setTitle(text).setBounds(1, 5).setLabels("Totalmente en Desacuerdo", "Totalmente de Acuerdo").setRequired(false);
  });

  form.addParagraphTextItem().setTitle("Comentario o sugerencia adicional sobre el proceso (opcional)").setRequired(false);

  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  Logger.log("Form 03 TAM creado: " + form.getEditUrl());
  Logger.log("  Respuesta: " + form.getPublishedUrl());
}

// ─────────────────────────────────────────────────────────────────────────────
// LISTAS DE APOYO ESTANDARIZADAS (censal N=14, 11 centros DISA Apurímac II)
// ─────────────────────────────────────────────────────────────────────────────
function generarCodigosTrabajadores() {
  const codes = [];
  for (let i = 1; i <= 14; i++) {
    codes.push("TRAB-" + (i < 10 ? "0" + i : i));
  }
  return codes;
}

function obtenerCentrosAcopio() {
  return [
    "Centro de Acopio Almacén Central DISA Apurímac II (Andahuaylas)",
    "Centro de Acopio C.S. San Jerónimo",
    "Centro de Acopio C.S. Talavera",
    "Centro de Acopio C.S. Huancabamba",
    "Centro de Acopio C.S. Turpo",
    "Centro de Acopio C.S. Kishuará",
    "Centro de Acopio C.S. Huancarama",
    "Centro de Acopio C.S. Pacucha",
    "Centro de Acopio C.S. Pampachiri",
    "Centro de Acopio Almacén Subregional Chincheros",
    "Centro de Acopio C.S. Uripa"
  ];
}
