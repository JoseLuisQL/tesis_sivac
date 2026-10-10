import os
import json
import subprocess
from pathlib import Path

def test_compat():
    test_dir = Path("salidas/_tmp_auditoria/compat_test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    target = test_dir / "target_dir"
    link = test_dir / "link_dir"
    target.mkdir(exist_ok=True)
    (target / "test.txt").write_text("contenido_de_prueba", encoding="utf-8")
    
    # 1. Test Junction en Windows (no requiere permisos de Administrador ni Developer Mode)
    cmd = f'cmd /c mklink /J "{link.resolve()}" "{target.resolve()}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    junction_ok = link.exists() and (link / "test.txt").read_text(encoding="utf-8") == "contenido_de_prueba"
    print("Prueba Junction (mklink /J):", "EXITOSA" if junction_ok else f"FALLIDA ({res.stderr.strip()})")
    
    # Cleanup junction
    if link.exists():
        subprocess.run(f'cmd /c rmdir "{link.resolve()}"', shell=True, capture_output=True)
        
    # 2. Test Simulación Frontmatter Droid vs Claude
    print("\n--- Mapeo de herramientas de agentes ---")
    claude_tools = ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "PowerShell", "Agent", "Skill", "TaskCreate", "AskUserQuestion"]
    tool_map = {
        "Read": "Read",
        "Write": "Create",
        "Edit": "Edit",
        "Grep": "Grep",
        "Glob": "Glob",
        "Bash": "Execute",
        "PowerShell": "Execute",
        "Agent": "Task",
        "Skill": "Skill",
        "TaskCreate": "TodoWrite",
        "AskUserQuestion": "AskUser"
    }
    mapped = [tool_map.get(t, t) for t in claude_tools]
    # Remove duplicates
    mapped_unique = sorted(list(set(mapped)))
    print("Herramientas en Claude:", claude_tools)
    print("Herramientas mapeadas a Droid:", mapped_unique)

if __name__ == "__main__":
    test_compat()
