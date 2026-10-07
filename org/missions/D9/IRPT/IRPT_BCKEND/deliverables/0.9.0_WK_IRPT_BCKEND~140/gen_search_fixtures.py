#!/usr/bin/env python3
"""IB-pr-338: write the two search-response fixtures the portal reader tests read.

The fixtures are built by `build()` in infra/aws/lambda/investor-reporting/directory/tests/
test_search_readers_overage.py (the real guarded irpt-directory-search handler, recorded storage,
controlled 2026 clock). Run from the workspace root:

    python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~140/gen_search_fixtures.py [--check]

--check writes nothing and exits 1 if a committed file differs from a fresh build.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
TEST = ROOT / "infra/aws/lambda/investor-reporting/directory/tests/test_search_readers_overage.py"
OUT = ROOT / "portal/src/pages/InvestorReporting/__tests__/ir-62-overage/fixtures"


def main(argv):
    spec = importlib.util.spec_from_file_location("ir62_search_readers", TEST)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    built = mod.build()
    drift = []
    OUT.mkdir(parents=True, exist_ok=True)
    for arm, parts in built.items():
        for kind, body in parts.items():
            name = "%s.%s.json" % (arm, kind)
            text = json.dumps(body, indent=2, sort_keys=True) + "\n"
            path = OUT / name
            if "--check" in argv:
                if not path.is_file() or path.read_text(encoding="utf-8") != text:
                    drift.append(name)
            else:
                path.write_text(text, encoding="utf-8", newline="\n")
                print("wrote", path.relative_to(ROOT).as_posix(), len(text), "bytes")
    if drift:
        print("DRIFT:", drift)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
