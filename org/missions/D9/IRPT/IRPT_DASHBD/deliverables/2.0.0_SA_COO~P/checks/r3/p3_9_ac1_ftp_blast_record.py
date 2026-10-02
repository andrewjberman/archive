"""DB-9-AC1 -- every reader of the shared Schwab code table is found, and the foreign-tax move's served delta is measured
per reader; the adapter's override retirement exists as a patch that applies cleanly at HEAD.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/FTP_INTERNAL_BLAST_R3.json:
  {"codes": ["FTP/FC/WD", "FTR/FC/WD"], "table": "<path of the CRO's file>", "files_scanned": n,
   "readers": [{"path", "firm", "served": true|false}],
   "per_reader_delta": [{"path", "firm", "rows": n, "abs_usd": x, "net_usd": x, "partitions": n}],
   "adapter_override_patch": "<repo-relative path of a .patch>"}
Grades: both codes named; files_scanned > 0; the readers include data/assets/scripts/gold/runners_49f/a05_ref_txn_classification.py;
every served reader has a per_reader_delta row with integer rows and numeric dollars; the patch file exists and
`git apply --check` accepts it at the repo root. Usage: python <this file> <repo_root>
"""
import json
import subprocess
import sys
from pathlib import Path

ENGINE_49F = "data/assets/scripts/gold/runners_49f/a05_ref_txn_classification.py"


def fail(msg):
    print("FAIL: " + msg)
    print("DB-9-AC1 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/FTP_INTERNAL_BLAST_R3.json"
    if not p.is_file():
        fail("no record at %s" % p)
    r = json.loads(p.read_text(encoding="utf-8"))
    if set(r.get("codes") or []) != {"FTP/FC/WD", "FTR/FC/WD"}:
        fail("codes %r" % r.get("codes"))
    if int(r.get("files_scanned") or 0) <= 0:
        fail("files_scanned is not positive")
    readers = r.get("readers") or []
    paths = [str(x.get("path", "")).replace("\\", "/") for x in readers]
    if ENGINE_49F not in paths:
        fail("the 49F engine %s is not among the readers" % ENGINE_49F)
    deltas = {str(d.get("path", "")).replace("\\", "/"): d for d in (r.get("per_reader_delta") or [])}
    served = [x for x in readers if x.get("served") is True]
    for x in served:
        d = deltas.get(str(x["path"]).replace("\\", "/"))
        if d is None:
            fail("served reader %s has no per_reader_delta row" % x["path"])
        if not isinstance(d.get("rows"), int):
            fail("rows for %s is not an integer" % x["path"])
        for k in ("abs_usd", "net_usd"):
            if not isinstance(d.get(k), (int, float)):
                fail("%s for %s is not numeric" % (k, x["path"]))
    patch = root / str(r.get("adapter_override_patch") or "")
    if not patch.is_file():
        fail("no patch at %s" % patch)
    rc = subprocess.run(["git", "apply", "--check", str(patch)], cwd=str(root), capture_output=True, text=True)
    if rc.returncode != 0:
        fail("git apply --check refused the patch: %s" % (rc.stderr or rc.stdout).strip()[:300])
    print("OK: %d reader(s) of %d file(s) scanned, %d served with a delta row; patch applies at HEAD" % (
        len(readers), int(r["files_scanned"]), len(served)))
    print("DB-9-AC1 PASS")


if __name__ == "__main__":
    main()
