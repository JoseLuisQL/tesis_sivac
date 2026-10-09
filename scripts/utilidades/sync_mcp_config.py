import json
import shutil
from pathlib import Path

def sync_mcp():
    user_mcp_path = Path.home() / ".factory" / "mcp.json"
    backup_path = Path.home() / ".factory" / "mcp.json.bak"

    if user_mcp_path.exists():
        shutil.copy2(user_mcp_path, backup_path)
        with open(user_mcp_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
    else:
        user_config = {"mcpServers": {}}

    if "mcpServers" not in user_config:
        user_config["mcpServers"] = {}

    settings_path = Path(r"C:\MisInvestigaciones\tesis\sivac\.claude\settings.local.json")
    with open(settings_path, "r", encoding="utf-8") as f:
        claude_settings = json.load(f)
    env = claude_settings.get("env", {})

    mcp_path = Path(r"C:\MisInvestigaciones\tesis\sivac\.mcp.json")
    with open(mcp_path, "r", encoding="utf-8") as f:
        project_mcp = json.load(f)

    servers = project_mcp.get("mcpServers", {})

    for name, srv in servers.items():
        srv_copy = dict(srv)
        srv_copy["disabled"] = False
        
        if "headers" in srv_copy:
            resolved_headers = {}
            for h_k, h_v in srv_copy["headers"].items():
                for env_k, env_v in env.items():
                    pattern = "${" + env_k + "}"
                    if pattern in h_v:
                        h_v = h_v.replace(pattern, env_v)
                resolved_headers[h_k] = h_v
            srv_copy["headers"] = resolved_headers

        user_config["mcpServers"][name] = srv_copy

    with open(user_mcp_path, "w", encoding="utf-8") as f:
        json.dump(user_config, f, indent=2)

    server_names = list(user_config["mcpServers"].keys())
    print(f"MCP configuration synced successfully. Servers configured: {server_names}")

if __name__ == "__main__":
    sync_mcp()
