#!/usr/bin/env python3
"""HVST-w-2 AC6 (guard a) -- a PLANTED test that WOULD fire the producer's real re-authentication, run INSIDE the
capture runner's own process and REFUSED by the in-process guard.

This wrapper does not touch lib/ and never runs the unguarded variant. It invokes the capture runner from the
command line exactly as AC1 does (`python .../ac1_capped_capture.py`), adding only `--planted-reauth-test`, which
makes the runner run the planted calls IN PLACE OF the producer run. The runner installs the guards in its own
process, prints the identity of the guard object each entry point resolves to, refuses to plant anything unless every
entry point is a guard, and prints per planted call: the refusal, browser_started, credential_read, network_attempted.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[7]
RUNNER = HERE / "ac1_capped_capture.py"
env = dict(os.environ)
env.pop("PYTHONPATH", None)          # no sitecustomize/PYTHONPATH delivery of anything, ever
cmd = [sys.executable, str(RUNNER), "--planted-reauth-test"]
print("AC6 -- invoking the capture runner in planted mode: %r" % (cmd,))
proc = subprocess.run(cmd, cwd=str(REPO), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out = proc.stdout.decode("utf-8", "replace")
print("---- runner output (VERBATIM) ----")
print(out)
print("---- end runner output ----")
refused = re.findall(r"^\[REFUSED\] ", out, re.M)
not_refused = re.findall(r"^\[NOT REFUSED\]|^\[UNEXPECTED", out, re.M)
ident = re.findall(r"IS_GUARD=True", out)
non_guard = re.findall(r"IS_GUARD=False", out)
browser_false = len(re.findall(r"browser_started: False", out))
cred_false = len(re.findall(r"credential_read: False", out))
print("runner rc=%d" % proc.returncode)
print("planted calls refused: %d; not refused/unexpected: %d" % (len(refused), len(not_refused)))
print("entry points resolving to a guard object inside the runner process: %d (non-guard: %d)" % (len(ident), len(non_guard)))
print("per-call 'browser_started: False' lines: %d; 'credential_read: False' lines: %d" % (browser_false, cred_false))
ok = (proc.returncode == 0 and refused and not not_refused and not non_guard and ident
      and browser_false == len(refused) and cred_false == len(refused))
print("AC6: %s" % ("PLANTED RE-AUTH REFUSED AT EVERY ENTRY POINT" if ok else "FAILED"))
sys.exit(0 if ok else 1)
