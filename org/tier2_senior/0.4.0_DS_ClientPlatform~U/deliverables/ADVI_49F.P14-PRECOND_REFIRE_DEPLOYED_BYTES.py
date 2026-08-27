"""THE CONVERGED DEPLOY CONDITION (COO 76509 + CTO 76515's folded delta, extended by CTO 76526):
re-fire the exercised arms AGAINST THE DEPLOYED BYTES, not against the working tree.

This is a distinct claim from anything run before the deploy. Every earlier arm exercised the
REPO copy; these fetch the three objects from s3://opal-data-49financial/_code/ into a clean
directory and run THOSE. If the deploy mangled anything -- truncation, a line-ending mishap, the
wrong file at the right key -- only this catches it.

  ARM 1  flagless a00 on the pre-epoch date -> the ORIGINAL refusal, matched on its REASON.
         This arm IS the nightly's safety: the scheduled fire passes no flag.
  ARM 2  flagged a00 at the measured epoch  -> the mode's own refusal, verbatim.
         The arm whose silent loss would turn the mode into a bypass.
  ARM 3  flagless ENTRYPOINT                -> a00's argv byte-identical to the pre-DH-6 vintage.
         The nightly document passes no new parameter, so this is the nightly's other half.
"""
import importlib.util
import subprocess
import sys
import shutil
from pathlib import Path

REPO = Path("C:/Users/AndrewBerman/Desktop/ajb_workspace")
RUNNERS = REPO / "data/assets/scripts/gold/runners_49f"
sys.path.insert(0, str(RUNNERS))
import runner_common as rc  # noqa: E402

STAGE = Path(sys.argv[0]).resolve().parent / "_deployed_bytes"
if STAGE.exists():
    shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)
FILES = ["a00_runner.py", "a00_dim_account.py", "chain_49f_entrypoint.py"]

print("Fetching the DEPLOYED objects (not the repo copies) into a clean directory:")
for f in FILES:
    body = rc.s3().get_object(Bucket="opal-data-49financial", Key=f"_code/{f}")["Body"].read()
    (STAGE / f).write_bytes(body)
    same_as_repo = body == (RUNNERS / f).read_bytes()
    print(f"  {f:<26} {len(body):>7,} B   identical to repo copy: {same_as_repo}")
# the deployed runner imports runner_common and the core; vendor what it needs beside it
for dep in ("runner_common.py", "POLICY_BLOCK.json"):
    shutil.copy2(RUNNERS / dep, STAGE / dep)
(STAGE / "lib").mkdir(exist_ok=True)
shutil.copy2(REPO / "lib/trading_calendar.py", STAGE / "lib/trading_calendar.py")

PRE_EPOCH = "2026-03-24"
ORIGINAL_REFUSAL = "no conversion record attests fact_acc"
results = {}


def run(args, label):
    p = subprocess.run([sys.executable, "a00_runner.py"] + args, cwd=str(STAGE),
                       capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    print(f"\n--- {label}   rc={p.returncode}")
    for ln in [x for x in out.splitlines() if x.strip()][:3]:
        print(f"    | {ln[:145]}")
    return p.returncode, out


print("\n" + "=" * 78)
print("ARM 1 -- FLAGLESS on the pre-epoch date, from DEPLOYED bytes (the nightly's safety)")
rc1, out1 = run(["--date", PRE_EPOCH, "--dry-run"], "deployed a00, no flag")
arm1 = rc1 != 0 and ORIGINAL_REFUSAL in out1
print(f"    reproduces the ORIGINAL refusal REASON (not merely non-zero rc): {arm1}")
results["ARM1 flagless refusal preserved"] = arm1

print("\n" + "=" * 78)
print("ARM 2 -- FLAGGED at the measured epoch, from DEPLOYED bytes (the anti-bypass arm)")
spec = importlib.util.spec_from_file_location("dep_a00", STAGE / "a00_runner.py")
mod = importlib.util.module_from_spec(spec)
sys.modules["dep_a00"] = mod
spec.loader.exec_module(mod)
epoch = mod.attestation_epoch()
print(f"    epoch measured BY THE DEPLOYED CODE: {epoch}")
rc2, out2 = run(["--date", epoch, "--dry-run", "--declared-historical"],
                f"deployed a00, flag at epoch {epoch}")
arm2 = rc2 != 0 and "PRE-EPOCH dates only" in out2 and epoch in out2
print(f"    refuses loudly, naming the epoch and the reason: {arm2}")
results["ARM2 mode guard survived deploy"] = arm2

print("\n" + "=" * 78)
print("ARM 3 -- FLAGLESS ENTRYPOINT, from DEPLOYED bytes (the nightly's other half)")
spec = importlib.util.spec_from_file_location("dep_chain", STAGE / "chain_49f_entrypoint.py")
dep_chain = importlib.util.module_from_spec(spec)
sys.modules["dep_chain"] = dep_chain
spec.loader.exec_module(dep_chain)
PRE_DH6 = "bc585df628"
tmp = RUNNERS / "_refire_tmp_pre.py"
tmp.write_bytes(subprocess.run(
    ["git", "show", f"{PRE_DH6}:data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py"],
    capture_output=True, check=True, cwd=str(REPO)).stdout)
try:
    spec = importlib.util.spec_from_file_location("pre_chain", tmp)
    pre_chain = importlib.util.module_from_spec(spec)
    sys.modules["pre_chain"] = pre_chain
    spec.loader.exec_module(pre_chain)
    wd = STAGE / "wd"
    old = dict(pre_chain._stage_list(PRE_EPOCH, False, wd))
    new = dict(dep_chain._stage_list(PRE_EPOCH, False, wd, False))
    arm3 = old == new
    print(f"    deployed entrypoint, flagless: a00 argv == pre-DH-6 vintage: "
          f"{old['a00_dim_account'] == new['a00_dim_account']}")
    print(f"    ALL {len(old)} stages identical: {arm3}")
    flagged = dict(dep_chain._stage_list(PRE_EPOCH, False, wd, True))
    carries = "--declared-historical" in flagged["a00_dim_account"]
    leaked = [n for n, a in flagged.items()
              if n != "a00_dim_account" and "--declared-historical" in a]
    print(f"    and flagged, the DEPLOYED entrypoint carries it to a00: {carries}, leaks: {leaked}")
    arm3 = arm3 and carries and not leaked
finally:
    tmp.unlink(missing_ok=True)
    print(f"    temp baseline removed from producer tree: {not tmp.exists()}")
results["ARM3 entrypoint flagless byte-identical + carries when flagged"] = arm3

print("\n" + "=" * 78)
for k, v in results.items():
    print(f"  {'PASS' if v else '*** FAIL ***':<14} {k}")
ok = all(results.values())
print(f"  ALL ARMS ON DEPLOYED BYTES: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
