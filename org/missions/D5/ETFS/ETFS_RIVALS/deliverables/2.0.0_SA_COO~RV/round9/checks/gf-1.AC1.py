"""RIV-gf-1 AC1 (CTO~Z ruling on row Z-S29: IDVZ/PFOE join the daily pull through a rivalfunds-owned gate file; no
Positioning file is written or read differently). Measured: `universe.d12_enabled()` reads only the process environment
(`universe.py:36-37`); the vehicle sets no D12 variable and `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd` may
not be edited.

Interface (prescribed): `data/etfs/scripts/rivalfunds/leg_gates.json` holds {"RIVALFUNDS_LEG_ENABLE": "0"|"1",
"RIVALFUNDS_LEG_D12": "0"|"1", "RIVALFUNDS_LEG_D13": "0"|"1"}; a gate reads ON when the environment says "1" OR the file says
"1" (one direction: the environment never turns a file "1" off); the module-level path `universe.GATES_FILE` names the file
and a test may point it elsewhere. The committed file ships every gate "0".
Fixture (offline): a temporary gate file; the map cache cleared between arms.
  - (a) environment unset, file D12 "1" -> `d12_enabled()` True and IDVZ's source_policy reads bloomberg_primary;
  - (b) environment D12 "1", file D12 "0" -> True;
  - (c) control: environment unset, file D12 "0" -> False and IDVZ reads its home policy;
  - (d) the committed leg_gates.json reads every gate "0".
FAIL at base: (a) and (d) FAIL (no file, no GATES_FILE); (b) and (c) PASS."""
import json
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

GATE = "RIVALFUNDS_LEG_D12"


def run(v):
    c.setup_path()
    from rivalfunds import universe

    def policy(fund):
        universe._CACHE.clear()
        return universe.policy(fund)

    saved = {g: os.environ.pop(g, None) for g in universe.GATES}
    has_file = hasattr(universe, "GATES_FILE")
    orig = getattr(universe, "GATES_FILE", None)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="rv_gf1_")) / "leg_gates.json"
    try:
        def arm(env_val, file_val):
            for g in universe.GATES:
                os.environ.pop(g, None)
            if env_val is not None:
                os.environ[GATE] = env_val
            tmp.write_text(json.dumps({g: "0" for g in universe.GATES} | {GATE: file_val}), encoding="utf-8")
            if has_file:
                universe.GATES_FILE = tmp
            universe._CACHE.clear()
            return universe.d12_enabled(), policy("IDVZ")

        a = arm(None, "1")
        b = arm("1", "0")
        cc = arm(None, "0")
        print("(a) env unset, file 1:", a, "| (b) env 1, file 0:", b, "| (c) env unset, file 0:", cc)
        v.check(has_file and a == (True, "bloomberg_primary"), "(a) a file D12 '1' alone turns D12 on and IDVZ reads bloomberg_primary")
        v.check(b[0] is True, "(b) the environment '1' turns D12 on whatever the file says")
        v.check(cc[0] is False and cc[1] != "bloomberg_primary", "(c) control: both off -> D12 off, IDVZ keeps its home policy")
    finally:
        if has_file:
            universe.GATES_FILE = orig
        for g, val in saved.items():
            os.environ.pop(g, None)
            if val is not None:
                os.environ[g] = val
        universe._CACHE.clear()
    committed = c.ROOT / "data" / "etfs" / "scripts" / "rivalfunds" / "leg_gates.json"
    doc = json.loads(committed.read_text(encoding="utf-8")) if committed.exists() else None
    print("committed leg_gates.json:", doc)
    v.check(isinstance(doc, dict) and all(str(doc.get(g)) == "0" for g in ("RIVALFUNDS_LEG_ENABLE", GATE, "RIVALFUNDS_LEG_D13")),
            "(d) the committed leg_gates.json ships every gate '0'")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
