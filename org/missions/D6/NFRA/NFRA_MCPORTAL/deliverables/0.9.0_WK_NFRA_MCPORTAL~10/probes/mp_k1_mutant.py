"""CONTROLS.mutant for MP-k-1: drop the 'call must be OPEN now' check from the close handler, run the refusal test,
restore the exact original bytes. Expect the real run to pass and the mutant run to fail test_close_refuses_call_not_open."""
import os
import subprocess
import sys
root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
gw = os.path.join(root, "infra", "aws", "ec2", "opal-gateway")
target = os.path.join(gw, "app", "admin_fabric_calls.py")
cmd = [sys.executable, "-m", "pytest", "tests/test_admin_fabric_calls.py", "-k", "test_close_refuses_call_not_open",
       "-q", "-p", "no:cacheprovider", "--color=no"]
def run():
    p = subprocess.run(cmd, cwd=gw, capture_output=True, text=True)
    return p.returncode, (p.stdout.strip().splitlines() or [""])[-1]
orig = open(target, "rb").read()
needle = b"if call_id not in open_ids:"
assert orig.count(needle) == 1
real = run()
try:
    open(target, "wb").write(orig.replace(needle, b"if False:"))
    mutant = run()
finally:
    open(target, "wb").write(orig)
assert open(target, "rb").read() == orig
print("REAL:", real, "MUTANT:", mutant)
print("VERDICT:", "PASS-MP-K1-MUTANT" if real[0] == 0 and mutant[0] != 0 else "FAIL-MP-K1-MUTANT")
