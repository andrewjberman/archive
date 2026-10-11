"""IRPT_DASHBD round 64 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4143 on row IRPT_DASHBD-D2-W93-S3.

Cell: DB-b-120 the dim_return_method contract lists method row 3, and tieout_tolerance_proposed takes the same claim as the five thresholds
(typed, never a bare null). One LOCAL cell before ADVI_COTBKF's Cottonwood mint.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB64-1-AC1  the contract reads contract_version 0.5.0 with a self-consistent schema_hash; method_versions lists row 3 and its
              valuation_source equals the producer's METHOD_ROWS[3]; the contract's column names equal the keys of the row
              emit_method_row returns (upload=False) for five absent thresholds and no tieout on the declared 49F entry; that row's
              tieout_tolerance_proposed is None with tieout_tolerance_proposed_claim == "absent"; table_schema types
              tieout_tolerance_proposed as the contract does, never null; and a tieout value with no stated claim reads "held".
  DB64-1-AC2  ~95/ROW3_AND_TIEOUT_CLAIM.json: rule24 {mece, same_grain, intent_coherence, state_coherence}, each with a finding and
              evidence [{file, line}] resolving at HEAD; tests {passed > 0, failed == 0, new_test}; the new test file passes under pytest.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
CONTRACT = "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
SOURCES = "data/assets/scripts/gold/irpt_reporting/sources.json"
KEYS = ("tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight")
POSTULATES = {"mece", "same_grain", "intent_coherence", "state_coherence"}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB64"))
        sys.exit(1)

    if cid == "DB64-1-AC1":
        c = json.loads((root / CONTRACT).read_bytes().decode("utf-8"))
        if c.get("contract_version") != "0.5.0":
            fail("contract_version %r, want 0.5.0" % c.get("contract_version"))
        cols = c.get("columns") or []
        names = [x.get("name") for x in cols]
        ctype = {x.get("name"): x.get("type") for x in cols}
        lines = sorted("%s:%s" % (x.get("name"), x.get("type")) for x in cols)
        if hashlib.sha256(chr(10).join(lines).encode("utf-8")).hexdigest() != c.get("schema_hash"):
            fail("schema_hash does not equal sha256 over the contract's own sorted name:type lines")
        sys.path.insert(0, str(root))
        sys.path.insert(0, str((root / PRODUCER).parent))
        spec = importlib.util.spec_from_file_location("ard_under_check", str(root / PRODUCER))
        ard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ard)
        mv3 = [m for m in (c.get("method_versions") or []) if m.get("method_version") == 3]
        if len(mv3) != 1 or mv3[0].get("valuation_source") != ard.METHOD_ROWS[3]["valuation_source"]:
            fail("method_versions does not list row 3 with the producer's valuation_source %r" % ard.METHOD_ROWS[3]["valuation_source"])
        src = json.loads((root / SOURCES).read_bytes().decode("utf-8"))
        entry = [v for k, v in src.items() if not k.startswith("_") and isinstance(v, dict)][0]
        th = {k: None for k in KEYS}
        th["threshold_claims"] = {k: "absent" for k in KEYS}
        res = ard.emit_method_row(None, ard.firm_scope(entry), th, upload=False, src=entry)
        row, tab = res["row"], res.get("table_schema") or {}
        if sorted(row) != sorted(names):
            fail("row keys and contract columns differ: only in row %r, only in contract %r"
                 % (sorted(set(row) - set(names)), sorted(set(names) - set(row))))
        if row.get("tieout_tolerance_proposed") is not None or row.get("tieout_tolerance_proposed_claim") != "absent":
            fail("no tieout: value %r, claim %r (want None and absent)" % (row.get("tieout_tolerance_proposed"), row.get("tieout_tolerance_proposed_claim")))
        if tab.get("tieout_tolerance_proposed") in (None, "null") or tab.get("tieout_tolerance_proposed") != ctype.get("tieout_tolerance_proposed"):
            fail("tieout_tolerance_proposed arrow type %r, the contract says %r" % (tab.get("tieout_tolerance_proposed"), ctype.get("tieout_tolerance_proposed")))
        res2 = ard.emit_method_row(None, ard.firm_scope(entry), th, upload=False, src=entry, tieout=0.037)
        if res2["row"].get("tieout_tolerance_proposed_claim") != "held":
            fail("a tieout value with no stated claim reads %r, want held" % res2["row"].get("tieout_tolerance_proposed_claim"))
        print("OK: contract 0.5.0 lists row 3; its %d columns equal the row's keys; the tie-out carries its claim and is typed" % len(names))
    elif cid == "DB64-1-AC2":
        p = root / (D + "95/ROW3_AND_TIEOUT_CLAIM.json")
        if not p.is_file():
            fail("no record")
        r = json.loads(p.read_bytes().decode("utf-8"))
        ps = r.get("rule24") or {}
        if set(ps) != POSTULATES:
            fail("rule24 %r" % sorted(ps))
        for k in sorted(ps):
            ev = ps[k].get("evidence") or []
            if not str(ps[k].get("finding") or "").strip() or not ev:
                fail("postulate %s lacks a finding or evidence" % k)
            for e in ev:
                if not (root / str(e.get("file") or "")).is_file() or not isinstance(e.get("line"), int):
                    fail("postulate %s evidence %r does not name a file and line" % (k, e))
        t = r.get("tests") or {}
        nt = str(t.get("new_test") or "").split("::")[0]
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not nt or not (root / nt).is_file():
            fail("tests %r" % t)
        if subprocess.run([sys.executable, "-m", "pytest", nt, "-q"], cwd=str(root), capture_output=True).returncode != 0:
            fail("pytest %s did not exit 0" % nt)
        print("OK: rule-24 record present; %s passes" % nt)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
