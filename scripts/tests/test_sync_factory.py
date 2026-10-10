# -*- coding: utf-8 -*-
"""Pruebas unitarias para scripts/sync_factory.py."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import yaml

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from scripts import sync_factory  # noqa: E402


def test_tool_mapping():
    """Verifica que las herramientas de Claude se traduzcan correctamente a Droid."""
    input_tools = [
        "Write",
        "Bash",
        "PowerShell",
        "Agent",
        "AskUserQuestion",
        "Read",
        "Edit",
        "Grep",
        "Glob",
        "Skill",
        "TodoWrite",
        "TaskCreate",
    ]
    mapped = sync_factory.map_tools(input_tools)
    expected = ["Create", "Execute", "Task", "AskUser", "Read", "Edit", "Grep", "Glob"]
    assert mapped == expected
    # Comprobar que Bash y PowerShell colapsen a un solo Execute
    assert mapped.count("Execute") == 1
    # Comprobar que Skill y TodoWrite sean excluidos
    assert "Skill" not in mapped
    assert "TodoWrite" not in mapped


def test_sync_agents_in_tmp(tmp_path):
    """Verifica la generación de droids desde agentes en un directorio temporal."""
    project_root = tmp_path / "sivac"
    claude_agents = project_root / ".claude" / "agents"
    claude_agents.mkdir(parents=True)

    agent_content = """---
name: guardian-consistencia
description: Custodio metodológico.
model: sonnet
tools:
  - Read
  - Write
  - Bash
  - PowerShell
skills:
  - matriz-consistencia
squad: Squad B
---

# GUARDIÁN DE CONSISTENCIA
Instrucciones del sistema.
"""
    (claude_agents / "guardian-consistencia.md").write_text(agent_content, encoding="utf-8")

    droids_dir = project_root / ".factory" / "droids"
    droids_dir.mkdir(parents=True)

    generated = sync_factory.sync_agents(project_root, droids_dir)
    assert len(generated) == 1

    droid_file = generated[0]
    assert droid_file.name == "guardian-consistencia.md"

    content = droid_file.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Cabecera obligatoria en primera línea
    assert lines[0] == sync_factory.HEADER_WARNING

    # Frontmatter válido
    parts = content.split("---", 2)
    assert len(parts) >= 3
    fm = yaml.safe_load(parts[1])
    assert fm["name"] == "guardian-consistencia"
    assert fm["model"] == "inherit"
    assert fm["tools"] == ["Read", "Create", "Execute"]
    assert "GUARDIÁN DE CONSISTENCIA" in parts[2]


def test_generate_mcp_config(tmp_path):
    """Verifica la resolución y generación de mcp.json."""
    project_root = tmp_path / "sivac"
    project_root.mkdir(parents=True)

    mcp_json = {
        "mcpServers": {
            "firecrawl": {
                "type": "http",
                "url": "https://mcp.firecrawl.dev/v2/mcp",
                "headers": {"Authorization": "Bearer ${FIRECRAWL_KEY}"},
            }
        }
    }
    (project_root / ".mcp.json").write_text(json.dumps(mcp_json), encoding="utf-8")

    claude_settings = project_root / ".claude"
    claude_settings.mkdir(parents=True)
    settings_local = {"env": {"FIRECRAWL_KEY": "secret-token-123"}}
    (claude_settings / "settings.local.json").write_text(json.dumps(settings_local), encoding="utf-8")

    out_file = project_root / ".factory" / "mcp.json"
    out_file.parent.mkdir(parents=True)

    res = sync_factory.generate_mcp_config(project_root, out_file)
    assert out_file.exists()

    with open(out_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    servers = data["mcpServers"]
    assert "firecrawl" in servers
    assert servers["firecrawl"]["headers"]["Authorization"] == "Bearer secret-token-123"
    assert "zotero" in servers
    assert "context7" in servers


def test_generate_hooks_config(tmp_path):
    """Verifica la generación de hooks.json."""
    project_root = tmp_path / "sivac"
    out_file = project_root / ".factory" / "hooks.json"
    out_file.parent.mkdir(parents=True)

    res = sync_factory.generate_hooks_config(project_root, out_file)
    assert out_file.exists()

    with open(out_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "PreToolUse" in data
    assert "SessionStart" in data
    assert "SubagentStop" in data
    assert "Stop" in data

    pretool = data["PreToolUse"][0]["hooks"][0]["command"]
    assert "pretooluse_blocker.cjs" in pretool


def test_verify_sync_on_actual_project():
    """Verifica que el entorno real cumpla con todos los criterios de sincronización."""
    project_root = RAIZ
    verif = sync_factory.verify_sync(project_root)
    assert verif["valid"] is True, f"Errores en verify_sync: {verif['errors']}"
    assert verif["droids_count"] == 14
    assert verif["skills_count"] == 21
    assert len(verif["mcp_servers"]) == 5
    assert "PreToolUse" in verif["hook_events"]
