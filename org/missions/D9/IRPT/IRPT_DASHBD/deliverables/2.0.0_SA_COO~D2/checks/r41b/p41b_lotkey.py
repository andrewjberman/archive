"""IRPT_DASHBD round 41, lot-key chain (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 10 (msg 3225, row S40 BLOCKING): the
11:41Z R37 fire logged LOTS_SKIPPED 2026-10-08 (a realized lot repeats with the same date, quantity and proceeds). R37 stays live (Branch B).

Cells: DB-b-87 read the 10-08 repeat pairs and decide by the producer's rule (extend the key by the minimal real lot attribute under a rule-24
record, or file a source duplicate -- never dedupe silently), and re-size both kit days with the full lots stage; DB-b-88 the R37 packet delta,
the re-pinned release and the 10-08 lots backfill.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB41b-1-AC1  ~62/LOTS_KEY_R41.json repeat_census {day "2026-10-08", pairs int > 0, per_pair a list of {differing_columns list}} and decision:
               EXTEND_KEY -> new_key strictly extends the current contract key and equals the HEAD contract primary_key, and rule24_record
               names an existing file; SOURCE_DUPLICATE -> every pair's differing_columns is empty and source_row names a row id.
  DB41b-1-AC2  kit_runs for 2026-10-07 and 2026-10-08, each {accounts >= 7000, lots_rows int, peak_mb < 1740.8, total_s < 765}; on
               EXTEND_KEY both days have refusals == 0 and lots_rows > 0; on SOURCE_DUPLICATE 2026-10-08 refuses by name (refusals >= 1).
  DB41b-1-AC3  tests {passed > 0, failed == 0, new_test "<file>::<function>"} with that function defined at HEAD.
  DB41b-2-AC1  ~63/R37_DELTA_RECORD.json plan {0,1,0} or {0,3,0}, apply.complete true, readback.code_sha256 equal to the HEAD source map's
               deployed_code_sha256, delta_packet an existing file naming the new key and 2026-10-08, ledger_entry an existing change_management
               file carrying the delta packet's sha256 prefix.
  DB41b-2-AC2  backfill {day "2026-10-08", lots_skipped 0, realized_rows int > 0, unrealized_rows int > 0, activity_rows int > 0,
               returns_bytes_equal true}.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
CON = "org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json"
CUR = ["firm", "account_id", "business_date", "lot_id", "quantity", "proceeds"]
FN = "irpt-49f-reporting-gold-lambda"


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB41b"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid.startswith("DB41b-1-"):
        r = load(D + "62/LOTS_KEY_R41.json")
        dec = r.get("decision")
        if cid == "DB41b-1-AC1":
            c = r.get("repeat_census") or {}
            pp = c.get("per_pair")
            if c.get("day") != "2026-10-08" or not isinstance(c.get("pairs"), int) or c["pairs"] <= 0 or not isinstance(pp, list) \
                    or len(pp) != c["pairs"] or any(not isinstance(x, dict) or not isinstance(x.get("differing_columns"), list) for x in pp):
                fail("repeat_census %r" % {k: c.get(k) for k in ("day", "pairs")})
            if dec == "EXTEND_KEY":
                nk = r.get("new_key")
                ck = load(CON).get("primary_key")
                if not isinstance(nk, list) or not set(CUR) < set(nk) or ck != nk:
                    fail("new_key %r must strictly extend %r and equal the contract %r" % (nk, CUR, ck))
                if not (root / str(r.get("rule24_record") or "")).is_file():
                    fail("rule24_record %r is not a file" % r.get("rule24_record"))
                print("OK: %d pair(s); key extended to %r (contract equal, rule-24 record present)" % (c["pairs"], nk))
            elif dec == "SOURCE_DUPLICATE":
                if any(x["differing_columns"] for x in pp) or not str(r.get("source_row") or "").startswith("IRPT_DASHBD-"):
                    fail("SOURCE_DUPLICATE needs every pair identical and a source_row id")
                print("OK: %d identical pair(s) filed as a source duplicate (%s); refusal kept" % (c["pairs"], r["source_row"]))
            else:
                fail("decision %r" % dec)
        elif cid == "DB41b-1-AC2":
            kr = r.get("kit_runs") or {}
            for day in ("2026-10-07", "2026-10-08"):
                x = kr.get(day) or {}
                if not isinstance(x.get("accounts"), int) or x["accounts"] < 7000 or not isinstance(x.get("lots_rows"), int) \
                        or not num(x.get("peak_mb")) or x["peak_mb"] >= 1740.8 or not num(x.get("total_s")) or x["total_s"] >= 765 \
                        or not isinstance(x.get("refusals"), int):
                    fail("kit_runs[%s] %r" % (day, x))
            if dec == "EXTEND_KEY" and any(kr[d]["refusals"] != 0 or kr[d]["lots_rows"] <= 0 for d in kr if d in ("2026-10-07", "2026-10-08")):
                fail("EXTEND_KEY needs 0 refusals and lots rows on both days")
            if dec == "SOURCE_DUPLICATE" and kr["2026-10-08"]["refusals"] < 1:
                fail("SOURCE_DUPLICATE: 2026-10-08 must still refuse by name")
            print("OK: kit " + "; ".join("%s %s MB %s s refusals %d" % (d, kr[d]["peak_mb"], kr[d]["total_s"], kr[d]["refusals"]) for d in ("2026-10-07", "2026-10-08")))
        elif cid == "DB41b-1-AC3":
            t = r.get("tests") or {}
            m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(t.get("new_test") or ""))
            if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not m \
                    or not (root / m.group(1)).is_file() or not re.search(r"^def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M):
                fail("tests %r" % t)
            print("OK: tests %d passed, 0 failed; new test %s" % (t["passed"], t["new_test"]))
        else:
            fail("unknown criterion %r" % cid)
    elif cid.startswith("DB41b-2-"):
        r = load(D + "63/R37_DELTA_RECORD.json")
        if cid == "DB41b-2-AC1":
            pl = r.get("plan") or {}
            if (pl.get("add"), pl.get("destroy")) != (0, 0) or pl.get("change") not in (1, 3) or (r.get("apply") or {}).get("complete") is not True:
                fail("plan %r / apply %r" % (pl, r.get("apply")))
            want = ((load("infra/aws/lambda/ci/lambda-source-map.json").get("functions") or {}).get(FN) or {}).get("deployed_code_sha256")
            if (r.get("readback") or {}).get("code_sha256") != want or not want:
                fail("readback %r vs source map %r" % ((r.get("readback") or {}).get("code_sha256"), want))
            dp = root / str(r.get("delta_packet") or "")
            if not dp.is_file() or "2026-10-08" not in dp.read_text(encoding="utf-8"):
                fail("delta_packet %r missing or does not name 2026-10-08" % r.get("delta_packet"))
            import hashlib
            sha = hashlib.sha256(dp.read_bytes()).hexdigest()[:8]
            le = root / str(r.get("ledger_entry") or "")
            if not str(r.get("ledger_entry") or "").startswith("org/critical_paths/change_management/") or not le.is_file() or sha not in le.read_text(encoding="utf-8", errors="replace"):
                fail("ledger_entry %r not pinned to the delta packet (%s)" % (r.get("ledger_entry"), sha))
            print("OK: delta applied %s, live = source map, ledger pinned %s" % (pl, sha))
        elif cid == "DB41b-2-AC2":
            b = r.get("backfill") or {}
            if b.get("day") != "2026-10-08" or b.get("lots_skipped") != 0 or b.get("returns_bytes_equal") is not True \
                    or any(not isinstance(b.get(k), int) or b[k] <= 0 for k in ("realized_rows", "unrealized_rows", "activity_rows")):
                fail("backfill %r" % b)
            print("OK: 2026-10-08 lots backfilled (realized %d, unrealized %d, activity %d), returns byte-equal" % (b["realized_rows"], b["unrealized_rows"], b["activity_rows"]))
        else:
            fail("unknown criterion %r" % cid)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
