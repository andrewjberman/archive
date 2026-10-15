"""plant_r18.py -- the ISSUER's cut-time planted arms for c21.AC1-AC2, c23.AC1-AC3 and c22.AC1 (standing battery clause 1). NOT given to a worker, NOT a criterion. Run from the repo root.

Builds a GOOD catalog from the catalog at BASE_REF (bucket rule, the assets map, the 12 new Schwab rows, the tool-index bucket and source_group) and bad ones that change one thing each, then runs the checks
with C21_CATALOG / C23_CATALOG / C23_GW / C22_GW set and compares every exit code with the wanted one."""
import collections
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "c4c106aea1"
GW = "infra/aws/ec2/opal-gateway"
CATP = GW + "/app/refs/DATA_CATALOG.yaml"
MAP = json.load(open("org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round18/assets_group_map.json", encoding="ascii"))["rows"]
REGP = "infra/logic/registry/catalog_fork_keys.json"
SECS = ("silver_datasets", "portal_datasets", "harvest_datasets")
tmp = tempfile.mkdtemp(prefix="plant_r18_")


def git_show(path):
    r = subprocess.run(["git", "show", "%s:%s" % (BASE, path)], capture_output=True, check=True)
    return r.stdout


def dump(cat, name):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="ascii", newline="\n") as fh:
        yaml.safe_dump(cat, fh, sort_keys=False, allow_unicode=False, width=1000000)
    return p


def good_catalog():
    cat = yaml.safe_load(git_show(CATP).decode("ascii"))
    top = cat["bucket"]
    rows = {}
    for s in SECS:
        for r in cat[s]:
            rows[r["entity"]] = r
    for e, r in rows.items():
        b = r.get("bucket")
        if isinstance(b, str) and b.startswith("opal-data-"):
            continue
        r["bucket"] = "dynamodb" if (isinstance(b, str) and "ynamo" in b) else top
    for e, w in MAP.items():
        if e in rows:
            rows[e].update({"bucket": w["bucket"], "vendor": w["vendor"], "firm": w["firm"]})
            if "nl_tags" in w:
                rows[e]["nl_tags"] = list(w["nl_tags"])
                rows[e].pop("nl_tags_basis", None)
    tmpl = rows["opal_data_assets_silver_schwab_08242234_fact_accounts"] if "opal_data_assets_silver_schwab_08242234_fact_accounts" in rows else next(
        r for r in cat["silver_datasets"] if r["entity"].startswith("opal_data_assets_silver_schwab_08242234_fact_"))
    for e, w in MAP.items():
        if e not in rows:
            n = copy.deepcopy(tmpl)
            n.update({"entity": e, "bucket": w["bucket"], "vendor": w["vendor"], "firm": w["firm"], "read_tool": None, "tools": [], "gap_owner": "NFRA_OPLGTW", "retired": False, "key_template": "x/{date}"})
            n.pop("retired_reason", None)
            cat["silver_datasets"].append(n)
            rows[e] = n
    by_tool = collections.defaultdict(collections.Counter)
    for r in rows.values():
        if r.get("read_tool"):
            by_tool[r["read_tool"]][r["bucket"]] += 1
    for t in cat["tool_index"]:
        name = t["tool"]
        if t.get("member") == "a" and rows.get(str(t.get("index")), {}).get("bucket"):
            b = rows[str(t["index"])]["bucket"]
        elif name in by_tool:
            b = sorted(by_tool[name].items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        else:
            b = "graph" if t["member"] == "c" else top
        t["bucket"] = b
        sv = sorted({(rr["vendor"], rr["firm"]) for rr in rows.values() if rr.get("read_tool") == name and rr.get("bucket") in ("opal-data-assets", "opal-data-bd") and rr.get("vendor")})
        if sv:
            t["serves"] = [{"vendor": v, "firm": f} for v, f in sv]
        else:
            t.pop("serves", None)
        t["source_group"] = {"id": b, "name": b if b.startswith("opal-data-") else ("Microsoft 365" if b == "graph" else b), "kind": "bucket" if b.startswith("opal-data-") else ("graph" if b == "graph" else "store")}
    return cat


def run(script, ac, env):
    r = subprocess.run([sys.executable, os.path.join(HERE, script), ac], env=dict(os.environ, **env), capture_output=True, text=True, timeout=290)
    return r.returncode


def main():
    good = good_catalog()
    gp = dump(good, "good.yaml")
    arms = []

    def variant(name, fn):
        c = copy.deepcopy(good)
        fn(c)
        return dump(c, name + ".yaml")

    def rowof(c, e):
        for s in SECS:
            for r in c[s]:
                if r["entity"] == e:
                    return r

    nobucket = variant("nobucket", lambda c: rowof(c, "harvest_article_sentiment").pop("bucket"))
    dyn = variant("dynstr", lambda c: rowof(c, "dynamodb_dynamodb_opal_news_articles").__setitem__("bucket", "none (DynamoDB us-east-1)"))
    toolbad = variant("toolbad", lambda c: next(t for t in c["tool_index"] if t["tool"] == "harvest_search_articles").__setitem__("bucket", "opal-data-assets"))
    sgid = variant("sgid", lambda c: next(t for t in c["tool_index"] if t["tool"] == "harvest_search_articles")["source_group"].__setitem__("id", "x-store"))
    sgkind = variant("sgkind", lambda c: next(t for t in c["tool_index"] if t["tool"] == "harvest_search_articles")["source_group"].__setitem__("kind", "store"))
    moved = variant("moved", lambda c: rowof(c, "harvest_article_sentiment").__setitem__("bucket", "opal-data-news-v2"))
    victim = next(e for e in MAP if "schwab_08403355_fact" in e)
    wrongv = variant("wrongvendor", lambda c: rowof(c, victim).__setitem__("vendor", "orion"))
    stray = variant("stray", lambda c: rowof(c, "harvest_article_sentiment").__setitem__("vendor", "schwab"))
    infer = variant("inferred", lambda c: rowof(c, "schwab_dim_asset").__setitem__("nl_tags_basis", "inferred"))
    only11 = variant("only11", lambda c: c["silver_datasets"].remove(rowof(c, "opal_data_assets_silver_schwab_08403355_dim_transaction")))
    extra = variant("extrarow", lambda c: c["silver_datasets"].append(dict(rowof(c, "opal_data_assets_silver_schwab_08403355_dim_asset"), entity="an_unexpected_row")))
    gapbad = variant("gapbad", lambda c: rowof(c, "opal_data_assets_silver_schwab_08403355_dim_asset").__setitem__("gap_owner", "NFRA_MCPINDEX"))
    serves_t = next(t for t in good["tool_index"] if t.get("serves"))["tool"]
    sv_wrong = variant("sv_wrong", lambda c: next(t for t in c["tool_index"] if t["tool"] == serves_t)["serves"].append({"vendor": "orion", "firm": "cottonwood"}))
    sv_extra = variant("sv_extra", lambda c: next(t for t in c["tool_index"] if t["tool"] == "harvest_search_articles").__setitem__("serves", [{"vendor": "schwab", "firm": "49financial"}]))
    sv_miss = variant("sv_miss", lambda c: next(t for t in c["tool_index"] if t["tool"] == serves_t).pop("serves"))
    reg_ok = {"labels": sorted({w[k] for w in MAP.values() for k in ("vendor", "firm")})}

    # the gateway trees for c23.AC3: good (the base code + the good catalog) and a leaking one
    d = os.path.join(tmp, "tree_good")
    os.makedirs(d)
    subprocess.run("git archive %s %s | tar -x -C %s" % (BASE, GW, d.replace("\\", "/")), shell=True, check=True)
    root = os.path.join(d, GW)
    shutil.copyfile(gp, os.path.join(root, "app", "refs", "DATA_CATALOG.yaml"))
    leak = os.path.join(tmp, "tree_leak")
    shutil.copytree(d, leak)
    pi = os.path.join(leak, GW, "app", "integrations", "opal_discover", "integration.py")
    s = open(pi, encoding="utf-8").read()
    GOOD_TXT = ('    if scoped and not (row_firm in catalog_gate.KNOWN_FIRMS and principal_class == "firm" and principal_firm == row_firm):\n        return None\n'
                '    firm = row_firm if scoped else catalog_gate.OPAL_INTERNAL')
    LEAK_TXT = ('    if scoped and not (row_firm in catalog_gate.KNOWN_FIRMS and principal_class == "firm"):\n        return None\n'
                '    firm = principal_firm if scoped else catalog_gate.OPAL_INTERNAL')
    assert GOOD_TXT in s, "the base discover rule moved"
    open(pi, "w", encoding="utf-8", newline="\n").write(s.replace(GOOD_TXT, LEAK_TXT))
    # a registry without the labels
    regdir = os.path.join(tmp, "reg")
    os.makedirs(regdir)

    arms = [("c21.ac1 good", "c21_check.py", "ac1", {"C21_CATALOG": gp}, 0), ("c21.ac2 good", "c21_check.py", "ac2", {"C21_CATALOG": gp}, 0),
            ("c21.ac1 base catalog", "c21_check.py", "ac1", {"C21_CATALOG": os.path.join(tmp, "base.yaml")}, 1),
            ("c21.ac1 a row without bucket", "c21_check.py", "ac1", {"C21_CATALOG": nobucket}, 1), ("c21.ac1 a 'none (DynamoDB...)' string", "c21_check.py", "ac1", {"C21_CATALOG": dyn}, 1),
            ("c21.ac1 a valid S3 bucket moved", "c21_check.py", "ac1", {"C21_CATALOG": moved}, 1),
            ("c21.ac2 a tool bucket different from its rows", "c21_check.py", "ac2", {"C21_CATALOG": toolbad}, 1), ("c21.ac2 source_group.id != bucket", "c21_check.py", "ac2", {"C21_CATALOG": sgid}, 1),
            ("c21.ac2 source_group.kind wrong", "c21_check.py", "ac2", {"C21_CATALOG": sgkind}, 1),
            ("c23.ac1 good (registry labels supplied by the arm)", "c23_check.py", "ac1", {"C23_CATALOG": gp, "C23_REG_OVERRIDE": json.dumps(reg_ok)}, 0),
            ("c23.ac1 a wrong vendor on one row", "c23_check.py", "ac1", {"C23_CATALOG": wrongv, "C23_REG_OVERRIDE": json.dumps(reg_ok)}, 1),
            ("c23.ac1 a stray vendor", "c23_check.py", "ac1", {"C23_CATALOG": stray, "C23_REG_OVERRIDE": json.dumps(reg_ok)}, 1),
            ("c23.ac1 a row still inferred", "c23_check.py", "ac1", {"C23_CATALOG": infer, "C23_REG_OVERRIDE": json.dumps(reg_ok)}, 1),
            ("c23.ac1 the registry holds no labels", "c23_check.py", "ac1", {"C23_CATALOG": gp, "C23_REG_OVERRIDE": json.dumps({"labels": []})}, 1),
            ("c23.ac2 good", "c23_check.py", "ac2", {"C23_CATALOG": gp}, 0), ("c23.ac2 only 11 new rows", "c23_check.py", "ac2", {"C23_CATALOG": only11}, 1),
            ("c23.ac2 an unexpected extra row", "c23_check.py", "ac2", {"C23_CATALOG": extra}, 1), ("c23.ac2 a wrong gap owner", "c23_check.py", "ac2", {"C23_CATALOG": gapbad}, 1),
            ("c23.ac4 good", "c23_check.py", "ac4", {"C23_CATALOG": gp}, 0), ("c23.ac4 a serves pair added that no row has", "c23_check.py", "ac4", {"C23_CATALOG": sv_wrong}, 1),
            ("c23.ac4 serves on a tool no assets row names", "c23_check.py", "ac4", {"C23_CATALOG": sv_extra}, 1), ("c23.ac4 serves missing", "c23_check.py", "ac4", {"C23_CATALOG": sv_miss}, 1),
            ("c23.ac3 good tree", "c23_check.py", "ac3", {"C23_GW": root}, 0), ("c23.ac3 a leaking discover rule", "c23_check.py", "ac3", {"C23_GW": os.path.join(leak, GW)}, 1)]
    # the base catalog file for the c21.ac1 base arm
    open(os.path.join(tmp, "base.yaml"), "wb").write(git_show(CATP))
    ok = wrong = 0
    for label, script, ac, env, want in arms:
        rc = run(script, ac, env)
        if rc == want:
            ok += 1
            print("ARM ok:    %s -> rc=%d" % (label, rc))
        else:
            wrong += 1
            print("ARM WRONG: %s -> rc=%d want %d" % (label, rc, want))
    print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if wrong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
