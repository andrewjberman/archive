"""EN-b-42 round 9 -- the worker's OWN re-measurement of the stale remediation backlog.

CALLS the gate's own limb (never re-derives it): srg._stale_open_row(
    srg._remediation_rows_for_project(root, "LGIC_ENFORCE")[0], current_round, srg.STALE_OPEN_ROW_N_ROUNDS)

Both census reads return a TUPLE (value, note); each is unpacked explicitly and every intermediate
denominator is printed, because a bare-list unpack of `_remediation_ids_for_project` once produced a
plausible `109 rowless of 109`.

Usage: python measure_stale_r9.py <current_round:int> [--json <out>]
Reads the INDEX of the checkout it runs in (the gate's own read), never the worktree bytes.
Read-only: writes nothing unless --json is given.
"""

import importlib.util
import io
import json
import os
import subprocess
import sys


def load_gate(root):
    path = os.path.join(root, ".tools", "surprise-row-gate.py")
    spec = importlib.util.spec_from_file_location("srg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) < 2:
        print("usage: measure_stale_r9.py <current_round> [--json <out>]")
        return 2
    current_round = int(sys.argv[1])
    out_path = None
    if "--json" in sys.argv:
        out_path = sys.argv[sys.argv.index("--json") + 1]
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    srg = load_gate(root)

    ids, inote = srg._remediation_ids_for_project(root, "LGIC_ENFORCE")
    rows_by_id, rnote = srg._remediation_rows_for_project(root, "LGIC_ENFORCE")
    if ids is None or rows_by_id is None:
        print("ERROR: census could not run: ids-note=%r rows-note=%r" % (inote, rnote))
        return 1
    n = srg.STALE_OPEN_ROW_N_ROUNDS
    stale = srg._stale_open_row(rows_by_id, current_round, n)
    if stale is None:
        print("ERROR: _stale_open_row returned None (could not check)")
        return 1
    print("root: %s  HEAD: %s" % (root, head))
    print("intermediate: ids_from_tuple=%d  rows=%d  (key sets equal: %s)"
          % (len(ids), len(rows_by_id), set(ids) == set(rows_by_id)))
    print("current_round=%d  N_ROUNDS=%d  remediation_rows=%d  stale=%d"
          % (current_round, n, len(rows_by_id), len(stale)))
    detail = []
    for rid in stale:
        rem = rows_by_id[rid].get("remediation") or {}
        detail.append({"id": rid, "owner_on_row": rem.get("owner"), "round_on_row": rem.get("round"),
                       "state": rem.get("state"),
                       "item": rows_by_id[rid].get("item") or rows_by_id[rid].get("remediates"),
                       "keys": sorted(rows_by_id[rid].keys())})
    if out_path:
        with io.open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"head": head, "current_round": current_round, "N_ROUNDS": n,
                       "ids_from_tuple": len(ids), "rows": len(rows_by_id), "stale": len(stale),
                       "stale_rows": detail}, fh, indent=1, ensure_ascii=True)
            fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
