"""IRPT_DASHBD round 62 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 4060: the thresholds a method row states carry their claim.

Cell: DB-b-118 the producer's thresholds input and the dim_return_method row gain a per-value CLAIM (measured / inferred / held / absent), so a
row written for a run whose thresholds were never measured states that in a field a consumer can reject on. Rule-24 record first, then the
change with tests. No S3 write.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB62-1-AC1  ~93/THRESHOLD_CLAIM_RULE24.json: postulates holds exactly mece, same_grain, intent_coherence, state_coherence, each with a
              finding and evidence [{file, line}] resolving at HEAD; token_census.files_scanned > 0 with int hits and files for each of
              measured, inferred, held, absent and the chosen field name; decision names field_name, where_written and
              file_without_claims (what the writer does for a thresholds file carrying no claims).
  DB62-1-AC2  the producer declares THRESHOLD_CLAIMS as exactly (measured, inferred, held, absent); the record's tests.new_test file exists
              and `python -m pytest <that file> -q` exits 0 at HEAD; tests {passed > 0, failed == 0}.
  DB62-1-AC3  (AMENDMENT 1) the dim_return_method contract reads contract_version 0.4.0; its schema_hash equals sha256 over its own sorted
              name:type lines; its column names equal the keys of the row emit_method_row returns (upload=False) for an all-absent
              thresholds input on the declared 49F entry; and that result's `table_schema` gives each of the five value columns the
              arrow type the contract names, never the null type.
"""
import ast
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
CONTRACT = "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
SOURCES = "data/assets/scripts/gold/irpt_reporting/sources.json"
POSTULATES = {"mece", "same_grain", "intent_coherence", "state_coherence"}
CLAIMS = ("measured", "inferred", "held", "absent")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB62"))
        sys.exit(1)

    p = root / (D + "93/THRESHOLD_CLAIM_RULE24.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    if cid not in ("DB62-1-AC1", "DB62-1-AC2", "DB62-1-AC3"):
        fail("unknown criterion %r" % cid)
    if cid == "DB62-1-AC1":
        ps = r.get("postulates") or {}
        if set(ps) != POSTULATES:
            fail("postulates %r" % sorted(ps))
        for k in sorted(ps):
            ev = ps[k].get("evidence") or []
            if not str(ps[k].get("finding") or "").strip() or not ev:
                fail("postulate %s lacks a finding or evidence" % k)
            for e in ev:
                if not (root / str(e.get("file") or "")).is_file() or not isinstance(e.get("line"), int):
                    fail("postulate %s evidence %r does not name a file and line" % (k, e))
        dec = r.get("decision") or {}
        for k in ("field_name", "where_written", "file_without_claims"):
            if not str(dec.get(k) or "").strip():
                fail("decision.%s missing" % k)
        tc = r.get("token_census") or {}
        toks = tc.get("tokens") or {}
        if not isinstance(tc.get("files_scanned"), int) or tc["files_scanned"] <= 0:
            fail("token_census.files_scanned %r" % tc.get("files_scanned"))
        for t in CLAIMS + (dec["field_name"],):
            e = toks.get(t) or {}
            if not isinstance(e.get("hits"), int) or not isinstance(e.get("files"), int):
                fail("token_census lacks %r with int hits and files" % t)
        print("OK: four postulates answered, census over %d files, field %r" % (tc["files_scanned"], dec["field_name"]))
    elif cid == "DB62-1-AC2":
        tree = ast.parse((root / PRODUCER).read_text(encoding="utf-8"))
        got = None
        for n in tree.body:
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "THRESHOLD_CLAIMS" for t in n.targets):
                try:
                    got = tuple(ast.literal_eval(n.value))
                except ValueError:
                    fail("THRESHOLD_CLAIMS is not a literal")
        if got != CLAIMS:
            fail("THRESHOLD_CLAIMS %r, want %r" % (got, CLAIMS))
        t = r.get("tests") or {}
        nt = str(t.get("new_test") or "").split("::")[0]
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not nt or not (root / nt).is_file():
            fail("tests %r" % t)
        run = subprocess.run([sys.executable, "-m", "pytest", nt, "-q"], cwd=str(root), capture_output=True)
        if run.returncode != 0:
            fail("pytest %s exited %d" % (nt, run.returncode))
        print("OK: THRESHOLD_CLAIMS is the four; %s passes" % nt)
    elif cid == "DB62-1-AC3":
        # AMENDMENT 1 (rows IRPT_DASHBD-D2-W93-S1 and S2): the contract describes the row the producer writes, and an all-absent row is typed.
        import hashlib
        import importlib.util
        c = json.loads((root / CONTRACT).read_bytes().decode("utf-8"))
        if c.get("contract_version") != "0.4.0":
            fail("contract_version %r, want 0.4.0" % c.get("contract_version"))
        cols = c.get("columns") or []
        names = [x.get("name") for x in cols]
        lines = sorted("%s:%s" % (x.get("name"), x.get("type")) for x in cols)
        if hashlib.sha256(chr(10).join(lines).encode("utf-8")).hexdigest() != c.get("schema_hash"):
            fail("schema_hash does not equal sha256 over the contract's own sorted name:type lines")
        sys.path.insert(0, str(root))
        sys.path.insert(0, str((root / PRODUCER).parent))
        spec = importlib.util.spec_from_file_location("ard_under_check", str(root / PRODUCER))
        ard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ard)
        keys = ("tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight")
        th = {k: None for k in keys}
        th["threshold_claims"] = {k: "absent" for k in keys}
        src = json.loads((root / SOURCES).read_bytes().decode("utf-8"))
        entry = [v for k, v in src.items() if not k.startswith("_") and isinstance(v, dict)][0]
        res = ard.emit_method_row(None, ard.firm_scope(entry), th, upload=False, src=entry)
        row = res["row"]
        if sorted(row) != sorted(names):
            fail("row keys and contract columns differ: only in row %r, only in contract %r"
                 % (sorted(set(row) - set(names)), sorted(set(names) - set(row))))
        tab = res.get("table_schema") or {}
        ctype = {x["name"]: x["type"] for x in cols}
        for k in keys:
            if tab.get(k) in (None, "null") or tab.get(k) != ctype.get(k):
                fail("all-absent row: column %s arrow type %r, the contract says %r (a null-typed column is the defect)" % (k, tab.get(k), ctype.get(k)))
        print("OK: contract 0.4.0 columns equal the row's %d keys; schema_hash self-consistent; the five value columns are typed on an all-absent row" % len(names))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
