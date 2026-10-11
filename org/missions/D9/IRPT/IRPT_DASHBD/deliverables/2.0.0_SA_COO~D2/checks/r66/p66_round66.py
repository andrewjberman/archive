"""IRPT_DASHBD round 66 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4634.

Cell: DB-b-122 method row 3 states income ABSENT by design with its reason; row 2 is unchanged and a test shows it; contract 0.6.0;
rule-24 record first; and the never-widen PACKET for rewriting the one served method-row object (no S3 write in this cell).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB66-1-AC1  emit_method_row (upload=False), five absent thresholds, per declared source entry: the entry naming method row 3 returns
              income_basis None, income_basis_claim "absent" and a non-empty income_basis_reason; the entry naming row 2 returns
              income_basis "cash_when_received" with a claim in the producer's THRESHOLD_CLAIMS other than "absent"; both rows hold
              every one of the 29 columns the contract listed at 0.5.0; table_schema types income_basis as string, never null.
  DB66-1-AC2  the contract reads contract_version 0.6.0 with a self-consistent schema_hash; its column names equal the row's keys;
              income_basis is nullable there; and ~97/METHOD_ROW3_INCOME.json carries rule24 {mece, same_grain, intent_coherence,
              state_coherence}, each with a finding and evidence [{file, line}], token_census non-empty, and tests {passed > 0,
              failed == 0, new_test} whose file passes under pytest.
  DB66-1-AC3  ~97/NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME.md exists and the record's packet {path, sha256, object_address,
              writers_counted (int >= 1), readers_counted (int >= 0), rollback} agrees: sha256 is the file's, object_address equals the
              address the dry run returns for the row-3 entry, rollback non-empty; and s3_writes == 0.
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
COLS_050 = (
    "method_version", "method", "flow_convention", "income_basis", "value_basis", "value_basis_ruling", "fee_basis", "tolerance",
    "large_flow_share", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight", "tolerance_claim",
    "large_flow_share_claim", "plausibility_band_low_claim", "plausibility_band_high_claim",
    "comparability_max_excluded_weight_claim", "threshold_claims_source", "guard_substitution", "day_count",
    "tieout_tolerance_proposed", "tieout_tolerance_proposed_claim", "tieout_tolerance", "tieout_tolerance_ruling", "gips_alignment",
    "measured_at", "schema_version", "source_pipeline", "firm")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB66"))
        sys.exit(1)

    def rows():
        sys.path.insert(0, str(root))
        sys.path.insert(0, str((root / PRODUCER).parent))
        spec = importlib.util.spec_from_file_location("ard_under_check", str(root / PRODUCER))
        ard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ard)
        src = json.loads((root / SOURCES).read_bytes().decode("utf-8"))
        th = {k: None for k in KEYS}
        th["threshold_claims"] = {k: "absent" for k in KEYS}
        out = {}
        for v in src.values():
            if isinstance(v, dict) and ard.method_version_of(v) in (2, 3):
                out[ard.method_version_of(v)] = ard.emit_method_row(None, ard.firm_scope(v), th, upload=False, src=v)
        if sorted(out) != [2, 3]:
            fail("the declared sources name method rows %r, want one entry for 2 and one for 3" % sorted(out))
        return ard, out

    def record():
        p = root / (D + "97/METHOD_ROW3_INCOME.json")
        if not p.is_file():
            fail("no record")
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB66-1-AC1":
        ard, out = rows()
        r3, r2 = out[3]["row"], out[2]["row"]
        if r3.get("income_basis") is not None or r3.get("income_basis_claim") != "absent" or not str(r3.get("income_basis_reason") or "").strip():
            fail("row 3: income_basis %r, claim %r, reason %r (want None, absent, a reason)"
                 % (r3.get("income_basis"), r3.get("income_basis_claim"), r3.get("income_basis_reason")))
        ok = [c for c in ard.THRESHOLD_CLAIMS if c != "absent"]
        if r2.get("income_basis") != "cash_when_received" or r2.get("income_basis_claim") not in ok:
            fail("row 2: income_basis %r, claim %r (want cash_when_received and one of %r)" % (r2.get("income_basis"), r2.get("income_basis_claim"), ok))
        for n, r in ((2, r2), (3, r3)):
            miss = [c for c in COLS_050 if c not in r]
            if miss:
                fail("row %d lost %d of the 29 columns of contract 0.5.0: %r" % (n, len(miss), miss))
        t = (out[3].get("table_schema") or {}).get("income_basis")
        if t in (None, "null") or "string" not in str(t):
            fail("row 3 lands income_basis as arrow type %r, want a typed string null" % t)
        print("OK: row 3 states income absent with a reason and lands typed; row 2 still reads cash_when_received (%s); 29 of 29 earlier columns kept"
              % r2["income_basis_claim"])
    elif cid == "DB66-1-AC2":
        c = json.loads((root / CONTRACT).read_bytes().decode("utf-8"))
        if c.get("contract_version") != "0.6.0":
            fail("contract_version %r, want 0.6.0" % c.get("contract_version"))
        cols = c.get("columns") or []
        lines = sorted("%s:%s" % (x.get("name"), x.get("type")) for x in cols)
        if hashlib.sha256(chr(10).join(lines).encode("utf-8")).hexdigest() != c.get("schema_hash"):
            fail("schema_hash does not equal sha256 over the contract's own sorted name:type lines")
        _ard, out = rows()
        names = [x.get("name") for x in cols]
        if sorted(out[3]["row"]) != sorted(names):
            fail("row keys and contract columns differ: only in row %r, only in contract %r"
                 % (sorted(set(out[3]["row"]) - set(names)), sorted(set(names) - set(out[3]["row"]))))
        ib = [x for x in cols if x.get("name") == "income_basis"]
        if len(ib) != 1 or ib[0].get("nullable") is not True:
            fail("the contract does not state income_basis nullable")
        r = record()
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
        if not str(r.get("token_census") or "").strip():
            fail("no token census")
        t = r.get("tests") or {}
        nt = str(t.get("new_test") or "").split("::")[0]
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not nt or not (root / nt).is_file():
            fail("tests %r" % t)
        if subprocess.run([sys.executable, "-m", "pytest", nt, "-q"], cwd=str(root), capture_output=True).returncode != 0:
            fail("pytest %s did not exit 0" % nt)
        print("OK: contract 0.6.0, %d columns equal the row's keys, income_basis nullable; rule-24 record and census present; %s passes" % (len(names), nt))
    elif cid == "DB66-1-AC3":
        r = record()
        pk = r.get("packet") or {}
        p = root / str(pk.get("path") or "")
        if p.name != "NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME.md" or not p.is_file():
            fail("packet file %r" % pk.get("path"))
        if hashlib.sha256(p.read_bytes()).hexdigest() != pk.get("sha256"):
            fail("the record's sha256 is not the packet file's")
        _ard, out = rows()
        if pk.get("object_address") != out[3]["address"]:
            fail("packet object_address %r, the dry run says %r" % (pk.get("object_address"), out[3]["address"]))
        if not isinstance(pk.get("writers_counted"), int) or pk["writers_counted"] < 1 or not isinstance(pk.get("readers_counted"), int) \
                or pk["readers_counted"] < 0 or not str(pk.get("rollback") or "").strip():
            fail("packet lacks writers_counted, readers_counted or rollback")
        if r.get("s3_writes") != 0:
            fail("s3_writes %r, want 0" % r.get("s3_writes"))
        print("OK: packet for %s, %d writer(s) and %d reader(s) counted, rollback stated; no S3 write" % (pk["object_address"], pk["writers_counted"], pk["readers_counted"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
