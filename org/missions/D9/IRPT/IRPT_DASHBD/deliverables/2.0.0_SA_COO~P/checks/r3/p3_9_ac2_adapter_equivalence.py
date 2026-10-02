"""DB-9-AC2 -- the adapter's output does not move when its override retires TOGETHER with the table edit.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/FTP_ADAPTER_EQUIVALENCE_R3.json:
  {"partitions": n, "accounts": n, "withholding_rows": n, "max_abs_diff_external_flow": x, "max_abs_diff_total_return_daily": x,
   "runs": [{"label": "today", "code": "<commit>", "table": "<sha256 of the table read>"},
            {"label": "after", "code": "<patched>", "table": "<sha256 of the edited table>"}]}
Grades: partitions >= 20 and accounts > 0 and withholding_rows > 0 (the comparison crosses rows the move touches);
two runs labelled today/after whose table hashes differ; both max_abs_diff fields are exactly 0.
Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path


def fail(msg):
    print("FAIL: " + msg)
    print("DB-9-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/FTP_ADAPTER_EQUIVALENCE_R3.json"
    if not p.is_file():
        fail("no record at %s" % p)
    r = json.loads(p.read_text(encoding="utf-8"))
    if int(r.get("partitions") or 0) < 20:
        fail("partitions %r < 20" % r.get("partitions"))
    if int(r.get("accounts") or 0) <= 0 or int(r.get("withholding_rows") or 0) <= 0:
        fail("accounts or withholding_rows not positive")
    runs = {x.get("label"): x for x in (r.get("runs") or [])}
    if set(runs) != {"today", "after"}:
        fail("runs %r, need today and after" % sorted(runs))
    if runs["today"].get("table") == runs["after"].get("table"):
        fail("the two runs read the same table bytes")
    for k in ("max_abs_diff_external_flow", "max_abs_diff_total_return_daily"):
        if r.get(k) != 0 and r.get(k) != 0.0:
            fail("%s = %r, not 0" % (k, r.get(k)))
    print("OK: %d partitions, %d accounts, %d withholding rows, 0 difference" % (
        int(r["partitions"]), int(r["accounts"]), int(r["withholding_rows"])))
    print("DB-9-AC2 PASS")


if __name__ == "__main__":
    main()
