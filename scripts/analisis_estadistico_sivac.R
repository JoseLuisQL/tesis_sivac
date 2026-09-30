# ==============================================================================
# SISTEMA WEB SIVAC — PIPELINE DE ANÁLISIS ESTADÍSTICO REPRODUCIBLE EN R
# Escuela Profesional de Ingeniería de Sistemas — Universidad Nacional José María Arguedas
# Autor: Analista Estadístico (analista-estadistico)
# Directriz: Cero Alucinaciones, Verificabilidad Matemática y Normas APA 7.ª edición
# ==============================================================================

# 1. Definición de Rutas
base_dir <- getwd()
ruta_pretest <- file.path(base_dir, "datos", "bd_sivac_pretest.csv")
ruta_postest <- file.path(base_dir, "datos", "bd_sivac_postest.csv")
ruta_salida  <- file.path(base_dir, "salidas", "reporte_estadistico_r.txt")

cat("==============================================================================\n")
cat("SIVAC: ANÁLISIS ESTADÍSTICO DESCRIPTIVO E INFERENCIAL EN LENGUAJE R\n")
cat("==============================================================================\n")

if (!file.exists(ruta_pretest) || !file.exists(ruta_postest)) {
  cat("[!] Error: Archivos de datos no encontrados.\n")
  cat("[!] Estado: BLOQUEADO (Esperando entrega de datos de campo del tesista).\n")
  quit(status = 0)
}

# 2. Carga de Datos
df_pre  <- read.csv(ruta_pretest,  stringsAsFactors = FALSE)
df_post <- read.csv(ruta_postest, stringsAsFactors = FALSE)

# Ordenar por sujeto_id
df_pre  <- df_pre[order(df_pre$sujeto_id), ]
df_post <- df_post[order(df_post$sujeto_id), ]

cat(sprintf("[*] Datos cargados exitosamente: N = %d sujetos censales.\n", nrow(df_pre)))

# 3. Función de Confiabilidad: Alfa de Cronbach
calcular_alfa_cronbach_r <- function(items) {
  k <- ncol(items)
  var_items <- sum(apply(items, 2, var))
  puntos_totales <- rowSums(items)
  var_total <- var(puntos_totales)
  alfa <- (k / (k - 1)) * (1 - (var_items / var_total))
  return(alfa)
}

items_tam_cols <- c(paste0("ap_0", 1:5), paste0("up_0", 1:5))
alfa_pre  <- calcular_alfa_cronbach_r(df_pre[, items_tam_cols])
alfa_post <- calcular_alfa_cronbach_r(df_post[, items_tam_cols])

cat("\n[+] CONFIABILIDAD PSICOMÉTRICA (ALFA DE CRONBACH - CUESTIONARIO TAM):\n")
cat(sprintf("    - Pretest (10 ítems):  alpha = %.4f\n", alfa_pre))
cat(sprintf("    - Postest (10 ítems):  alpha = %.4f\n", alfa_post))

# 4. Pruebas de Normalidad de Shapiro-Wilk sobre Diferencias Pareadas
cat("\n[+] PRUEBAS DE NORMALIDAD DE SHAPIRO-WILK (DIFERENCIAS D = POST - PRE):\n")

variables_eval <- list(
  list(col = "t_reg",           nom = "Tiempo de Registro (min)",            dir = "less"),
  list(col = "t_vale",          nom = "Tiempo de Emisión de Vales (min)",    dir = "less"),
  list(col = "rsd",             nom = "% Registros sin Discrepancia",       dir = "greater"),
  list(col = "cpe",             nom = "% Concordancia Programada/Entregada", dir = "greater"),
  list(col = "score_ap",        nom = "Aceptación del Proceso (TAM)",        dir = "greater"),
  list(col = "score_up",        nom = "Utilidad Percibida (TAM)",            dir = "greater"),
  list(col = "score_tam_total", nom = "Satisfacción Global TAM",             dir = "greater")
)

resultados_shapiro <- data.frame(Variable = character(), W = numeric(), p_valor = numeric(), Normal = character())

for (v in variables_eval) {
  diff <- df_post[[v$col]] - df_pre[[v$col]]
  sh <- shapiro.test(diff)
  es_norm <- ifelse(sh$p.value > 0.05, "SÍ (Normal)", "NO (No normal)")
  cat(sprintf("    - %-40s: W = %.4f, p = %.4e -> %s\n", v$nom, sh$statistic, sh$p.value, es_norm))
}

# 5. Pruebas de Hipótesis Inferencial: Rangos con Signo de Wilcoxon
cat("\n[+] CONTRASTE INFERENCIAL NO PARAMÉTRICO DE WILCOXON (MUESTRAS PAREADAS):\n")

for (v in variables_eval) {
  x1 <- df_pre[[v$col]]
  x2 <- df_post[[v$col]]

  # Wilcoxon pareado
  wt_one <- wilcox.test(x2, x1, paired = TRUE, alternative = v$dir, exact = FALSE, correct = TRUE)
  wt_two <- wilcox.test(x2, x1, paired = TRUE, alternative = "two.sided", exact = FALSE, correct = TRUE)

  # Z aproximado
  p_two <- wt_two$p.value
  z_score <- qnorm(1 - p_two / 2)
  diff_mean <- mean(x2 - x1)
  if ((v$dir == "less" && diff_mean > 0) || (v$dir == "greater" && diff_mean < 0)) {
    z_score <- -abs(z_score)
  } else {
    z_score <- abs(z_score)
  }

  r_rosenthal <- abs(z_score) / sqrt(2 * length(x1))

  cat(sprintf("    - %-38s: V = %.1f, Z = %.3f, p_one = %.4e, r = %.3f\n",
              v$nom, wt_one$statistic, z_score, wt_one$p.value, r_rosenthal))
}

cat("\n==============================================================================\n")
cat("[*] Análisis estadístico reproducible en R completado con éxito.\n")
cat("==============================================================================\n")
