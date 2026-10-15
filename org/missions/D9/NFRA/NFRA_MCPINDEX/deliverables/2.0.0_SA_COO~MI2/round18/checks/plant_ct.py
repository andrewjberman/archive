"""plant_ct.py -- planted arms for ct_check.py (run from the repo root): a good group-map file passes and each planted defect fails. Exit 0 when every arm behaves."""
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ct_check as ct  # noqa: E402

sys.path.insert(0, os.path.join("workflows", "atom_decomposition"))
import derive_nl_tags  # noqa: E402

spec = json.load(open(os.path.join(HERE, "slices.json"), encoding="utf-8"))
allrows = ct.rows()


def good(slice_id):
    out = {}
    for e in spec[slice_id]["entities"]:
        r = allrows[e]
        text = e + " " + str(r.get("business_meaning") or "") + " " + " ".join(str(q) for q in (r.get("example_questions") or []))
        w = next(x for x in re.findall(r"[a-z]{4,}", text.lower()))
        out[e] = {"nl_tags": [w + " zzq", "zzq one", "zzq two", "zzq three", "zzq four"]}
    return {"rows": out}


def run(slice_id, data):
    d = tempfile.mkdtemp(prefix="ct_plant_")
    json.dump(data, open(os.path.join(d, os.path.basename(spec[slice_id]["file"])), "w"))
    env = dict(os.environ, CT_DIR=d)
    return subprocess.run([sys.executable, os.path.join(HERE, "ct_check.py"), "slice", slice_id], capture_output=True, text=True, env=env).returncode


def mutate(fn):
    x = copy.deepcopy(good("p1"))
    fn(x["rows"], sorted(x["rows"])[0])
    return x


def copied(rows, k):
    r = allrows[k]
    rows[k]["nl_tags"] = (derive_nl_tags.derive_tags(k, r.get("business_meaning") or "", r.get("example_questions") or []) + ["zzq one", "zzq two"])[:6]


def repeated(rows, k):
    t = rows[k]["nl_tags"]
    rows[k]["nl_tags"] = [t[0], t[0], t[2], t[3], t[4]]


arms = [("good file passes", run("p1", good("p1")) == 0)]
arms.append(("fewer than 4 tags fails", run("p1", mutate(lambda r, k: r[k].update(nl_tags=r[k]["nl_tags"][:3]))) != 0))
arms.append(("more than 6 tags fails", run("p1", mutate(lambda r, k: r[k].update(nl_tags=r[k]["nl_tags"] + ["zzq five", "zzq six"]))) != 0))
arms.append(("a tag with a symbol fails", run("p1", mutate(lambda r, k: r[k]["nl_tags"].append("bad tag!"))) != 0))
arms.append(("an uppercase tag fails", run("p1", mutate(lambda r, k: r[k]["nl_tags"].append("Has Upper"))) != 0))
arms.append(("a one-word tag fails", run("p1", mutate(lambda r, k: r[k]["nl_tags"].append("single"))) != 0))
arms.append(("a missing entity fails", run("p1", mutate(lambda r, k: r.pop(k))) != 0))
arms.append(("an extra entity fails", run("p1", mutate(lambda r, k: r.update(extra_entity={"nl_tags": ["a b", "c d", "e f", "g h"]}))) != 0))
arms.append(("an extra key beside nl_tags fails", run("p1", mutate(lambda r, k: r[k].update(bucket="x"))) != 0))
arms.append(("a repeated tag fails", run("p1", mutate(repeated)) != 0))
arms.append(("copied derived tags fail", run("p1", mutate(copied)) != 0))
arms.append(("tags with no word from the row fail", run("p1", mutate(lambda r, k: r[k].update(nl_tags=["zzqx aa", "zzqx bb", "zzqx cc", "zzqx dd"]))) != 0))
for n, ok in arms:
    print("ARM %s: %s" % ("ok " if ok else "BAD", n))
print("PLANTED %d of %d" % (sum(1 for _n, o in arms if o), len(arms)))
sys.exit(0 if all(o for _n, o in arms) else 1)
