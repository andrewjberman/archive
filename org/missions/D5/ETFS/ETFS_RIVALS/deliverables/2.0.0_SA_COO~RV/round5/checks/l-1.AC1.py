"""RIV-l-1 AC1 (PRD v0.8; analysis item 7) -- the v0.8 Bloomberg leg is BUILT and INERT: the four new names (IDVZ, PFOE, ACWI,
IWM) are in the map as PENDING and join the leg only behind the gate `RIVALFUNDS_LEG_ENABLE=1`, which the issuer sets after the
request-cost measurement. The vehicle runs the CLOUD working tree, so merging this cell must change nothing it requests.

Offline (no Bloomberg call, no S3):
  - inert: with the gate unset, `universe.funds(source_policy="bloomberg_primary")` is exactly TXUE, BIDD, CGIC, INEQ, SCHY;
    `universe.policy("IDVZ")` is home_producer; `collector_bloomberg.funds_for_day` on a local sink names none of the four;
  - the map carries ACWI (group IDVZ) and IWM (group PFOE) as `index_control`, `bloomberg_primary`, `"leg": "pending"`;
  - enabled (a fresh process with RIVALFUNDS_LEG_ENABLE=1): funds_for_day names IDVZ, PFOE, ACWI and IWM; policy("IDVZ") and
    policy("PFOE") read bloomberg_primary; each group's ONE index_control is ACWI (IDVZ) and IWM (PFOE), SCHY reads rival; and
    `collector_bloomberg.request_plan(date)` returns {"funds": [...], "names": <len(funds)>, ...} covering the four."""
import json
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-09-29"
NEW = {"IDVZ", "PFOE", "ACWI", "IWM"}
PROBE = r"""
import json, sys
sys.path[:0] = sys.argv[1:3]
from rivalfunds import collector_bloomberg as cb, sinks, universe
s = sinks.get_sink("local:" + sys.argv[3])
fs, _ = cb.funds_for_day(s, "%s", {})
ents = universe.entries() if hasattr(universe, "entries") else []
ctl = {g: [e["fund_id"] for e in ents if e["group_id"] == g and e.get("role") == "index_control"] for g in ("IDVZ", "PFOE")}
role_schy = [e.get("role") for e in ents if e["fund_id"] == "SCHY"]
plan = cb.request_plan("%s") if hasattr(cb, "request_plan") else None
print(json.dumps({"funds": fs, "pol_idvz": universe.policy("IDVZ"), "pol_pfoe": universe.policy("PFOE"),
                  "bbg": universe.funds(source_policy="bloomberg_primary"), "ctl": ctl, "schy": role_schy, "plan": plan}))
""" % (D, D)


def probe(enable):
    env = {k: v for k, v in os.environ.items() if k != "RIVALFUNDS_LEG_ENABLE"}
    if enable:
        env["RIVALFUNDS_LEG_ENABLE"] = "1"
    tmp = c.tmpdir("rv_l1_")
    p = subprocess.run([sys.executable, "-c", PROBE, str(c.ROOT / "data" / "etfs" / "scripts"), str(c.ROOT), tmp],
                       env=env, capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[-400:])
    return json.loads(p.stdout.strip().splitlines()[-1])


def run(v):
    c.setup_path()
    off = probe(False)
    print("gate unset:", {k: off[k] for k in ("funds", "pol_idvz", "bbg")})
    v.check(off["bbg"] == ["TXUE", "BIDD", "CGIC", "INEQ", "SCHY"] and off["pol_idvz"] == "home_producer"
            and not (NEW & set(off["funds"])), "inert: with the gate unset the leg requests exactly today's funds")
    raw = json.loads((c.ROOT / "data" / "etfs" / "scripts" / "rivalfunds" / "peer_groups.json").read_text(encoding="utf-8"))
    pend = {(e["group_id"], e["fund_id"]) for e in raw["entries"] if e.get("role") == "index_control"
            and e.get("source_policy") == "bloomberg_primary" and e.get("leg") == "pending"}
    print("pending index_control entries:", sorted(pend))
    v.check({("IDVZ", "ACWI"), ("PFOE", "IWM")} <= pend, "the map carries ACWI (IDVZ) and IWM (PFOE) as pending index controls")
    on = probe(True)
    print("gate set:", {k: on[k] for k in ("funds", "pol_idvz", "pol_pfoe", "ctl", "schy")}, "plan:", str(on["plan"])[:160])
    plan = on["plan"] or {}
    v.check(NEW <= set(on["funds"]) and on["pol_idvz"] == on["pol_pfoe"] == "bloomberg_primary"
            and on["ctl"] == {"IDVZ": ["ACWI"], "PFOE": ["IWM"]} and set(on["schy"]) == {"rival"}
            and NEW <= set(plan.get("funds") or []) and plan.get("names") == len(plan.get("funds") or []),
            "enabled: the four join the leg, one index control per group, SCHY rival, and request_plan covers them")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
