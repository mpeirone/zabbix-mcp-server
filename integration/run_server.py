"""Launcher for Zabbix MCP Server in stdio mode.

Adds src/ to the import path before starting the server, consistent
with the approach used in the project's Dockerfile.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from zabbix_mcp_server import mcp  # noqa: E402

mcp.run()
