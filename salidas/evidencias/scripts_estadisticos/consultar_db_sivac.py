# -*- coding: utf-8 -*-
import psycopg2
from pathlib import Path

env_path = Path("C:/Proyectos/syncova/backend/.env")
db_url = None
for line in env_path.read_text(encoding="utf-8").splitlines():
    if line.startswith("DATABASE_URL="):
        db_url = line.split("=", 1)[1].strip().strip("\"'").split("?")[0]

conn = psycopg2.connect(db_url)
cur = conn.cursor()

print("=" * 80)
print("CENTROS DE ACOPIO REALES REGISTRADOS EN LA BASE DE DATOS SIVAC (POSTGRESQL)")
print("=" * 80)

query = """
SELECT
    ca.id,
    ca.codigo,
    ca.nombre,
    ca.responsable,
    COALESCE(mr.nombre, 'ALMACÉN CENTRAL / SIN MICRORED') as microred,
    COALESCE(r.nombre, 'SEDE CENTRAL DISA') as red
FROM centros_acopio ca
LEFT JOIN microredes mr ON ca.microred_id = mr.id
LEFT JOIN redes r ON mr.red_id = r.id
ORDER BY ca.codigo NULLS FIRST, ca.nombre;
"""
cur.execute(query)
rows = cur.fetchall()

centros_reales = []
for r in rows:
    centros_reales.append({
        "id": str(r[0]),
        "codigo": r[1] or "S/C",
        "nombre": r[2],
        "responsable": r[3] or "No asignado",
        "microred": r[4],
        "red": r[5]
    })
    print(f"Cód: {str(r[1]):10s} | Centro: {r[2]:32s} | Microred: {r[4]:25s} | Red: {r[5]}")

print(f"\nTotal centros de acopio reales en BD: {len(centros_reales)}")

# Guardar catálogo real en JSON para uso en todo el laboratorio
import json
out_json = Path("datos/schemas/centros_acopio_reales_sivac.json")
out_json.write_text(json.dumps(centros_reales, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Catálogo oficial exportado a: {out_json}")

# Consultar también usuarios reales en la BD
print("\n" + "=" * 80)
print("USUARIOS REGISTRADOS EN LA BASE DE DATOS SIVAC")
print("=" * 80)
cur.execute("""
SELECT u.id, u.usuario, u.email, u.rol, u.nombres, u.apellidos, ca.nombre as centro
FROM usuarios u
LEFT JOIN centros_acopio ca ON u.centro_acopio_id = ca.id
ORDER BY u.id;
""")
for u in cur.fetchall():
    print(f"User: {u[1]:15s} | Rol: {u[3]:15s} | Nombre: {str(u[4])} {str(u[5])} | Centro: {str(u[6])}")

conn.close()
