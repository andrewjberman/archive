"""ADVI_FIRMBKTS round 1 check for cell FB-t-2 (the mapping table and the reading list), issuer 2.0.0_SA_COO~F1.

Grades mapping.json and reading_list.json against census.json and lib/opal_naming.py address() (5 arms).
--root points at another tree (the issuer's positive control). Never edit this file.
"""
import argparse
import json
import os
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
FIRM = {"opal-data-bd": "49financial", "opal-data-inf": "inflection", "opal-data-cot": "cottonwood"}
DECISIONS = {("opal-data-inf", "gold/meta/pipeline-complete.json"): "FWD-7",
             ("opal-data-inf", "orion/jwt/current.json"): "FWD-8"}
DISPOSITIONS = ("MOVE", "HOME", "RETIRE", "DECISION", "FAULT")
SEGMENTS = ("source", "scope", "tier", "table", "partition")


def _root(arg):
    if arg:
        return arg
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip()


def _load(root, name):
    with open(os.path.join(root, DELIV, name), encoding="utf-8") as fh:
        return json.load(fh)


def arms(root):
    sys.path.insert(0, os.path.join(_root(None), "lib"))  # the builders always come from the checkout
    import opal_naming
    census = _load(root, "census.json")
    mapping = _load(root, "mapping.json")
    rl = _load(root, "reading_list.json")
    res = []
    rows = mapping.get("rows") or []
    res.append(("M1 mapping.json names the census it placed (census_listed_at equals census.json listed_at)",
                bool(rows) and mapping.get("census_listed_at") == census.get("listed_at")))

    want = {(b, c["prefix"]): c for b, bd in census["buckets"].items() for c in bd["classes"]}
    got = [(r.get("bucket"), r.get("prefix")) for r in rows]
    dup = len(got) - len(set(got))
    missing = set(want) - set(got)
    extra = set(got) - set(want)
    print("  census classes=%d mapping rows=%d duplicates=%d unplaced=%d not-in-census=%d"
          % (len(want), len(got), dup, len(missing), len(extra)))
    for m in sorted(missing)[:5]:
        print("    UNPLACED %s %s" % m)
    res.append(("M2 every census class has exactly one row and no row names a class the census lacks",
                not dup and not missing and not extra))

    m3 = True
    counts = dict.fromkeys(DISPOSITIONS, 0)
    for r in rows:
        d = r.get("disposition")
        if d not in DISPOSITIONS:
            print("    OFF-ENUM %s %s %r" % (r.get("bucket"), r.get("prefix"), d))
            m3 = False
            continue
        counts[d] += 1
        k = (r.get("bucket"), r.get("prefix"))
        if (k in DECISIONS) != (d == "DECISION") or (d == "DECISION" and r.get("decision_ref") != DECISIONS[k]):
            print("    DECISION-ROW %s %s %s" % (k[0], k[1], d))
            m3 = False
        if d in ("MOVE", "HOME") and not (isinstance(r.get("dest"), dict) and r.get("address") and r.get("dest_pattern")
                                          and isinstance(r.get("reading_ids"), dict)):
            m3 = False
        if d == "RETIRE" and not r.get("reason"):
            m3 = False
        if d == "FAULT" and not r.get("fault_row"):
            m3 = False
        if not r.get("rule"):
            m3 = False
    print("  dispositions: %s" % ", ".join("%s=%d" % kv for kv in counts.items()))
    res.append(("M3 every row's disposition is on the enum with its required fields; the two DECISION rows are "
                "exactly Door 6's key (FWD-7) and B2 (FWD-8)", m3))

    m4 = True
    placed = [r for r in rows if r.get("disposition") in ("MOVE", "HOME")]
    for r in placed:
        dest = r["dest"]
        try:
            built = opal_naming.address(*[dest[s] for s in SEGMENTS], object=dest.get("object"))
        except Exception as e:
            print("    BUILDER-REFUSED %s %s: %s" % (r["bucket"], r["prefix"], str(e)[:160]))
            m4 = False
            continue
        if built != r["address"]:
            print("    TYPED %s %s: stored %r, builder %r" % (r["bucket"], r["prefix"], r["address"], built))
            m4 = False
        if r["disposition"] == "MOVE":
            firm = FIRM[r["bucket"]]
            if dest["scope"] != firm or not built.startswith("s3://opal-data-%s/" % firm):
                print("    SCOPE %s %s -> %s" % (r["bucket"], r["prefix"], built))
                m4 = False
        elif dest["tier"] not in ("bronze", "silver") or not built.startswith("s3://opal-data-assets/"):
            print("    HOME %s %s -> %s" % (r["bucket"], r["prefix"], built))
            m4 = False
    print("  placed rows graded through address(): %d" % len(placed))
    res.append(("M4 every MOVE/HOME address is exactly address()'s output; MOVE scope is the bucket's firm in its "
                "firm bucket, HOME is bronze/silver in opal-data-assets", m4 and bool(placed)))

    m5 = True
    locs = rl.get("locations") or []
    byid = {}
    for e in locs:
        if set(e) != {"id", "location"} or e["id"] in byid or "/" in e["id"] or "opal" in e["id"]:
            m5 = False
        byid[e["id"]] = e.get("location")
    samples = {(b, c["prefix"]): c["sample_key"] for b, bd in census["buckets"].items() for c in bd["classes"]}
    arm_of = {}
    for r in placed:
        ids = r["reading_ids"]
        if byid.get(ids.get("canonical")) != r["address"]:
            m5 = False
        if byid.get(ids.get("legacy")) != "s3://%s/%s" % (r["bucket"], samples[(r["bucket"], r["prefix"])]):
            m5 = False
        arm_of[ids.get("canonical")] = "c"
        arm_of[ids.get("legacy")] = "l"
    if len(locs) != 2 * len(placed) or set(arm_of) != set(byid):
        m5 = False
    half = [arm_of.get(e["id"]) for e in locs[: len(locs) // 2]]
    if half and len(set(half)) < 2:
        m5 = False
    print("  reading list entries=%d (2 x %d placed rows), first-half arms=%s" % (len(locs), len(placed), sorted(set(half))))
    res.append(("M5 reading_list.json carries only id and location, one canonical and one legacy entry per placed "
                "row, ids opaque, the two arms interleaved", m5))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = arms(root)
    except Exception as e:
        print("ABSENT or unreadable: %s (%s: %s)" % (DELIV, type(e).__name__, str(e)[:160]))
        res = [("mapping.json, reading_list.json and census.json present", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 1 MAPPING: %d of 5 arms" % n)
    sys.exit(0 if n == 5 else 1)


if __name__ == "__main__":
    main()
