"""RIV-f-4 AC2 (analysis ruling 3, row Z-S13) -- the issuer identity floor is per FUND: `resolved_floor()` accepts per-fund entries
under `issuer`, so BASG is held to its own floor while GQGU keeps its own.

Pure (guardrails only), through the f-3 override with
  {"min_resolved_fraction": {"issuer": {"BASG": 0.95, "GQGU": 0.23}, "bloomberg": 0.99, "home_producer": 0.0}}:
  - BASG 5 of 10 resolved, source issuer -> FAIL, the reason naming BASG's floor 0.95 (today the dict makes the floor unreadable);
  - GQGU 3 of 10 resolved, source issuer -> PASS (its own 0.23);
  - an issuer fund the table does not name (NEWI, 9 of 10) -> graded against the STRICTEST issuer floor (0.95): 0.9 FAILs, and the
    reason names NEWI;
  - control: TXUE 10 of 10, source bloomberg -> PASS."""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

OVER = {"min_resolved_fraction": {"issuer": {"BASG": 0.95, "GQGU": 0.23}, "bloomberg": 0.99, "home_producer": 0.0}}


def run(v):
    c.setup_path()
    from rivalfunds import guardrails
    from rivalfunds.tests.test_f3_identity_floors import _reports

    os.environ[guardrails.OVERRIDE_ENV] = json.dumps(OVER)
    cfg = guardrails.load_config()

    def grade(fund, resolved, source):
        r = guardrails.identity_coverage(_reports(fund, resolved=resolved), cfg, source)
        print(f"  {fund} {resolved}/10 {source}: {r['status']} -- {r['reason'][:150]}")
        return r

    b = grade("BASG", 5, "issuer")
    v.check(b["status"] == "FAIL" and "0.95" in b["reason"] and "BASG" in b["reason"], "BASG 0.5 FAILs its own floor 0.95")
    g = grade("GQGU", 3, "issuer")
    v.check(g["status"] == "PASS", "GQGU 0.3 PASSes its own floor 0.23")
    n = grade("NEWI", 9, "issuer")
    v.check(n["status"] == "FAIL" and "NEWI" in n["reason"], "an unnamed issuer fund is held to the strictest issuer floor")
    t = grade("TXUE", 10, "bloomberg")
    v.check(t["status"] == "PASS", "control: a bloomberg fund is graded as before")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
