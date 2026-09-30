"""Shared import path for the round-19 ~P checks: the performance package of the worktree given as argv[1]."""
import sys
from pathlib import Path


def install(root):
    root = Path(root).resolve()
    package = root / "infra" / "aws" / "lambda" / "investor-reporting" / "performance"
    if not (package / "f49_engine.py").is_file():
        raise SystemExit("FAIL: no performance package under %s" % root)
    for path in (package, package.parent / "reports", package.parent / "_ids", package.parent / "_authz",
                 root / "data" / "assets" / "scripts" / "gold" / "runners_49f", root / "lib"):
        sys.path.insert(0, str(path))
    return root, package
