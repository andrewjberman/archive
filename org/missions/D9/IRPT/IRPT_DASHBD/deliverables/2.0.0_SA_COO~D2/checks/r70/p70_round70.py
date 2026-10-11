"""IRPT_DASHBD round 70 (issuer 2.0.0_SA_COO~D2) -- the ENRICHMENT LIST of 1.0.0_SA_CTO~DELL2's ROUND-69 ANALYSIS @90cb3e774b, five cells.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB70-1-AC1  ~105/PACKAGE_AND_MANIFEST_READ.json: package {read (bool), key_names (list), key_count, digit_runs_8plus,
              five_values_equal_to_tracked (true / false / "NOT_ESTABLISHED")} and returns_manifest {read (bool), key_names, key_count,
              digit_runs_8plus}; a part not read carries a non-empty `reason`; values_kept == 0; s3_writes == 0; and NO string anywhere
              in the record holds a run of 8 or more digits (members named *sha256 excepted).
  DB70-2-AC1  the producer exposes served_thresholds(thresholds): for an input carrying the five values, a threshold_claims object and
              two extra keys, it returns exactly the five values plus threshold_claims; the literal `"thresholds": thresholds` no
              longer occurs in the producer.
  DB70-3-AC1  the contract no longer gives "FWD-3 does not separate income" as a cause, its schema_hash is unchanged, and
              ~107/PROSE_LINES.json states build_manifest_text CORRECTED (then the tracked build manifest's columns_null.method_version
              no longer reads "NULL on purpose" and its method_row is byte-for-byte what it was) or REFUSED_BY_LANE with the refusal.
  DB70-4-AC1  method_version_of REFUSES an entry that names a non-custodian row and declares no valuation_source, still returns 2 for an
              entry naming row 2 without one, and still resolves both entries of sources.json (2 and 3).
  DB70-5-AC1  ~108/UNCLASSED_90.json: denominator 90; classes [{cause, count, rule}] plus remainder {count, why} sum to 90;
              client_figures == 0; s3_writes == 0; a remainder of 90 carries a non-empty read_denied or why; no run of 8+ digits.
"""
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
ARD = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
CONTRACT = "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json"
BUILD_MANIFEST = "org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~79/ard_cottonwood_manifest.json"
SCHEMA_HASH = "fd468e209e53f14514380089c9281b0ca90f947ab8eaf53c841bdee666bdfba1"
METHOD_ROW_SHA = "7e2b15c57bdbe1c2152a64a1c13e0934c37bff6efc62546fadbab794d05ab888"
FIVE = ["tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high", "comparability_max_excluded_weight"]
RUN = re.compile(r"\d{8,}")


def long_digit_runs(obj, name=""):
    """Paths of strings (and dict keys) holding a run of 8 or more digits; members named *sha256 are skipped."""
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if RUN.search(str(k)):
                hits.append(name + "/<key>")
            if not str(k).endswith("sha256"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def load_producer(root):
    p = root / ARD
    sys.path.insert(0, str(p.parent))
    spec = importlib.util.spec_from_file_location("ard_under_check", str(p))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB70"))
        sys.exit(1)

    def record(rel):
        p = root / (M + rel)
        if not p.is_file():
            fail("no record %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB70-1-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~105/PACKAGE_AND_MANIFEST_READ.json")
        for part in ("package", "returns_manifest"):
            d = r.get(part) or {}
            if not isinstance(d.get("read"), bool):
                fail("%s.read is not a bool" % part)
            if d["read"]:
                if not isinstance(d.get("key_names"), list) or d.get("key_count") != len(d["key_names"]) \
                        or not isinstance(d.get("digit_runs_8plus"), int):
                    fail("%s lacks key_names, a matching key_count or digit_runs_8plus" % part)
            elif not str(d.get("reason") or "").strip():
                fail("%s was not read and gives no reason" % part)
        eq = r["package"].get("five_values_equal_to_tracked")
        if eq not in (True, False, "NOT_ESTABLISHED"):
            fail("package.five_values_equal_to_tracked %r" % eq)
        if r.get("values_kept") != 0 or r.get("s3_writes") != 0:
            fail("values_kept %r, s3_writes %r" % (r.get("values_kept"), r.get("s3_writes")))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: package read=%s (%s keys, %s long digit runs); returns manifest read=%s (%s keys, %s long digit runs); equal to tracked: %s"
              % (r["package"]["read"], r["package"].get("key_count"), r["package"].get("digit_runs_8plus"),
                 r["returns_manifest"]["read"], r["returns_manifest"].get("key_count"), r["returns_manifest"].get("digit_runs_8plus"), eq))
    elif cid == "DB70-2-AC1":
        src = (root / ARD).read_text(encoding="utf-8")
        n = src.count('"thresholds": thresholds')
        if n:
            fail("the producer still copies the whole thresholds object at %d site(s)" % n)
        mod = load_producer(root)
        fn = getattr(mod, "served_thresholds", None)
        if fn is None:
            fail("the producer has no served_thresholds")
        claims = {k: "held" for k in FIVE}
        given = {**{k: 0.5 for k in FIVE}, "threshold_claims": claims, "per_account_note": {"a": 1}, "another_key": [1, 2]}
        out = fn(given)
        if sorted(out) != sorted(FIVE + ["threshold_claims"]):
            fail("served_thresholds returned keys %r" % sorted(out))
        if any(out[k] != 0.5 for k in FIVE) or out["threshold_claims"] != claims:
            fail("served_thresholds changed a value or a claim")
        print("OK: served_thresholds keeps the five values and their claims and drops 2 of 2 extra keys; 0 whole-object copies left")
    elif cid == "DB70-3-AC1":
        text = (root / CONTRACT).read_text(encoding="utf-8")
        n = text.count("FWD-3 does not separate income")
        if n:
            fail("the contract still gives the outcome id as the cause at %d place(s)" % n)
        if json.loads(text).get("schema_hash") != SCHEMA_HASH:
            fail("the contract's schema_hash moved")
        r = record("0.9.0_WK_IRPT_DASHBD~107/PROSE_LINES.json")
        state = r.get("build_manifest_text")
        bm = json.loads((root / BUILD_MANIFEST).read_bytes().decode("utf-8"))
        if hashlib.sha256(json.dumps(bm["method_row"], sort_keys=True).encode()).hexdigest() != METHOD_ROW_SHA:
            fail("the build manifest's method_row moved")
        if state == "CORRECTED":
            if "NULL on purpose" in str(bm["columns_null"].get("method_version")):
                fail("CORRECTED stated, and the build manifest still reads NULL on purpose")
        elif state == "REFUSED_BY_LANE":
            if not str(r.get("refusal") or "").strip():
                fail("REFUSED_BY_LANE without the refusal text")
        else:
            fail("build_manifest_text %r" % state)
        print("OK: the contract's two prose lines no longer name the outcome id; schema_hash unchanged; build manifest text %s; method_row unmoved" % state)
    elif cid == "DB70-4-AC1":
        mod = load_producer(root)
        f = mod.method_version_of
        try:
            got = f({"method_version": 3})
        except SystemExit as e:
            if "REFUSED" not in str(e):
                fail("row 3 with no valuation_source exits without a REFUSED: %r" % str(e)[:80])
        else:
            fail("row 3 with no valuation_source is not refused (returned %r)" % (got,))
        if f({"method_version": 2}) != 2:
            fail("row 2 with no valuation_source no longer resolves to 2")
        srcs = json.loads((root / "data/assets/scripts/gold/irpt_reporting/sources.json").read_text(encoding="utf-8"))
        entries = [v for v in srcs.values() if isinstance(v, dict) and "method_version" in v] if isinstance(srcs, dict) else []
        got = sorted(f(e) for e in entries)
        if got != [2, 3]:
            fail("sources.json entries resolve to %r, want [2, 3]" % got)
        print("OK: row 3 with no valuation_source is REFUSED; row 2 without one still resolves; 2 of 2 sources.json entries resolve")
    elif cid == "DB70-5-AC1":
        r = record("0.9.0_WK_IRPT_DASHBD~108/UNCLASSED_90.json")
        cl = r.get("classes")
        rem = r.get("remainder") or {}
        if r.get("denominator") != 90 or not isinstance(cl, list) or not isinstance(rem.get("count"), int):
            fail("denominator %r, classes or remainder.count missing" % r.get("denominator"))
        for c in cl:
            if not str(c.get("cause") or "").strip() or not isinstance(c.get("count"), int) or c["count"] < 1 or not str(c.get("rule") or "").strip():
                fail("a class lacks cause, a positive count or a rule: %r" % c.get("cause"))
        total = sum(c["count"] for c in cl) + rem["count"]
        if total != 90:
            fail("classes and remainder sum to %d, not 90" % total)
        if rem["count"] and not str(rem.get("why") or "").strip():
            fail("a remainder with no why")
        if rem["count"] == 90 and not str(r.get("read_denied") or rem.get("why") or "").strip():
            fail("nothing classed and no reason")
        if r.get("client_figures") != 0 or r.get("s3_writes") != 0:
            fail("client_figures %r, s3_writes %r" % (r.get("client_figures"), r.get("s3_writes")))
        hits = long_digit_runs(r)
        if hits:
            fail("the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: 90 segments: %d class(es) holding %d, remainder %d" % (len(cl), total - rem["count"], rem["count"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
