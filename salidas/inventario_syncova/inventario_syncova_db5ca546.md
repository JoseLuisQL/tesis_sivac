# Inventario del código SIVAC (syncova)

- Repositorio: `C:\Proyectos\syncova` (solo lectura)
- Commit documentado: `db5ca5464c7162e56d72fe5f59e1fa02668045c4` (sha1; rama `main`; fuente: git rev-parse HEAD)
- Fecha del commit: 2026-09-10T08:58:54-05:00 — feat: implement ReporteService with inventory, movement, and critical stock reporting interfaces
- Huella SHA-256 del inventario: `83418cc5edd6b02dcc815a8b5d51b0fe6616d63adfe871cac196f50311e59bd5`
- Generado: 2026-10-01T00:57:49+00:00

## Resumen

| Elemento | Cantidad |
| --- | --- |
| modelos | 31 |
| enums | 12 |
| relaciones | 94 |
| endpoints | 291 |
| endpoints_sin_autenticacion | 68 |
| rutas_react | 44 |
| archivos_prueba | 16 |
| casos_prueba_aprox | 151 |
| variables_entorno | 23 |
| migraciones_prisma | 7 |
| paquetes_npm | 2 |

## Stack

| Paquete | Rol | Versión declarada |
| --- | --- | --- |
| react | Biblioteca de interfaz | ^18.3.1 |
| vite | Empaquetador/dev server | ^5.4.19 |
| typescript | Lenguaje | ^5.5.3 |
| express | Servidor HTTP | ^4.18.2 |
| @prisma/client | ORM (cliente) | ^5.7.1 |
| prisma | ORM (CLI) | ^5.7.1 |
| react-router-dom | Enrutamiento cliente | ^6.20.1 |
| tailwindcss | Estilos | ^3.4.1 |
| jest | Pruebas unitarias | ^29.7.0 |
| @playwright/test | Pruebas E2E | ^1.58.2 |
| axios | Cliente HTTP | ^1.18.1 |
| jsonwebtoken | Autenticación JWT | ^9.0.2 |
| bcrypt | Hash de contraseñas | ^6.0.0 |
| recharts | Gráficos | ^2.8.0 |
| exceljs | Exportación Excel | ^4.4.0 |
| zod | Validación | ^4.3.6 |
| express-validator | Validación | ^7.2.1 |
| joi | Validación | ^17.11.0 |
| tsx | Ejecución TS | ^4.6.2 |
| helmet | Seguridad HTTP | ^7.1.0 |
| cors | CORS | ^2.8.5 |
| express-rate-limit | Limitación de tasa | ^7.1.5 |

### package.json (sistema-vacunas-apurimac 1.0.0)

Dependencias: 16; devDependencies: 16

| Script npm | Comando |
| --- | --- |
| dev | `vite` |
| typecheck | `tsc -p tsconfig.app.json --noEmit` |
| build | `tsc -p tsconfig.app.json --noEmit && vite build` |
| lint | `eslint .` |
| preview | `vite preview` |
| design:lint | `node scripts/sync-design-md.mjs --check` |
| design:sync | `node scripts/sync-design-md.mjs` |
| design:export:tailwind | `node scripts/sync-design-md.mjs --print-tailwind` |
| design:export:dtcg | `node scripts/sync-design-md.mjs --print-dtcg` |

### backend/package.json (sivac-backend 1.0.0)

Dependencias: 26; devDependencies: 22

| Script npm | Comando |
| --- | --- |
| dev | `tsx watch src/index.ts` |
| build | `tsc` |
| start | `node -r ./register-aliases.js dist/index.js` |
| db:generate | `prisma generate` |
| db:push | `prisma db push` |
| db:migrate | `prisma migrate dev` |
| db:seed | `tsx prisma/seed.ts` |
| db:studio | `prisma studio` |
| db:reset | `prisma migrate reset` |
| db:migrate-entrega-base | `tsx scripts/migrate-entrega-base.ts` |
| db:create-triggers | `tsx scripts/create-triggers.ts` |
| db:setup | `tsx scripts/setup-database.ts` |
| db:migrate-tipo-vale | `node scripts/apply-tipo-vale-migration.js` |
| test:multiple-vouchers | `node scripts/test-multiple-vouchers.js` |
| verify:solution | `node scripts/verify-solution.js` |
| clear-rate-limit | `node ../scripts/clear-rate-limit.js` |
| fix:lotes | `tsx scripts/run-lote-correction.ts` |
| fix:lotes-verify | `tsx scripts/run-lote-correction.ts -- --verificar-solo` |
| fix:lotes-correct | `tsx scripts/run-lote-correction.ts -- --corregir --backup` |
| fix:lotes-dt | `tsx scripts/run-lote-correction.ts -- --caso-dt` |
| lint | `node ../node_modules/eslint/bin/eslint.js src/**/*.ts` |
| lint:fix | `node ../node_modules/eslint/bin/eslint.js src/**/*.ts --fix` |
| test | `jest --forceExit` |
| test:watch | `jest --watch` |

## Estructura (niveles 1 y 2)

| Carpeta | Archivos |
| --- | --- |
| agent | 14 |
| agent/skills | 14 |
| backend | 222 |
| backend/docs | 4 |
| backend/migrations | 3 |
| backend/prisma | 20 |
| backend/scripts | 24 |
| backend/src | 159 |
| docker | 6 |
| docker/db-init | 1 |
| docker/sql | 2 |
| docs | 17 |
| docs/ci | 2 |
| public | 3 |
| scripts | 2 |
| src | 314 |
| src/components | 222 |
| src/config | 4 |
| src/constants | 1 |
| src/contexts | 5 |
| src/hooks | 30 |
| src/services | 34 |
| src/styles | 4 |
| src/types | 4 |
| src/utils | 6 |
| tests | 1 |
| tests/ui | 1 |

Excluidos (no leídos): .agents (1), .claude (1), .factory (1), .git (1), .playwright-cli (1), dist (2), node_modules (2), output (1), test-results (1), uploads (1)
Secretos omitidos sin abrir: 4

## Esquema Prisma

| Modelo | Tabla | Campos | Archivo:línea |
| --- | --- | --- | --- |
| Red | redes | 8 | backend/prisma/schema.prisma:98 |
| Microred | microredes | 10 | backend/prisma/schema.prisma:113 |
| CentroAcopio | centros_acopio | 16 | backend/prisma/schema.prisma:131 |
| Establecimiento | establecimientos | 19 | backend/prisma/schema.prisma:155 |
| Vacuna | vacunas | 20 | backend/prisma/schema.prisma:181 |
| Jeringa | jeringas | 11 | backend/prisma/schema.prisma:209 |
| LoteVacuna | lotes_vacunas | 15 | backend/prisma/schema.prisma:227 |
| LoteJeringa | lotes_jeringas | 15 | backend/prisma/schema.prisma:249 |
| Usuario | usuarios | 29 | backend/prisma/schema.prisma:271 |
| UsuarioCentroAcopio | usuarios_centros_acopio | 6 | backend/prisma/schema.prisma:309 |
| IciDemidRegistro | ici_demid_registros | 30 | backend/prisma/schema.prisma:324 |
| PlanificacionAnual | planificacion_anual | 11 | backend/prisma/schema.prisma:364 |
| ProgramacionAnualCenares | programacion_anual_cenares | 12 | backend/prisma/schema.prisma:383 |
| MovimientoVacuna | movimientos_vacunas | 20 | backend/prisma/schema.prisma:408 |
| EntregaAdicional | entregas_adicionales | 10 | backend/prisma/schema.prisma:436 |
| ValeEntrega | vales_entrega | 18 | backend/prisma/schema.prisma:454 |
| ValeDetalle | vales_detalle | 11 | backend/prisma/schema.prisma:481 |
| Kardex | kardex | 19 | backend/prisma/schema.prisma:500 |
| Alerta | alertas | 13 | backend/prisma/schema.prisma:526 |
| ConfiguracionSistema | configuracion_sistema | 9 | backend/prisma/schema.prisma:550 |
| StockInicialMensual | stock_inicial_mensual | 9 | backend/prisma/schema.prisma:564 |
| ConfiguracionJeringaVacunaDefecto | configuracion_jeringa_vacuna_defecto | 10 | backend/prisma/schema.prisma:584 |
| ConfiguracionJeringaVacunaCentro | configuracion_jeringa_vacuna_centro | 12 | backend/prisma/schema.prisma:607 |
| Role | roles | 10 | backend/prisma/schema.prisma:637 |
| Permission | permissions | 11 | backend/prisma/schema.prisma:656 |
| RolePermission | role_permissions | 6 | backend/prisma/schema.prisma:678 |
| PermisoOperativo | permisos_operativos | 14 | backend/prisma/schema.prisma:698 |
| SibotSession | sibot_sessions | 9 | backend/prisma/schema.prisma:723 |
| SibotAttachment | sibot_attachments | 13 | backend/prisma/schema.prisma:740 |
| SibotToolExecution | sibot_tool_executions | 12 | backend/prisma/schema.prisma:762 |
| SibotSecurityEvent | sibot_security_events | 9 | backend/prisma/schema.prisma:783 |

### Red

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombre | String |  | UK |  |
| codigo | String? |  | UK |  |
| descripcion | String? |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| microredes | Microred[] | relación |  |  |

### Microred

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombre | String |  |  |  |
| codigo | String? |  |  |  |
| descripcion | String? |  |  |  |
| redId | String |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| red | Red | relación |  |  |
| centrosAcopio | CentroAcopio[] | relación |  |  |

### CentroAcopio

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombre | String |  |  |  |
| codigo | String? |  | UK |  |
| microredId | String? |  |  |  |
| direccion | String |  |  |  |
| responsable | String |  |  |  |
| telefono | String? |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| microred | Microred? | relación |  |  |
| establecimientos | Establecimiento[] | relación |  |  |
| usuarios | Usuario[] | relación |  |  |
| usuariosAsignados | UsuarioCentroAcopio[] | relación |  |  |
| valesEntrega | ValeEntrega[] | relación |  |  |
| configuracionesJeringaVacuna | ConfiguracionJeringaVacunaCentro[] | relación |  |  |

### Establecimiento

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombre | String |  |  |  |
| tipo | TipoEstablecimiento | enum |  |  |
| codigo | String |  | UK |  |
| centroAcopioId | String |  |  |  |
| direccion | String |  |  |  |
| responsable | String |  |  |  |
| telefono | String? |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| centroAcopio | CentroAcopio | relación |  |  |
| usuarios | Usuario[] | relación |  |  |
| planificaciones | PlanificacionAnual[] | relación |  |  |
| movimientos | MovimientoVacuna[] | relación |  |  |
| valesDetalle | ValeDetalle[] | relación |  |  |
| kardexOrigen | Kardex[] | relación |  |  |
| kardexDestino | Kardex[] | relación |  |  |
| iciDemidRegistros | IciDemidRegistro[] | relación |  |  |

### Vacuna

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| codigo | String? |  |  |  |
| nombre | String |  |  |  |
| tipo | String |  |  |  |
| presentacion | String |  |  |  |
| dosisPorFrasco | Int |  |  |  |
| tiempoVidaUtil | Int |  |  |  |
| temperaturaAlmacenamiento | String |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| lotes | LoteVacuna[] | relación |  |  |
| planificaciones | PlanificacionAnual[] | relación |  |  |
| movimientos | MovimientoVacuna[] | relación |  |  |
| valesDetalle | ValeDetalle[] | relación |  |  |
| configuracionesDefecto | ConfiguracionJeringaVacunaDefecto[] | relación |  |  |
| configuracionesCentro | ConfiguracionJeringaVacunaCentro[] | relación |  |  |
| programacionesCenares | ProgramacionAnualCenares[] | relación |  |  |
| stocksInicialesMensuales | StockInicialMensual[] | relación |  |  |
| iciDemidRegistros | IciDemidRegistro[] | relación |  |  |

### Jeringa

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| tipo | String |  |  |  |
| capacidad | String |  |  |  |
| color | String |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| lotes | LoteJeringa[] | relación |  |  |
| configuracionesDefecto | ConfiguracionJeringaVacunaDefecto[] | relación |  |  |
| configuracionesCentro | ConfiguracionJeringaVacunaCentro[] | relación |  |  |
| programacionesCenares | ProgramacionAnualCenares[] | relación |  |  |

### LoteVacuna

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| numero | String |  | UK |  |
| vacunaId | String |  |  |  |
| fechaIngreso | DateTime |  |  |  |
| fechaVencimiento | DateTime |  |  |  |
| formaIngreso | FormaIngreso | enum |  |  |
| comprobanteClase | ComprobanteClase | enum |  |  |
| numeroComprobante | String |  |  |  |
| cantidadInicial | Int |  |  |  |
| cantidadActual | Int |  |  |  |
| estado | EstadoLote | enum |  | disponible |
| observaciones | String? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| vacuna | Vacuna | relación |  |  |

### LoteJeringa

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| jeringaId | String |  |  |  |
| numero | String |  | UK |  |
| fechaIngreso | DateTime |  |  |  |
| fechaVencimiento | DateTime? |  |  |  |
| formaIngreso | FormaIngreso | enum |  |  |
| comprobanteClase | ComprobanteClase | enum |  |  |
| numeroComprobante | String |  |  |  |
| cantidadInicial | Int |  |  |  |
| cantidadActual | Int |  |  |  |
| estado | EstadoLote | enum |  | disponible |
| observaciones | String? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| jeringa | Jeringa | relación |  |  |

### Usuario

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombres | String |  |  |  |
| apellidos | String |  |  |  |
| email | String |  | UK |  |
| usuario | String |  | UK |  |
| passwordHash | String |  |  |  |
| rol | RolUsuario | enum |  |  |
| roleId | String? |  |  |  |
| establecimientoId | String? |  |  |  |
| centroAcopioId | String? |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| ultimoAcceso | DateTime? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| establecimiento | Establecimiento? | relación |  |  |
| centroAcopio | CentroAcopio? | relación |  |  |
| centrosAcopioAsignados | UsuarioCentroAcopio[] | relación |  |  |
| role | Role? | relación |  |  |
| movimientos | MovimientoVacuna[] | relación |  |  |
| entregas | EntregaAdicional[] | relación |  |  |
| vales | ValeEntrega[] | relación |  |  |
| kardex | Kardex[] | relación |  |  |
| alertas | Alerta[] | relación |  |  |
| iciDemidRegistros | IciDemidRegistro[] | relación |  |  |
| permisosOperativos | PermisoOperativo[] | relación |  |  |
| permisosOperativosCreados | PermisoOperativo[] | relación |  |  |
| sibotSessions | SibotSession[] | relación |  |  |
| sibotToolExecutions | SibotToolExecution[] | relación |  |  |
| sibotSecurityEvents | SibotSecurityEvent[] | relación |  |  |

### UsuarioCentroAcopio

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| usuarioId | String |  |  |  |
| centroAcopioId | String |  |  |  |
| createdAt | DateTime |  |  | now() |
| usuario | Usuario | relación |  |  |
| centroAcopio | CentroAcopio | relación |  |  |

### IciDemidRegistro

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| establecimientoId | String |  |  |  |
| vacunaId | String |  |  |  |
| anio | Int |  |  |  |
| microRed | String |  |  |  |
| codigoMed | String |  |  |  |
| medicamentoOriginal | String |  |  |  |
| medff | String? |  |  |  |
| medtip | String? |  |  |  |
| medpet | String? |  |  |  |
| medest | String? |  |  |  |
| distribucionMensual | Int[] |  |  | [] |
| mesesDisponibles | Int[] |  |  | [] |
| stockFin | Int |  |  | 0 |
| totalDistribu | Int |  |  | 0 |
| mesRotacion | Int? |  |  |  |
| cpma | Decimal? |  |  |  |
| mesAbastec | Decimal? |  |  |  |
| disponibilidad | String? |  |  |  |
| situacion | String? |  |  |  |
| fecExp | DateTime? |  |  |  |
| requerimiento | Decimal? |  |  |  |
| ajuste | Decimal? |  |  |  |
| archivoNombre | String? |  |  |  |
| usuarioId | String? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| establecimiento | Establecimiento | relación |  |  |
| vacuna | Vacuna | relación |  |  |
| usuario | Usuario? | relación |  |  |

### PlanificacionAnual

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| establecimientoId | String |  |  |  |
| vacunaId | String |  |  |  |
| anio | Int |  |  |  |
| metaAnual | Int |  |  |  |
| distribucionMensual | Int[] |  |  |  |
| estado | EstadoPlanificacion | enum |  | borrador |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| establecimiento | Establecimiento | relación |  |  |
| vacuna | Vacuna | relación |  |  |

### ProgramacionAnualCenares

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| vacunaId | String? |  |  |  |
| jeringaId | String? |  |  |  |
| anio | Int |  |  |  |
| programadoQ1 | Int |  |  | 0 |
| programadoQ2 | Int |  |  | 0 |
| programadoQ3 | Int |  |  | 0 |
| programadoQ4 | Int |  |  | 0 |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| vacuna | Vacuna? | relación |  |  |
| jeringa | Jeringa? | relación |  |  |

### MovimientoVacuna

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| establecimientoId | String |  |  |  |
| vacunaId | String |  |  |  |
| mes | Int |  |  |  |
| anio | Int |  |  |  |
| saldoAnterior | Int |  |  | 0 |
| transIngreso | Int |  |  | 0 |
| salida | Int |  |  | 0 |
| transSalida | Int |  |  | 0 |
| entrega | Int |  |  | 0 |
| entregaBase | Int? |  |  |  |
| observaciones | String? |  |  |  |
| fechaMovimiento | DateTime |  |  | now() |
| usuarioId | String |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| establecimiento | Establecimiento | relación |  |  |
| vacuna | Vacuna | relación |  |  |
| usuario | Usuario | relación |  |  |
| entregasAdicionales | EntregaAdicional[] | relación |  |  |

### EntregaAdicional

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| movimientoVacunaId | String |  |  |  |
| numeroEntrega | Int |  |  |  |
| cantidad | Int |  |  |  |
| fechaEntrega | DateTime |  |  | now() |
| motivo | String? |  |  |  |
| usuarioId | String |  |  |  |
| createdAt | DateTime |  |  | now() |
| movimientoVacuna | MovimientoVacuna | relación |  |  |
| usuario | Usuario | relación |  |  |

### ValeEntrega

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("gen_random_uuid()") |
| numero | String |  | UK |  |
| centroAcopioId | String |  |  |  |
| mes | Int |  |  |  |
| anio | Int |  |  |  |
| fechaGeneracion | DateTime |  |  | now() |
| estado | EstadoVale | enum |  | generado |
| tipoVale | TipoVale | enum |  | completo |
| gruposEntregasAdicionales | String? |  |  |  |
| totalVacunas | Int |  |  | 0 |
| totalEstablecimientos | Int |  |  | 0 |
| usuarioId | String |  |  |  |
| observaciones | String? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| centroAcopio | CentroAcopio | relación |  |  |
| usuario | Usuario | relación |  |  |
| detalles | ValeDetalle[] | relación |  |  |

### ValeDetalle

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| valeEntregaId | String |  |  |  |
| establecimientoId | String |  |  |  |
| vacunaId | String |  |  |  |
| cantidadProgramada | Int |  |  | 0 |
| cantidadAdicional | Int |  |  | 0 |
| numeroEntregaAdicional | Int? |  |  |  |
| createdAt | DateTime |  |  | now() |
| valeEntrega | ValeEntrega | relación |  |  |
| establecimiento | Establecimiento | relación |  |  |
| vacuna | Vacuna | relación |  |  |

### Kardex

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| tipo | String |  |  |  |
| itemId | String |  |  |  |
| loteId | String |  |  |  |
| tipoMovimiento | TipoMovimientoKardex | enum |  |  |
| cantidad | Int |  |  |  |
| saldoAnterior | Int |  |  | 0 |
| saldoActual | Int |  |  |  |
| establecimientoOrigenId | String? |  |  |  |
| establecimientoDestinoId | String? |  |  |  |
| documento | String |  |  |  |
| numeroDocumento | String |  |  |  |
| observaciones | String? |  |  |  |
| usuarioId | String |  |  |  |
| fechaMovimiento | DateTime |  |  | now() |
| createdAt | DateTime |  |  | now() |
| establecimientoOrigen | Establecimiento? | relación |  |  |
| establecimientoDestino | Establecimiento? | relación |  |  |
| usuario | Usuario | relación |  |  |

### Alerta

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| tipo | TipoAlerta | enum |  |  |
| titulo | String |  |  |  |
| descripcion | String |  |  |  |
| nivel | NivelAlerta | enum |  |  |
| fechaCreacion | DateTime |  |  | now() |
| fechaVencimiento | DateTime? |  |  |  |
| leida | Boolean |  |  | false |
| usuarioId | String? |  |  |  |
| parametros | Json? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| usuario | Usuario? | relación |  |  |

### ConfiguracionSistema

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| clave | String |  | UK |  |
| valor | String |  |  |  |
| descripcion | String? |  |  |  |
| tipoDato | String |  |  | "string" |
| categoria | String |  |  | "general" |
| esPublico | Boolean |  |  | false |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |

### StockInicialMensual

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| vacunaId | String |  |  |  |
| mes | Int |  |  |  |
| anio | Int |  |  |  |
| stockInicial | Int |  |  |  |
| fechaCaptura | DateTime |  |  | now() |
| observaciones | String? |  |  |  |
| createdAt | DateTime |  |  | now() |
| vacuna | Vacuna | relación |  |  |

### ConfiguracionJeringaVacunaDefecto

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| vacunaId | String |  |  |  |
| jeringaId | String |  |  |  |
| multiplicador | Decimal |  |  | 1.0 |
| prioridad | Int |  |  | 1 |
| activo | Boolean |  |  | true |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| vacuna | Vacuna | relación |  |  |
| jeringa | Jeringa | relación |  |  |

### ConfiguracionJeringaVacunaCentro

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| centroAcopioId | String |  |  |  |
| vacunaId | String |  |  |  |
| jeringaId | String |  |  |  |
| multiplicador | Decimal |  |  | 1.0 |
| prioridad | Int |  |  | 1 |
| activo | Boolean |  |  | true |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| centroAcopio | CentroAcopio | relación |  |  |
| vacuna | Vacuna | relación |  |  |
| jeringa | Jeringa | relación |  |  |

### Role

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombre | String |  | UK |  |
| descripcion | String? |  |  |  |
| codigo | String |  | UK |  |
| estado | EstadoGeneral | enum |  | activo |
| esDefault | Boolean |  |  | false |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| rolePermissions | RolePermission[] | relación |  |  |
| usuarios | Usuario[] | relación |  |  |

### Permission

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| nombre | String |  | UK |  |
| descripcion | String? |  |  |  |
| codigo | String |  | UK |  |
| recurso | String |  |  |  |
| accion | String |  |  |  |
| categoria | String |  |  |  |
| estado | EstadoGeneral | enum |  | activo |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| rolePermissions | RolePermission[] | relación |  |  |

### RolePermission

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| roleId | String |  |  |  |
| permissionId | String |  |  |  |
| createdAt | DateTime |  |  | now() |
| role | Role | relación |  |  |
| permission | Permission | relación |  |  |

### PermisoOperativo

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| tipo | String |  |  |  |
| usuarioId | String? |  |  |  |
| mes | Int |  |  |  |
| anio | Int |  |  |  |
| habilitado | Boolean |  |  | false |
| programado | Boolean |  |  | false |
| fechaActivacion | DateTime? |  |  |  |
| fechaDesactivacion | DateTime? |  |  |  |
| creadoPorId | String |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| usuario | Usuario? | relación |  |  |
| creadoPor | Usuario | relación |  |  |

### SibotSession

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| localSessionId | String |  | UK |  |
| usuarioId | String |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| usuario | Usuario | relación |  |  |
| attachments | SibotAttachment[] | relación |  |  |
| toolExecutions | SibotToolExecution[] | relación |  |  |
| securityEvents | SibotSecurityEvent[] | relación |  |  |

### SibotAttachment

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| sessionId | String |  |  |  |
| tipo | String |  |  |  |
| mimeType | String |  |  |  |
| nombreOriginal | String |  |  |  |
| nombreArchivo | String |  |  |  |
| storagePath | String |  |  |  |
| tamanoBytes | Int |  |  |  |
| sha256 | String |  |  |  |
| metadata | Json? |  |  |  |
| createdAt | DateTime |  |  | now() |
| updatedAt | DateTime |  |  | now() |
| session | SibotSession | relación |  |  |

### SibotToolExecution

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| sessionId | String? |  |  |  |
| usuarioId | String |  |  |  |
| toolName | String |  |  |  |
| status | String |  |  |  |
| filtersApplied | Json? |  |  |  |
| evidence | Json? |  |  |  |
| recordCount | Int? |  |  |  |
| durationMs | Int? |  |  |  |
| createdAt | DateTime |  |  | now() |
| session | SibotSession? | relación |  |  |
| usuario | Usuario | relación |  |  |

### SibotSecurityEvent

| Campo | Tipo | Mod. | PK/UK | Default |
| --- | --- | --- | --- | --- |
| id | String |  | PK  | dbgenerated("uuid_generate_v4()") |
| sessionId | String? |  |  |  |
| usuarioId | String |  |  |  |
| tipo | String |  |  |  |
| severidad | String |  |  |  |
| detalle | Json? |  |  |  |
| createdAt | DateTime |  |  | now() |
| session | SibotSession? | relación |  |  |
| usuario | Usuario | relación |  |  |

### Enums

| Enum | Valores |
| --- | --- |
| TipoEstablecimiento | centro_salud, puesto_salud, hospital |
| EstadoGeneral | activo, inactivo |
| EstadoPlanificacion | borrador, aprobado, ejecutado |
| EstadoLote | disponible, vencido, agotado |
| FormaIngreso | PRIMER_TRIMESTRE, SEGUNDO_TRIMESTRE, TERCER_TRIMESTRE, CUARTO_TRIMESTRE |
| ComprobanteClase | PECOSA, GUIA, TRASLADO, OTROS |
| RolUsuario | administrador, coordinador, responsable_acopio, operador |
| TipoMovimientoKardex | ingreso, salida, transferencia, ajuste |
| EstadoVale | generado, impreso, entregado |
| TipoVale | completo, solo_base, solo_adicionales |
| TipoAlerta | vencimiento, stock_bajo, discrepancia, sistema |
| NivelAlerta | info, warning, error, success |

### Relaciones

| Origen.campo | Destino | Cardinalidad | FK | Archivo:línea |
| --- | --- | --- | --- | --- |
| Red.microredes | Microred | 1:N |  | backend/prisma/schema.prisma:108 |
| Microred.red | Red | N:1 | redId | backend/prisma/schema.prisma:124 |
| Microred.centrosAcopio | CentroAcopio | 1:N |  | backend/prisma/schema.prisma:125 |
| CentroAcopio.microred | Microred | N:1 | microredId | backend/prisma/schema.prisma:144 |
| CentroAcopio.establecimientos | Establecimiento | 1:N |  | backend/prisma/schema.prisma:145 |
| CentroAcopio.usuarios | Usuario | 1:N |  | backend/prisma/schema.prisma:146 |
| CentroAcopio.usuariosAsignados | UsuarioCentroAcopio | 1:N |  | backend/prisma/schema.prisma:147 |
| CentroAcopio.valesEntrega | ValeEntrega | 1:N |  | backend/prisma/schema.prisma:148 |
| CentroAcopio.configuracionesJeringaVacuna | ConfiguracionJeringaVacunaCentro | 1:N |  | backend/prisma/schema.prisma:149 |
| Establecimiento.centroAcopio | CentroAcopio | N:1 | centroAcopioId | backend/prisma/schema.prisma:169 |
| Establecimiento.usuarios | Usuario | 1:N |  | backend/prisma/schema.prisma:170 |
| Establecimiento.planificaciones | PlanificacionAnual | 1:N |  | backend/prisma/schema.prisma:171 |
| Establecimiento.movimientos | MovimientoVacuna | 1:N |  | backend/prisma/schema.prisma:172 |
| Establecimiento.valesDetalle | ValeDetalle | 1:N |  | backend/prisma/schema.prisma:173 |
| Establecimiento.kardexOrigen | Kardex | 1:N |  | backend/prisma/schema.prisma:174 |
| Establecimiento.kardexDestino | Kardex | 1:N |  | backend/prisma/schema.prisma:175 |
| Establecimiento.iciDemidRegistros | IciDemidRegistro | 1:N |  | backend/prisma/schema.prisma:176 |
| Vacuna.lotes | LoteVacuna | 1:N |  | backend/prisma/schema.prisma:195 |
| Vacuna.planificaciones | PlanificacionAnual | 1:N |  | backend/prisma/schema.prisma:196 |
| Vacuna.movimientos | MovimientoVacuna | 1:N |  | backend/prisma/schema.prisma:197 |
| Vacuna.valesDetalle | ValeDetalle | 1:N |  | backend/prisma/schema.prisma:198 |
| Vacuna.configuracionesDefecto | ConfiguracionJeringaVacunaDefecto | 1:N |  | backend/prisma/schema.prisma:199 |
| Vacuna.configuracionesCentro | ConfiguracionJeringaVacunaCentro | 1:N |  | backend/prisma/schema.prisma:200 |
| Vacuna.programacionesCenares | ProgramacionAnualCenares | 1:N |  | backend/prisma/schema.prisma:201 |
| Vacuna.stocksInicialesMensuales | StockInicialMensual | 1:N |  | backend/prisma/schema.prisma:202 |
| Vacuna.iciDemidRegistros | IciDemidRegistro | 1:N |  | backend/prisma/schema.prisma:203 |
| Jeringa.lotes | LoteJeringa | 1:N |  | backend/prisma/schema.prisma:219 |
| Jeringa.configuracionesDefecto | ConfiguracionJeringaVacunaDefecto | 1:N |  | backend/prisma/schema.prisma:220 |
| Jeringa.configuracionesCentro | ConfiguracionJeringaVacunaCentro | 1:N |  | backend/prisma/schema.prisma:221 |
| Jeringa.programacionesCenares | ProgramacionAnualCenares | 1:N |  | backend/prisma/schema.prisma:222 |
| LoteVacuna.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:244 |
| LoteJeringa.jeringa | Jeringa | N:1 | jeringaId | backend/prisma/schema.prisma:266 |
| Usuario.establecimiento | Establecimiento | N:1 | establecimientoId | backend/prisma/schema.prisma:288 |
| Usuario.centroAcopio | CentroAcopio | N:1 | centroAcopioId | backend/prisma/schema.prisma:289 |
| Usuario.centrosAcopioAsignados | UsuarioCentroAcopio | 1:N |  | backend/prisma/schema.prisma:290 |
| Usuario.role | Role | N:1 | roleId | backend/prisma/schema.prisma:291 |
| Usuario.movimientos | MovimientoVacuna | 1:N |  | backend/prisma/schema.prisma:292 |
| Usuario.entregas | EntregaAdicional | 1:N |  | backend/prisma/schema.prisma:293 |
| Usuario.vales | ValeEntrega | 1:N |  | backend/prisma/schema.prisma:294 |
| Usuario.kardex | Kardex | 1:N |  | backend/prisma/schema.prisma:295 |
| Usuario.alertas | Alerta | 1:N |  | backend/prisma/schema.prisma:296 |
| Usuario.iciDemidRegistros | IciDemidRegistro | 1:N |  | backend/prisma/schema.prisma:297 |
| Usuario.permisosOperativos | PermisoOperativo | 1:N |  | backend/prisma/schema.prisma:298 |
| Usuario.permisosOperativosCreados | PermisoOperativo | 1:N |  | backend/prisma/schema.prisma:299 |
| Usuario.sibotSessions | SibotSession | 1:N |  | backend/prisma/schema.prisma:300 |
| Usuario.sibotToolExecutions | SibotToolExecution | 1:N |  | backend/prisma/schema.prisma:301 |
| Usuario.sibotSecurityEvents | SibotSecurityEvent | 1:N |  | backend/prisma/schema.prisma:302 |
| UsuarioCentroAcopio.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:315 |
| UsuarioCentroAcopio.centroAcopio | CentroAcopio | N:1 | centroAcopioId | backend/prisma/schema.prisma:316 |
| IciDemidRegistro.establecimiento | Establecimiento | N:1 | establecimientoId | backend/prisma/schema.prisma:353 |
| IciDemidRegistro.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:354 |
| IciDemidRegistro.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:355 |
| PlanificacionAnual.establecimiento | Establecimiento | N:1 | establecimientoId | backend/prisma/schema.prisma:376 |
| PlanificacionAnual.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:377 |
| ProgramacionAnualCenares.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:396 |
| ProgramacionAnualCenares.jeringa | Jeringa | N:1 | jeringaId | backend/prisma/schema.prisma:397 |
| MovimientoVacuna.establecimiento | Establecimiento | N:1 | establecimientoId | backend/prisma/schema.prisma:427 |
| MovimientoVacuna.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:428 |
| MovimientoVacuna.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:429 |
| MovimientoVacuna.entregasAdicionales | EntregaAdicional | 1:N |  | backend/prisma/schema.prisma:430 |
| EntregaAdicional.movimientoVacuna | MovimientoVacuna | N:1 | movimientoVacunaId | backend/prisma/schema.prisma:447 |
| EntregaAdicional.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:448 |
| ValeEntrega.centroAcopio | CentroAcopio | N:1 | centroAcopioId | backend/prisma/schema.prisma:472 |
| ValeEntrega.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:473 |
| ValeEntrega.detalles | ValeDetalle | 1:N |  | backend/prisma/schema.prisma:474 |
| ValeDetalle.valeEntrega | ValeEntrega | N:1 | valeEntregaId | backend/prisma/schema.prisma:492 |
| ValeDetalle.establecimiento | Establecimiento | N:1 | establecimientoId | backend/prisma/schema.prisma:493 |
| ValeDetalle.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:494 |
| Kardex.establecimientoOrigen | Establecimiento | N:1 | establecimientoOrigenId | backend/prisma/schema.prisma:519 |
| Kardex.establecimientoDestino | Establecimiento | N:1 | establecimientoDestinoId | backend/prisma/schema.prisma:520 |
| Kardex.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:521 |
| Alerta.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:541 |
| StockInicialMensual.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:575 |
| ConfiguracionJeringaVacunaDefecto.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:595 |
| ConfiguracionJeringaVacunaDefecto.jeringa | Jeringa | N:1 | jeringaId | backend/prisma/schema.prisma:596 |
| ConfiguracionJeringaVacunaCentro.centroAcopio | CentroAcopio | N:1 | centroAcopioId | backend/prisma/schema.prisma:619 |
| ConfiguracionJeringaVacunaCentro.vacuna | Vacuna | N:1 | vacunaId | backend/prisma/schema.prisma:620 |
| ConfiguracionJeringaVacunaCentro.jeringa | Jeringa | N:1 | jeringaId | backend/prisma/schema.prisma:621 |
| Role.rolePermissions | RolePermission | 1:N |  | backend/prisma/schema.prisma:648 |
| Role.usuarios | Usuario | 1:N |  | backend/prisma/schema.prisma:649 |
| Permission.rolePermissions | RolePermission | 1:N |  | backend/prisma/schema.prisma:669 |
| RolePermission.role | Role | N:1 | roleId | backend/prisma/schema.prisma:685 |
| RolePermission.permission | Permission | N:1 | permissionId | backend/prisma/schema.prisma:686 |
| PermisoOperativo.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:713 |
| PermisoOperativo.creadoPor | Usuario | N:1 | creadoPorId | backend/prisma/schema.prisma:714 |
| SibotSession.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:730 |
| SibotSession.attachments | SibotAttachment | 1:N |  | backend/prisma/schema.prisma:731 |
| SibotSession.toolExecutions | SibotToolExecution | 1:N |  | backend/prisma/schema.prisma:732 |
| SibotSession.securityEvents | SibotSecurityEvent | 1:N |  | backend/prisma/schema.prisma:733 |
| SibotAttachment.session | SibotSession | N:1 | sessionId | backend/prisma/schema.prisma:754 |
| SibotToolExecution.session | SibotSession | N:1 | sessionId | backend/prisma/schema.prisma:774 |
| SibotToolExecution.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:775 |
| SibotSecurityEvent.session | SibotSession | N:1 | sessionId | backend/prisma/schema.prisma:792 |
| SibotSecurityEvent.usuario | Usuario | N:1 | usuarioId | backend/prisma/schema.prisma:793 |

## Endpoints Express

Total: 291; sin autenticación detectada: 68

| Método | Ruta | Autenticación | Autorización | Handler | Archivo:línea |
| --- | --- | --- | --- | --- | --- |
| GET | /health | ninguna |  | healthCheck | backend/src/index.ts:57 |
| GET | /api/health | ninguna |  | healthCheck | backend/src/index.ts:58 |
| GET | /api | ninguna |  | (función en línea) | backend/src/index.ts:61 |
| GET | /api/alertas/stream | ninguna |  | AlertaController.stream | backend/src/routes/alertas.ts:10 |
| GET | /api/alertas/stats | obligatoria | denyResponsableAcopio | AlertaController.getStats | backend/src/routes/alertas.ts:17 |
| GET | /api/alertas/no-leidas | obligatoria | denyResponsableAcopio | AlertaController.getUnreadForUser | backend/src/routes/alertas.ts:24 |
| GET | /api/alertas/verificar-y-generar | obligatoria | denyResponsableAcopio | AlertaController.verifyAndGenerate | backend/src/routes/alertas.ts:33 |
| DELETE | /api/alertas/limpiar-antiguas | obligatoria | validatePermissions(['admin']) | AlertaController.cleanupOldAlerts | backend/src/routes/alertas.ts:41 |
| POST | /api/alertas/generar-automaticas | obligatoria | validatePermissions(['admin', 'coordinador']) | AlertaController.generateAutomatic | backend/src/routes/alertas.ts:50 |
| DELETE | /api/alertas/limpiar-resueltas | obligatoria | validatePermissions(['admin']) | AlertaController.cleanupResolved | backend/src/routes/alertas.ts:57 |
| PUT | /api/alertas/leer-multiples | obligatoria | denyResponsableAcopio | AlertaController.markMultipleAsRead | backend/src/routes/alertas.ts:65 |
| GET | /api/alertas | obligatoria | denyResponsableAcopio | AlertaController.getAll | backend/src/routes/alertas.ts:81 |
| POST | /api/alertas | obligatoria | denyResponsableAcopio | AlertaController.create | backend/src/routes/alertas.ts:95 |
| GET | /api/alertas/:id | obligatoria | denyResponsableAcopio | AlertaController.getById | backend/src/routes/alertas.ts:103 |
| PUT | /api/alertas/:id | obligatoria | denyResponsableAcopio | AlertaController.update | backend/src/routes/alertas.ts:119 |
| DELETE | /api/alertas/:id | obligatoria | validatePermissions(['admin', 'coordinador']) | AlertaController.delete | backend/src/routes/alertas.ts:127 |
| PUT | /api/alertas/:id/leer | obligatoria | denyResponsableAcopio | AlertaController.markAsRead | backend/src/routes/alertas.ts:135 |
| POST | /api/auth/login | ninguna |  | AuthController.login | backend/src/routes/auth.ts:72 |
| POST | /api/auth/refresh | ninguna |  | AuthController.refreshToken | backend/src/routes/auth.ts:82 |
| POST | /api/auth/logout | obligatoria |  | AuthController.logout | backend/src/routes/auth.ts:91 |
| POST | /api/auth/change-password | obligatoria |  | AuthController.changePassword | backend/src/routes/auth.ts:102 |
| GET | /api/auth/profile | obligatoria |  | AuthController.getProfile | backend/src/routes/auth.ts:111 |
| GET | /api/auth/verify | obligatoria |  | AuthController.verifyAuth | backend/src/routes/auth.ts:120 |
| GET | /api/auth/health | ninguna |  | (función en línea) | backend/src/routes/auth.ts:128 |
| POST | /api/auth/clear-rate-limit | ninguna |  | clearRateLimitEndpoint | backend/src/routes/auth.ts:173 |
| GET | /api/centros-acopio | obligatoria | validatePermissions(['admin', 'supervisor']) | CentroAcopioController.getAll | backend/src/routes/centros-acopio.ts:166 |
| GET | /api/centros-acopio/:id | obligatoria | validatePermissions(['admin', 'supervisor']) | CentroAcopioController.getById | backend/src/routes/centros-acopio.ts:194 |
| GET | /api/centros-acopio/microred/:microredId | obligatoria | validatePermissions(['admin', 'supervisor', 'operador']) | CentroAcopioController.getByMicrored | backend/src/routes/centros-acopio.ts:220 |
| GET | /api/centros-acopio/red/:redId | obligatoria | validatePermissions(['admin', 'supervisor', 'operador']) | CentroAcopioController.getByRed | backend/src/routes/centros-acopio.ts:246 |
| POST | /api/centros-acopio | obligatoria | validatePermissions(['admin']) | CentroAcopioController.create | backend/src/routes/centros-acopio.ts:276 |
| PUT | /api/centros-acopio/:id | obligatoria | validatePermissions(['admin']) | CentroAcopioController.update | backend/src/routes/centros-acopio.ts:316 |
| DELETE | /api/centros-acopio/:id | obligatoria | validatePermissions(['admin']) | CentroAcopioController.delete | backend/src/routes/centros-acopio.ts:348 |
| GET | /api/configuracion-jeringa-vacuna/defecto | ninguna |  | ConfiguracionJeringaVacunaController.getAllDefecto | backend/src/routes/configuracion-jeringa-vacuna.ts:24 |
| POST | /api/configuracion-jeringa-vacuna/defecto | ninguna |  | ConfiguracionJeringaVacunaController.createDefecto | backend/src/routes/configuracion-jeringa-vacuna.ts:36 |
| PUT | /api/configuracion-jeringa-vacuna/defecto/:id | ninguna |  | ConfiguracionJeringaVacunaController.updateDefecto | backend/src/routes/configuracion-jeringa-vacuna.ts:47 |
| DELETE | /api/configuracion-jeringa-vacuna/defecto/:id | ninguna |  | ConfiguracionJeringaVacunaController.deleteDefecto | backend/src/routes/configuracion-jeringa-vacuna.ts:55 |
| GET | /api/configuracion-jeringa-vacuna/centro | ninguna |  | ConfiguracionJeringaVacunaController.getAllCentro | backend/src/routes/configuracion-jeringa-vacuna.ts:73 |
| POST | /api/configuracion-jeringa-vacuna/centro | ninguna |  | ConfiguracionJeringaVacunaController.createCentro | backend/src/routes/configuracion-jeringa-vacuna.ts:86 |
| PUT | /api/configuracion-jeringa-vacuna/centro/:id | ninguna |  | ConfiguracionJeringaVacunaController.updateCentro | backend/src/routes/configuracion-jeringa-vacuna.ts:97 |
| DELETE | /api/configuracion-jeringa-vacuna/centro/:id | ninguna |  | ConfiguracionJeringaVacunaController.deleteCentro | backend/src/routes/configuracion-jeringa-vacuna.ts:105 |
| GET | /api/configuracion-jeringa-vacuna/efectiva/:vacunaId | ninguna |  | ConfiguracionJeringaVacunaController.getConfiguracionEfectiva | backend/src/routes/configuracion-jeringa-vacuna.ts:118 |
| GET | /api/configuracion-jeringa-vacuna/calcular | ninguna |  | ConfiguracionJeringaVacunaController.calcularJeringasGet | backend/src/routes/configuracion-jeringa-vacuna.ts:129 |
| POST | /api/configuracion-jeringa-vacuna/calcular | ninguna |  | ConfiguracionJeringaVacunaController.calcularJeringas | backend/src/routes/configuracion-jeringa-vacuna.ts:139 |
| GET | /api/configuracion/public | ninguna |  | ConfiguracionController.getPublicConfigurations | backend/src/routes/configuracion.ts:64 |
| GET | /api/configuracion/sistema/info | ninguna |  | ConfiguracionController.getSystemInfo | backend/src/routes/configuracion.ts:74 |
| GET | /api/configuracion/categorias | ninguna |  | ConfiguracionController.getCategories | backend/src/routes/configuracion.ts:84 |
| GET | /api/configuracion/logo | ninguna |  | ConfiguracionController.getLogo | backend/src/routes/configuracion.ts:94 |
| GET | /api/configuracion/logo/file | ninguna |  | ConfiguracionController.getLogoFile | backend/src/routes/configuracion.ts:104 |
| GET | /api/configuracion | obligatoria | authorize(['administrador']); requirePermissions(['config_general:read']) | ConfiguracionController.getAllConfigurations | backend/src/routes/configuracion.ts:120 |
| GET | /api/configuracion/categoria/:categoria | obligatoria | authorize(['administrador', 'coordinador']); requirePermissions(['config_general:read']) | ConfiguracionController.getByCategory | backend/src/routes/configuracion.ts:132 |
| GET | /api/configuracion/:clave | obligatoria | authorize(['administrador', 'coordinador']); requirePermissions(['config_general:read']) | ConfiguracionController.getByKey | backend/src/routes/configuracion.ts:145 |
| POST | /api/configuracion | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.create | backend/src/routes/configuracion.ts:158 |
| POST | /api/configuracion/logo | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.uploadLogo | backend/src/routes/configuracion.ts:171 |
| DELETE | /api/configuracion/logo | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.deleteLogo | backend/src/routes/configuracion.ts:184 |
| POST | /api/configuracion/backup/export | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.exportDatabaseBackup | backend/src/routes/configuracion.ts:195 |
| PUT | /api/configuracion/bulk | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.bulkUpdate | backend/src/routes/configuracion.ts:206 |
| PUT | /api/configuracion/:id | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.update | backend/src/routes/configuracion.ts:219 |
| PATCH | /api/configuracion/:clave/valor | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.updateByKey | backend/src/routes/configuracion.ts:233 |
| DELETE | /api/configuracion/:id | obligatoria | authorize(['administrador']); requirePermissions(['config_general:write']) | ConfiguracionController.delete | backend/src/routes/configuracion.ts:247 |
| GET | /api/dashboard | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getDashboardData | backend/src/routes/dashboard.ts:19 |
| GET | /api/dashboard/estadisticas | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getEstadisticas | backend/src/routes/dashboard.ts:26 |
| GET | /api/dashboard/movimientos-mensuales | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getMovimientosMensuales | backend/src/routes/dashboard.ts:33 |
| GET | /api/dashboard/stock-por-vacuna | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getStockPorVacuna | backend/src/routes/dashboard.ts:40 |
| GET | /api/dashboard/centros-acopio-status | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getCentrosAcopioStatus | backend/src/routes/dashboard.ts:47 |
| GET | /api/dashboard/centros-acopio | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getCentrosAcopio | backend/src/routes/dashboard.ts:56 |
| GET | /api/dashboard/alertas-recientes | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getAlertasRecientes | backend/src/routes/dashboard.ts:63 |
| GET | /api/dashboard/alertas | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getAlertasRecientes | backend/src/routes/dashboard.ts:72 |
| GET | /api/dashboard/actividad-reciente | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getActividadReciente | backend/src/routes/dashboard.ts:79 |
| GET | /api/dashboard/actividad | obligatoria | requireCentroAcopioAssignment; requirePermissions(['dashboard:read']) | DashboardController.getActividadReciente | backend/src/routes/dashboard.ts:88 |
| GET | /api/entregas-adicionales/movimiento/:movimientoId | ninguna |  | EntregaAdicionalController.getByMovimiento | backend/src/routes/entregas-adicionales.ts:16 |
| GET | /api/entregas-adicionales/movimiento/:movimientoId/estadisticas | ninguna |  | EntregaAdicionalController.getEstadisticasByMovimiento | backend/src/routes/entregas-adicionales.ts:24 |
| GET | /api/entregas-adicionales/:id | ninguna |  | EntregaAdicionalController.getById | backend/src/routes/entregas-adicionales.ts:32 |
| POST | /api/entregas-adicionales | ninguna |  | EntregaAdicionalController.create | backend/src/routes/entregas-adicionales.ts:40 |
| PUT | /api/entregas-adicionales/:id | ninguna |  | EntregaAdicionalController.update | backend/src/routes/entregas-adicionales.ts:49 |
| DELETE | /api/entregas-adicionales/:id | ninguna |  | EntregaAdicionalController.delete | backend/src/routes/entregas-adicionales.ts:57 |
| GET | /api/establecimientos | obligatoria | requirePermissions(['establecimientos:read']); requireCentroAcopioAssignment | EstablecimientoController.getAll | backend/src/routes/establecimientos.ts:25 |
| GET | /api/establecimientos/centros-acopio | obligatoria | requirePermissions(['establecimientos:read']); requireCentroAcopioAssignment | EstablecimientoController.getCentrosAcopio | backend/src/routes/establecimientos.ts:32 |
| GET | /api/establecimientos/opciones-jerarquicas | obligatoria | requirePermissions(['establecimientos:read']); requireCentroAcopioAssignment | EstablecimientoController.getOpcionesJerarquicas | backend/src/routes/establecimientos.ts:39 |
| GET | /api/establecimientos/centro-acopio/:centroAcopioId | obligatoria | requirePermissions(['establecimientos:read']); requireCentroAcopioAssignment | EstablecimientoController.getByCentroAcopio | backend/src/routes/establecimientos.ts:47 |
| GET | /api/establecimientos/codigo/:codigo | obligatoria | requirePermissions(['establecimientos:read']); requireCentroAcopioAssignment | EstablecimientoController.getByCodigo | backend/src/routes/establecimientos.ts:55 |
| GET | /api/establecimientos/:id | obligatoria | requirePermissions(['establecimientos:read']); requireCentroAcopioAssignment | EstablecimientoController.getById | backend/src/routes/establecimientos.ts:63 |
| POST | /api/establecimientos | obligatoria | requirePermissions(['establecimientos:write']); requireCentroAcopioAssignment | EstablecimientoController.create | backend/src/routes/establecimientos.ts:71 |
| PUT | /api/establecimientos/:id | obligatoria | requirePermissions(['establecimientos:write']); requireCentroAcopioAssignment | EstablecimientoController.update | backend/src/routes/establecimientos.ts:80 |
| DELETE | /api/establecimientos/:id | obligatoria | requirePermissions(['establecimientos:write']); requireCentroAcopioAssignment | EstablecimientoController.delete | backend/src/routes/establecimientos.ts:88 |
| GET | /api/ici-demid/anios-disponibles | obligatoria | authorize(['administrador']); requireCentroAcopioAssignment; requirePermissions(['ici_demid:read']) | IciDemidController.getAniosDisponibles | backend/src/routes/ici-demid.ts:14 |
| GET | /api/ici-demid | obligatoria | authorize(['administrador']); requireCentroAcopioAssignment; requirePermissions(['ici_demid:read']) | IciDemidController.getAll | backend/src/routes/ici-demid.ts:15 |
| POST | /api/ici-demid/preview-import | obligatoria | requirePermissions(['ici_demid:write']); denyNonAdmin; authorize(['administrador']); requireCentroAcopioAssignment; requirePermissions(['ici_demid:read']) | IciDemidController.previewImport | backend/src/routes/ici-demid.ts:16 |
| POST | /api/ici-demid/importar | obligatoria | requirePermissions(['ici_demid:write']); denyNonAdmin; authorize(['administrador']); requireCentroAcopioAssignment; requirePermissions(['ici_demid:read']) | IciDemidController.importFromExcel | backend/src/routes/ici-demid.ts:17 |
| GET | /api/jeringas | ninguna |  | JeringaController.getAll | backend/src/routes/jeringas.ts:21 |
| GET | /api/jeringas/activas | ninguna |  | JeringaController.getActivas | backend/src/routes/jeringas.ts:28 |
| GET | /api/jeringas/stats/stock | ninguna |  | JeringaController.getStockStats | backend/src/routes/jeringas.ts:36 |
| GET | /api/jeringas/:id | ninguna |  | JeringaController.getById | backend/src/routes/jeringas.ts:44 |
| POST | /api/jeringas | ninguna |  | JeringaController.create | backend/src/routes/jeringas.ts:52 |
| PUT | /api/jeringas/:id | ninguna |  | JeringaController.update | backend/src/routes/jeringas.ts:61 |
| DELETE | /api/jeringas/:id | ninguna |  | JeringaController.delete | backend/src/routes/jeringas.ts:69 |
| GET | /api/kardex/estadisticas | obligatoria | denyResponsableAcopio | KardexController.getEstadisticas | backend/src/routes/kardex.ts:28 |
| GET | /api/kardex/consultas-predefinidas | obligatoria | denyResponsableAcopio | KardexController.getConsultasPredefinidas | backend/src/routes/kardex.ts:35 |
| GET | /api/kardex/export/stats | obligatoria | denyResponsableAcopio | KardexController.getExportStats | backend/src/routes/kardex.ts:51 |
| POST | /api/kardex/export/excel | obligatoria | denyResponsableAcopio | KardexController.exportToExcel | backend/src/routes/kardex.ts:62 |
| POST | /api/kardex/export/pdf | obligatoria | denyResponsableAcopio | KardexController.exportToPDF | backend/src/routes/kardex.ts:73 |
| POST | /api/kardex/export/csv | obligatoria | denyResponsableAcopio | KardexController.exportToCSV | backend/src/routes/kardex.ts:82 |
| GET | /api/kardex/trazabilidad/:loteId | obligatoria | denyResponsableAcopio | KardexController.getTrazabilidadLote | backend/src/routes/kardex.ts:90 |
| POST | /api/kardex/generar-automatico | obligatoria | denyResponsableAcopio | KardexController.generarMovimientoAutomatico | backend/src/routes/kardex.ts:109 |
| GET | /api/kardex | obligatoria | denyResponsableAcopio | KardexController.getAll | backend/src/routes/kardex.ts:127 |
| POST | /api/kardex | obligatoria | denyResponsableAcopio | KardexController.create | backend/src/routes/kardex.ts:147 |
| GET | /api/kardex/:id | obligatoria | denyResponsableAcopio | KardexController.getById | backend/src/routes/kardex.ts:155 |
| PUT | /api/kardex/:id | obligatoria | denyResponsableAcopio | KardexController.update | backend/src/routes/kardex.ts:171 |
| DELETE | /api/kardex/:id | obligatoria | denyResponsableAcopio | KardexController.delete | backend/src/routes/kardex.ts:179 |
| GET | /api/lotes-jeringas/stats | ninguna |  | LoteJeringaController.getStats | backend/src/routes/lotes-jeringas.ts:14 |
| GET | /api/lotes-jeringas/stock-bajo | ninguna |  | LoteJeringaController.getStockBajo | backend/src/routes/lotes-jeringas.ts:22 |
| GET | /api/lotes-jeringas/jeringa/:jeringaId | ninguna |  | LoteJeringaController.getByJeringa | backend/src/routes/lotes-jeringas.ts:30 |
| GET | /api/lotes-jeringas | ninguna |  | LoteJeringaController.getAll | backend/src/routes/lotes-jeringas.ts:42 |
| GET | /api/lotes-jeringas/:id | ninguna |  | LoteJeringaController.getById | backend/src/routes/lotes-jeringas.ts:50 |
| POST | /api/lotes-jeringas | ninguna |  | LoteJeringaController.create | backend/src/routes/lotes-jeringas.ts:58 |
| PUT | /api/lotes-jeringas/:id | ninguna |  | LoteJeringaController.update | backend/src/routes/lotes-jeringas.ts:67 |
| DELETE | /api/lotes-jeringas/:id | ninguna |  | LoteJeringaController.delete | backend/src/routes/lotes-jeringas.ts:75 |
| GET | /api/lotes-vacunas/stats | ninguna |  | LoteVacunaController.getStats | backend/src/routes/lotes-vacunas.ts:15 |
| GET | /api/lotes-vacunas/proximos-vencer | ninguna |  | LoteVacunaController.getProximosAVencer | backend/src/routes/lotes-vacunas.ts:23 |
| GET | /api/lotes-vacunas/vacuna/:vacunaId | ninguna |  | LoteVacunaController.getByVacuna | backend/src/routes/lotes-vacunas.ts:31 |
| GET | /api/lotes-vacunas | ninguna |  | LoteVacunaController.getAll | backend/src/routes/lotes-vacunas.ts:44 |
| GET | /api/lotes-vacunas/:id | ninguna |  | LoteVacunaController.getById | backend/src/routes/lotes-vacunas.ts:52 |
| POST | /api/lotes-vacunas | ninguna |  | LoteVacunaController.create | backend/src/routes/lotes-vacunas.ts:60 |
| PUT | /api/lotes-vacunas/:id | obligatoria |  | LoteVacunaController.update | backend/src/routes/lotes-vacunas.ts:69 |
| DELETE | /api/lotes-vacunas/:id | ninguna |  | LoteVacunaController.delete | backend/src/routes/lotes-vacunas.ts:77 |
| GET | /api/microredes | obligatoria | validatePermissions(['admin', 'supervisor']) | MicroredController.getAll | backend/src/routes/microredes.ts:140 |
| GET | /api/microredes/:id | obligatoria | validatePermissions(['admin', 'supervisor']) | MicroredController.getById | backend/src/routes/microredes.ts:168 |
| GET | /api/microredes/red/:redId | obligatoria | validatePermissions(['admin', 'supervisor', 'operador']) | MicroredController.getByRed | backend/src/routes/microredes.ts:194 |
| POST | /api/microredes | obligatoria | validatePermissions(['admin']) | MicroredController.create | backend/src/routes/microredes.ts:224 |
| PUT | /api/microredes/:id | obligatoria | validatePermissions(['admin']) | MicroredController.update | backend/src/routes/microredes.ts:264 |
| DELETE | /api/microredes/:id | obligatoria | validatePermissions(['admin']) | MicroredController.delete | backend/src/routes/microredes.ts:296 |
| GET | /api/movimientos/anios-disponibles | obligatoria | requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.getAniosDisponibles | backend/src/routes/movimientos.ts:104 |
| GET | /api/movimientos/progreso-vales | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.getProgresoVales | backend/src/routes/movimientos.ts:110 |
| GET | /api/movimientos/ajuste-entregas/datos/:vacunaId/:mes/:anio | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | AjusteEntregasController.obtenerDatosParaAjuste | backend/src/routes/movimientos.ts:116 |
| GET | /api/movimientos/ajuste-entregas/verificar/:vacunaId/:mes/:anio | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | AjusteEntregasController.verificarDisponibilidad | backend/src/routes/movimientos.ts:117 |
| POST | /api/movimientos/ajuste-entregas/calcular-opciones | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | AjusteEntregasController.calcularOpcionesAjuste | backend/src/routes/movimientos.ts:118 |
| POST | /api/movimientos/ajuste-entregas/ejecutar | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | AjusteEntregasController.ejecutarAjuste | backend/src/routes/movimientos.ts:119 |
| GET | /api/movimientos/plantilla/vacuna/:vacunaId/anio/:anio | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.descargarPlantillaVacuna | backend/src/routes/movimientos.ts:125 |
| GET | /api/movimientos/plantilla/masiva/anio/:anio | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.descargarPlantillaMasiva | backend/src/routes/movimientos.ts:126 |
| POST | /api/movimientos/importar/vacuna/:vacunaId/anio/:anio | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.importarDesdeExcelVacuna | backend/src/routes/movimientos.ts:128 |
| POST | /api/movimientos/debug-plantilla/anio/:anio | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.debugPlantilla | backend/src/routes/movimientos.ts:136 |
| POST | /api/movimientos/validar-plantilla/anio/:anio | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.validarPlantilla | backend/src/routes/movimientos.ts:144 |
| POST | /api/movimientos/importar/masivo/anio/:anio | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.importarDesdeExcelMasivo | backend/src/routes/movimientos.ts:152 |
| POST | /api/movimientos/reporte-errores | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.generarReporteErrores | backend/src/routes/movimientos.ts:160 |
| POST | /api/movimientos/exportar/vacuna/:vacunaId | obligatoria | requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.exportarPorVacuna | backend/src/routes/movimientos.ts:170 |
| POST | /api/movimientos/exportar/todas-vacunas | obligatoria | requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.exportarTodasVacunas | backend/src/routes/movimientos.ts:171 |
| GET | /api/movimientos/estadisticas | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.getEstadisticas | backend/src/routes/movimientos.ts:177 |
| GET | /api/movimientos/stock-disponible | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.getStockDisponible | backend/src/routes/movimientos.ts:178 |
| POST | /api/movimientos/generar-desde-planificacion/:planificacionId | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.generarDesdeplanificacion | backend/src/routes/movimientos.ts:184 |
| POST | /api/movimientos/sincronizar-saldo-anterior | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.sincronizarSaldoAnterior | backend/src/routes/movimientos.ts:185 |
| POST | /api/movimientos/actualizar-stock-siguiente-mes | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.actualizarStockInicialSiguienteMes | backend/src/routes/movimientos.ts:186 |
| GET | /api/movimientos | obligatoria | requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.getAll | backend/src/routes/movimientos.ts:192 |
| GET | /api/movimientos/:id | obligatoria | requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.getById | backend/src/routes/movimientos.ts:193 |
| POST | /api/movimientos | obligatoria | requirePermissions(['movimientos:write']); requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.create | backend/src/routes/movimientos.ts:194 |
| PUT | /api/movimientos/:id | obligatoria | requirePermissions(['movimientos:write']); requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.update | backend/src/routes/movimientos.ts:199 |
| DELETE | /api/movimientos/:id | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.delete | backend/src/routes/movimientos.ts:201 |
| POST | /api/movimientos/:movimientoId/entregas-adicionales | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.createEntregaAdicional | backend/src/routes/movimientos.ts:207 |
| PUT | /api/movimientos/entregas-adicionales/:id | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.updateEntregaAdicional | backend/src/routes/movimientos.ts:208 |
| DELETE | /api/movimientos/entregas-adicionales/:id | obligatoria | requirePermissions(['movimientos:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['movimientos:read']) | MovimientosController.deleteEntregaAdicional | backend/src/routes/movimientos.ts:209 |
| GET | /api/permisos-operativos/mis-permisos | obligatoria |  | PermisoOperativoController.getMisPermisos | backend/src/routes/permisos-operativos.ts:15 |
| GET | /api/permisos-operativos | obligatoria | authorize(['administrador']) | PermisoOperativoController.getResponsablesConPermisos | backend/src/routes/permisos-operativos.ts:27 |
| POST | /api/permisos-operativos/toggle | obligatoria | authorize(['administrador']) | PermisoOperativoController.togglePermiso | backend/src/routes/permisos-operativos.ts:42 |
| GET | /api/permisos-operativos/usuario/:usuarioId | obligatoria | authorize(['administrador']) | PermisoOperativoController.getPermisosUsuario | backend/src/routes/permisos-operativos.ts:49 |
| POST | /api/permisos-operativos/procesar-programados | obligatoria | authorize(['administrador']) | PermisoOperativoController.procesarProgramados | backend/src/routes/permisos-operativos.ts:56 |
| GET | /api/permissions/stats | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getStats | backend/src/routes/permissions.ts:13 |
| GET | /api/permissions/categorias | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getCategorias | backend/src/routes/permissions.ts:20 |
| GET | /api/permissions/recursos | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getRecursos | backend/src/routes/permissions.ts:27 |
| GET | /api/permissions/acciones | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getAcciones | backend/src/routes/permissions.ts:34 |
| GET | /api/permissions/grouped | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getGroupedByCategory | backend/src/routes/permissions.ts:41 |
| GET | /api/permissions/codigo/:codigo | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getByCodigo | backend/src/routes/permissions.ts:48 |
| GET | /api/permissions | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getAll | backend/src/routes/permissions.ts:62 |
| POST | /api/permissions | obligatoria | requirePermissions(['permisos:assign']); validatePermissions(['admin']) | PermissionController.create | backend/src/routes/permissions.ts:76 |
| GET | /api/permissions/:id | obligatoria | requirePermissions(['permisos:read']); validatePermissions(['admin']) | PermissionController.getById | backend/src/routes/permissions.ts:83 |
| PUT | /api/permissions/:id | obligatoria | requirePermissions(['permisos:assign']); validatePermissions(['admin']) | PermissionController.update | backend/src/routes/permissions.ts:97 |
| DELETE | /api/permissions/:id | obligatoria | requirePermissions(['permisos:assign']); validatePermissions(['admin']) | PermissionController.delete | backend/src/routes/permissions.ts:104 |
| PATCH | /api/permissions/:id/estado | obligatoria | requirePermissions(['permisos:assign']); validatePermissions(['admin']) | PermissionController.changeEstado | backend/src/routes/permissions.ts:112 |
| GET | /api/planificacion/anios-disponibles | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.getAniosDisponibles | backend/src/routes/planificacion.ts:108 |
| GET | /api/planificacion/estadisticas | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.getEstadisticas | backend/src/routes/planificacion.ts:116 |
| GET | /api/planificacion/vacuna/:vacunaId/anio/:anio | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.getByVacunaAndYear | backend/src/routes/planificacion.ts:126 |
| POST | /api/planificacion/importar | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.importar | backend/src/routes/planificacion.ts:134 |
| POST | /api/planificacion/distribucion-automatica | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.distribucionAutomatica | backend/src/routes/planificacion.ts:142 |
| GET | /api/planificacion | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.getAll | backend/src/routes/planificacion.ts:157 |
| GET | /api/planificacion/:id | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.getById | backend/src/routes/planificacion.ts:165 |
| POST | /api/planificacion | obligatoria | requirePermissions(['planificacion:write']); requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.create | backend/src/routes/planificacion.ts:173 |
| PUT | /api/planificacion/:id | obligatoria | requirePermissions(['planificacion:write']); requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.update | backend/src/routes/planificacion.ts:182 |
| DELETE | /api/planificacion/:id | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.delete | backend/src/routes/planificacion.ts:192 |
| GET | /api/planificacion/plantilla/vacuna/:vacunaId/anio/:anio | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.descargarPlantillaVacuna | backend/src/routes/planificacion.ts:201 |
| GET | /api/planificacion/plantilla/masiva/anio/:anio | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.descargarPlantillaMasiva | backend/src/routes/planificacion.ts:209 |
| POST | /api/planificacion/importar/vacuna/:vacunaId/anio/:anio | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.importarDesdeExcelVacuna | backend/src/routes/planificacion.ts:219 |
| POST | /api/planificacion/importar/masivo/anio/:anio | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.importarDesdeExcelMasivo | backend/src/routes/planificacion.ts:234 |
| POST | /api/planificacion/:id/sincronizar-movimientos | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.sincronizarConMovimientos | backend/src/routes/planificacion.ts:248 |
| GET | /api/planificacion/verificar/:establecimientoId/:vacunaId/:anio | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.verificarExistenciaPlanificacion | backend/src/routes/planificacion.ts:258 |
| GET | /api/planificacion/verificar-disponibilidad/:establecimientoId/:vacunaId/:mes/:anio | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.verificarDisponibilidadEntregas | backend/src/routes/planificacion.ts:269 |
| POST | /api/planificacion/registrar-mes-actual | obligatoria | requirePermissions(['planificacion:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.registrarEntregaMesActual | backend/src/routes/planificacion.ts:282 |
| POST | /api/planificacion/exportar/vacuna/:vacunaId | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.exportarPorVacuna | backend/src/routes/planificacion.ts:295 |
| POST | /api/planificacion/exportar/todas-vacunas | obligatoria | requireCentroAcopioAssignment; requirePermissions(['planificacion:read']) | PlanificacionController.exportarTodasVacunas | backend/src/routes/planificacion.ts:307 |
| GET | /api/reportes/planificacion/programacion-anual | ninguna |  | PlanificacionReportesController.generarProgramacionAnual | backend/src/routes/planificacionReportes.ts:19 |
| GET | /api/reportes/planificacion/cumplimiento-metas | ninguna |  | PlanificacionReportesController.generarCumplimientoMetas | backend/src/routes/planificacionReportes.ts:31 |
| GET | /api/reportes/planificacion/proyeccion-demanda | ninguna |  | PlanificacionReportesController.generarProyeccionDemanda | backend/src/routes/planificacionReportes.ts:43 |
| GET | /api/reportes/planificacion/distribucion-geografica | ninguna |  | PlanificacionReportesController.generarDistribucionGeografica | backend/src/routes/planificacionReportes.ts:54 |
| POST | /api/reportes/planificacion/programacion-anual/exportar | ninguna |  | PlanificacionReportesController.exportarProgramacionAnual | backend/src/routes/planificacionReportes.ts:66 |
| POST | /api/reportes/planificacion/cumplimiento-metas/exportar | ninguna |  | PlanificacionReportesController.exportarCumplimientoMetas | backend/src/routes/planificacionReportes.ts:78 |
| POST | /api/reportes/planificacion/proyeccion-demanda/exportar | ninguna |  | PlanificacionReportesController.exportarProyeccionDemanda | backend/src/routes/planificacionReportes.ts:90 |
| POST | /api/reportes/planificacion/distribucion-geografica/exportar | ninguna |  | PlanificacionReportesController.exportarDistribucionGeografica | backend/src/routes/planificacionReportes.ts:102 |
| GET | /api/programacion-anual-cenares | ninguna |  | ProgramacionAnualCenaresController.getAll | backend/src/routes/programacionAnualCenares.ts:17 |
| GET | /api/programacion-anual-cenares/tabla/:anio | ninguna |  | ProgramacionAnualCenaresController.getDatosTablaCompleta | backend/src/routes/programacionAnualCenares.ts:25 |
| GET | /api/programacion-anual-cenares/:id | ninguna |  | ProgramacionAnualCenaresController.getById | backend/src/routes/programacionAnualCenares.ts:33 |
| POST | /api/programacion-anual-cenares | ninguna |  | ProgramacionAnualCenaresController.create | backend/src/routes/programacionAnualCenares.ts:41 |
| PUT | /api/programacion-anual-cenares/:id | ninguna |  | ProgramacionAnualCenaresController.update | backend/src/routes/programacionAnualCenares.ts:50 |
| POST | /api/programacion-anual-cenares/exportar | ninguna |  | ProgramacionAnualCenaresController.exportarProgramacionSeguimientoAnual | backend/src/routes/programacionAnualCenares.ts:60 |
| POST | /api/programacion-anual-cenares/sincronizar-saldos | ninguna |  | ProgramacionAnualCenaresController.sincronizarSaldos | backend/src/routes/programacionAnualCenares.ts:68 |
| DELETE | /api/programacion-anual-cenares/:id | ninguna |  | ProgramacionAnualCenaresController.delete | backend/src/routes/programacionAnualCenares.ts:76 |
| GET | /api/redes | obligatoria | validatePermissions(['admin', 'supervisor']) | RedController.getAll | backend/src/routes/redes.ts:142 |
| GET | /api/redes/:id | obligatoria | validatePermissions(['admin', 'supervisor']) | RedController.getById | backend/src/routes/redes.ts:179 |
| POST | /api/redes | obligatoria | validatePermissions(['admin']) | RedController.create | backend/src/routes/redes.ts:220 |
| PUT | /api/redes/:id | obligatoria | validatePermissions(['admin']) | RedController.update | backend/src/routes/redes.ts:271 |
| DELETE | /api/redes/:id | obligatoria | validatePermissions(['admin']) | RedController.delete | backend/src/routes/redes.ts:312 |
| GET | /api/reportes/stock-actual | obligatoria | denyResponsableAcopio | ReporteController.generarStockActual | backend/src/routes/reportes.ts:23 |
| GET | /api/reportes/stock-critico | obligatoria | denyResponsableAcopio | ReporteController.generarStockCritico | backend/src/routes/reportes.ts:26 |
| GET | /api/reportes/proximos-vencimientos | obligatoria | denyResponsableAcopio | ReporteController.generarProximosVencimientos | backend/src/routes/reportes.ts:29 |
| GET | /api/reportes/lotes-vencidos | obligatoria | denyResponsableAcopio | ReporteController.generarLotesVencidos | backend/src/routes/reportes.ts:32 |
| POST | /api/reportes/kardex-detallado | obligatoria | denyResponsableAcopio | ReporteController.generarKardexDetallado | backend/src/routes/reportes.ts:35 |
| GET | /api/reportes/estadisticas | obligatoria | denyResponsableAcopio | ReporteController.obtenerEstadisticas | backend/src/routes/reportes.ts:38 |
| GET | /api/reportes/movimientos-mensuales | obligatoria | denyResponsableAcopio | ReporteController.generarMovimientosMensuales | backend/src/routes/reportes.ts:45 |
| GET | /api/reportes/consumo-historico | obligatoria | denyResponsableAcopio | ReporteController.generarConsumoHistorico | backend/src/routes/reportes.ts:48 |
| GET | /api/reportes/entregas-por-establecimiento | obligatoria | denyResponsableAcopio | ReporteController.generarEntregasPorEstablecimiento | backend/src/routes/reportes.ts:51 |
| GET | /api/reportes/eficiencia-distribucion | obligatoria | denyResponsableAcopio | ReporteController.generarEficienciaDistribucion | backend/src/routes/reportes.ts:54 |
| POST | /api/reportes/movimientos-por-eess | obligatoria | denyResponsableAcopio | ReporteController.generarMovimientosPorEESS | backend/src/routes/reportes.ts:57 |
| POST | /api/reportes/movimientos-mensuales/exportar | obligatoria | denyResponsableAcopio | ReporteController.exportarMovimientosMensuales | backend/src/routes/reportes.ts:64 |
| POST | /api/reportes/consumo-historico/exportar | obligatoria | denyResponsableAcopio | ReporteController.exportarConsumoHistorico | backend/src/routes/reportes.ts:67 |
| POST | /api/reportes/entregas-por-establecimiento/exportar | obligatoria | denyResponsableAcopio | ReporteController.exportarEntregasPorEstablecimiento | backend/src/routes/reportes.ts:70 |
| POST | /api/reportes/eficiencia-distribucion/exportar | obligatoria | denyResponsableAcopio | ReporteController.exportarEficienciaDistribucion | backend/src/routes/reportes.ts:73 |
| POST | /api/reportes/movimientos-por-eess/exportar | obligatoria | denyResponsableAcopio | ReporteController.exportarMovimientosPorEESS | backend/src/routes/reportes.ts:76 |
| POST | /api/reportes/stock-actual/export/excel | obligatoria | denyResponsableAcopio | ReporteController.exportarStockActualExcel | backend/src/routes/reportes.ts:83 |
| POST | /api/reportes/stock-critico/export/excel | obligatoria | denyResponsableAcopio | ReporteController.exportarStockCriticoExcel | backend/src/routes/reportes.ts:86 |
| POST | /api/reportes/proximos-vencimientos/export/excel | obligatoria | denyResponsableAcopio | ReporteController.exportarProximosVencimientosExcel | backend/src/routes/reportes.ts:89 |
| POST | /api/reportes/lotes-vencidos/export/excel | obligatoria | denyResponsableAcopio | ReporteController.exportarLotesVencidosExcel | backend/src/routes/reportes.ts:92 |
| POST | /api/reportes/kardex-detallado/export/excel | obligatoria | denyResponsableAcopio | ReporteController.exportarKardexDetalladoExcel | backend/src/routes/reportes.ts:95 |
| POST | /api/reportes/stock-vacunas-eess/exportar | obligatoria | denyResponsableAcopio | ReporteController.exportarStockVacunasEESS | backend/src/routes/reportes.ts:98 |
| GET | /api/roles/stats | obligatoria | requirePermissions(['roles:read']); validatePermissions(['admin']) | RoleController.getStats | backend/src/routes/roles.ts:13 |
| GET | /api/roles/codigo/:codigo | obligatoria | requirePermissions(['roles:read']); validatePermissions(['admin']) | RoleController.getByCodigo | backend/src/routes/roles.ts:20 |
| GET | /api/roles/:id/permissions | obligatoria | requirePermissions(['roles:read']); validatePermissions(['admin']) | RoleController.getRolePermissions | backend/src/routes/roles.ts:27 |
| POST | /api/roles/:id/permissions | obligatoria | requirePermissions(['permisos:assign']); validatePermissions(['admin']) | RoleController.assignPermissions | backend/src/routes/roles.ts:34 |
| GET | /api/roles | obligatoria | requirePermissions(['roles:read']); validatePermissions(['admin']) | RoleController.getAll | backend/src/routes/roles.ts:46 |
| POST | /api/roles | obligatoria | requirePermissions(['roles:write']); validatePermissions(['admin']) | RoleController.create | backend/src/routes/roles.ts:57 |
| GET | /api/roles/:id | obligatoria | requirePermissions(['roles:read']); validatePermissions(['admin']) | RoleController.getById | backend/src/routes/roles.ts:65 |
| PUT | /api/roles/:id | obligatoria | requirePermissions(['roles:write']); validatePermissions(['admin']) | RoleController.update | backend/src/routes/roles.ts:76 |
| DELETE | /api/roles/:id | obligatoria | requirePermissions(['roles:write']); validatePermissions(['admin']) | RoleController.delete | backend/src/routes/roles.ts:83 |
| PATCH | /api/roles/:id/estado | obligatoria | requirePermissions(['roles:write']); validatePermissions(['admin']) | RoleController.changeEstado | backend/src/routes/roles.ts:91 |
| GET | /api/sibot/bootstrap | obligatoria |  | (función en línea) | backend/src/routes/sibot.ts:15 |
| POST | /api/sibot/chat | obligatoria |  | SibotController.chat | backend/src/routes/sibot.ts:32 |
| GET | /api/usuarios | obligatoria | authorize(['administrador']) | UsuarioController.getAll | backend/src/routes/usuarios.ts:23 |
| GET | /api/usuarios/activos | obligatoria | authorize(['administrador']) | UsuarioController.getActivos | backend/src/routes/usuarios.ts:30 |
| GET | /api/usuarios/stats | obligatoria | authorize(['administrador']) | UsuarioController.getStats | backend/src/routes/usuarios.ts:37 |
| GET | /api/usuarios/rol/:rol | obligatoria | authorize(['administrador']) | UsuarioController.getByRol | backend/src/routes/usuarios.ts:45 |
| GET | /api/usuarios/:id | obligatoria | authorize(['administrador']) | UsuarioController.getById | backend/src/routes/usuarios.ts:53 |
| POST | /api/usuarios | obligatoria | authorize(['administrador']) | UsuarioController.create | backend/src/routes/usuarios.ts:61 |
| PUT | /api/usuarios/:id | obligatoria | authorize(['administrador']) | UsuarioController.update | backend/src/routes/usuarios.ts:70 |
| DELETE | /api/usuarios/:id | obligatoria | authorize(['administrador']) | UsuarioController.delete | backend/src/routes/usuarios.ts:78 |
| POST | /api/usuarios/:id/change-password | obligatoria | authorize(['administrador']) | UsuarioController.changePassword | backend/src/routes/usuarios.ts:87 |
| PATCH | /api/usuarios/:id/estado | obligatoria | authorize(['administrador']) | UsuarioController.changeEstado | backend/src/routes/usuarios.ts:96 |
| POST | /api/usuarios/:id/ultimo-acceso | obligatoria | authorize(['administrador']) | UsuarioController.updateUltimoAcceso | backend/src/routes/usuarios.ts:104 |
| GET | /api/vacunas | obligatoria | requirePermissions(['vacunas:read']); requireCentroAcopioAssignment | VacunaController.getAll | backend/src/routes/vacunas.ts:24 |
| GET | /api/vacunas/activas | obligatoria | requirePermissions(['vacunas:read']); requireCentroAcopioAssignment | VacunaController.getActivas | backend/src/routes/vacunas.ts:31 |
| GET | /api/vacunas/stats/stock | obligatoria | requirePermissions(['vacunas:read']); requireCentroAcopioAssignment | VacunaController.getStockStats | backend/src/routes/vacunas.ts:39 |
| GET | /api/vacunas/:id | obligatoria | requirePermissions(['vacunas:read']); requireCentroAcopioAssignment | VacunaController.getById | backend/src/routes/vacunas.ts:47 |
| POST | /api/vacunas | obligatoria | requirePermissions(['vacunas:write']); requireCentroAcopioAssignment | VacunaController.create | backend/src/routes/vacunas.ts:55 |
| PUT | /api/vacunas/:id | obligatoria | requirePermissions(['vacunas:write']); requireCentroAcopioAssignment | VacunaController.update | backend/src/routes/vacunas.ts:64 |
| DELETE | /api/vacunas/:id | obligatoria | requirePermissions(['vacunas:write']); requireCentroAcopioAssignment | VacunaController.delete | backend/src/routes/vacunas.ts:72 |
| POST | /api/vales/generar | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.generarVale | backend/src/routes/vales.ts:35 |
| POST | /api/vales/validar-stock | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.validarStock | backend/src/routes/vales.ts:50 |
| POST | /api/vales/vista-previa | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getVistaPrevia | backend/src/routes/vales.ts:64 |
| GET | /api/vales | obligatoria | requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getVales | backend/src/routes/vales.ts:79 |
| GET | /api/vales/estadisticas | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getEstadisticas | backend/src/routes/vales.ts:89 |
| GET | /api/vales/tipos-generados | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getTiposValesGenerados | backend/src/routes/vales.ts:100 |
| GET | /api/vales/verificar-existencia | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.verificarValesExistentes | backend/src/routes/vales.ts:112 |
| POST | /api/vales/verificar-existencia-batch | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.verificarValesExistentesBatch | backend/src/routes/vales.ts:124 |
| GET | /api/vales/grupos-entregas-generados | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getGruposEntregasAdicionalesGenerados | backend/src/routes/vales.ts:135 |
| GET | /api/vales/entregas-adicionales-disponibles | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getEntregasAdicionalesDisponibles | backend/src/routes/vales.ts:146 |
| GET | /api/vales/calcular-impacto-modificacion | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.calcularImpactoModificacion | backend/src/routes/vales.ts:160 |
| GET | /api/vales/:id | obligatoria | requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getValeById | backend/src/routes/vales.ts:169 |
| PATCH | /api/vales/:id/estado | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.cambiarEstado | backend/src/routes/vales.ts:183 |
| GET | /api/vales/:id/diagnostico | obligatoria | denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.diagnosticarVale | backend/src/routes/vales.ts:192 |
| POST | /api/vales/:id/limpiar-reversion | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.limpiarEstadoReversion | backend/src/routes/vales.ts:201 |
| POST | /api/vales/:id/revertir | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.revertirVale | backend/src/routes/vales.ts:210 |
| POST | /api/vales/:id/sincronizar | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.sincronizarVale | backend/src/routes/vales.ts:223 |
| GET | /api/vales/:id/modificaciones | obligatoria | requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getModificaciones | backend/src/routes/vales.ts:232 |
| POST | /api/vales/:id/export/excel | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.exportarExcel | backend/src/routes/vales.ts:252 |
| POST | /api/vales/export/combined/excel | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.exportarValesCombinados | backend/src/routes/vales.ts:270 |
| POST | /api/vales/:id/export/pdf | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.exportarPDF | backend/src/routes/vales.ts:286 |
| POST | /api/vales/:id/export/preview | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.getExportPreview | backend/src/routes/vales.ts:295 |
| POST | /api/vales/auto-sync | obligatoria | requirePermissions(['vales:write']); denyResponsableAcopio; requireCentroAcopioAssignment; requirePermissions(['vales:read']) | ValeController.autoSync | backend/src/routes/vales.ts:310 |

## Rutas React Router

| Path | Componente | Roles | Archivo componente | Archivo:línea |
| --- | --- | --- | --- | --- |
| / | → dashboard |  |  | src/components/Alertas/AlertasModule.tsx:120 |
| dashboard | DashboardAlertas |  | src/components/Alertas/DashboardAlertas.tsx | src/components/Alertas/AlertasModule.tsx:121 |
| alertas | GestionAlertas |  | src/components/Alertas/GestionAlertas.tsx | src/components/Alertas/AlertasModule.tsx:132 |
| reportes | ReportesAlertas |  | src/components/Alertas/ReportesAlertas.tsx | src/components/Alertas/AlertasModule.tsx:136 |
| configuracion | ConfiguracionAlertas |  | src/components/Alertas/ConfiguracionAlertas.tsx | src/components/Alertas/AlertasModule.tsx:145 |
| * |  |  |  | src/components/Alertas/AlertasModule.tsx:146 |
| (index) |  |  |  | src/components/Configuracion/Configuracion.tsx:133 |
|  | ConfiguracionGroupView |  |  | src/components/Configuracion/Configuracion.tsx:135 |
| * |  |  |  | src/components/Configuracion/Configuracion.tsx:171 |
| / |  |  |  | src/components/Establecimientos/EstablecimientosModule.tsx:72 |
| redes | Redes |  | src/components/Redes/Redes.tsx | src/components/Establecimientos/EstablecimientosModule.tsx:73 |
| microredes | Microredes |  | src/components/Microredes/Microredes.tsx | src/components/Establecimientos/EstablecimientosModule.tsx:74 |
| centros-acopio | CentrosAcopio |  | src/components/CentrosAcopio/CentrosAcopio.tsx | src/components/Establecimientos/EstablecimientosModule.tsx:84 |
| establecimientos | Establecimientos |  | src/components/Establecimientos/Establecimientos.tsx | src/components/Establecimientos/EstablecimientosModule.tsx:96 |
| / |  |  |  | src/components/Inventario/Inventario.tsx:28 |
| vacunas | GestionVacunas |  | src/components/Inventario/GestionVacunas.tsx | src/components/Inventario/Inventario.tsx:29 |
| jeringas | GestionJeringas |  | src/components/Inventario/GestionJeringas.tsx | src/components/Inventario/Inventario.tsx:30 |
| lotes-vacunas | LotesVacunasPage |  | src/components/Inventario/LotesVacunasPage.tsx | src/components/Inventario/Inventario.tsx:31 |
| lotes-jeringas | LotesJeringasPage |  | src/components/Inventario/LotesJeringasPage.tsx | src/components/Inventario/Inventario.tsx:32 |
| configuracion-jeringas | ConfiguracionJeringas |  | src/components/Inventario/ConfiguracionJeringas.tsx | src/components/Inventario/Inventario.tsx:33 |
| / | → inventario |  |  | src/components/Reportes/Reportes.tsx:129 |
| inventario | InventarioTab |  |  | src/components/Reportes/Reportes.tsx:130 |
| movimientos | MovimientosTab |  |  | src/components/Reportes/Reportes.tsx:139 |
| planificacion | PlanificacionTab |  |  | src/components/Reportes/Reportes.tsx:149 |
| programacion-seguimiento-anual | CenaresTab |  |  | src/components/Reportes/Reportes.tsx:158 |
| configuracion | ConfiguracionTab |  |  | src/components/Reportes/Reportes.tsx:167 |
| * |  |  |  | src/components/Reportes/Reportes.tsx:179 |
| / |  |  |  | src/components/Usuarios/UsuariosModule.tsx:18 |
| usuarios | Usuarios |  | src/components/Usuarios/Usuarios.tsx | src/components/Usuarios/UsuariosModule.tsx:19 |
| roles | RolesManagement |  | src/components/Usuarios/RolesManagement.tsx | src/components/Usuarios/UsuariosModule.tsx:20 |
| permisos | PermissionsManagement |  | src/components/Usuarios/PermissionsManagement.tsx | src/components/Usuarios/UsuariosModule.tsx:21 |
| / | → /dashboard |  |  | src/components/routing/AppRoutes.tsx:39 |
| /dashboard | Dashboard |  | src/components/Dashboard/Dashboard.tsx | src/components/routing/AppRoutes.tsx:42 |
| /establecimientos/* | EstablecimientosModule |  | src/components/Establecimientos/EstablecimientosModule.tsx | src/components/routing/AppRoutes.tsx:52 |
| /inventario/* | Inventario |  | src/components/Inventario/Inventario.tsx | src/components/routing/AppRoutes.tsx:62 |
| /movimientos | Movimientos |  | src/components/Movimientos/Movimientos.tsx | src/components/routing/AppRoutes.tsx:72 |
| /planificacion/* | Planificacion |  | src/components/Planificacion/Planificacion.tsx | src/components/routing/AppRoutes.tsx:82 |
| /ici-demid/* | IciDemid | administrador | src/components/IciDemid/IciDemid.tsx | src/components/routing/AppRoutes.tsx:91 |
| /kardex | Kardex |  | src/components/Kardex/Kardex.tsx | src/components/routing/AppRoutes.tsx:101 |
| /reportes/* | Reportes |  | src/components/Reportes/Reportes.tsx | src/components/routing/AppRoutes.tsx:111 |
| /alertas/* | AlertasModule |  | src/components/Alertas/AlertasModule.tsx | src/components/routing/AppRoutes.tsx:121 |
| /usuarios/* | UsuariosModule | administrador | src/components/Usuarios/UsuariosModule.tsx | src/components/routing/AppRoutes.tsx:131 |
| /configuracion/* | Configuracion | administrador | src/components/Configuracion/Configuracion.tsx | src/components/routing/AppRoutes.tsx:141 |
| * | → /dashboard |  |  | src/components/routing/AppRoutes.tsx:151 |

## Pruebas

Archivos: 16; casos (aprox.): 151; marcos: @playwright/test, jest

| Archivo | Tipo | Suites | Casos |
| --- | --- | --- | --- |
| backend/src/__tests__/middleware/accessControl.test.ts | unitaria | 1 | 4 |
| backend/src/__tests__/services/IciDemidService.test.ts | unitaria | 1 | 3 |
| backend/src/__tests__/services/JeringaService.test.ts | unitaria | 1 | 4 |
| backend/src/__tests__/services/ReporteExportService.test.ts | unitaria | 3 | 10 |
| backend/src/__tests__/services/lote-vacuna-protection.test.ts | unitaria | 3 | 4 |
| backend/src/__tests__/services/lote-vacuna-stock-correction.test.ts | unitaria | 1 | 1 |
| backend/src/__tests__/services/movimientos-entrega-adicional-stock.test.ts | unitaria | 1 | 2 |
| backend/src/__tests__/services/permission-readonly.test.ts | unitaria | 1 | 2 |
| backend/src/__tests__/utils/centroAcopioUtils.test.ts | unitaria | 5 | 9 |
| backend/src/__tests__/utils/errors.test.ts | unitaria | 11 | 16 |
| backend/src/__tests__/utils/logger.test.ts | unitaria | 1 | 5 |
| backend/src/__tests__/utils/password.test.ts | unitaria | 5 | 20 |
| backend/src/__tests__/utils/response.test.ts | unitaria | 12 | 16 |
| backend/src/__tests__/utils/validation.test.ts | unitaria | 19 | 41 |
| src/components/Inventario/__tests__/NuevoIngreso.test.tsx | unitaria | 1 | 12 |
| tests/ui/usuarios-rbac.spec.ts | e2e | 0 | 2 |

## Variables de entorno (solo nombres)

| Variable | Usos | Ejemplos |
| --- | --- | --- |
| AI_API_KEY | 1 | backend/src/services/sibot/aiConfig.ts:24 |
| AI_BASE_URL | 1 | backend/src/services/sibot/aiConfig.ts:34 |
| AI_MODEL | 2 | backend/src/controllers/SibotController.ts:112, backend/src/services/sibot/aiConfig.ts:33 |
| AI_PROVIDER | 2 | backend/src/controllers/SibotController.ts:90, backend/src/services/sibot/aiConfig.ts:20 |
| AI_PROVIDER_NAME | 1 | backend/src/services/sibot/aiConfig.ts:56 |
| API_URL | 1 | scripts/clear-rate-limit.js:9 |
| DATABASE_URL | 2 | backend/scripts/clean-production-db.ts:23, backend/src/services/ConfiguracionService.ts:72 |
| DEV | 10 | src/config/api.ts:28, src/contexts/AuthContext.tsx:122, src/contexts/AuthContext.tsx:126 |
| GOOGLE_GENERATIVE_AI_API_KEY | 1 | backend/src/services/sibot/aiConfig.ts:39 |
| MODE | 6 | src/components/Vales/ValesErrorBoundary.tsx:82, src/components/common/ErrorBoundary.tsx:121, src/config/valesConfig.ts:213 |
| NODE_ENV | 17 | backend/src/config/database.ts:11, backend/src/config/database.ts:16, backend/src/routes/auth.ts:12 |
| PG_BIN_DIR | 1 | backend/src/services/ConfiguracionService.ts:34 |
| PLAYWRIGHT_API_URL | 1 | tests/ui/usuarios-rbac.spec.ts:3 |
| PLAYWRIGHT_BASE_URL | 1 | playwright.config.ts:3 |
| SIBOT_GOOGLE_API_KEY | 1 | backend/src/services/sibot/aiConfig.ts:39 |
| SIBOT_GOOGLE_MODEL | 1 | backend/src/services/sibot/aiConfig.ts:40 |
| VITE_API_BASE_URL | 1 | src/config/valesConfig.ts:268 |
| VITE_API_URL | 6 | src/components/Movimientos/Movimientos.tsx:1754, src/config/api.ts:10, src/config/api.ts:11 |
| VITE_DEBUG | 1 | src/utils/debug.ts:7 |
| VITE_ENABLE_ANALYTICS | 1 | src/config/valesConfig.ts:279 |
| VITE_ENABLE_LOGS | 1 | src/config/valesConfig.ts:278 |
| VITE_ENABLE_MOCKS | 1 | src/config/valesConfig.ts:277 |
| VITE_ENVIRONMENT | 1 | src/utils/debug.ts:6 |

## Migraciones

Prisma: 7; SQL manuales: 3

| Migración | Prefijo de fecha |
| --- | --- |
| 20250908212722_add_programacion_anual_cenares | 20250908212722 |
| 20260101_add_version_field_optimistic_locking | 20260101 |
| 20260318_add_alertas_indexes | 20260318 |
| 20260325_add_ici_demid_registros | 20260325 |
| 20260331_add_sibot_support | 20260331 |
| 20260614064203_sync_schema_drift | 20260614064203 |
| 20260909_add_codigo_to_vacunas | 20260909 |

- `backend/migrations/001_add_configuracion_jeringa_vacuna.sql`
- `backend/migrations/001_simple_configuracion_jeringa_vacuna.sql`
- `backend/migrations/002_add_tipo_vale_support.sql`
