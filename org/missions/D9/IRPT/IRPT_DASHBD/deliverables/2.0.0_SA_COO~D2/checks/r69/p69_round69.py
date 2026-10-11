"""IRPT_DASHBD round 69 (issuer 2.0.0_SA_COO~D2) -- the APPLY of the signed pair on DB-b-128's packet (sha256 6fbce1ff...d064; COO half
@34cc62f4f7, CTO half @34a6a32212), by 0.7.0_AE_CloudOps~CB2.

Cell: DB-b-130 one overwrite of exactly two keys (Cottonwood dim_return_method, method_version=3) so the served income reason is worded for
the method. Capture first; the ETags read as the packet lists or the act stops; column diff; ledger opened before the write, closed after.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB69-1-AC1  the applier's METHOD_ROW3_REASON_APPLY.json: branch is A_WRITTEN or B_STOPPED; capture.keys holds exactly the two keys, each
              {key, sha256 (64 hex), size, etag, saved_path outside the repo}; capture.bucket_versioning stated; capture.etags_as_listed a
              bool and, on A_WRITTEN, true; ledger {slug, entry (an existing change_management file), opened_before_write true}.
  DB69-1-AC2  A_WRITTEN: diff.columns_changed == [income_basis_reason]; diff.other_columns_moved == 0 (measured_at excluded); served_after
              (read from the SERVED object after the write) has income_basis None, income_basis_claim "absent", income_basis_reason equal
              to the signed sentence, method_version 3; head_after lists both keys; keys_written == the two keys; rolled_back false;
              mint_verify contains "method_row=match"; ledger.closed true.
              B_STOPPED: s3_writes == 0, stop_reason non-empty, a row id, and ledger.closed true.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.7.0_AE_CloudOps~CB2/"
SENTENCE = ("A positions-based method values the account from its positions and cash, so income is inside that value and is"
            " not separated from it: the method states no income basis.")
PFX = "irpt/cottonwood/gold/dim_return_method/method_version=3/"
KEYS = sorted([PFX + "data.parquet", PFX + "manifest.json"])
LISTED = {PFX + "data.parquet": "9c774f3770e82ed5e7e6b2a4ebe3e7d3", PFX + "manifest.json": "6d5aabdd1e0f3cc9ff2a6c544bd327fd"}
SHA = re.compile(r"^[0-9a-f]{64}$")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB69"))
        sys.exit(1)

    p = root / (D + "METHOD_ROW3_REASON_APPLY.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    branch = r.get("branch")
    if branch not in ("A_WRITTEN", "B_STOPPED"):
        fail("branch %r" % branch)
    led = r.get("ledger") or {}
    if cid == "DB69-1-AC1":
        cap = r.get("capture") or {}
        ks = cap.get("keys") or []
        if sorted(str(k.get("key")) for k in ks) != KEYS:
            fail("capture.keys %r, want exactly %r" % (sorted(str(k.get("key")) for k in ks), KEYS))
        for k in ks:
            sp = str(k.get("saved_path") or "")
            if not SHA.match(str(k.get("sha256") or "")) or not isinstance(k.get("size"), int) or not str(k.get("etag") or "").strip() or not sp:
                fail("capture of %s lacks sha256, size, etag or saved_path" % k.get("key"))
            if str(root).replace("\\", "/").lower() in sp.replace("\\", "/").lower() or sp.replace("\\", "/").startswith("org/"):
                fail("the capture of %s is saved inside the repo" % k.get("key"))
        if not str(cap.get("bucket_versioning") or "").strip() or not isinstance(cap.get("etags_as_listed"), bool):
            fail("capture lacks bucket_versioning or etags_as_listed")
        if branch == "A_WRITTEN":
            if cap["etags_as_listed"] is not True or any(str(k["etag"]).strip('"') != LISTED[k["key"]] for k in ks):
                fail("A_WRITTEN with ETags that are not the packet's")
        entry = root / str(led.get("entry") or "")
        if not str(led.get("slug") or "").strip() or not str(led.get("entry") or "").startswith("org/critical_paths/change_management/") \
                or not entry.is_file() or led.get("opened_before_write") is not True:
            fail("ledger %r" % led)
        print("OK: both keys captured outside the repo with their hashes; bucket versioning %s; ledger %s opened before the write; branch %s"
              % (cap["bucket_versioning"], led["slug"], branch))
    elif cid == "DB69-1-AC2":
        if led.get("closed") is not True:
            fail("the ledger entry is not closed")
        if branch == "B_STOPPED":
            if r.get("s3_writes") != 0 or not str(r.get("stop_reason") or "").strip() or not str(r.get("row") or "").strip():
                fail("B_STOPPED wants s3_writes 0, a stop_reason and a row id")
            print("OK: the act stopped before the write (%s); nothing written" % str(r["stop_reason"])[:80])
        else:
            d = r.get("diff") or {}
            if sorted(d.get("columns_changed") or []) != ["income_basis_reason"] or d.get("other_columns_moved") != 0:
                fail("diff %r" % d)
            s = r.get("served_after") or {}
            if "income_basis" not in s or s["income_basis"] is not None or s.get("income_basis_claim") != "absent" \
                    or s.get("income_basis_reason") != SENTENCE or s.get("method_version") != 3:
                fail("served_after %r" % {k: s.get(k) for k in ("method_version", "income_basis", "income_basis_claim", "income_basis_reason")})
            if sorted(str(k.get("key")) for k in (r.get("head_after") or [])) != KEYS or sorted(r.get("keys_written") or []) != KEYS:
                fail("head_after or keys_written is not exactly the two keys")
            if r.get("rolled_back") is not False or "method_row=match" not in str(r.get("mint_verify") or ""):
                fail("rolled_back %r, mint_verify %r" % (r.get("rolled_back"), str(r.get("mint_verify"))[:80]))
            print("OK: two keys written; the income reason changed and no other column; the served row states the signed sentence; the mint's verify still matches; ledger closed")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
