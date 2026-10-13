"""IRPT_BCKEND round 180 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB180-1  IB-pr-514  READ-ONLY, counts only: the latest served 49 Financial HoldingsSnapshot built on the new package carries account_id on its ACCOUNT nodes (CTO RE 7016, round 180 item 1)
    AC1  the counts' arithmetic, and the positive snapshot was written in the 14:15Z build's window while the negative arm was written before the package was put
    AC2  the record carries no account content (no id, no mask, no long digit run) and no key beyond the revision names
    AC3  the CTO's reading: some ACCOUNT nodes carry account_id, every one is in the landed directory population, the pre-release snapshot reads 0, and nothing was written
"""
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
REC = PROJ + "deliverables/0.9.0_WK_IRPT_BCKEND~364/IB180-1_served_account_id_read.json"
BUILD_START = "2026-10-13T14:15:25Z"
BUILD_END_LATEST = "2026-10-13T14:30:00Z"
PUT_TIME = "2026-10-13T13:35:24Z"
BOUND_ZERO = ("aws_writes_made", "objects_uploaded", "functions_invoked", "hosts_started", "accounts_written", "figures_written", "files_deleted")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB180"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell != "IB180-1":
        fail("unknown criterion %r" % CID)
    r = load(REC)
    pos = r.get("positive") or {}
    neg = r.get("negative_arm") or {}
    if arm == "AC1":
        for k in ("account_nodes_total", "with_account_id", "in_directory_population"):
            if not is_int(pos.get(k)) or pos[k] < 0:
                fail("positive.%s must be an integer >= 0" % k)
        wo = pos.get("without_account_id") or {}
        if not is_int(wo.get("total")) or wo["total"] < 0:
            fail("positive.without_account_id.total must be an integer >= 0")
        if pos["with_account_id"] + wo["total"] != pos["account_nodes_total"]:
            fail("with_account_id + without_account_id.total must equal account_nodes_total")
        if pos["in_directory_population"] > pos["with_account_id"]:
            fail("in_directory_population cannot exceed with_account_id")
        br = wo.get("by_reason") or {}
        if sum(v for v in br.values() if is_int(v)) != wo["total"] or not all(is_int(v) and v >= 0 for v in br.values()):
            fail("without_account_id.by_reason must hold integer counts summing to the total")
        lm = str(pos.get("last_modified_utc", ""))
        if not (BUILD_START <= lm <= BUILD_END_LATEST):
            fail("the positive snapshot's last_modified_utc %r must fall in the 14:15Z build's window [%s, %s]" % (lm, BUILD_START, BUILD_END_LATEST))
        if not is_int(neg.get("account_nodes_total")) or neg["account_nodes_total"] <= 0 or not str(neg.get("last_modified_utc", "")).strip() or str(neg["last_modified_utc"]) >= PUT_TIME:
            fail("the negative arm needs a positive node total and a last_modified_utc before the package was put (%s)" % PUT_TIME)
        print("OK: %d ACCOUNT nodes: %d with account_id, %d without" % (pos["account_nodes_total"], pos["with_account_id"], wo["total"]))
    elif arm == "AC2":
        raw = json.dumps(r)
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", raw):
            fail("the record carries a long digit run")
        for bad in ("account_number", "masks", "\"account_ids\"", "node_id"):
            if bad in raw:
                fail("the record carries a forbidden key or word: %s" % bad)
        print("OK: the record carries counts and revision names only")
    elif arm == "AC3":
        if pos.get("with_account_id", 0) <= 0:
            fail("some ACCOUNT nodes must carry account_id after the release (reads %r): this is the finding if it is 0" % pos.get("with_account_id"))
        if pos.get("in_directory_population") != pos.get("with_account_id"):
            fail("every account_id written must be in the landed directory population (%r of %r)" % (pos.get("in_directory_population"), pos.get("with_account_id")))
        if neg.get("with_account_id") != 0:
            fail("the pre-release snapshot must read 0 with account_id (the negative arm), reads %r" % neg.get("with_account_id"))
        for k in BOUND_ZERO:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: the release writes account_id, all of it in the directory; the pre-release snapshot has none")
    else:
        fail("unknown criterion")
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
