"""RIV-lg-1 AC2 (row Z-S20; Andrew-direct smoke 2026-10-04 S1/S6): the v0.8 leg's ONE gate splits into D12 and D13, which
switch independently. Today `universe.LEG_GATE` (RIVALFUNDS_LEG_ENABLE) flips every pending key at once, so the controls'
backfill cannot run without the home funds' source switch and vice versa.

Interface (prescribed at the cut, issuer ruling):
  - `RIVALFUNDS_LEG_D12=1` applies the HOME entries' `pending_source_policy` (IDVZ, PFOE -> bloomberg_primary: their history
    from inception through Bloomberg);
  - `RIVALFUNDS_LEG_D13=1` admits the `"leg": "pending"` entries (ACWI, IWM as index_control: the benchmarks) and applies
    `pending_role` (SCHY index_control -> rival: "SCHY is not the benchmark, the benchmark is ACWI");
  - `RIVALFUNDS_LEG_ENABLE=1` (the existing gate) turns both on; all unset reads the map as today;
  - the map cache keys on every gate, so flipping one in-process is read at the next call.

  - (a) D13 only: ACWI and IWM in funds(); role(ACWI) == index_control; role(SCHY, IDVZ) == rival; policy(IDVZ) == home_producer;
  - (b) D12 only: policy(IDVZ) == policy(PFOE) == bloomberg_primary; ACWI not in funds(); role(SCHY, IDVZ) == index_control;
  - (c) control: all unset reads today's map (IDVZ home_producer, ACWI absent, SCHY index_control), and RIVALFUNDS_LEG_ENABLE=1
        turns both on (ACWI in, IDVZ bloomberg_primary, SCHY rival).
FAIL at base: (a) and (b) FAIL (the new gates do nothing); (c) PASSES."""
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

GATES = ("RIVALFUNDS_LEG_ENABLE", "RIVALFUNDS_LEG_D12", "RIVALFUNDS_LEG_D13")


def state(u, **on):
    for g in GATES:
        os.environ.pop(g, None)
    for g, val in on.items():
        os.environ[g] = val
    fs = u.funds()
    st = {"funds_has_acwi": "ACWI" in fs, "funds_has_iwm": "IWM" in fs, "idvz": u.policy("IDVZ"), "pfoe": u.policy("PFOE"),
          "schy": u.role("SCHY", "IDVZ"), "acwi": u.role("ACWI") if "ACWI" in fs else None}
    print(on or "all unset", st)
    return st


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import universe as u

    s = state(u, RIVALFUNDS_LEG_D13="1")
    v.check(s["funds_has_acwi"] and s["funds_has_iwm"] and s["acwi"] == "index_control" and s["schy"] == "rival"
            and s["idvz"] == "home_producer", "(a) D13 alone: ACWI/IWM join as controls, SCHY reads rival, IDVZ stays home_producer")
    s = state(u, RIVALFUNDS_LEG_D12="1")
    v.check(s["idvz"] == "bloomberg_primary" and s["pfoe"] == "bloomberg_primary" and not s["funds_has_acwi"]
            and s["schy"] == "index_control", "(b) D12 alone: IDVZ/PFOE read bloomberg_primary, no ACWI, SCHY stays index_control")
    s0 = state(u)
    s1 = state(u, RIVALFUNDS_LEG_ENABLE="1")
    v.check(s0["idvz"] == "home_producer" and not s0["funds_has_acwi"] and s0["schy"] == "index_control"
            and s1["funds_has_acwi"] and s1["idvz"] == "bloomberg_primary" and s1["schy"] == "rival",
            "(c) control: all unset reads today's map; RIVALFUNDS_LEG_ENABLE=1 turns both on")
    for g in GATES:
        os.environ.pop(g, None)


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
