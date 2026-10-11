"""ADVI_FIRMBKTS round 3 check for cell FB-f-2 (the table repair under the CTO's grain ruling), issuer 2.0.0_SA_COO~B1.

Ruling: ledger/ROUND_ANALYSIS.round2.md section 2 item 3, rules (a)-(e), closing D1-W4-S2..S6.

--arms structure  grades deliverables/mapping_v3.json against census.json, mapping.json (round 1), mapping_v2.json and
                  lib/opal_naming.py address() (5 arms, the round-2 structure arms moved one version).
--arms repair     grades rules (a)-(e) (5 arms). Arm T1 makes read-only HEAD calls on the placeholder keys.
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
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _load(root, name):
    with open(os.path.join(root, DELIV, name), encoding="utf-8") as fh:
        return json.load(fh)


def _docs(root):
    sys.path.insert(0, os.path.join(_root(None), "lib"))  # the builders always come from the checkout
    import opal_naming
    return (opal_naming, _load(root, "census.json"), _load(root, "mapping.json"), _load(root, "mapping_v2.json"),
            _load(root, "mapping_v3.json"))


def _by_key(rows):
    return {(r.get("bucket"), r.get("prefix")): r for r in rows}


def structure(root):
    naming, census, m1, m2, m3 = _docs(root)
    rows = m3.get("rows") or []
    res = []
    res.append(("S1 mapping_v3.json names the census it placed and the table it supersedes",
                bool(rows) and m3.get("census_listed_at") == census.get("listed_at")
                and m3.get("supersedes") == "mapping_v2.json" and bool(m3.get("live_listed_at"))))

    want = {(b, c["prefix"]): c["objects"] for b, bd in census["buckets"].items() for c in bd["classes"]}
    regrids = {(g.get("bucket"), g.get("parent")): g for g in (m3.get("regrids") or [])}
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
        n_kids = sum(1 for kb, _, kp in kids if (kb, kp) == (b, parent))
        if n_kids == 0 or g.get("children_objects") != g.get("listed_objects") or not g.get("listed_at"):
            print("    REGRID-DENOMINATOR %s %s children_objects=%s listed_objects=%s children=%d"
                  % (b, parent, g.get("children_objects"), g.get("listed_objects"), n_kids))
            ok2 = False
        covered.add((b, parent))
    missing = set(want) - covered
    extra = covered - set(want)
    print("  census classes=%d placed-directly=%d regridded-parents=%d child rows=%d duplicates=%d unplaced=%d "
          "not-in-census=%d" % (len(want), len(own), len(regrids), len(kids), dup, len(missing), len(extra)))
    for m in sorted(missing)[:5]:
        print("    UNPLACED %s %s" % m)
    res.append(("S2 every census class is placed once, or re-gridded into children whose objects sum to its LIVE "
                "listing, and no row names a class the census lacks", ok2 and not missing and not extra))

    counts = dict.fromkeys(DISPOSITIONS, 0)
    s3 = True
    for r in rows:
        d = r.get("disposition")
        if d not in DISPOSITIONS:
            print("    OFF-ENUM %s %s %r" % (r.get("bucket"), r.get("prefix"), d))
            s3 = False
            continue
        counts[d] += 1
        k = (r.get("bucket"), r.get("prefix"))
        if (k in DECISIONS) != (d == "DECISION") or (d == "DECISION" and r.get("decision_ref") != DECISIONS[k]):
            print("    DECISION-ROW %s %s %s" % (k[0], k[1], d))
            s3 = False
        if d in ("MOVE", "HOME") and not (isinstance(r.get("dest"), dict) and r.get("address") and r.get("dest_pattern")):
            s3 = False
        if d == "RETIRE" and not r.get("reason"):
            s3 = False
        if d == "FAULT" and not (r.get("reason") and SERIAL_RE.match(str(r.get("fault_owner", "")))):
            print("    FAULT-WITHOUT-OWNER %s %s owner=%r" % (r.get("bucket"), r.get("prefix"), r.get("fault_owner")))
            s3 = False
        if not r.get("rule"):
            s3 = False
    print("  dispositions: %s" % ", ".join("%s=%d" % kv for kv in counts.items()))
    res.append(("S3 every row's disposition is on the enum with its required fields; a FAULT row carries a reason "
                "and a named owner serial; the DECISION rows are exactly FWD-7 and FWD-8", s3 and bool(rows)))

    s4 = True
    placed = [r for r in rows if r.get("disposition") in ("MOVE", "HOME")]
    for r in placed:
        dest = r["dest"]
        try:
            built = naming.address(*[dest[s] for s in SEGMENTS], object=dest.get("object"))
        except Exception as e:  # noqa: BLE001
            print("    BUILDER-REFUSED %s %s: %s" % (r["bucket"], r["prefix"], str(e)[:160]))
            s4 = False
            continue
        if built != r["address"]:
            print("    TYPED %s %s: stored %r, builder %r" % (r["bucket"], r["prefix"], r["address"], built))
            s4 = False
        if r["disposition"] == "MOVE":
            firm = FIRM[r["bucket"]]
            if dest["scope"] != firm or not built.startswith("s3://opal-data-%s/" % firm):
                print("    SCOPE %s %s -> %s" % (r["bucket"], r["prefix"], built))
                s4 = False
        elif dest["tier"] not in ("bronze", "silver") or not built.startswith("s3://opal-data-assets/"):
            print("    HOME %s %s -> %s" % (r["bucket"], r["prefix"], built))
            s4 = False
    print("  placed rows graded through address(): %d" % len(placed))
    res.append(("S4 every MOVE/HOME address is exactly address()'s output; MOVE scope is the bucket's firm in its "
                "firm bucket, HOME is bronze/silver in opal-data-assets", s4 and bool(placed)))

    s5 = True
    by3 = _by_key(rows)
    n_same = 0
    for r in m2["rows"]:
        if r["disposition"] == "FAULT" or r.get("parent"):
            continue
        cur = by3.get((r["bucket"], r["prefix"]))
        if cur is None or any(cur.get(k) != r.get(k) for k in ("disposition", "address", "dest_pattern")):
            print("    DISTURBED %s %s" % (r["bucket"], r["prefix"]))
            s5 = False
        else:
            n_same += 1
    print("  round-2 placed, retired and decided classes unchanged: %d" % n_same)
    res.append(("S5 every class round 2 placed, retired or decided keeps its disposition, address and pattern "
                "(the difference control: the repair moves only the FAULT rows)", s5 and n_same > 0))
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
    naming, census, m1, m2, m3 = _docs(root)
    rows = m3.get("rows") or []
    res = []
    by3 = _by_key(rows)
    regrids = {(g.get("bucket"), g.get("parent")): g for g in (m3.get("regrids") or [])}

    # T1 rule (a): a zero-byte object whose key equals its class prefix is RETIRE
    import boto3
    s3 = boto3.client("s3")
    rule_a = [r for r in rows if str(r.get("rule", "")).startswith("3a")]
    t1 = True
    n_head = 0
    for r in rule_a:
        key = r.get("placeholder_key")
        if r.get("disposition") != "RETIRE" or not str(r.get("reason", "")).strip() or key != r.get("prefix"):
            print("    RULE-A-ROW %s %s disposition=%r placeholder_key=%r" % (r.get("bucket"), r.get("prefix"),
                                                                           r.get("disposition"), key))
            t1 = False
            continue
        try:
            head = s3.head_object(Bucket=r["bucket"], Key=key)
            n_head += 1
            if head["ContentLength"] != 0:
                print("    NOT-ZERO-BYTE %s %s %d" % (r["bucket"], key, head["ContentLength"]))
                t1 = False
        except Exception as e:  # noqa: BLE001
            print("    HEAD-FAILED %s %s %s" % (r["bucket"], key, type(e).__name__))
            t1 = False
    left = [r for r in rows if r.get("disposition") == "FAULT"
            and str(r.get("reason", "")).startswith("marker at the class prefix")]
    print("  rule (a) rows=%d live HEAD size 0 on %d; FAULT rows still reading 'marker at the class prefix'=%d"
          % (len(rule_a), n_head, len(left)))
    res.append(("T1 rule (a): every zero-byte placeholder is a RETIRE row whose live HEAD reads size 0, and no FAULT "
                "row still names a marker at its class prefix", t1 and bool(rule_a) and not left))

    # T2 rule (b): completion markers carry kind=marker, map to the R21 state home, are never re-gridded beside data
    markers = [r for r in rows if r.get("kind") == "marker"]
    t2 = bool(markers)
    for r in markers:
        d = r.get("dest") or {}
        if r.get("disposition") not in ("MOVE", "HOME") or d.get("tier") != "state":
            print("    MARKER-NOT-STATE %s %s disposition=%r tier=%r" % (r.get("bucket"), r.get("prefix"),
                                                                       r.get("disposition"), d.get("tier")))
            t2 = False
    mixed = 0
    for (b, parent), g in regrids.items():
        kinds = {r.get("kind") == "marker" for r in rows if r.get("bucket") == b and r.get("parent") == parent}
        if len(kinds) > 1:
            mixed += 1
            print("    MARKER-BESIDE-DATA %s %s" % (b, parent))
    print("  rule (b) kind=marker rows=%d (all tier state: %s); re-grids holding markers beside data=%d"
          % (len(markers), t2, mixed))
    res.append(("T2 rule (b): every row of kind marker maps to a state/ home through address() and no re-grid holds "
                "markers beside data", t2 and not mixed))

    # T3 rule (c): interleaved classes are re-gridded per date partition, no child cap
    t3 = True
    v2_inter = [(r["bucket"], r["prefix"]) for r in m2["rows"] if r["disposition"] == "FAULT"
                and "interleaved" in str(r.get("reason", ""))]
    n_ok = 0
    for k in v2_inter:
        cur = by3.get(k)
        if k in regrids:
            g = regrids[k]
            if g.get("partition_rule") != "per-date" or "cap" in g:
                print("    REGRID-RULE %s %s partition_rule=%r cap=%r" % (k[0], k[1], g.get("partition_rule"),
                                                                        g.get("cap")))
                t3 = False
            else:
                n_ok += 1
        elif cur is not None and cur.get("disposition") != "FAULT":
            n_ok += 1
        else:
            print("    STILL-INTERLEAVED %s %s" % k)
            t3 = False
    cap_left = [r for r in rows if r.get("disposition") == "FAULT"
                and re.search(r"more than 25|25-child|child limit", str(r.get("reason", "")))]
    print("  rule (c) round-2 interleaved FAULT classes=%d disposed under the rule=%d; FAULT rows citing a child "
          "limit=%d" % (len(v2_inter), n_ok, len(cap_left)))
    res.append(("T3 rule (c): every round-2 interleaved FAULT class is re-gridded per date partition with no child "
                "cap (or placed), and no FAULT row cites a child limit", t3 and bool(v2_inter) and not cap_left))

    # T4 rule (d): every shared destination table is ruled at a measured overlap
    groups = _collision_groups(rows)
    entries = {}
    t4 = True
    for c in m3.get("collisions") or []:
        key = (c.get("bucket"), c.get("source"), c.get("scope"), c.get("tier"), c.get("table"))
        entries[key] = c
        v = c.get("verdict")
        ov = c.get("overlap_keys")
        if v not in ("merge", "split") or not str(c.get("reason", "")).strip() or not isinstance(ov, int) \
                or (v == "merge" and ov != 0) or (v == "split" and ov <= 0):
            print("    COLLISION-ENTRY %s verdict=%r overlap_keys=%r" % (key, v, ov))
            t4 = False
    unruled = [k for k in groups if k not in entries]
    print("  rule (d) shared destination tables in the final rows=%d ruled=%d unruled=%d" % (len(groups),
                                                                                         len(entries), len(unruled)))
    for k in unruled[:5]:
        print("    UNRULED %s %s" % (k, groups[k][:4]))
    res.append(("T4 rule (d): every destination table that two or more classes of one bucket still share carries a "
                "merge ruling at overlap 0 or a split at a measured overlap above 0, with a reason", t4 and not unruled))

    # T5 rule (e): denominators
    t5 = True
    for (b, p), g in regrids.items():
        need = ("census_objects", "listed_objects", "difference", "listed_at")
        if any(g.get(k) is None for k in need) or g["difference"] != g["listed_objects"] - g["census_objects"]:
            print("    REGRID-COUNTS %s %s %s" % (b, p, {k: g.get(k) for k in need}))
            t5 = False
    md = os.path.join(root, DELIV, "MAPPING_TABLE_v3.md")
    ok_md = False
    faults = [r for r in rows if r.get("disposition") == "FAULT"]
    before = sum(1 for r in m2["rows"] if r["disposition"] == "FAULT")
    if os.path.isfile(md):
        text = open(md, encoding="utf-8").read()
        classes = sum(len(bd["classes"]) for bd in census["buckets"].values())
        objects = sum(c["objects"] for bd in census["buckets"].values() for c in bd["classes"])
        ok_md = (all(w in text for w in ("FAULT", "MOVE", "HOME", "RETIRE", "DECISION"))
                 and str(classes) in text and str(objects) in text.replace(",", "")
                 and ("FAULT before" in text and "FAULT after" in text)
                 and str(before) in text and str(len(faults)) in text)
    print("  rule (e) regrids=%d with census, listed and difference; FAULT before=%d after=%d; table view ok=%s"
          % (len(regrids), before, len(faults), ok_md))
    res.append(("T5 rule (e): every re-grid prints census objects, live objects and their difference, and "
                "MAPPING_TABLE_v3.md prints FAULT before and after with the class and object denominators",
                t5 and ok_md and all(SERIAL_RE.match(str(r.get("fault_owner", ""))) for r in faults)))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("structure", "repair"), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    total = 5
    try:
        res = (structure if a.arms == "structure" else repair)(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s: %s)" % (DELIV, type(e).__name__, str(e)[:160]))
        res = [("mapping_v3.json, mapping_v2.json, mapping.json and census.json present", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 3 MAPPING %s: %d of %d arms" % (a.arms.upper(), n, total))
    sys.exit(0 if n == total else 1)


if __name__ == "__main__":
    main()
