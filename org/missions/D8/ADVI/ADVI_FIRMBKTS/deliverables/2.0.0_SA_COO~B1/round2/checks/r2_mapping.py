"""ADVI_FIRMBKTS round 2 check for cell FB-e-1 (the mapping table's repair), issuer 2.0.0_SA_COO~B1.

--arms structure  grades deliverables/mapping_v2.json against census.json, the round-1 mapping.json and
                  lib/opal_naming.py address() (5 arms).
--arms repair     grades the repair itself: every round-1 FAULT class disposed, every remaining fault owned,
                  every destination-table collision ruled, the human view present (4 arms).
--root points at another tree (the issuer's positive control). Never edit this file.
Plain ASCII output; the last line carries the arm count.
"""
import argparse
import json
import os
import re
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
FIRM = {"opal-data-bd": "49financial", "opal-data-inf": "inflection", "opal-data-cot": "cottonwood"}
DECISIONS = {("opal-data-inf", "gold/meta/pipeline-complete.json"): "FWD-7",
             ("opal-data-inf", "orion/jwt/current.json"): "FWD-8"}
DISPOSITIONS = ("MOVE", "HOME", "RETIRE", "DECISION", "FAULT")
SEGMENTS = ("source", "scope", "tier", "table", "partition")
SERIAL_RE = re.compile(r"^\d+\.\d+\.\d+_[A-Z]{2}_[A-Za-z0-9]+(~[A-Za-z0-9]+)?$")


def _root(arg):
    if arg:
        return arg
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip()


def _load(root, name):
    with open(os.path.join(root, DELIV, name), encoding="utf-8") as fh:
        return json.load(fh)


def _docs(root):
    sys.path.insert(0, os.path.join(_root(None), "lib"))  # the builders always come from the checkout
    import opal_naming
    return opal_naming, _load(root, "census.json"), _load(root, "mapping.json"), _load(root, "mapping_v2.json")


def structure(root):
    naming, census, m1, m2 = _docs(root)
    rows = m2.get("rows") or []
    res = []
    res.append(("V1 mapping_v2.json names the census it placed and the table it supersedes",
                bool(rows) and m2.get("census_listed_at") == census.get("listed_at")
                and m2.get("supersedes") == "mapping.json"))

    want = {(b, c["prefix"]): c["objects"] for b, bd in census["buckets"].items() for c in bd["classes"]}
    r1_fault = {(r["bucket"], r["prefix"]) for r in m1["rows"] if r["disposition"] == "FAULT"}
    regrids = {(g.get("bucket"), g.get("parent")): g for g in (m2.get("regrids") or [])}
    own = [(r.get("bucket"), r.get("prefix")) for r in rows if not r.get("parent")]
    kids = [(r.get("bucket"), r.get("prefix"), r.get("parent")) for r in rows if r.get("parent")]
    dup = len(own) + len(kids) - len(set(own) | {(b, p) for b, p, _ in kids})
    ok2 = not dup
    covered = set(own)
    for b, p, parent in kids:
        if (b, parent) not in regrids or not p.startswith(parent):
            print("    CHILD-WITHOUT-REGRID %s %s (parent %s)" % (b, p, parent))
            ok2 = False
    for (b, parent), g in regrids.items():
        if (b, parent) not in r1_fault:
            print("    REGRID-OF-A-PLACED-CLASS %s %s" % (b, parent))
            ok2 = False
        n_kids = sum(1 for kb, _, kp in kids if (kb, kp) == (b, parent))
        if n_kids == 0 or g.get("children_objects") != g.get("parent_objects") or not g.get("listed_at"):
            print("    REGRID-DENOMINATOR %s %s children_objects=%s parent_objects=%s children=%d"
                  % (b, parent, g.get("children_objects"), g.get("parent_objects"), n_kids))
            ok2 = False
        covered.add((b, parent))
    missing = set(want) - covered
    extra = covered - set(want)
    print("  census classes=%d placed-directly=%d regridded-parents=%d child rows=%d duplicates=%d unplaced=%d "
          "not-in-census=%d" % (len(want), len(own), len(regrids), len(kids), dup, len(missing), len(extra)))
    for m in sorted(missing)[:5]:
        print("    UNPLACED %s %s" % m)
    res.append(("V2 every census class is placed once, or re-gridded into children whose objects sum to its "
                "own, and no row names a class the census lacks", ok2 and not missing and not extra))

    counts = dict.fromkeys(DISPOSITIONS, 0)
    v3 = True
    for r in rows:
        d = r.get("disposition")
        if d not in DISPOSITIONS:
            print("    OFF-ENUM %s %s %r" % (r.get("bucket"), r.get("prefix"), d))
            v3 = False
            continue
        counts[d] += 1
        k = (r.get("bucket"), r.get("prefix"))
        if (k in DECISIONS) != (d == "DECISION") or (d == "DECISION" and r.get("decision_ref") != DECISIONS[k]):
            print("    DECISION-ROW %s %s %s" % (k[0], k[1], d))
            v3 = False
        if d in ("MOVE", "HOME") and not (isinstance(r.get("dest"), dict) and r.get("address") and r.get("dest_pattern")):
            v3 = False
        if d == "RETIRE" and not r.get("reason"):
            v3 = False
        if d == "FAULT" and not (r.get("reason") and SERIAL_RE.match(str(r.get("fault_owner", "")))):
            print("    FAULT-WITHOUT-OWNER %s %s owner=%r" % (r.get("bucket"), r.get("prefix"), r.get("fault_owner")))
            v3 = False
        if not r.get("rule"):
            v3 = False
    print("  dispositions: %s" % ", ".join("%s=%d" % kv for kv in counts.items()))
    res.append(("V3 every row's disposition is on the enum with its required fields; a FAULT row carries a reason "
                "and a named owner serial; the DECISION rows are exactly FWD-7 and FWD-8", v3 and bool(rows)))

    v4 = True
    placed = [r for r in rows if r.get("disposition") in ("MOVE", "HOME")]
    for r in placed:
        dest = r["dest"]
        try:
            built = naming.address(*[dest[s] for s in SEGMENTS], object=dest.get("object"))
        except Exception as e:  # noqa: BLE001
            print("    BUILDER-REFUSED %s %s: %s" % (r["bucket"], r["prefix"], str(e)[:160]))
            v4 = False
            continue
        if built != r["address"]:
            print("    TYPED %s %s: stored %r, builder %r" % (r["bucket"], r["prefix"], r["address"], built))
            v4 = False
        if r["disposition"] == "MOVE":
            firm = FIRM[r["bucket"]]
            if dest["scope"] != firm or not built.startswith("s3://opal-data-%s/" % firm):
                print("    SCOPE %s %s -> %s" % (r["bucket"], r["prefix"], built))
                v4 = False
        elif dest["tier"] not in ("bronze", "silver") or not built.startswith("s3://opal-data-assets/"):
            print("    HOME %s %s -> %s" % (r["bucket"], r["prefix"], built))
            v4 = False
    print("  placed rows graded through address(): %d" % len(placed))
    res.append(("V4 every MOVE/HOME address is exactly address()'s output; MOVE scope is the bucket's firm in its "
                "firm bucket, HOME is bronze/silver in opal-data-assets", v4 and bool(placed)))

    v5 = True
    by_key = {(r["bucket"], r["prefix"]): r for r in rows}
    n_same = n_overlap = 0
    for r in m1["rows"]:
        if r["disposition"] == "FAULT":
            continue
        cur = by_key.get((r["bucket"], r["prefix"]))
        keys = ("disposition", "address", "dest_pattern")
        if cur is None or any(cur.get(k) != r.get(k) for k in keys):
            # the ONE permitted change to a round-1 row: a MOVE or HOME class whose MEASURED destination-key overlap with
            # another class is above 0 becomes a FAULT row owned by a named serial (ruling 1e), never a new placement
            if (cur is not None and r["disposition"] in ("MOVE", "HOME") and cur.get("disposition") == "FAULT"
                    and str(cur.get("reason", "")).startswith("destination-key overlap")
                    and SERIAL_RE.match(str(cur.get("fault_owner", "")))):
                n_overlap += 1
                continue
            print("    DISTURBED %s %s" % (r["bucket"], r["prefix"]))
            v5 = False
        else:
            n_same += 1
    print("  round-1 placed, retired and decided classes unchanged: %d; turned FAULT by a measured key overlap: %d"
          % (n_same, n_overlap))
    res.append(("V5 every class round 1 placed, retired or decided keeps its disposition, address and pattern, "
                "except a MOVE or HOME class a measured key overlap turned FAULT (the difference control: the repair "
                "moves only the FAULT classes)", v5 and n_same > 0))
    return res


def _collision_groups(rows):
    groups = {}
    for r in rows:
        if r.get("disposition") not in ("MOVE", "HOME") or not isinstance(r.get("dest"), dict):
            continue
        d = r["dest"]
        k = (r["bucket"], d.get("source"), d.get("scope"), d.get("tier"), d.get("table"))
        groups.setdefault(k, []).append(r["prefix"])
    return {k: sorted(v) for k, v in groups.items() if len(v) > 1}


def repair(root):
    naming, census, m1, m2 = _docs(root)
    rows = m2.get("rows") or []
    res = []
    r1_fault = {(r["bucket"], r["prefix"]) for r in m1["rows"] if r["disposition"] == "FAULT"}
    regrids = {(g.get("bucket"), g.get("parent")) for g in (m2.get("regrids") or [])}
    by_key = {(r.get("bucket"), r.get("prefix")): r for r in rows}
    disposed = 0
    for k in r1_fault:
        if k in regrids or (k in by_key and by_key[k].get("disposition") != "FAULT"):
            disposed += 1
    remaining = [r for r in rows if r.get("disposition") == "FAULT"]
    owners = {}
    for r in remaining:
        owners[r.get("fault_owner")] = owners.get(r.get("fault_owner"), 0) + 1
    print("  round-1 FAULT classes=%d re-gridded or placed=%d; FAULT rows remaining=%d owners=%s"
          % (len(r1_fault), disposed, len(remaining), json.dumps(owners, sort_keys=True)))
    res.append(("P1 every round-1 FAULT class is re-gridded or placed, or still a FAULT row with a reason and a "
                "named owner serial",
                bool(r1_fault) and all(
                    (k in regrids) or (k in by_key and (by_key[k].get("disposition") != "FAULT"
                                                        or (by_key[k].get("reason")
                                                            and SERIAL_RE.match(str(by_key[k].get("fault_owner", ""))))))
                    for k in r1_fault)))

    groups = _collision_groups(rows)
    entries = {}
    p2 = True
    for c in m2.get("collisions") or []:
        key = (c.get("bucket"), c.get("source"), c.get("scope"), c.get("tier"), c.get("table"))
        entries[key] = c
        if c.get("verdict") != "merge" or not str(c.get("reason", "")).strip() or c.get("overlap_keys") != 0:
            print("    COLLISION-ENTRY %s verdict=%r overlap_keys=%r" % (key, c.get("verdict"), c.get("overlap_keys")))
            p2 = False
    unruled = [k for k in groups if k not in entries]
    stray = [k for k in entries if k not in groups]
    print("  destination-table collisions in the final rows=%d ruled=%d unruled=%d stray entries=%d"
          % (len(groups), len(entries), len(unruled), len(stray)))
    for k in unruled[:5]:
        print("    UNRULED %s %s" % (k, groups[k][:4]))
    res.append(("P2 every destination table that two or more classes of one bucket still share has a merge ruling "
                "with a reason and a measured overlap of 0 keys", p2 and not unruled and not stray))

    no_new_decision = all((r["bucket"], r["prefix"]) in DECISIONS for r in rows if r.get("disposition") == "DECISION")
    retire_ok = all(str(r.get("reason", "")).strip() for r in rows if r.get("disposition") == "RETIRE")
    res.append(("P3 no worker-made DECISION row exists and every RETIRE row carries its reason (RETIRE moves "
                "nothing and deletes nothing)", no_new_decision and retire_ok))

    md = os.path.join(root, DELIV, "MAPPING_TABLE_v2.md")
    ok4 = False
    if os.path.isfile(md):
        text = open(md, encoding="utf-8").read()
        total = sum(c["objects"] for bd in census["buckets"].values() for c in bd["classes"])
        ok4 = all(w in text for w in ("FAULT", "MOVE", "HOME", "RETIRE", "DECISION")) and str(len(
            [1 for bd in census["buckets"].values() for _ in bd["classes"]])) in text and str(total) in text.replace(",", "")
    res.append(("P4 MAPPING_TABLE_v2.md exists and states the counts per disposition with the census class and "
                "object denominators", ok4))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("structure", "repair"), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    total = 5 if a.arms == "structure" else 4
    try:
        res = (structure if a.arms == "structure" else repair)(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (DELIV, type(e).__name__, str(e)[:160]))
        res = [("mapping_v2.json, mapping.json and census.json present", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 2 MAPPING %s: %d of %d arms" % (a.arms.upper(), n, total))
    sys.exit(0 if n == total else 1)


if __name__ == "__main__":
    main()
