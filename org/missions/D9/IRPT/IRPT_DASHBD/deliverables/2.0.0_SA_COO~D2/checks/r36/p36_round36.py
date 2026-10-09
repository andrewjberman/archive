"""IRPT_DASHBD round 36 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-35 ADDENDUM 4 (on ADJUDICATION_v20 @e9d4ac3755) and
PRD v0.8 FWD-11 @e8b44a8379. E1: the 49 Financial R35 activity-and-lot release APPLY under both halves (COO @cbad72eb7b, CTO @75acbfcb50).
E2: Cottonwood's adapter returns from Black Diamond, offline, tied out to BD. E3: Inflection's adapter returns from Orion, offline, lots
NO_LOTS until Eclipse tax lots are shown populated.

Usage: python <this file> <repo_root> <criterion_id>
  DB36-1-AC1  ~47/R35_APPLY_RECORD.json: plan {add 0, change 3, destroy 0}; apply.complete true; readback.code_sha256 equals the HEAD
              source map's deployed_code_sha256 for irpt-49f-reporting-gold-lambda and differs from the rollback anchor; ledger_entry
              names an existing file under org/critical_paths/change_management/. Base: FAIL.
  DB36-1-AC2  the same record's dry_run {duration_ms, max_memory_mb, objects_written, accounts, lots_rows}: objects_written == 0,
              duration_ms < 85% of 900 s (765,000) and max_memory_mb < 85% of 2048 MB (1,740.8); AMENDMENT 1: accounts >= 7,000 and
              lots_rows > 0, so the read sizes the lots stage over the population. Base: FAIL.
  DB36-1-AC3  the same record's first_fire {request_id, how in scheduled|adhoc, a1..a6 each {pass true, value non-empty}} with
              a4.delta == 0. Base: FAIL.
  DB36-<k>-AC1  (k=2 Cottonwood ~48 COT_RETURNS_TIEOUT.json; k=3 Inflection ~49 INF_RETURNS_TIEOUT.json): `source` (the adapter's input
              system) and `comparison_source` (the firm's own reported source, named by the cell's read -- PRD v0.8 @3eb7dbcf36, CVO
              msg 2330) both non-empty strings; accounts int >= 1, denominator int > 0, within int in [0, denominator],
              tolerance_pp == 0.35. Base: FAIL.
  DB36-<k>-AC2  misses: a list of length denominator - within, every entry's class a member of the record's non-empty `classes` list,
              none "UNCLASSED". Base: FAIL.
  DB36-<k>-AC3  output_columns equals the column set of org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json, output_sha256 is
              64-hex, and no .py under the worker folder calls put_object, upload_file, upload_fileobj or copy_object; for k=3 also
              lots_status maps exactly `accounts` accounts, each NO_LOTS or POPULATED. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
ANCHOR = "Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44="
FN = "irpt-49f-reporting-gold-lambda"
FIRM = {"2": ("48", "COT_RETURNS_TIEOUT.json"), "3": ("49", "INF_RETURNS_TIEOUT.json")}
WRITES = re.compile(r"\b(put_object|upload_file|upload_fileobj|copy_object)\s*\(")


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB36"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    m = re.match(r"^DB36-([123])-AC([123])$", cid)
    if not m:
        fail("unknown criterion %r" % cid)
    k, ac = m.group(1), m.group(2)

    if k == "1":
        r = load(P + "0.9.0_WK_IRPT_DASHBD~47/R35_APPLY_RECORD.json")
        if ac == "1":
            pl = r.get("plan") or {}
            if (pl.get("add"), pl.get("change"), pl.get("destroy")) != (0, 3, 0):
                fail("plan %r is not 0/3/0" % pl)
            if (r.get("apply") or {}).get("complete") is not True:
                fail("apply.complete is not true")
            sm = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_bytes().decode("utf-8"))
            want = ((sm.get("functions") or {}).get(FN) or {}).get("deployed_code_sha256")
            got = (r.get("readback") or {}).get("code_sha256")
            if not got or got != want or got == ANCHOR:
                fail("readback %r vs source map %r (must be equal and differ from the anchor %s)" % (got, want, ANCHOR))
            le = str(r.get("ledger_entry") or "")
            if not le.startswith("org/critical_paths/change_management/") or not (root / le).is_file():
                fail("ledger_entry %r is not an existing change_management file" % le)
            print("OK: plan 0/3/0, apply complete, live %s = source map, ledger %s" % (got[:12], le))
        elif ac == "2":
            d = r.get("dry_run") or {}
            if not num(d.get("duration_ms")) or not num(d.get("max_memory_mb")) or d.get("objects_written") != 0:
                fail("dry_run %r" % d)
            # AMENDMENT 1 (issuer, 2026-10-09 ~04:1xZ): the read must SIZE the lots stage -- a dry_run that computed no lots rows
            # (e.g. SOURCE_LAG on the only day) passes the limits vacuously. lots_rows: the lots-stage row count the run logged.
            if not isinstance(d.get("accounts"), int) or d["accounts"] < 7000 or not isinstance(d.get("lots_rows"), int) or d["lots_rows"] <= 0:
                fail("dry_run did not size the lots stage: accounts %r, lots_rows %r (need >= 7,000 accounts and lots_rows > 0)"
                     % (d.get("accounts"), d.get("lots_rows")))
            if d["duration_ms"] >= 765000 or d["max_memory_mb"] >= 1740.8:
                fail("dry_run at or over 85%% of a limit: %s ms, %s MB (a STOP and a row)" % (d["duration_ms"], d["max_memory_mb"]))
            print("OK: dry_run %s ms of 900,000, %s MB of 2,048, 0 objects written" % (d["duration_ms"], d["max_memory_mb"]))
        else:
            f = r.get("first_fire") or {}
            if not f.get("request_id") or f.get("how") not in ("scheduled", "adhoc"):
                fail("first_fire %r" % {a: f.get(a) for a in ("request_id", "how")})
            for a in ("a1", "a2", "a3", "a4", "a5", "a6"):
                x = f.get(a) or {}
                if x.get("pass") is not True or not str(x.get("value") or "").strip():
                    fail("first_fire.%s %r" % (a, x))
            if (f.get("a4") or {}).get("delta") != 0:
                fail("first_fire.a4.delta %r is not 0" % (f.get("a4") or {}).get("delta"))
            print("OK: first fire %s (%s): A1-A6 pass, A4 delta 0" % (f["request_id"], f["how"]))
    else:
        wk, name = FIRM[k]
        rel = P + "0.9.0_WK_IRPT_DASHBD~%s/" % wk
        r = load(rel + name)
        src, cmp_src = r.get("source"), r.get("comparison_source")
        if not str(src or "").strip() or not str(cmp_src or "").strip():
            fail("source %r / comparison_source %r must both be named" % (src, cmp_src))
        a, n, w = r.get("accounts"), r.get("denominator"), r.get("within")
        if ac == "1":
            if not isinstance(a, int) or a < 1 or not isinstance(n, int) or n <= 0 or not isinstance(w, int) or not 0 <= w <= n \
                    or r.get("tolerance_pp") != 0.35:
                fail("accounts %r, denominator %r, within %r, tolerance_pp %r" % (a, n, w, r.get("tolerance_pp")))
            print("OK: %s against %s: %d of %d within 0.35 pp over %d account(s)" % (src, cmp_src, w, n, a))
        elif ac == "2":
            cl, ms = r.get("classes"), r.get("misses")
            if not isinstance(cl, list) or not cl or not isinstance(ms, list) or not isinstance(n, int) or not isinstance(w, int):
                fail("classes %r / misses type %s" % (cl, type(ms).__name__))
            if len(ms) != n - w:
                fail("%d misses listed, %d expected (denominator - within)" % (len(ms), n - w))
            bad = [x for x in ms if not isinstance(x, dict) or x.get("class") not in cl or x.get("class") == "UNCLASSED"]
            if bad:
                fail("%d miss(es) unclassed or outside classes: %r" % (len(bad), bad[:3]))
            print("OK: %d misses, each classed in %r" % (len(ms), cl))
        else:
            con = json.loads((root / "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json").read_bytes().decode("utf-8"))
            want = {c["name"] if isinstance(c, dict) else c for c in con["columns"]}
            got = r.get("output_columns")
            if not isinstance(got, list) or set(got) != want:
                fail("output_columns differ from the contract: missing %r, extra %r" % (sorted(want - set(got or [])), sorted(set(got or []) - want)))
            if not re.fullmatch(r"[0-9a-f]{64}", str(r.get("output_sha256") or "")):
                fail("output_sha256 %r" % r.get("output_sha256"))
            hits = [str(p.relative_to(root)) for p in (root / rel).rglob("*.py") if WRITES.search(p.read_text(encoding="utf-8", errors="replace"))]
            if hits:
                fail("S3 write call in %r" % hits)
            if k == "3":
                ls = r.get("lots_status")
                if not isinstance(ls, dict) or len(ls) != a or any(v not in ("NO_LOTS", "POPULATED") for v in ls.values()):
                    fail("lots_status %r must map %r account(s) to NO_LOTS or POPULATED" % (ls if not isinstance(ls, dict) else len(ls), a))
            print("OK: output carries the contract's %d columns, sha %s..., no S3 write call" % (len(want), r["output_sha256"][:12]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
