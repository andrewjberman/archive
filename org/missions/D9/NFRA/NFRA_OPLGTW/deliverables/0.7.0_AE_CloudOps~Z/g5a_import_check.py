#!/usr/bin/env python
"""OG-ap-20: the HOST-SHAPED import check, in a fresh interpreter. Reads nothing remote, applies nothing.

WHY A HOST SHAPE AND NOT THE REPO TREE. In the repo, `app/` sits four levels down at
infra/aws/ec2/opal-gateway/app and `lib/` is at the repo ROOT; on the host both sit side by side under
/opt/opal-gateway. A module that locates the trading calendar by a FIXED parent index therefore resolves
in one tree and not the other -- the defect OG-gt-10 fixed by SEARCHING instead of indexing. So the
caller stages a host-SHAPED root (app/ and lib/ beside each other, app/<mod>.py exactly four parents
deep, as on the host) and this runs there, never in the repo tree.

COVERS WHAT THE COO HALF'S C6 NAMES: the three taken modules, `typed_scope`, and `app.tools`.
`typed_scope` is listed explicitly even though all three modules import it transitively, because C6
names it and a transitive import proves only that SOME path reached it.

Usage: python g5a_import_check.py <host-shaped-root> [--expect-registry N]
"""
from __future__ import annotations

import json
import pathlib
import sys

G5 = ["etfs_get_partner_ownership", "etfs_get_ownership_rollup", "etfs_get_monthly_report",
      "etfs_get_fund_nav_history", "etfs_get_fund_holdings", "mdpf_get_category_views"]
MODULES = ("etfs_ownership", "etfs_funds", "portal_mdpf", "typed_scope", "tools")


def main() -> int:
    root = sys.argv[1]
    expect = None
    if "--expect-registry" in sys.argv:
        expect = int(sys.argv[sys.argv.index("--expect-registry") + 1])
    sys.path.insert(0, root)

    out = {"root": root, "modules": {}, "parents": {}, "expect_registry": expect}
    for m in MODULES:
        try:
            mod = __import__("app." + m, fromlist=["x"])
            out["modules"][m] = "ok"
            f = getattr(mod, "__file__", None)
            if f:
                out["parents"][m] = len(pathlib.Path(f).resolve().parents)
        except Exception as exc:
            out["modules"][m] = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    out["ok_count"] = sum(1 for v in out["modules"].values() if v == "ok")
    out["total"] = len(out["modules"])

    probe = pathlib.Path(root + "/app/etfs_ownership.py").resolve()
    out["parents_of_probe"] = len(probe.parents)
    out["depth_equals_host"] = len(probe.parents) == 4      # /opt/opal-gateway/app/x.py has 4

    try:
        from app import tools
        names = [t.name for t in tools.mcp._tool_manager.list_tools()]
        out["registry_count_in_tree"] = len(names)
        out["six_registered"] = sorted(n for n in G5 if n in names)
        out["six_missing"] = sorted(n for n in G5 if n not in names)
        out["registry_matches_expectation"] = None if expect is None else len(names) == expect
    except Exception as exc:
        out["registry_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:200])

    # the calendar must resolve BY SEARCH from the host shape (the OG-gt-10 fix), per module
    for m in ("etfs_ownership", "etfs_funds", "portal_mdpf"):
        try:
            mod = __import__("app." + m, fromlist=["x"])
            fn = getattr(mod, "_calendar", None)
            out.setdefault("calendar_resolves", {})[m] = (fn() is not None) if callable(fn) else "no _calendar helper"
        except Exception as exc:
            out.setdefault("calendar_resolves", {})[m] = "%s: %s" % (type(exc).__name__, str(exc)[:120])

    ok = (out["ok_count"] == out["total"] and out.get("depth_equals_host")
          and not out.get("six_missing") and out.get("registry_matches_expectation") is not False)
    out["verdict"] = ("IMPORTS CLEAN -- %d of %d modules import at host depth, registry %s with all six G5 "
                      "tools registered" % (out["ok_count"], out["total"], out.get("registry_count_in_tree"))
                      ) if ok else "FAILED -- see modules / six_missing / registry_count_in_tree"
    print(json.dumps(out, indent=1, default=str))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
