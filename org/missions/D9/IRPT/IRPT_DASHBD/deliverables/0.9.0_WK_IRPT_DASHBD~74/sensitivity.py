"""TO-DB-b-99: threshold sensitivity of the DB-b-98 classifier, graded against THRESHOLDS.json (committed before this ran).
S3 GETs only; zero vendor calls. Usage: python sensitivity.py <repo_root> <rule_commit> [--cache <pickle>]  Writes SENSITIVITY.json beside this file.
Imports the DB-b-98 classifier unchanged and sets its module thresholds per setting."""
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
from botocore.config import Config

HERE = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
rule_commit = sys.argv[2]
cache = sys.argv[sys.argv.index("--cache") + 1] if "--cache" in sys.argv else None
TH = json.loads((HERE / "THRESHOLDS.json").read_bytes().decode("utf-8"))
sp = importlib.util.spec_from_file_location("c98", str(root / TH["classifier"]))
c98 = importlib.util.module_from_spec(sp)
sp.loader.exec_module(c98)

sp = importlib.util.spec_from_file_location("v2", str(root / c98.V2PY_REL))
v2m = importlib.util.module_from_spec(sp)
sp.loader.exec_module(v2m)
plan, (n_obj, bronze, gold, n_part, n_gold_accts) = v2m.load(root, cache)
v2 = json.loads((root / c98.V2_REL).read_bytes().decode("utf-8"))
outside = [x for x in v2["segments"] if x["verdict"] == "OUTSIDE"]
unexp = [x for x in outside if x["reason"] == "UNEXPLAINED"]
assert len(outside) == TH["denominator"] and len(unexp) == 510, (len(outside), len(unexp))
kept = {}
for x in outside:
    if x["reason"] != "UNEXPLAINED":
        kept[x["reason"]] = kept.get(x["reason"], 0) + 1
bdacct = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=32, retries={"max_attempts": 8, "mode": "standard"}))
need = {}
for x in unexp:
    need.setdefault(bdacct[x["account"]], set()).add((x["segment"]["start"], x["segment"]["end"]))
with ThreadPoolExecutor(16) as ex:
    bdx = dict(ex.map(lambda a: (a, c98.bd_fields(s3, a, need[a])), list(need)))

MECH = {"FLOW_TIMING": "V2 re-links the dated flow-bearing days under START flow timing and the gap closes; the BD side is its return only, BD's own transaction dates are not read (bd_side_dates_read false)",
        "INCOME_DATE": "V2 re-links with the dated income days removed and the gap closes; the BD side is its return only, BD's own income dates are not read (bd_side_dates_read false)"}
settings = {"peak_cut": TH["peak_cut"], "dollar_tie": TH["dollar_tie"]}
per, verdicts = {}, {}
for pc in TH["peak_cut"]:
    for dt in TH["dollar_tie"]:
        name = "%s|%s" % (pc, dt["name"])
        c98.NZ_FRAC, c98.DOLLAR_ABS, c98.DOLLAR_REL = pc, dt["abs"], dt["rel"]
        by = dict(kept)
        vs = []
        for x in unexp:
            bd = bdx[bdacct[x["account"]]][(x["segment"]["start"], x["segment"]["end"])]
            r = c98.classify(x, gold[x["account"]], bd)[0]
            vs.append(r)
            by[r] = by.get(r, 0) + 1
        per[name] = by
        verdicts[name] = vs
        print("%s %s sum=%d" % (name, by, sum(by.values())))

base = "0.01|current"
assert base == TH["baseline_setting"]
old = json.loads((HERE.parent / "0.9.0_WK_IRPT_DASHBD~73" / "UNEXPLAINED_CLASSIFIED.json").read_bytes().decode("utf-8"))
assert per[base] == old["by_reason"], ("baseline differs from DB-b-98", per[base], old["by_reason"])
cut = []
for i, x in enumerate(unexp):
    if verdicts[base][i] == "NEAR_ZERO_BASE":
        cut.append({"account": x["account"], "segment": x["segment"], "verdict_at": {n: verdicts[n][i] for n in per}})

reasons_all = sorted({r for by in per.values() for r in by})
meta = {}
for r in reasons_all:
    if r == "DEFECT":
        continue
    n0 = per[base].get(r, 0)
    cs = [by.get(r, 0) for by in per.values()]
    spread = max(cs) - min(cs)
    if r in kept:
        robust, basis = True, "assigned by V2, not threshold-dependent; count constant"
    else:
        robust = not (spread > 0.5 * n0)
        basis = "baseline %d; min %d max %d spread %d; limit %.1f" % (n0, min(cs), max(cs), spread, 0.5 * n0)
    mech = r in MECH
    meta[r] = {"claim": "inferred", "claim_basis": "no field of the landed Black Diamond record states a cause; the reason is read by a test from dollars, return, daysHeld or served series",
               "mechanical": mech, "mechanical_basis": MECH.get(r, "a threshold or fit test, not a two-sided read of flow or income dates"), "robust": robust, "robust_basis": basis, "count_min": min(cs), "count_max": max(cs), "baseline": n0}
final = dict(per[base])
regraded = 0
for r, m in meta.items():
    if not m["robust"]:
        regraded += final[r]
        final["UNEXPLAINED"] = final.get("UNEXPLAINED", 0) + final[r]
        final[r] = 0
rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~74", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-99", "vendor_calls": 0,
       "denominator": 990, "settings": settings, "per_setting": per, "cut_segments": cut, "final": {"by_reason": final, "reasons": meta,
       "regraded_to_unexplained": regraded}, "preregistration": {"thresholds_file": "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~74/THRESHOLDS.json",
       "rule_commit": rule_commit, "output_commit": "RECORDED_IN_NEXT_COMMIT"}}
(HERE / "SENSITIVITY.json").write_bytes((json.dumps(rec, indent=1) + "\n").encode("utf-8"))
print("OK: cut_segments %d; final %s" % (len(cut), final))
print({k: (v["claim"], v["robust"], v["robust_basis"]) for k, v in meta.items()})
