"""RIV-u-1 AC1 -- the universe loads the declared peer-group map: exactly the two groups, their members, roles and source
policies as the PRD's C-PEER-GROUPS states; a malformed map (a duplicate (group, fund), an unknown enum, a group without a
home) is refused."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import universe

    v.check(sorted(universe.groups()) == ["IDVZ", "PFOE"], f"groups {sorted(universe.groups())}")
    v.check(sorted(universe.funds(group_id="IDVZ")) == sorted(c.IDVZ_GROUP), f"IDVZ members {sorted(universe.funds(group_id='IDVZ'))}")
    v.check(sorted(universe.funds(group_id="PFOE")) == sorted(c.PFOE_GROUP), f"PFOE members {sorted(universe.funds(group_id='PFOE'))}")
    v.check(universe.role("IDVZ", "IDVZ") == "home" and universe.role("PFOE", "PFOE") == "home", "IDVZ and PFOE are home")
    v.check(universe.role("SCHY", "IDVZ") == "index_control", f"SCHY role {universe.role('SCHY', 'IDVZ')}")
    want = {**{f: "bloomberg_primary" for f in c.IDVZ_GROUP[1:]}, **{f: "issuer_first" for f in c.PFOE_GROUP[1:]},
            "IDVZ": "home_producer_pending", "PFOE": "home_producer_pending"}
    got = {f: universe.policy(f) for f in want}
    v.check(got == want, f"source policies as ruled (diff {[f for f in want if got[f] != want[f]]})")
    v.check(sorted(universe.funds(source_policy="bloomberg_primary")) == sorted(c.IDVZ_GROUP[1:]),
            "funds(source_policy='bloomberg_primary') is the five IDVZ rivals")

    src = json.loads(pathlib.Path(universe.DEFAULT_MAP).read_text(encoding="utf-8"))
    entries = src["entries"] if isinstance(src, dict) else src
    tmp = pathlib.Path(c.tmpdir("rv_g0_"))
    for label, mutate in [("duplicate (group, fund)", lambda e: e + [dict(e[0])]),
                          ("unknown source_policy", lambda e: [dict(e[0], source_policy="carrier_pigeon")] + e[1:]),
                          ("a group with no home", lambda e: [x for x in e if not (x["group_id"] == "IDVZ" and x["role"] == "home")])]:
        p = tmp / f"bad_{label.split()[0]}.json"
        bad = mutate([dict(x) for x in entries])
        p.write_text(json.dumps({**src, "entries": bad} if isinstance(src, dict) else bad), encoding="utf-8")
        try:
            universe.load(p)
            v.check(False, f"malformed map refused: {label} (it LOADED)")
        except ValueError as e:
            v.check(True, f"malformed map refused: {label} ({str(e)[:60]})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
