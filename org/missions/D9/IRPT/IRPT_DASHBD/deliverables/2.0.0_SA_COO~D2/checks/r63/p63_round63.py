"""IRPT_DASHBD round 63 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's R45 refresh 2 half, condition 1 (msg 4126).

Cell: DB-b-119 every reader of account_return_daily's manifest.json named with file and line, the count printed, and for each whether it
accepts a key it does not know. A strict reader is a STOP back to the CTO before the R45 apply.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB63-1-AC1  ~94/RETURNS_MANIFEST_READERS.json: scopes is a non-empty list of {scope, files_scanned (int > 0), patterns}; readers is a
              list of {file, line, how_it_reads, unknown_key in ACCEPTS / STRICT / NOT_ESTABLISHED, evidence}; reader_count equals
              len(readers); every reader's file exists at HEAD when it is inside this repo (in_repo true); verdict is NO_STRICT_READER
              only when no reader is STRICT or NOT_ESTABLISHED, STRICT_READER_FOUND when any is STRICT, else UNDETERMINED.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB63"))
        sys.exit(1)

    if cid != "DB63-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (D + "94/RETURNS_MANIFEST_READERS.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    scopes = r.get("scopes") or []
    if not scopes:
        fail("scopes empty")
    for s in scopes:
        if not s.get("scope") or not isinstance(s.get("files_scanned"), int) or s["files_scanned"] <= 0 or not s.get("patterns"):
            fail("scope %r lacks a name, a positive files_scanned or its patterns" % s.get("scope"))
    readers = r.get("readers")
    if not isinstance(readers, list) or r.get("reader_count") != len(readers):
        fail("reader_count %r against %r reader entries" % (r.get("reader_count"), None if readers is None else len(readers)))
    kinds = []
    for x in readers:
        if x.get("unknown_key") not in ("ACCEPTS", "STRICT", "NOT_ESTABLISHED"):
            fail("reader %r unknown_key %r" % (x.get("file"), x.get("unknown_key")))
        if not isinstance(x.get("line"), int) or not str(x.get("how_it_reads") or "").strip() or not str(x.get("evidence") or "").strip():
            fail("reader %r lacks a line, how_it_reads or evidence" % x.get("file"))
        if x.get("in_repo") is True and not (root / str(x.get("file"))).is_file():
            fail("reader file %r is not at HEAD" % x.get("file"))
        kinds.append(x["unknown_key"])
    want = "STRICT_READER_FOUND" if "STRICT" in kinds else ("UNDETERMINED" if "NOT_ESTABLISHED" in kinds else "NO_STRICT_READER")
    if r.get("verdict") != want:
        fail("verdict %r, the readers give %s" % (r.get("verdict"), want))
    print("OK: %d reader(s) over %d scope(s); verdict %s" % (len(readers), len(scopes), want))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
