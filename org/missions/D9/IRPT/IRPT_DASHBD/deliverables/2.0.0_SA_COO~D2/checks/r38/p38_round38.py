"""IRPT_DASHBD round 38 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-37 ADDENDUM 6 @fb5579ddfc (on ADJUDICATION_v22 @153e101791).

Cells: DB-b-78 the R37 release APPLY under both halves (COO @9395a9c1bc, CTO @e64eb96736); DB-b-79 Orion's gross-of-fees return landed as
silver with its as-of (W53-S1); DB-b-80 the ratified taxonomy gains the four account_boundary keys and the 48 header, the adapter reads them,
the tie-out re-read on both bases from the landed gross (W49-S3, W54-S1); DB-b-81 the fee slices printed with COMPLETE/PARTIAL and their
denominators (W53-S2).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB38-1-AC1  ~55/R37_APPLY_RECORD.json plan {0,3,0}; apply.complete true; readback.code_sha256 equal to the HEAD source map's
              deployed_code_sha256 for irpt-49f-reporting-gold-lambda and not the anchor; ledger_entry an existing change_management file
              whose text carries the R37 packet sha256 prefix 848dd864 (the pinned ledger).
  DB38-1-AC2  dry_run {accounts >= 7000, lots_rows > 0, objects_written == 0, duration_ms <= 765000, max_memory_mb <= 1740.8}.
  DB38-1-AC3  first_fire {request_id, how scheduled|adhoc, a1..a7 each {pass true, value non-empty}, a4.delta == 0, a7.members == 18}.
  DB38-2-AC1  ~57/ORION_GROSS_SILVER.json address starting "s3://" and containing "/silver/", as_of non-empty, rows int > 0, objects int > 0,
              columns a list naming a gross return column (a name containing "gross").
  DB38-2-AC2  the record's builder_call names lib/opal_naming address( and its printed output equals address.
  DB38-3-AC1  data/inf/scripts/silver/orion_cashflow_taxonomy.yaml: Internal Account Journal In account_boundary "in"; Internal Account
              Journal Out "out"; Federal and State Tax Withheld "out" with account_boundary_when "before_tax_return"; no other entry
              carries account_boundary; schema_collapse_audit.total_type_desc_entries_v2 == len(types) == 48.
  DB38-3-AC2  ~56: the adapter's orion_sources.json carries no inter_account_comment / tax_withheld_comment, and a .py in ~56 reads
              "account_boundary" and names orion_cashflow_taxonomy.yaml.
  DB38-3-AC3  ~56/INF_TIEOUT_R38.json gross {denominator int > 0, within int in range} and net {same}, gross_source starting "s3://"
              (the landed silver, never a live pull) with as_of.
  DB38-4-AC1  ~58/INF_FEE_SLICES_R38.json slices: the six keys, each {value number, readable int, denominator int > 0, status} with
              status "PARTIAL" iff readable < denominator, else "COMPLETE".
  DB38-4-AC2  the record prints a one-line `statement` per PARTIAL slice naming readable of denominator.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
ANCHOR = "Mex71Y5gk9RYE9q885knj3Ph12xV2Y9eVqMl3uJ1Z44="
FN = "irpt-49f-reporting-gold-lambda"
SLICES = ["supervised", "unsupervised", "supervision_total", "billed", "unbilled", "billing_total"]


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB38"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def bases(r):
        for b in ("gross", "net"):
            x = r.get(b) or {}
            n, w = x.get("denominator"), x.get("within")
            if not isinstance(n, int) or n <= 0 or not isinstance(w, int) or not 0 <= w <= n:
                fail("%s %r" % (b, x))
        return r["gross"], r["net"]

    if cid.startswith("DB38-1-"):
        r = load(D + "55/R37_APPLY_RECORD.json")
        if cid == "DB38-1-AC1":
            pl = r.get("plan") or {}
            if (pl.get("add"), pl.get("change"), pl.get("destroy")) != (0, 3, 0) or (r.get("apply") or {}).get("complete") is not True:
                fail("plan %r / apply %r" % (pl, r.get("apply")))
            sm = load("infra/aws/lambda/ci/lambda-source-map.json")
            want = ((sm.get("functions") or {}).get(FN) or {}).get("deployed_code_sha256")
            got = (r.get("readback") or {}).get("code_sha256")
            if not got or got != want or got == ANCHOR:
                fail("readback %r vs source map %r (equal, and not the anchor)" % (got, want))
            le = str(r.get("ledger_entry") or "")
            p = root / le
            if not le.startswith("org/critical_paths/change_management/") or not p.is_file() or "848dd864" not in p.read_bytes().decode("utf-8", "replace"):
                fail("ledger_entry %r missing, or not pinned to the R37 packet (848dd864)" % le)
            print("OK: 0/3/0 applied, live %s = source map, ledger pinned %s" % (got[:12], le))
        elif cid == "DB38-1-AC2":
            d = r.get("dry_run") or {}
            if not isinstance(d.get("accounts"), int) or d["accounts"] < 7000 or not isinstance(d.get("lots_rows"), int) or d["lots_rows"] <= 0 \
                    or d.get("objects_written") != 0 or not num(d.get("duration_ms")) or not num(d.get("max_memory_mb")):
                fail("dry_run %r" % {k: d.get(k) for k in ("accounts", "lots_rows", "objects_written", "duration_ms", "max_memory_mb")})
            if d["duration_ms"] > 765000 or d["max_memory_mb"] > 1740.8:
                fail("dry_run over the 85%% line: %s ms, %s MB (roll back before 11:41Z)" % (d["duration_ms"], d["max_memory_mb"]))
            print("OK: dry_run %d accounts, lots_rows %d, %s ms, %s MB, 0 written" % (d["accounts"], d["lots_rows"], d["duration_ms"], d["max_memory_mb"]))
        elif cid == "DB38-1-AC3":
            f = r.get("first_fire") or {}
            if not f.get("request_id") or f.get("how") not in ("scheduled", "adhoc"):
                fail("first_fire %r" % {k: f.get(k) for k in ("request_id", "how")})
            for a in ("a1", "a2", "a3", "a4", "a5", "a6", "a7"):
                x = f.get(a) or {}
                if x.get("pass") is not True or not str(x.get("value") or "").strip():
                    fail("first_fire.%s %r" % (a, x))
            if (f.get("a4") or {}).get("delta") != 0 or (f.get("a7") or {}).get("members") != 18:
                fail("a4.delta %r / a7.members %r" % ((f.get("a4") or {}).get("delta"), (f.get("a7") or {}).get("members")))
            print("OK: first fire %s (%s): A1-A7 pass, A4 delta 0, A7 18 member hashes" % (f["request_id"], f["how"]))
        else:
            fail("unknown criterion %r" % cid)
    elif cid.startswith("DB38-2-"):
        r = load(D + "57/ORION_GROSS_SILVER.json")
        a = str(r.get("address") or "")
        if cid == "DB38-2-AC1":
            cols = r.get("columns")
            if not a.startswith("s3://") or "/silver/" not in a or not str(r.get("as_of") or "").strip() or not isinstance(r.get("rows"), int) \
                    or r["rows"] <= 0 or not isinstance(r.get("objects"), int) or r["objects"] <= 0 or not isinstance(cols, list) \
                    or not any("gross" in str(c).lower() for c in cols):
                fail("record %r" % {k: r.get(k) for k in ("address", "as_of", "rows", "objects", "columns")})
            print("OK: %d rows in %d object(s) at %s, as_of %s" % (r["rows"], r["objects"], a, r["as_of"]))
        elif cid == "DB38-2-AC2":
            bc = r.get("builder_call") or {}
            if "address(" not in str(bc.get("call") or "") or bc.get("output") != a:
                fail("builder_call %r does not print the address %r" % (bc, a))
            print("OK: address is builder output: %s" % bc["call"])
        else:
            fail("unknown criterion %r" % cid)
    elif cid.startswith("DB38-3-"):
        if cid == "DB38-3-AC1":
            import yaml
            p = root / "data/inf/scripts/silver/orion_cashflow_taxonomy.yaml"
            y = yaml.safe_load(p.read_bytes().decode("utf-8"))
            types = y.get("types") or []
            want = {"Internal Account Journal In": ("in", None), "Internal Account Journal Out": ("out", None),
                    "Federal Tax Withheld": ("out", "before_tax_return"), "State Tax Withheld": ("out", "before_tax_return")}
            got = {t["type_desc"]: (t.get("account_boundary"), t.get("account_boundary_when")) for t in types if "account_boundary" in t}
            if got != want:
                fail("account_boundary entries %r != %r" % (got, want))
            n = (y.get("schema_collapse_audit") or {}).get("total_type_desc_entries_v2")
            if len(types) != 48 or n != 48:
                fail("types %d, header total_type_desc_entries_v2 %r (both 48)" % (len(types), n))
            print("OK: 4 entries carry account_boundary as adopted; 48 types, header 48")
        elif cid == "DB38-3-AC2":
            s = load(D + "56/orion_sources.json")
            txt = json.dumps(s)
            if "inter_account_comment" in txt or "tax_withheld_comment" in txt:
                fail("orion_sources.json still carries the departure comments")
            hit = [str(q.relative_to(root)) for q in (root / (D + "56")).rglob("*.py")
                   if "account_boundary" in q.read_text(encoding="utf-8", errors="replace") and "orion_cashflow_taxonomy.yaml" in q.read_text(encoding="utf-8", errors="replace")]
            if not hit:
                fail("no adapter .py in ~56 reads account_boundary from orion_cashflow_taxonomy.yaml")
            print("OK: departure removed; %s reads the ratified keys" % hit[0])
        elif cid == "DB38-3-AC3":
            r = load(D + "56/INF_TIEOUT_R38.json")
            g, n = bases(r)
            if not str(r.get("gross_source") or "").startswith("s3://") or not str(r.get("as_of") or "").strip():
                fail("gross_source %r / as_of %r (the landed silver)" % (r.get("gross_source"), r.get("as_of")))
            print("OK: gross %d of %d, net %d of %d, gross from %s as of %s" % (g["within"], g["denominator"], n["within"], n["denominator"], r["gross_source"], r["as_of"]))
        else:
            fail("unknown criterion %r" % cid)
    elif cid.startswith("DB38-4-"):
        r = load(D + "58/INF_FEE_SLICES_R38.json")
        sl = r.get("slices") or {}
        bad = []
        for k in SLICES:
            x = sl.get(k) or {}
            ok = num(x.get("value")) and isinstance(x.get("readable"), int) and isinstance(x.get("denominator"), int) and x["denominator"] > 0
            if not ok or x.get("status") != ("PARTIAL" if x["readable"] < x["denominator"] else "COMPLETE"):
                bad.append(k)
        if bad:
            fail("slices not {value, readable, denominator, status by rule}: %r" % bad)
        partial = [k for k in SLICES if sl[k]["status"] == "PARTIAL"]
        if cid == "DB38-4-AC1":
            print("OK: 6 slices; PARTIAL %r" % partial)
        elif cid == "DB38-4-AC2":
            st = r.get("statement") or {}
            miss = [k for k in partial if not re.search(r"\b%d\b.*\b%d\b" % (sl[k]["readable"], sl[k]["denominator"]), str(st.get(k) or ""))]
            if miss:
                fail("PARTIAL slice(s) without a statement naming readable of denominator: %r" % miss)
            print("OK: %d PARTIAL slice(s) stated with their denominators" % len(partial))
        else:
            fail("unknown criterion %r" % cid)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
