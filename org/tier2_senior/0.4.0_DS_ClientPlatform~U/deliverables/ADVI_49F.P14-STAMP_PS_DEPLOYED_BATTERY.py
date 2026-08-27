"""ADVI_49F.P14-STAMP -- PS-2 / PS-3 / PS-4 / PS-5b fired against the DEPLOYED bundle.

The face asks for the arms against the DEPLOYED objects, not the repo copies -- a distinct
claim, and the only one that catches a deploy that mangled or landed the wrong file at the
right key. Everything runs out of a clean directory populated from the whole
s3://opal-data-49financial/_code/ prefix, which is the bundle the SSM document actually
executes (a hand-picked subset is a DIFFERENT subject -- my first attempt did that and died
at a05, which needs ref/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_*.json).

  PS-2  pre-epoch date, flagged, FULL CHAIN -> all FOUR manifests declared-historical-pre-epoch,
        short_read_tie_ran=False, attested=-1
  PS-3  attested date, flagless, FULL CHAIN -> converter-attested end to end with the real count
  PS-4  a00 record removed -> each of the three writers REFUSES loudly, naming the record
  PS-5b flagless entrypoint invariance (DH-6 precedent): a00's + c02's argv differ from the
        pre-STAMP vintage by EXACTLY the two ruled mirror tokens, and NOTHING else changed.

EXPECTED-DELTA WIDENING (CTO ruling 76887 option (a), face amended by COO @0b76eeaec2): c02's
chain stage now carries the same `m` token as a00's. Before that token, c02's emit block --
gated `if args.local_out or args.upload` -- was SKIPPED on every dry-run, so canonical/twr_daily
wrote no local manifest and PS-2/PS-3 were structurally 3-of-4 in the sanctioned QA form. This
run is the same battery against the redeployed entrypoint.

Nothing is uploaded: every chain invocation omits --upload.

Author: 0.4.0_DS_ClientPlatform~U | ADVI_49F.P14-STAMP | 2026-08-27
"""
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path("C:/Users/AndrewBerman/Desktop/ajb_workspace")
RUNNERS = REPO / "data/assets/scripts/gold/runners_49f"
sys.path.insert(0, str(RUNNERS))
import runner_common as rc  # noqa: E402

SCRATCH = Path("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
               "C--Users-AndrewBerman-Desktop-ajb-workspace/"
               "9c462caa-4942-4b63-85d3-1783cfb1645f/scratchpad")
STAGE = SCRATCH / "_ps_deployed2"
if STAGE.exists():
    shutil.rmtree(STAGE, ignore_errors=True)
STAGE.mkdir(parents=True)
pag = rc.s3().get_paginator("list_objects_v2")
keys = [o["Key"] for page in pag.paginate(Bucket="opal-data-49financial", Prefix="_code/")
        for o in page.get("Contents", []) if not o["Key"].endswith("/")]
print(f"Syncing the DEPLOYED bundle: {len(keys)} objects under _code/")
for k in keys:
    dst = STAGE / k[len("_code/"):]
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(rc.s3().get_object(Bucket="opal-data-49financial", Key=k)["Body"].read())
print(f"  staged {len(keys)} objects into {STAGE}")
if not (STAGE / "lib" / "trading_calendar.py").is_file():
    (STAGE / "lib").mkdir(exist_ok=True)
    shutil.copy2(REPO / "lib/trading_calendar.py", STAGE / "lib/trading_calendar.py")
    print("  NOTE: lib/trading_calendar.py not in the bundle -- vendored from repo, stated")

PRE, ATT = "2026-03-24", "2026-08-24"
TABLES = (("dimensions", "dim_account"), ("canonical", "flow_ledger"),
          ("canonical", "nna_canonical"), ("canonical", "twr_daily"))
results = {}


def manifests(mirror, date):
    out = {}
    for tier, tbl in TABLES:
        p = Path(mirror) / tier / tbl / f"date={date}" / "manifest.json"
        out[f"{tier}/{tbl}"] = (json.loads(p.read_text(encoding="utf-8"))
                                if p.is_file() else None)
    return out


def show(m):
    for k, v in m.items():
        print(f"    {k:<26} {(v or {}).get('attestation_basis', 'NO MANIFEST'):<30} "
              f"tie_ran={(v or {}).get('short_read_tie_ran', '-')} "
              f"attested={(v or {}).get('attested', '-')}")


def run_chain(date, flagged, tag):
    wd = STAGE / f"wd_{tag}"
    if wd.exists():
        shutil.rmtree(wd, ignore_errors=True)
    args = [sys.executable, "chain_49f_entrypoint.py", "--date", date, "--workdir", str(wd)]
    if flagged:
        args.append("--declared-historical")
    p = subprocess.run(args, cwd=str(STAGE), capture_output=True, text=True)
    blob = (p.stdout or "") + (p.stderr or "")
    tail = [x for x in blob.splitlines() if "CHAIN" in x]
    print(f"    rc={p.returncode} | {tail[-1][:90] if tail else 'no CHAIN line'}")
    return p.returncode, wd / "canon_mirror"


print(f"\n{'='*76}\nPS-2  PRE-EPOCH ARM on DEPLOYED bytes, full chain, {PRE}, flagged")
rc2, mir2 = run_chain(PRE, True, "pre")
m2 = manifests(mir2, PRE)
show(m2)
# ALL FOUR manifests, ALL THREE ruled fields. My first pass checked `attested` on dim_account
# ONLY -- which is the implementation's shape, not the criterion's -- and scored 4-of-4 while
# the third field reached exactly 1 of 4 tables. The denominator is printed either way now.
ps2 = rc2 == 0 and all(v and v.get("attestation_basis") == "declared-historical-pre-epoch"
                       and v.get("short_read_tie_ran") is False
                       and v.get("attested") == -1 for v in m2.values())
print(f"    all four carry the -1 sentinel: "
      f"{sum(1 for v in m2.values() if (v or {}).get('attested') == -1)} of {len(m2)}")
results["PS-2"] = ps2

print(f"\n{'='*76}\nPS-3  ATTESTED CONTROL ARM on DEPLOYED bytes, full chain, {ATT}, flagless")
rc3, mir3 = run_chain(ATT, False, "att")
m3 = manifests(mir3, ATT)
show(m3)
att_n = (m3["dimensions/dim_account"] or {}).get("attested")
ps3 = rc3 == 0 and all(v and v.get("attestation_basis") == "converter-attested"
                       and v.get("short_read_tie_ran") is True
                       and v.get("attested") == att_n for v in m3.values())
ps3 = ps3 and isinstance(att_n, int) and att_n > 0
print(f"    all four carry the SAME real count: "
      f"{sum(1 for v in m3.values() if (v or {}).get('attested') == att_n)} of {len(m3)}")
print(f"    real attested count present and positive: {att_n}")
results["PS-3"] = ps3

print(f"\n{'='*76}\nPS-4  REFUSAL ARM on DEPLOYED bytes -- a00 record REMOVED, writers must refuse")
if mir3.exists():
    shutil.rmtree(mir3 / "dimensions" / "dim_account", ignore_errors=True)
ps4 = {}
for script, extra in (("c00_flow_ledger.py",
                       ["--ref-local", str(mir3), "--boundary-local", str(mir3),
                        "--prices-local", str(mir3)]),
                      ("c01_nna_canonical.py", ["--canonical-local", str(mir3)]),
                      ("c02_twr_engine.py", ["--canonical-local", str(mir3),
                                             "--calendar-local", str(mir3)])):
    p = subprocess.run([sys.executable, script, "--date", ATT, "--dry-run",
                        "--local-out", str(mir3)] + extra,
                       cwd=str(STAGE), capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    named = "attestation basis unavailable: no a00 record" in out
    ps4[script] = (p.returncode != 0 and named)
    print(f"    {script:<26} rc={p.returncode} refuses-naming-the-record={named}")
results["PS-4"] = all(ps4.values())

print(f"\n{'='*76}\nPS-5b FLAGLESS ENTRYPOINT INVARIANCE on DEPLOYED bytes -- expected delta is "
      f"EXACTLY\n      the two ruled mirror tokens (a00 per 76736(i), c02 per 76887)")
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("dep_chain", STAGE / "chain_49f_entrypoint.py")
dep = importlib.util.module_from_spec(spec)
sys.modules["dep_chain"] = dep
spec.loader.exec_module(dep)
PRE_STAMP = "43a2b1d872"   # the last vintage before ruling (i) landed a00's token
tmp = STAGE / "_pre_chain_vintage.py"
tmp.write_bytes(subprocess.run(
    ["git", "show", f"{PRE_STAMP}:data/assets/scripts/gold/runners_49f/chain_49f_entrypoint.py"],
    capture_output=True, check=True, cwd=str(REPO)).stdout)
spec2 = importlib.util.spec_from_file_location("pre_chain", tmp)
pre = importlib.util.module_from_spec(spec2)
sys.modules["pre_chain"] = pre
spec2.loader.exec_module(pre)
wd = STAGE / "wd_inv"
mirror_tok = ["--local-out", str(wd / "canon_mirror")]
old = dict(pre._stage_list(ATT, False, wd, False))
new = dict(dep._stage_list(ATT, False, wd, False))
diffs = {k: (old[k], new[k]) for k in old if old[k] != new[k]}
print(f"    stages compared: {len(old)} | stages whose argv changed: {len(diffs)}")
# MULTISET DIFF, not membership. The membership form FAILED this arm for the wrong reason on
# the first run: c02's argv already contained the mirror PATH as the VALUE of --canonical-local,
# so `[x for x in n if x not in o]` deduped the added path away and reported the delta as
# ['--local-out'] alone. A set/membership test cannot see a second copy of a token that is
# already present -- and it failed in the direction that under-reports the change.
def added(o, n):
    c = Counter(n)
    c.subtract(Counter(o))
    return [x for x in n if c[x] > 0 and not c.__setitem__(x, c[x] - 1)]


def removed(o, n):
    c = Counter(o)
    c.subtract(Counter(n))
    return [x for x in o if c[x] > 0 and not c.__setitem__(x, c[x] - 1)]


for k, (o, n) in diffs.items():
    print(f"      {k}: added {added(o, n)}  removed {removed(o, n)}")
ps5b = (set(diffs) == {"a00_dim_account", "c02_twr_daily"}
        and all(added(o, n) == mirror_tok and not removed(o, n) for o, n in diffs.values()))
# NEGATIVE CONTROL: the same predicate must REJECT a third stage changing, and must reject a
# token that is not the ruled one. Both are constructed, not asserted.
fake = dict(new)
fake["a03_dim_security"] = new["a03_dim_security"] + ["--local-out", str(wd / "canon_mirror")]
neg1 = set({k: 1 for k in old if old[k] != fake[k]}) != {"a00_dim_account", "c02_twr_daily"}
fake2 = dict(new)
fake2["c02_twr_daily"] = new["c02_twr_daily"] + ["--declared-historical"]
d2 = {k: (old[k], fake2[k]) for k in old if old[k] != fake2[k]}
neg2 = not all(added(o, n) == mirror_tok for o, n in d2.values())
print(f"    exactly the two ruled stages, each by exactly the mirror token: {ps5b}")
print(f"    NEG CTRL a third stage changing REJECTED: {neg1} | "
      f"a non-ruled token on c02 REJECTED: {neg2}")
results["PS-5b"] = ps5b and neg1 and neg2

print(f"\n{'='*76}")
for k, v in results.items():
    print(f"  {k:<7} {'PASS' if v else '*** FAIL ***'}")
print(f"  ALL: {all(results.values())}")
sys.exit(0 if all(results.values()) else 1)
