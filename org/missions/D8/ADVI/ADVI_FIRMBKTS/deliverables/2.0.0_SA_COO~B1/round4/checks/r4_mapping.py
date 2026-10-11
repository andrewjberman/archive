"""ADVI_FIRMBKTS round 4 check for cell FB-g-4 (the table repair under the S2-S11 edge rulings), issuer 2.0.0_SA_COO~B1.

Rulings: ledger/ROUND_ANALYSIS.round3.md section 2 (S2, S3, S5-S11), on top of the round-2 grain ruling and ADDENDUM 1.

--arms structure  grades deliverables/mapping_v4.json against census.json, mapping.json (round 1), mapping_v3.json and
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
    return (opal_naming, _load(root, "census.json"), _load(root, "mapping.json"), _load(root, "mapping_v3.json"),
            _load(root, "mapping_v4.json"))


def _by_key(rows):
    return {(r.get("bucket"), r.get("prefix")): r for r in rows}


def structure(root):
    naming, census, m1, m2, m3 = _docs(root)
    rows = m3.get("rows") or []
    res = []
    res.append(("S1 mapping_v4.json names the census it placed and the table it supersedes",
                bool(rows) and m3.get("census_listed_at") == census.get("listed_at")
                and m3.get("supersedes") == "mapping_v3.json" and bool(m3.get("live_listed_at"))))

    want = {(b, c["prefix"]): c["objects"] for b, bd in census["buckets"].items() for c in bd["classes"]}
    regrids = {(g.get("bucket"), g.get("parent")): g for g in (m3.get("regrids") or [])}
    # a rule-3a row is an OBJECT-grain RETIRE of one zero-byte placeholder whose key equals its class prefix; the class's
    # data keeps its own class-grain row at the same prefix (ruling (a): the class is unblocked), so the two never collide
    ph = [r for r in rows if r.get("placeholder_key") and str(r.get("rule", "")).startswith("3a")]
    cls_rows = [r for r in rows if r not in ph]
    # CTO S7: a class may hold a `complete` and a `skip` marker row at one key; they are told apart by marker_kind
    own = [(r.get("bucket"), r.get("prefix"), r.get("marker_kind") if r.get("kind") == "marker" else None)
           for r in cls_rows if not r.get("parent")]
    own_ph = [(r.get("bucket"), r.get("prefix")) for r in ph]
    kids = [(r.get("bucket"), r.get("prefix"), r.get("parent")) for r in cls_rows if r.get("parent")]
    dup = (len(own) - len(set(own))) + (len(kids) - len({(b, p, par) for b, p, par in kids}))         + len({(b, p) for b, p, k in own if k is None} & {(b, p) for b, p, _ in kids}) + (len(own_ph) - len(set(own_ph)))
    ok2 = not dup
    covered = {(b, p) for b, p, _ in own} | set(own_ph)
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
    # S9 (CTO ruling, ROUND_ANALYSIS.round3.md section 2): the sum check compares against the LIVE listing, both numbers
    # printed. A class a producer is still writing carries `moving: true` and a reason, and its live count may exceed.
    live_ok = True
    try:
        import boto3
        s3 = boto3.client("s3")
        n_live = n_diff = 0
        for (b, p), g in sorted(regrids.items()):
            cnt = 0
            for page in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix=p):
                cnt += len(page.get("Contents", []))
            n_live += 1
            same = cnt == g.get("listed_objects")
            moving = g.get("moving") is True and str(g.get("moving_reason", "")).strip() != ""                 and cnt >= (g.get("listed_objects") or 0)
            if not (same or moving):
                n_diff += 1
                print("    LIVE-DIFFERS %s %s listed=%s live=%s" % (b, p, g.get("listed_objects"), cnt))
                live_ok = False
        print("  S9 re-grid parents listed live: %d; differing from the table's listed_objects: %d" % (n_live, n_diff))
    except Exception as e:  # noqa: BLE001
        print("    LIVE-LISTING-FAILED %s" % type(e).__name__)
        live_ok = False
    res.append(("S2 every census class is placed once, or re-gridded into children whose objects sum to its LIVE "
                "listing (listed again here, both numbers printed), and no row names a class the census lacks",
                ok2 and not missing and not extra and live_ok))

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
            # S10: a class-grain row has no partition; its address is the builder's output up to the table directory
            class_grain = dest.get("partition") in (None, "")
            segs = [dest.get(s) if s != "partition" else ("x" if class_grain else dest.get("partition"))
                    for s in SEGMENTS]
            built = naming.address(*segs, object=dest.get("object"))
            if class_grain:
                built = built[:-1]
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
        if r.get("kind") != "marker" and ("{partition}" in str(r.get("address")) or "{object}" in str(r.get("address"))):
            continue  # ruling S10 rewrites it at class grain; the difference control does not hold it to its token
        cur = by3.get((r["bucket"], r["prefix"]))
        if cur is None or any(cur.get(k) != r.get(k) for k in ("disposition", "address", "dest_pattern")):
            print("    DISTURBED %s %s" % (r["bucket"], r["prefix"]))
            s5 = False
        else:
            n_same += 1
    print("  previous-table placed, retired and decided classes unchanged: %d" % n_same)
    res.append(("S5 every class the previous table placed, retired or decided keeps its disposition, address and pattern "
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
    by4 = _by_key(rows)
    r1 = {(r.get("bucket"), r.get("prefix")): r for r in (m1.get("rows") or [])}
    regrids = {(g.get("bucket"), g.get("parent")): g for g in (m3.get("regrids") or [])}
    applied = set((m3.get("rulings_applied") or {}).keys())
    want = {"S2", "S3", "S5", "S6", "S7", "S8", "S9", "S10", "S11"}

    # U1 ruling S2: an overlap-0 MERGE names its destination table in the entry
    u1 = True
    n_merge = 0
    for c in m3.get("collisions") or []:
        if c.get("verdict") == "merge":
            n_merge += 1
            dt = str(c.get("destination_table", "")).strip()
            if not dt or dt != str(c.get("table", "")).strip():
                print("    MERGE-WITHOUT-DESTINATION %s %s destination_table=%r" % (c.get("bucket"), c.get("table"), dt))
                u1 = False
    nodest = [r for r in rows if r.get("disposition") in ("MOVE", "HOME")
              and isinstance(r.get("dest"), dict) and not str(r["dest"].get("table", "")).strip()]
    print("  S2 merge rulings=%d; placed rows with no table=%d; rulings applied=%s"
          % (n_merge, len(nodest), ",".join(sorted(applied))))
    res.append(("U1 S2: every overlap-0 MERGE names its destination table, no placed row lacks one, and the table "
                "lists the rulings it applied", u1 and not nodest and want <= applied))

    # U2 ruling S3: a round-1 placed row stays as placed, and gains no kind
    u2 = True
    n_r1 = 0
    for k, r in r1.items():
        if r.get("disposition") in ("FAULT", None):
            continue
        cur = by4.get(k)
        n_r1 += 1
        if cur is None or any(cur.get(f) != r.get(f) for f in ("disposition", "address", "dest_pattern")) \
                or ("kind" in cur and "kind" not in r):
            print("    ROUND1-ROW-MOVED %s %s" % k)
            u2 = False
    print("  S3 round-1 placed rows kept as placed with no kind added: %d" % n_r1)
    res.append(("U2 S3: every round-1 placed row keeps its disposition, address and pattern and gains no `kind`",
                u2 and n_r1 > 0))

    # U3 rulings S5, S7, S8, S11: markers
    u3 = True
    markers = [r for r in rows if r.get("kind") == "marker"]
    seen = {}
    fams = ("bronze_complete", "silver_complete", "gold_complete")
    n_skip = 0
    for r in markers:
        d = r.get("dest") or {}
        fam = r.get("state_family")
        mm = r.get("marker_match") or []
        if fam not in fams or d.get("tier") != "state" or d.get("table") != fam or not str(r.get("writer", "")).strip() \
                or r.get("marker_kind") not in ("complete", "skip") or not mm:
            print("    MARKER-ROW %s %s family=%r table=%r tier=%r writer=%r kind=%r"
                  % (r.get("bucket"), r.get("prefix"), fam, d.get("table"), d.get("tier"), r.get("writer"),
                     r.get("marker_kind")))
            u3 = False
            continue
        if any("_SKIP.json" in str(x) for x in mm):
            n_skip += 1
            if r.get("marker_kind") != "skip":
                print("    SKIP-NOT-SKIP %s %s" % (r.get("bucket"), r.get("prefix")))
                u3 = False
        key = (r.get("bucket"), d.get("scope"), d.get("table"), d.get("partition"))
        if key in seen and seen[key] != r.get("writer"):
            print("    MARKER-COLLISION-ACROSS-WRITERS %s %s" % (r.get("bucket"), key[1:]))
            u3 = False
        seen.setdefault(key, r.get("writer"))
    print("  S5/S7/S8/S11 marker rows=%d skip markers=%d distinct (bucket,scope,table,partition)=%d"
          % (len(markers), n_skip, len(seen)))
    res.append(("U3 S5/S7/S8/S11: every marker row is in a <tier>_complete state family with its writer named, a skip "
                "marker where the literal tail is _SKIP.json (at least one such row: S7), and no two writers share a "
                "state key", u3 and bool(markers) and n_skip >= 1))

    # U4 ruling S6: a QA-named feed is QA only if its WRITER is a QA tool
    u4 = True
    n_qa = 0
    qa_re = re.compile(r"(^|/)(qa|diag|probe|test)[-_/]|[-_/](qa|diag|probe)(/|$)", re.I)
    # a row the previous table already placed, retired or decided is copied unchanged (S3, S5) and is not re-judged
    prev_fixed = {(r.get("bucket"), r.get("prefix")) for r in m2["rows"] if r.get("disposition") != "FAULT"}
    for r in rows:
        if not qa_re.search(str(r.get("prefix", ""))):
            continue
        if (r.get("bucket"), r.get("prefix")) in prev_fixed:
            continue
        n_qa += 1
        v = r.get("qa_verdict")
        if v == "unresolved" and r.get("disposition") == "FAULT" and "S6" in str(r.get("reason", ""))                 and SERIAL_RE.match(str(r.get("fault_owner", ""))):
            continue  # S6 cannot classify without a writer: FAULT with the ruling cited and an owner
        if v not in ("qa-tool", "production") or not str(r.get("qa_writer", "")).strip():
            print("    QA-NAMED-WITHOUT-WRITER %s %s" % (r.get("bucket"), r.get("prefix")))
            u4 = False
        elif v == "qa-tool" and r.get("disposition") != "RETIRE":
            print("    QA-TOOL-NOT-RETIRED %s %s" % (r.get("bucket"), r.get("prefix")))
            u4 = False
        elif v == "production" and r.get("disposition") not in ("MOVE", "HOME"):
            print("    PRODUCTION-NOT-PLACED %s %s" % (r.get("bucket"), r.get("prefix")))
            u4 = False
    print("  S6 QA-named classes judged by their writer: %d" % n_qa)
    res.append(("U4 S6: every QA-named class names its writer; a QA-tool writer is RETIRE, a production writer is "
                "placed", u4))

    # U5 rulings S9, S10 and the denominators
    u5 = True
    for (b, p), g in regrids.items():
        need = ("census_objects", "listed_objects", "difference", "listed_at")
        if any(g.get(k) is None for k in need) or g["difference"] != g["listed_objects"] - g["census_objects"]:
            print("    REGRID-COUNTS %s %s" % (b, p))
            u5 = False
    # S10: a class-grain row's address carries no partition token
    bad_tok = [r for r in rows if r.get("disposition") in ("MOVE", "HOME") and not r.get("kind")
               and ("{partition}" in str(r.get("address")) or "{object}" in str(r.get("address")))]
    md = os.path.join(root, DELIV, "MAPPING_TABLE_v4.md")
    faults = [r for r in rows if r.get("disposition") == "FAULT"]
    before = sum(1 for r in m2["rows"] if r["disposition"] == "FAULT")
    ok_md = False
    if os.path.isfile(md):
        text = open(md, encoding="utf-8").read()
        ok_md = ("FAULT before" in text and "FAULT after" in text and str(before) in text and str(len(faults)) in text
                 and all(str(g.get("listed_objects")) in text.replace(",", "") for g in regrids.values()))
    own_ok = all(SERIAL_RE.match(str(r.get("fault_owner", ""))) for r in faults)
    print("  S9/S10 regrids=%d FAULT before=%d after=%d table view ok=%s class rows with a partition token=%d"
          % (len(regrids), before, len(faults), ok_md, len(bad_tok)))
    res.append(("U5 S9/S10: every re-grid prints census, LIVE and difference, MAPPING_TABLE_v4.md prints FAULT before and "
                "after with each re-grid's live count, a class-grain row carries no partition token, and every FAULT has "
                "an owner", u5 and ok_md and own_ok and not bad_tok and len(faults) <= before))
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
        res = [("mapping_v4.json, mapping_v3.json, mapping.json and census.json present", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 MAPPING %s: %d of %d arms" % (a.arms.upper(), n, total))
    sys.exit(0 if n == total else 1)


if __name__ == "__main__":
    main()
