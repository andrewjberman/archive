"""HVST-p-4 controls: (1) MUTANT -- AC2 run against a scratch copy of the runtime records with barrons' verification_repairs
set to 1 must FAIL its assertions; (2) DETERMINISM -- AC1 and AC2 run twice compare equal once the clock lines are removed;
(3) SOCKET -- with the block on, socket creation raises. Local reads and a scratch copy under .scratch/ only; no network."""
import os
import shutil
import subprocess
import sys
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p4_common as C  # noqa: E402

SCR = C.WT / ".scratch" / "p4_mutant_runtime"
if SCR.exists():
    shutil.rmtree(SCR)
for sub in ("runs", "run_records", "auth", "verification", "secrets"):
    (SCR / sub).mkdir(parents=True)
for f in ("events.jsonl", "progress.sqlite3", "nopecha-barrons-compatibility.json"):
    shutil.copy(C.RUNTIME / f, SCR / f)
for sub in ("runs", "run_records"):
    for p in (C.RUNTIME / sub).glob("20260930T0*"):
        shutil.copy(p, SCR / sub / p.name)
for sub in ("auth", "verification"):
    for d in (C.RUNTIME / sub).iterdir():
        (SCR / sub / d.name).mkdir()
for p in (C.RUNTIME / "secrets").glob("*.dpapi"):
    (SCR / "secrets" / p.name).write_bytes(b"")  # presence only; contents are never copied
bpath = next((SCR / "runs").glob("*-barrons-*.json"))
value = json.loads(bpath.read_text(encoding="utf-8"))
value["verification_repairs"] = 1
bpath.write_text(json.dumps(value), encoding="utf-8")

# (1) mutant
code = (
    "import sys, runpy\n"
    "sys.path.insert(0, %r)\n"
    "import p4_common as C\n"
    "from pathlib import Path\n"
    "C.RUNTIME = Path(%r)\n"
    "runpy.run_path(%r, run_name='__main__')\n" % (str(HERE), str(SCR), str(HERE / "p4_ac2_route.py"))
)
proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, encoding="utf-8")
tail = [x for x in (proc.stderr or "").splitlines() if x.strip()][-1:] or [""]
print("MUTANT: AC2 on a copy with barrons verification_repairs=1 -> rc=%d ; last stderr line: %s" % (proc.returncode, tail[0]))
mutant_fired = proc.returncode != 0 and "ASSERTION FAILED" in (proc.stderr or "")
print("MUTANT STATUS:", "FIRED-AS-EXPECTED" if mutant_fired else "DID-NOT-FIRE")
shutil.rmtree(SCR)


# (2) determinism
def run(name):
    out = subprocess.run([sys.executable, str(HERE / name)], capture_output=True, text=True, encoding="utf-8")
    lines = [x for x in out.stdout.splitlines() if not x.startswith("NOW_UTC") and "age_now" not in x]
    return out.returncode, lines


same = True
for name in ("p4_ac1_refusals.py", "p4_ac2_route.py"):
    a, b = run(name), run(name)
    print("DETERMINISM %s: rc %d/%d ; %d lines vs %d lines ; identical=%s" % (name, a[0], b[0], len(a[1]), len(b[1]), a == b))
    same = same and a == b
print("DETERMINISM STATUS:", "STABLE" if same else "UNSTABLE")

# (3) socket block negative control
restore = C.block_sockets()
import socket  # noqa: E402
try:
    socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    blocked = False
except RuntimeError as exc:
    blocked = True
    print("SOCKET CONTROL: creation raised:", exc)
restore()
print("SOCKET STATUS:", "BLOCKED" if blocked else "NOT-BLOCKED")
for p in HERE.glob("__pycache__"):
    shutil.rmtree(p, ignore_errors=True)
_ = os
sys.exit(0 if (mutant_fired and same and blocked) else 1)
