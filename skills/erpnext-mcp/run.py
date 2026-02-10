#!/usr/bin/env python3
"""Entrypoint wrapper to run the ERPNext MCP server as a module."""
import os
import sys

# Ensure current directory is in PYTHONPATH so "src" package can be imported
root = os.path.dirname(__file__)
if root not in sys.path:
    sys.path.insert(0, root)

# Execute as module
os.execvp(sys.executable, [sys.executable, "-m", "src.erpnext_mcp.server"])