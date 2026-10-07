"""IRPT_DASHBD TO-DB-b-40 (round 25, workstream B) -- the controls for the hardened classify_and_sum. LOCAL; no S3.

Loads the served producer as it stood at the round-25 issuance commit (`git show 09eafc7c24:...`) beside the hardened source and runs
the same synthetic conditional-bearing day through both. Run from the worktree root:

    python <this file>                 # writes CONTROLS_E3.json beside this file

The old source is placed under .scratch/ at a depth that keeps its root-relative paths valid; it is never imported by the producer.
ASCII only.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path.cwd().resolve()
G = "data/assets/scripts/gold/irpt_reporting/"
OLD_PIN = "09eafc7c24"
OUT = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~22/CONTROLS_E3.json"
OPTION = "future.infer_string"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    old_text = subprocess.run(["git", "show", "%s:%saccount_return_daily.py" % (OLD_PIN, G)], capture_output=True, check=True).stdout
    home = ROOT / ".scratch" / "o1" / "o2" / "o3" / "o4"           # parents[5] of a file here is the worktree root
    home.mkdir(parents=True, exist_ok=True)
    (home / "account_return_daily.py").write_bytes(old_text)
    (home / "sources.json").write_bytes((ROOT / G / "sources.json").read_bytes())
    for extra in ("lib", "data/assets/scripts/lib", G.rstrip("/"), G + "tests"):
        sys.path.insert(0, str(ROOT / extra))
    new = load("ard_new", ROOT / G / "account_return_daily.py")
    old = load("ard_old", home / "account_return_daily.py")
    import test_account_return_daily_none as t            # the synthetic day the tests use

    def run(mod, option):
        pd.set_option(OPTION, option)
        decl = mod.load_declaration()
        src = mod.source_entry(decl, mod.declared_sources(decl)[0])
        table, keycols = mod.load_classification(src)
        return mod.classify_and_sum(t.trn_frame(t.ROWS), src, table, keycols)

    try:
        res = {(n, o): run(m, o) for n, m in (("old", old), ("new", new)) for o in (False, True)}
    finally:
        pd.set_option(OPTION, True)
    conditional = sum(1 for r in t.ROWS if r[1] == "$JNL")
    out = {
        "task_order": "IRPT_DASHBD.TO-DB-b-40", "worker": "0.9.0_WK_IRPT_DASHBD~22", "pandas": pd.__version__, "old_pin": OLD_PIN,
        "synthetic_day": {"rows": len(t.ROWS), "conditional_rows": conditional},
        "old_equals_new_with_string_inference_off": bool(res[("old", False)] == res[("new", False)]),
        "new_inference_on_equals_new_inference_off": bool(res[("new", True)] == res[("new", False)]),
        "old_with_string_inference_on": {"accounts_in_flow": len(res[("old", True)][0]),
                                         "rows_resolved": sum(res[("old", True)][4].get(k, 0) for k in (
                                             "resolved_pair-match", "resolved_same-account-type-transfer",
                                             "resolved_text-counterpart", "external-by-default"))},
        "new_with_string_inference_on": {"accounts_in_flow": len(res[("new", True)][0]),
                                         "rows_resolved": sum(res[("new", True)][4].get(k, 0) for k in (
                                             "resolved_pair-match", "resolved_same-account-type-transfer",
                                             "resolved_text-counterpart", "external-by-default"))},
    }
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
