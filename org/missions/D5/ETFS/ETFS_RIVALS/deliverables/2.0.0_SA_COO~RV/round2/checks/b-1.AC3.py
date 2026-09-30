"""RIV-b-1 AC3 -- the vehicle leg is added gated OFF, without editing any existing line: the vehicle file at 2e38c030f4
(its last change before this round) is a line-for-line subsequence of the new file; the new leg is labelled
:rivalfunds_bbg_leg, sits after :prune, skips unless RIVALFUNDS_BBG_LEG is 1, owns RC_RIVBBG with codes 80-83 and RC_RIVENR
with 84-87, and never assigns %RC%, %RC_ETF% or %RC_CONS%."""
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

VEH = "integrations/bloomberg/pipeline/scheduled_daily_pull.cmd"
BASE = "2e38c030f4"


def run(v):
    root = c.setup_path()
    new = (root / VEH).read_bytes().decode("ascii").splitlines()
    old = subprocess.run(["git", "show", f"{BASE}:{VEH}"], capture_output=True, check=True, cwd=root).stdout.decode("ascii").splitlines()
    it = iter(new)
    missing = [ln for ln in old if not any(ln == x for x in it)]
    v.check(not missing, f"all {len(old)} base lines survive in order ({len(missing)} missing/edited; first {missing[:1]})")
    txt = "\n".join(new)
    i_prune, i_leg = txt.find("\n:prune"), txt.find("\n:rivalfunds_bbg_leg")
    v.check(i_leg > i_prune > 0, f":rivalfunds_bbg_leg placed after :prune ({i_prune}, {i_leg})")
    leg = txt[i_leg:] if i_leg > 0 else ""
    v.check(re.search(r'if\s+(/i\s+)?not\s+"%RIVALFUNDS_BBG_LEG%"\s*==\s*"1"\s+goto', leg, re.I) is not None,
            "the leg skips unless RIVALFUNDS_BBG_LEG==1")
    for code in ("80", "81", "82", "83", "84", "85", "86", "87"):
        v.check(re.search(rf"\b{code}\b", leg) is not None, f"exit code {code} documented in the leg")
    v.check("RC_RIVBBG" in leg and "RC_RIVENR" in leg, "own rc variables RC_RIVBBG and RC_RIVENR")
    bad = re.findall(r"set\s+\"?(RC|RC_ETF|RC_CONS)=", leg, re.I)
    v.check(not bad, f"the leg never assigns RC, RC_ETF or RC_CONS ({bad})")
    v.check(bool(re.search(r"enrichment_bloomberg\.py", leg)) and bool(re.search(r"if\s+not\s+exist", leg, re.I)),
            "enrichment is invoked only if its file exists")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
