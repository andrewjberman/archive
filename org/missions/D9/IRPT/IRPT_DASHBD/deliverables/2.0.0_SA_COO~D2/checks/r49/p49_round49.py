"""IRPT_DASHBD round 49 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 15 (msg 3492, @74243ee7c8; FWD-8 NOT REALIZED) and
ADDENDUM 13.2 (msg 3501).

Cells: DB-b-99 the classifier's threshold sensitivity, pre-registration and per-reason claim; DB-b-100 the 74 W73-S1 DEFECT segments;
DB-b-101 the 123 W73-S2 DEFECT segments; DB-b-102 method_version taken from the firm's sources entry (never a default 2).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB49-1-AC1  ~74/SENSITIVITY.json: settings holds the peak cuts 0.005, 0.01, 0.02 and at least three dollar-tie settings; per_setting maps each
              setting to by_reason counts that each sum to 990; cut_segments lists the 156 NEAR_ZERO_BASE segments at 1%; every reason in
              final.by_reason carries claim inferred|confirmed and robust true|false; no robust-false reason keeps segments in final (they are
              UNEXPLAINED there); final.by_reason sums to 990.
  DB49-1-AC2  ~74/SENSITIVITY.json preregistration.rule_commit and .output_commit are commits at HEAD, rule_commit an ancestor of output_commit and
              not equal to it, and the rule commit touches thresholds_file while the output commit touches SENSITIVITY.json.
  DB49-2-AC1  ~75/W73_S1_RESOLUTION.json: 74 distinct segments, each disposition PRODUCER_FIX or BD_SIDE; a PRODUCER_FIX carries test
              "<file>::<function>" at HEAD; a BD_SIDE carries evidence naming a file at HEAD; counts sum to 74.
  DB49-3-AC1  ~76/W73_S2_RESOLUTION.json: the same shape over 123 segments.
  DB49-4-AC1  ~77/METHOD_FROM_SOURCE.json tests {passed > 0, failed == 0, new_test, negative_test} at HEAD; account_return_daily.py's
              build_manifest no longer writes the module constant METHOD_VERSION directly; every custody source in sources.json carries
              method_version.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
SOURCES = "data/assets/scripts/gold/irpt_reporting/sources.json"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB49"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    def fn_ok(s):
        m = re.fullmatch(r"([^:]+\.py)::(\w+)", str(s or ""))
        return bool(m) and (root / m.group(1)).is_file() and bool(
            re.search(r"^\s*def %s\(" % re.escape(m.group(2)), (root / m.group(1)).read_text(encoding="utf-8"), re.M))

    def git(*a):
        return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True)

    def resolution(rel, n):
        r = load(rel)
        segs = r.get("segments") or []
        keys = [(s.get("account"), json.dumps(s.get("segment"), sort_keys=True)) for s in segs]
        if len(segs) != n or len(set(keys)) != n:
            fail("%d segments (%d distinct), want %d" % (len(segs), len(set(keys)), n))
        counts = {}
        for s in segs:
            d = s.get("disposition")
            if d == "PRODUCER_FIX":
                if not fn_ok(s.get("test")):
                    fail("PRODUCER_FIX without a test at HEAD: %r" % s.get("test"))
            elif d == "BD_SIDE":
                ev = str(s.get("evidence") or "")
                if not ev or not (root / ev.split("#")[0]).is_file():
                    fail("BD_SIDE without evidence at HEAD: %r" % ev)
            else:
                fail("disposition %r" % d)
            counts[d] = counts.get(d, 0) + 1
        print("OK: %d segments: %r" % (n, counts))

    if cid == "DB49-1-AC1":
        r = load(D + "74/SENSITIVITY.json")
        st = r.get("settings") or {}
        if sorted(st.get("peak_cut") or []) != [0.005, 0.01, 0.02] or len(st.get("dollar_tie") or []) < 3:
            fail("settings %r" % st)
        per = r.get("per_setting") or {}
        if not per or any(sum((v or {}).values()) != 990 for v in per.values()):
            fail("per_setting sums %r" % {k: sum((v or {}).values()) for k, v in per.items()})
        if len(r.get("cut_segments") or []) != 156:
            fail("cut_segments %d, want 156" % len(r.get("cut_segments") or []))
        fin = r.get("final") or {}
        by, meta = fin.get("by_reason") or {}, fin.get("reasons") or {}
        if sum(by.values()) != 990:
            fail("final sums %d" % sum(by.values()))
        for k, v in by.items():
            if k in ("UNEXPLAINED", "DEFECT"):
                continue
            m = meta.get(k) or {}
            if m.get("claim") not in ("inferred", "confirmed") or m.get("robust") not in (True, False):
                fail("reason %s claim/robust %r" % (k, m))
            if m.get("robust") is False and v:
                fail("non-robust reason %s keeps %d segments" % (k, v))
        print("OK: %d settings graded; final %r" % (len(per), by))
    elif cid == "DB49-1-AC2":
        r = load(D + "74/SENSITIVITY.json")
        pr = r.get("preregistration") or {}
        rc, oc, tf = pr.get("rule_commit"), pr.get("output_commit"), pr.get("thresholds_file")
        if not rc or not oc or rc == oc or git("merge-base", "--is-ancestor", rc, oc).returncode != 0:
            fail("rule_commit %r is not a strict ancestor of output_commit %r" % (rc, oc))
        rf = git("show", "--name-only", "--format=", rc).stdout.split()
        of = git("show", "--name-only", "--format=", oc).stdout.split()
        if not tf or tf not in rf or not any(f.endswith("SENSITIVITY.json") for f in of):
            fail("rule commit files %r / output commit files %r / thresholds_file %r" % (rf, of, tf))
        print("OK: thresholds %s committed at %s before output %s" % (tf, rc[:10], oc[:10]))
    elif cid == "DB49-2-AC1":
        resolution(D + "75/W73_S1_RESOLUTION.json", 74)
    elif cid == "DB49-3-AC1":
        resolution(D + "76/W73_S2_RESOLUTION.json", 123)
    elif cid == "DB49-4-AC1":
        r = load(D + "77/METHOD_FROM_SOURCE.json")
        t = r.get("tests") or {}
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not fn_ok(t.get("new_test")) \
                or not fn_ok(t.get("negative_test")):
            fail("tests %r" % t)
        src = (root / PRODUCER).read_text(encoding="utf-8")
        m = re.search(r"^def build_manifest\(.*?(?=^def |\Z)", src, re.S | re.M)
        if not m or re.search(r'"method_version":\s*METHOD_VERSION\b', m.group(0)):
            fail("build_manifest still writes METHOD_VERSION directly")
        doc = json.loads((root / SOURCES).read_bytes().decode("utf-8"))
        srcs = {k: v for k, v in doc.items() if isinstance(v, dict) and not k.startswith("_")}
        if not srcs or any("method_version" not in v for v in srcs.values()):
            fail("a source lacks method_version")
        print("OK: build_manifest takes method_version from the entry; %d passed" % t["passed"])
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
