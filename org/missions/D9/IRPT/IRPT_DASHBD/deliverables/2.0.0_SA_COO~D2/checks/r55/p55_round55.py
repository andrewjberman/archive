"""IRPT_DASHBD round 55 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ADDENDUM 20 (memory: both remedies, the step before Monday) and
ADDENDUM 19 item 2 (the FWD-8 comparator restates Black Diamond to Opal's declared conventions, pre-registered; CONVENTION only within 0.35pp).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB55-1-AC1  ~84/NEVER_WIDEN_PACKET_MEMSTEP.md carries "## Census", "## Branch A", "## Branch B", "## Rollback", "## COO half", "## CTO half", each
              half reading UNSIGNED; ~84/MEMSTEP_CENSUS.json: base_codesha256 == oNgy4rnr, memory_before == 2048, memory_after > 2048, and
              changed == ["memory_size"] (the setting only, no code).
  DB55-2-AC1  ~85/STAGE_MEMORY.json: stages is a non-empty list of {stage, peak_mb} measured on a kit day, largest_stage names the max, and
              after.largest_stage_peak_mb < before.largest_stage_peak_mb; tests {passed > 0, failed == 0, new_test} at HEAD.
  DB55-3-AC1  ~86/RESTATED_TIEOUT.json (repo record, no 10/11-digit zero-led token): n_outside_before == 990; by_reason sums to 990 and holds
              CONVENTION; private_record {path, sha256} matches; preregistration.rule_commit is a strict ancestor of output_commit and the
              rule commit touches restatement_rule_file.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~"
LIVE = "oNgy4rnrduvN9N2axhsHBfe9izZKd8dZGeFGXAIh+cM="
TOK = re.compile(r"(?<![0-9A-Za-z])0\d{9,10}(?![0-9A-Za-z])")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB55"))
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

    if cid == "DB55-1-AC1":
        p = root / (D + "84/NEVER_WIDEN_PACKET_MEMSTEP.md")
        if not p.is_file():
            fail("no packet")
        t = p.read_text(encoding="utf-8")
        for h in ("## Census", "## Branch A", "## Branch B", "## Rollback", "## COO half", "## CTO half"):
            if h not in t:
                fail("missing %r" % h)
        for h in ("## COO half", "## CTO half"):
            if "UNSIGNED" not in re.split(r"\n## ", t.split(h, 1)[1], maxsplit=1)[0]:
                fail("%s not UNSIGNED" % h)
        c = load(D + "84/MEMSTEP_CENSUS.json")
        if c.get("base_codesha256") != LIVE or c.get("memory_before") != 2048 or not isinstance(c.get("memory_after"), int) \
                or c["memory_after"] <= 2048 or c.get("changed") != ["memory_size"]:
            fail("census %r" % {k: c.get(k) for k in ("base_codesha256", "memory_before", "memory_after", "changed")})
        print("OK: memory step %d -> %d, setting only; halves UNSIGNED" % (c["memory_before"], c["memory_after"]))
    elif cid == "DB55-2-AC1":
        r = load(D + "85/STAGE_MEMORY.json")
        st = r.get("stages") or []
        if not st or any(not isinstance(s.get("peak_mb"), (int, float)) for s in st):
            fail("stages %r" % st)
        big = max(st, key=lambda s: s["peak_mb"])
        if r.get("largest_stage") != big.get("stage"):
            fail("largest_stage %r is not the max %r" % (r.get("largest_stage"), big.get("stage")))
        b, a = (r.get("before") or {}).get("largest_stage_peak_mb"), (r.get("after") or {}).get("largest_stage_peak_mb")
        if not isinstance(b, (int, float)) or not isinstance(a, (int, float)) or not a < b:
            fail("before %r / after %r" % (b, a))
        t = r.get("tests") or {}
        if not isinstance(t.get("passed"), int) or t["passed"] <= 0 or t.get("failed") != 0 or not fn_ok(t.get("new_test")):
            fail("tests %r" % t)
        print("OK: %s peak %.1f -> %.1f MB" % (big["stage"], b, a))
    elif cid == "DB55-3-AC1":
        rel = D + "86/RESTATED_TIEOUT.json"
        r = load(rel)
        if TOK.search((root / rel).read_text(encoding="utf-8")):
            fail("repo record carries an account-like token")
        by = r.get("by_reason") or {}
        if r.get("n_outside_before") != 990 or sum(by.values()) != 990 or "CONVENTION" not in by:
            fail("n_outside_before %r / by_reason %r" % (r.get("n_outside_before"), by))
        pr = r.get("private_record") or {}
        pp = Path(str(pr.get("path") or ""))
        if not pp.is_absolute() or not pp.is_file() or hashlib.sha256(pp.read_bytes()).hexdigest() != pr.get("sha256"):
            fail("private_record %r" % pr)
        pre = r.get("preregistration") or {}
        rc, oc, rf = pre.get("rule_commit"), pre.get("output_commit"), pre.get("restatement_rule_file")
        if not rc or not oc or rc == oc or git("merge-base", "--is-ancestor", rc, oc).returncode != 0:
            fail("rule_commit %r not a strict ancestor of output_commit %r" % (rc, oc))
        if not rf or rf not in git("show", "--name-only", "--format=", rc).stdout.split():
            fail("rule commit does not touch %r" % rf)
        print("OK: restated comparator %r" % by)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
