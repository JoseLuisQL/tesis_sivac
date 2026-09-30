#!/usr/bin/env node
const fs = require('fs');
const path = 'C:/MisInvestigaciones/obsidian_vault/00_SISTEMA/ESTADO_TESIS.md';

try {
  if (fs.existsSync(path)) {
    const content = fs.readFileSync(path, 'utf8');
    const firstLines = content.split('\n').slice(0, 25).join('\n');
    console.log(`\n=== [SIVAC-THESIS-LAB] ESTADO ACTUAL DE LA TESIS ===\n${firstLines}\n====================================================\n`);
  } else {
    console.log('[SIVAC-THESIS-LAB] Inicializando ecosistema. ESTADO_TESIS.md pendiente de generación.');
  }
} catch (e) {
  // Silent fallback
}
process.exit(0);
