#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIVAC-THESIS-LAB — Generador Determinista de Compatibilidad (.claude/ -> .factory/)
Fase E / Bloque 2 del Plan de Migración v3.0

Sincroniza deterministamente la configuración canónica de Claude Code (.claude/)
hacia el formato nativo de Factory Droid (.factory/):
  1. Agentes (.claude/agents/*.md -> .factory/droids/*.md) con frontmatter Droid y cabecera de advertencia.
  2. Skills (.claude/skills -> .factory/skills) mediante enlace directorio (Junction Windows) o copia espejo.
  3. Servidores MCP (.mcp.json + settings.local.json -> .factory/mcp.json) con resolución de variables.
  4. Hooks de ciclo de vida (.claude/hooks -> .factory/hooks.json) para PreToolUse, SessionStart y SubagentStop.

Uso:
  python scripts/sync_factory.py              # Ejecuta sincronización completa y validación
  python scripts/sync_factory.py --check      # Solo valida el estado actual de .factory/
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import yaml

# Mapeo oficial de herramientas Claude Code -> Factory Droid
TOOL_MAPPING = {
    "Write": "Create",
    "Bash": "Execute",
    "PowerShell": "Execute",
    "Agent": "Task",
    "AskUserQuestion": "AskUser",
    "Read": "Read",
    "Edit": "Edit",
    "Grep": "Grep",
    "Glob": "Glob",
    "LS": "LS",
}

# Herramientas auto-inyectadas o específicas de Claude a excluir del arreglo tools en Droid
EXCLUDED_TOOLS = {
    "Skill",
    "TodoWrite",
    "TaskCreate",
    "TaskGet",
    "TaskList",
    "TaskUpdate",
    "Tasks",
}

# Asignación canónica de servidores MCP por agente (Tabla E2 / Catálogo MCP)
AGENT_MCP_MAP = {
    "director-general": ["zotero", "ydc-server", "firecrawl"],
    "investigador-bibliografico": ["zotero", "ydc-server", "firecrawl"],
    "verificador-integridad": ["zotero"],
    "especialista-forms": ["playwright"],
    "ingeniero-sivac": ["context7"],
    "documentador-xp": ["context7", "playwright"],
    "redactor-academico": ["zotero"],
}

HEADER_WARNING = "<!-- GENERADO AUTOMÁTICAMENTE desde .claude/agents/ — NO EDITAR DIRECTAMENTE -->"


def get_project_root() -> Path:
    """Retorna la ruta raíz del proyecto SIVAC."""
    return Path(__file__).resolve().parent.parent


def ensure_directories(project_root: Path) -> dict[str, Path]:
    """Crea la estructura base de directorios .factory/."""
    factory_dir = project_root / ".factory"
    droids_dir = factory_dir / "droids"
    factory_dir.mkdir(parents=True, exist_ok=True)
    droids_dir.mkdir(parents=True, exist_ok=True)
    return {
        "factory": factory_dir,
        "droids": droids_dir,
        "skills": factory_dir / "skills",
        "mcp": factory_dir / "mcp.json",
        "hooks": factory_dir / "hooks.json",
    }


def map_tools(claude_tools: list[str]) -> list[str]:
    """Traduce la lista de herramientas de Claude Code a Factory Droid."""
    mapped: list[str] = []
    for tool in claude_tools:
        if tool in EXCLUDED_TOOLS:
            continue
        droid_tool = TOOL_MAPPING.get(tool, tool)
        if droid_tool not in mapped:
            mapped.append(droid_tool)
    return mapped


def sync_agents(project_root: Path, droids_dir: Path) -> list[Path]:
    """
    Lee cada agente en .claude/agents/*.md y genera su equivalente en .factory/droids/<name>.md.
    """
    agents_dir = project_root / ".claude" / "agents"
    if not agents_dir.exists():
        raise FileNotFoundError(f"Directorio de agentes no encontrado: {agents_dir}")

    agent_files = sorted(agents_dir.glob("*.md"))
    generated_files: list[Path] = []

    for agent_path in agent_files:
        content = agent_path.read_text(encoding="utf-8")
        parts = content.split("---", 2)
        if len(parts) < 3:
            print(f"ADVERTENCIA: Archivo {agent_path.name} no contiene frontmatter válido.")
            continue

        raw_fm = yaml.safe_load(parts[1]) or {}
        body = parts[2].strip()

        agent_name = raw_fm.get("name", agent_path.stem).lower().strip()
        description = raw_fm.get("description", "").strip()
        model = "inherit"

        raw_tools = raw_fm.get("tools", [])
        mapped_tools = map_tools(raw_tools)

        # Determinar servidores MCP para el agente
        mcp_servers = list(raw_fm.get("mcpServers", []))
        catalog_mcps = AGENT_MCP_MAP.get(agent_name, [])
        for mcp in catalog_mcps:
            if mcp not in mcp_servers:
                mcp_servers.append(mcp)

        # Construir archivo con cabecera en primera línea y frontmatter nativo Droid
        lines: list[str] = [
            HEADER_WARNING,
            "---",
            f"name: {agent_name}",
        ]

        if description:
            # Si contiene saltos de línea o caracteres complejos, formatear adecuadamente
            if "\n" in description:
                lines.append("description: >-")
                for dline in description.splitlines():
                    if dline.strip():
                        lines.append(f"  {dline.strip()}")
            else:
                lines.append(f"description: {description}")

        lines.append(f"model: {model}")

        if mapped_tools:
            lines.append("tools:")
            for tool in mapped_tools:
                lines.append(f"  - {tool}")

        if mcp_servers:
            lines.append("mcpServers:")
            for srv in mcp_servers:
                lines.append(f"  - {srv}")

        lines.append("---")
        lines.append("")
        if body:
            lines.append(body)
        lines.append("")

        droid_file = droids_dir / f"{agent_name}.md"
        droid_file.write_text("\n".join(lines), encoding="utf-8")
        generated_files.append(droid_file)

    return generated_files


def sync_skills(project_root: Path, factory_skills: Path) -> dict[str, str | int]:
    """
    Sincroniza .claude/skills hacia .factory/skills creando un Directory Junction en Windows
    o una copia espejo sincronizada como alternativa.
    """
    claude_skills = project_root / ".claude" / "skills"
    if not claude_skills.exists():
        raise FileNotFoundError(f"Directorio de skills no encontrado: {claude_skills}")

    result: dict[str, str | int] = {
        "status": "ok",
        "method": "",
        "skills_count": 0,
    }

    # Si ya existe el destino, verificar si contiene las skills o si necesita reemplazo
    if factory_skills.exists():
        try:
            existing = [d.name for d in factory_skills.iterdir() if d.is_dir()]
            expected = [d.name for d in claude_skills.iterdir() if d.is_dir()]
            if set(expected).issubset(set(existing)):
                result["method"] = "existente"
                result["skills_count"] = len(existing)
                return result
        except Exception:
            pass

        # Si no coincide completamente, intentar remover el enlace previo
        try:
            subprocess.run(["cmd", "/c", "rmdir", str(factory_skills)], capture_output=True)
        except Exception:
            pass

    # Intentar crear Junction NTFS en Windows
    try:
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(factory_skills), str(claude_skills)],
            capture_output=True,
            text=True,
            check=True,
        )
        count = len([d for d in factory_skills.iterdir() if d.is_dir()])
        result["method"] = "junction"
        result["skills_count"] = count
        return result
    except Exception as exc:
        # Fallback a copia espejo
        shutil.copytree(claude_skills, factory_skills, dirs_exist_ok=True)
        count = len([d for d in factory_skills.iterdir() if d.is_dir()])
        result["method"] = "copia_espejo"
        result["skills_count"] = count
        result["warning"] = f"Fallback a copia por: {exc}"
        return result


def generate_mcp_config(project_root: Path, output_file: Path) -> dict:
    """
    Lee .mcp.json y .claude/settings.local.json, resuelve cabeceras y variables,
    y escribe .factory/mcp.json con los servidores mcp activos:
    firecrawl, ydc-server, playwright, zotero, context7.
    """
    mcp_path = project_root / ".mcp.json"
    settings_local_path = project_root / ".claude" / "settings.local.json"
    home_claude_path = Path.home() / ".claude.json"
    home_factory_mcp_path = Path.home() / ".factory" / "mcp.json"

    # 1. Cargar variables de entorno locales de Claude
    env_vars: dict[str, str] = {}
    if settings_local_path.exists():
        try:
            with open(settings_local_path, "r", encoding="utf-8") as f:
                settings_data = json.load(f)
                env_vars.update(settings_data.get("env", {}))
        except Exception as e:
            print(f"Aviso: No se pudo leer {settings_local_path}: {e}")

    # Agregar variables del entorno del sistema
    env_vars.update(dict(os.environ))

    # 2. Cargar servidores base desde .mcp.json
    base_servers: dict[str, dict] = {}
    if mcp_path.exists():
        try:
            with open(mcp_path, "r", encoding="utf-8") as f:
                base_servers = json.load(f).get("mcpServers", {})
        except Exception as e:
            print(f"Aviso: No se pudo leer {mcp_path}: {e}")

    # 3. Cargar configuraciones globales desde ~/.claude.json y ~/.factory/mcp.json
    global_claude_servers: dict[str, dict] = {}
    if home_claude_path.exists():
        try:
            with open(home_claude_path, "r", encoding="utf-8") as f:
                global_claude_servers = json.load(f).get("mcpServers", {})
        except Exception:
            pass

    global_factory_servers: dict[str, dict] = {}
    if home_factory_mcp_path.exists():
        try:
            with open(home_factory_mcp_path, "r", encoding="utf-8") as f:
                global_factory_servers = json.load(f).get("mcpServers", {})
        except Exception:
            pass

    # 4. Construir configuración unificada
    target_servers: dict[str, dict] = {}

    # Servidores desde .mcp.json (firecrawl, ydc-server, playwright)
    for name, srv in base_servers.items():
        srv_copy = dict(srv)
        srv_copy["disabled"] = False

        if "headers" in srv_copy:
            resolved_headers: dict[str, str] = {}
            for h_k, h_v in srv_copy["headers"].items():
                val = str(h_v)
                for env_k, env_v in env_vars.items():
                    pattern = f"${{{env_k}}}"
                    if pattern in val:
                        val = val.replace(pattern, env_v)
                resolved_headers[h_k] = val
            srv_copy["headers"] = resolved_headers

        target_servers[name] = srv_copy

    # Servidor Zotero
    if "zotero" in global_factory_servers:
        target_servers["zotero"] = dict(global_factory_servers["zotero"])
    elif "zotero" in global_claude_servers:
        target_servers["zotero"] = dict(global_claude_servers["zotero"])
    else:
        # Fallback canónico de Zotero
        zotero_cmd = str(Path.home() / ".local" / "bin" / "zotero-mcp.exe")
        target_servers["zotero"] = {
            "type": "stdio",
            "command": zotero_cmd,
            "args": [],
            "env": {
                "ZOTERO_LOCAL": "true",
                "ZOTERO_EMBEDDING_MODEL": "default",
            },
        }

    # Servidor Context7
    if "context7" in global_claude_servers:
        c7_config = dict(global_claude_servers["context7"])
        target_servers["context7"] = c7_config
    elif "context7" in global_factory_servers:
        target_servers["context7"] = dict(global_factory_servers["context7"])
    else:
        # Fallback canónico de Context7
        c7_key = env_vars.get("CONTEXT7_API_KEY", "")
        headers = {}
        if c7_key:
            headers["CONTEXT7_API_KEY"] = c7_key
        target_servers["context7"] = {
            "type": "http",
            "url": "https://mcp.context7.com/mcp",
            "headers": headers,
        }

    # Asegurar que los 5 servidores requeridos estén presentes
    for req in ("firecrawl", "ydc-server", "playwright", "zotero", "context7"):
        if req not in target_servers:
            print(f"ADVERTENCIA: Servidor requerido '{req}' no pudo ser configurado.")

    final_mcp_config = {"mcpServers": target_servers}

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_mcp_config, f, indent=2, ensure_ascii=False)

    return final_mcp_config


def generate_hooks_config(project_root: Path, output_file: Path) -> dict:
    """
    Configura los eventos PreToolUse, SessionStart y SubagentStop apuntando
    a los scripts universales .claude/hooks/*.cjs.
    """
    hooks_dir = project_root / ".claude" / "hooks"
    pretooluse_script = str(hooks_dir / "pretooluse_blocker.cjs")
    session_start_script = str(hooks_dir / "session_start.cjs")
    handoff_script = str(hooks_dir / "handoff_reminder.cjs")

    hooks_config = {
        "PreToolUse": [
            {
                "matcher": "*",
                "hooks": [
                    {
                        "type": "command",
                        "command": f'node "{pretooluse_script}"',
                        "timeout": 10,
                    }
                ],
            }
        ],
        "SessionStart": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": f'node "{session_start_script}"',
                        "timeout": 10,
                    }
                ],
            }
        ],
        "SubagentStop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": f'node "{handoff_script}"',
                        "timeout": 10,
                    }
                ],
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": f'node "{handoff_script}"',
                        "timeout": 10,
                    }
                ],
            }
        ],
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(hooks_config, f, indent=2, ensure_ascii=False)

    return hooks_config


def verify_sync(project_root: Path) -> dict:
    """
    Verifica que la sincronización cumpla los 4 criterios de aceptación:
      1. 14 droids en .factory/droids/
      2. 21 skills en .factory/skills/
      3. .factory/mcp.json JSON válido con 5 servidores
      4. .factory/hooks.json JSON válido con los hooks configurados
    """
    errors: list[str] = []
    summary: dict[str, any] = {}

    droids_dir = project_root / ".factory" / "droids"
    skills_dir = project_root / ".factory" / "skills"
    mcp_file = project_root / ".factory" / "mcp.json"
    hooks_file = project_root / ".factory" / "hooks.json"

    # 1. Verificar droids
    if not droids_dir.exists():
        errors.append(f"No existe el directorio {droids_dir}")
        summary["droids_count"] = 0
    else:
        droid_files = list(droids_dir.glob("*.md"))
        summary["droids_count"] = len(droid_files)
        summary["droids"] = [p.name for p in droid_files]
        if len(droid_files) != 14:
            errors.append(f"Se esperaban 14 droids, pero se encontraron {len(droid_files)}.")

        # Verificar cabecera en cada droid
        for df in droid_files:
            first_line = df.read_text(encoding="utf-8").splitlines()[0] if df.stat().st_size > 0 else ""
            if HEADER_WARNING not in first_line:
                errors.append(f"Droid {df.name} no contiene la cabecera obligatoria en la primera línea.")

    # 2. Verificar skills
    if not skills_dir.exists():
        errors.append(f"No existe el directorio {skills_dir}")
        summary["skills_count"] = 0
    else:
        skill_dirs = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        summary["skills_count"] = len(skill_dirs)
        summary["skills"] = skill_dirs
        if len(skill_dirs) < 21:
            errors.append(f"Se esperaban al menos 21 skills, se encontraron {len(skill_dirs)}.")

    # 3. Verificar mcp.json
    if not mcp_file.exists():
        errors.append(f"No existe {mcp_file}")
    else:
        try:
            with open(mcp_file, "r", encoding="utf-8") as f:
                mcp_data = json.load(f)
            servers = list(mcp_data.get("mcpServers", {}).keys())
            summary["mcp_servers"] = servers
            for req in ("firecrawl", "ydc-server", "playwright", "zotero", "context7"):
                if req not in servers:
                    errors.append(f"Servidor MCP '{req}' falta en {mcp_file}")
        except Exception as e:
            errors.append(f"Error parseando {mcp_file}: {e}")

    # 4. Verificar hooks.json
    if not hooks_file.exists():
        errors.append(f"No existe {hooks_file}")
    else:
        try:
            with open(hooks_file, "r", encoding="utf-8") as f:
                hooks_data = json.load(f)
            events = list(hooks_data.keys())
            summary["hook_events"] = events
            for req in ("PreToolUse", "SessionStart", "SubagentStop"):
                if req not in events:
                    errors.append(f"Evento de hook '{req}' falta en {hooks_file}")
        except Exception as e:
            errors.append(f"Error parseando {hooks_file}: {e}")

    summary["errors"] = errors
    summary["valid"] = len(errors) == 0
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="SIVAC-THESIS-LAB: Generador determinista de sincronización .claude/ -> .factory/"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verifica la consistencia sin re-generar archivos",
    )
    args = parser.parse_args()

    project_root = get_project_root()
    print("=" * 70)
    print(" SIVAC-THESIS-LAB — SINCRONIZADOR DETERMINISTA CLAUDE -> FACTORY DROID")
    print(f" Raíz del proyecto: {project_root}")
    print("=" * 70)

    if not args.check:
        dirs = ensure_directories(project_root)
        print("\n[1/4] Sincronizando Agentes (.claude/agents/*.md -> .factory/droids/*.md)...")
        droids = sync_agents(project_root, dirs["droids"])
        print(f"  OK: {len(droids)} droids generados en {dirs['droids']}")

        print("\n[2/4] Sincronizando Skills (.claude/skills -> .factory/skills)...")
        skills_res = sync_skills(project_root, dirs["skills"])
        print(f"  OK: {skills_res['skills_count']} skills vinculadas mediante {skills_res['method']}")

        print("\n[3/4] Generando configuración de Servidores MCP (.factory/mcp.json)...")
        mcp_res = generate_mcp_config(project_root, dirs["mcp"])
        srv_list = list(mcp_res.get("mcpServers", {}).keys())
        print(f"  OK: {len(srv_list)} servidores configurados: {', '.join(srv_list)}")

        print("\n[4/4] Generando configuración de Hooks de Seguridad (.factory/hooks.json)...")
        hooks_res = generate_hooks_config(project_root, dirs["hooks"])
        print(f"  OK: Eventos configurados: {', '.join(hooks_res.keys())}")

    print("\n" + "-" * 70)
    print(" VERIFICACIÓN DE INTEGRIDAD Y CALIDAD")
    print("-" * 70)
    verification = verify_sync(project_root)

    print(f" Droids encontrados:  {verification.get('droids_count', 0)} / 14")
    print(f" Skills encontradas:  {verification.get('skills_count', 0)} / 21")
    print(f" Servidores MCP:      {', '.join(verification.get('mcp_servers', []))}")
    print(f" Hooks configurados:  {', '.join(verification.get('hook_events', []))}")

    if verification["valid"]:
        print("\n Sincronización COMPLETADA con ÉXITO. Todos los criterios validados.")
        sys.exit(0)
    else:
        print("\n FALLO EN LA VERIFICACIÓN:")
        for err in verification["errors"]:
            print(f"   - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
