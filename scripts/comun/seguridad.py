# -*- coding: utf-8 -*-
"""
Módulo de seguridad y protección de activos de SIVAC-THESIS-LAB.
Implementa Regla Canónica 01 (01_seguridad.md):
- Bloqueo de escritura en referencias/, syncova, PROYECTO_TESIS.docx y datos/raw/.
- Verificación de no sobrescritura y hashes criptográficos SHA-256.
"""
import hashlib
import sys
from pathlib import Path
from typing import Union

RUTAS_SOLO_LECTURA = (
    "syncova",
    "referencias/",
    "ejemplos_tesis",
    "ejemplo_validacion",
    "proyecto_tesis.docx",
    "datos/raw/",
)


def configurar_utf8() -> None:
    """Configura la salida estándar en UTF-8 para evitar errores en consolas cp1252."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def asegurar_escritura_permitida(ruta: Union[str, Path]) -> Path:
    """Verifica que la ruta objetivo no pertenezca a ningún directorio protegido de solo lectura."""
    p = Path(ruta).resolve()
    normalizada = str(p).lower().replace("\\", "/")
    for protegida in RUTAS_SOLO_LECTURA:
        if protegida in normalizada:
            raise PermissionError(
                f"[SEGURIDAD BLOQUEADA] Escritura prohibida en ruta de solo lectura: '{p}' "
                f"(coincide con '{protegida}' - Regla Canónica 01)."
            )
    return p


def asegurar_no_sobrescribe(origen: Union[str, Path], destino: Union[str, Path]) -> Path:
    """Garantiza que el archivo destino no sea igual al origen ni sobrescriba un insumo protegido."""
    p_orig = Path(origen).resolve()
    p_dest = asegurar_escritura_permitida(destino)
    if p_orig == p_dest:
        raise PermissionError(
            f"[SEGURIDAD BLOQUEADA] El archivo de destino no puede ser idéntico al origen: '{p_dest}'."
        )
    return p_dest


def sha256_archivo(ruta: Union[str, Path]) -> str:
    """Calcula el hash SHA-256 hexadecimal de un archivo en disco."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()
