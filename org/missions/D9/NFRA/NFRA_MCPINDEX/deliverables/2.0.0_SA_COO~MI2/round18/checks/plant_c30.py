"""plant_c30.py -- the standing battery's planted arms for c30_check.py bucket (run from the repo root): a GOOD catalog must pass and each planted defect must fail.
scope and tests grade the real tree (a fresh generator run, the new test file), so their PASS arm is not plantable; the base FAIL is the arm for those.
Prints one line per arm and `PLANTED k of n`. Exit 0 when every arm behaves."""
import copy
import json
import os
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c30_check as c  # noqa: E402

base = c.base_catalog()
EXCL = json.load(open(c.R18 + "/entity_exclusions.json", encoding="utf-8"))["entities"]


def good():
    d = copy.deepcopy(base)
    for r in d["silver_datasets"]:
        if r["entity"].startswith("dynamodb_"):
            r["bucket"] = "dynamodb"
    for r in d["portal_datasets"]:
        r["bucket"] = "opal-data-portal-v2"
    d["silver_datasets"] = [r for r in d["silver_datasets"] if r["entity"] not in c.DROPPED and r["entity"] not in EXCL]
    for sec in ("portal_datasets", "harvest_datasets"):
        for r in d[sec]:
            if r.get("nl_tags_basis") == "inferred":
                r["nl_tags"] = ["curated one", "curated two", "curated three", "curated four"]
                r.pop("nl_tags_basis")
    return d


def run(cat):
    f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
    yaml.safe_dump(cat, f, sort_keys=False)
    f.close()
    env = dict(os.environ, C30_CATALOG=f.name)
    r = subprocess.run([sys.executable, os.path.join(HERE, "c30_check.py"), "bucket"], capture_output=True, text=True, env=env)
    os.unlink(f.name)
    return r.returncode


arms = []
g = good()
arms.append(("good catalog passes bucket", run(g) == 0))
x = copy.deepcopy(g)
x["silver_datasets"][[r["entity"] for r in x["silver_datasets"]].index("dynamodb_dynamodb_opal_keyword_intelligence")]["bucket"] = "none (DynamoDB us-east-1)"
arms.append(("a prose dynamodb bucket fails", run(x) != 0))
x = copy.deepcopy(g)
x["portal_datasets"][0].pop("bucket")
arms.append(("a portal_datasets row with no bucket fails", run(x) != 0))
x = copy.deepcopy(g)
for r in x["silver_datasets"]:
    if r["entity"].startswith("opal_data_etfs_"):
        r["bucket"] = "etfs"
        break
arms.append(("a changed etfs bucket spelling fails", run(x) != 0))
x = copy.deepcopy(g)
for r in x["silver_datasets"]:
    if r["entity"].startswith("opal_data_assets_"):
        r["business_meaning"] = "changed"
        break
arms.append(("an assets row changed outside the ASSETS keys fails the difference control", run(x) != 0))
x = copy.deepcopy(g)
x["silver_datasets"][0]["business_meaning"] = "changed"
if x["silver_datasets"][0]["entity"].startswith(c.RESEARCH_PREFIX):
    x["silver_datasets"][1]["business_meaning"] = "changed"
arms.append(("a changed non-bucket field fails", run(x) != 0))
x = copy.deepcopy(g)
x["silver_datasets"].append(copy.deepcopy(next(r for r in base["silver_datasets"] if r["entity"] in EXCL)))
arms.append(("an excluded entity still in the catalog fails", run(x) != 0))
x = copy.deepcopy(g)
x["needs"] = x["needs"][:-1]
arms.append(("a changed top-level section (needs) fails", run(x) != 0))
x = copy.deepcopy(g)
x["harvest_datasets"][0]["nl_tags_basis"] = "inferred"
arms.append(("a research row still inferred fails", run(x) != 0))
for name, ok in arms:
    print("ARM %s: %s" % ("ok " if ok else "BAD", name))
print("PLANTED %d of %d" % (sum(1 for _n, o in arms if o), len(arms)))
sys.exit(0 if all(o for _n, o in arms) else 1)
