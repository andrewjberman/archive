import os

with open(".env") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        k, _, v = line.partition("=")
        os.environ[k] = v

import app.server  # noqa: F401  -- triggers integrations.register_enabled(mcp, ...)
from app.tools import mcp

names = sorted(t.name for t in mcp._tool_manager.list_tools())
print(len(names))
for n in names:
    print(n)
