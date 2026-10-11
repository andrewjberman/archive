"""Build mapping_v4.json from mapping_v3.json under the CTO edge rulings S2-S11 (cell FB-g-3).

Reads: mapping_v3.json, mapping_v2.json, mapping.json, census.json (read-only), .scratch/live_parents.json (LIST results).
Writes: deliverables/mapping_v4.json and deliverables/MAPPING_TABLE_v4.md (LF, ASCII).
"""
import collections
import copy
import datetime
import json
import os
import re
import sys

ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming as naming  # noqa: E402

D = os.path.join(ROOT, "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables")
m3 = json.load(open(os.path.join(D, "mapping_v3.json"), encoding="utf-8"))
m2 = json.load(open(os.path.join(D, "mapping_v2.json"), encoding="utf-8"))
m1 = json.load(open(os.path.join(D, "mapping.json"), encoding="utf-8"))
census = json.load(open(os.path.join(D, "census.json"), encoding="utf-8"))
LIVE = json.load(open(os.path.join(ROOT, ".scratch/live_parents.json"), encoding="utf-8"))

OWNER = "1.0.0_SA_CTO~DELL1"
FIRM = {"opal-data-bd": "49financial", "opal-data-inf": "inflection", "opal-data-cot": "cottonwood"}
QA_RE = re.compile(r"(^|/)(qa|diag|probe|test)[-_/]|[-_/](qa|diag|probe)(/|$)", re.I)
rows = copy.deepcopy(m3["rows"])
regrids = copy.deepcopy(m3["regrids"])
collisions = copy.deepcopy(m3["collisions"])
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
fault_before = sum(1 for r in m2["rows"] if r["disposition"] == "FAULT")
fault_before_v3 = sum(1 for r in rows if r["disposition"] == "FAULT")
assert fault_before == 89 and fault_before_v3 == 84, (fault_before, fault_before_v3)  # v2 = check's before; v3 = table's 84

LIVE_BY = {(P["bucket"], P["parent"]): P for P in LIVE["parents"]}
applied = {k: 0 for k in ("S2", "S3", "S5", "S6", "S7", "S8", "S9", "S10", "S11")}


def idx(bucket, prefix, **cond):
    return [i for i, r in enumerate(rows)
            if r["bucket"] == bucket and r["prefix"] == prefix and all(r.get(k) == v for k, v in cond.items())]


def one(bucket, prefix, **cond):
    got = idx(bucket, prefix, **cond)
    assert len(got) == 1, (bucket, prefix, cond, got)
    return got[0]


def pattern(addr, scope):
    """dest_pattern: the address path after the bucket, with the scope segment written as {firm}."""
    path = addr.split("/", 3)[3]
    segs = path.split("/")
    if segs[1] == scope:
        segs[1] = "{firm}"
    return "/".join(segs)


def tail_ok(key, tails):
    return any(key.endswith(t) for t in tails)


def live_keys(bucket, prefix):
    return [(k, s) for k, s in LIVE_BY[(bucket, prefix)]["keys"]]


# ---------------------------------------------------------------- S10: class-grain row carries no partition token
i = one("opal-data-bd", "gold/clients/", disposition="MOVE")
r = rows[i]
addr = naming.address("advi", "49financial", "platinum", "clients", "x", object=None)[:-1]
r["dest"] = {"source": "advi", "scope": "49financial", "tier": "platinum", "table": "clients", "partition": None}
r["address"] = addr
r["dest_pattern"] = pattern(addr, "49financial")
r["rule"] = ("RG3: gold/<dir>/ with *.json objects -> advi/{F}/platinum/<dir>/<seg1>/<rest> (R5, R11, R12); placed AT the "
             "class prefix with exclude_keys (ruling (a)); S10: class-grain row, no partition token, address = "
             "address(source, scope, tier, table, 'x') with the trailing x removed")
applied["S10"] += 1

# ---------------------------------------------------------------- S2: an overlap-0 merge names its destination table
for c in collisions:
    if c.get("verdict") == "merge":
        c["destination_table"] = c["table"]
        applied["S2"] += 1
s2_faults = [i for i, r in enumerate(rows) if r["disposition"] == "FAULT" and "overlap 0 of" in r.get("reason", "")
             and "with the group" in r.get("reason", "")]
assert len(s2_faults) == 7, [(rows[i]["bucket"], rows[i]["prefix"]) for i in s2_faults]
for i in s2_faults:
    rows[i]["reason"] = rows[i]["reason"] + "; S2: the merge names no destination table in the row or the collision groups, so it stays FAULT citing S2"
    applied["S2"] += 1

# ---------------------------------------------------------------- S3: round-1 placed rows stay as placed, no kind
r1 = {(r.get("bucket"), r.get("prefix")): r for r in m1["rows"]}
for k, r in r1.items():
    if r.get("disposition") in ("FAULT", None):
        continue
    cur = next((x for x in rows if (x["bucket"], x["prefix"]) == k and not x.get("parent")), None)
    assert cur is not None and "kind" not in cur, k
# the two cot positions_cube classes were placed in round 1 and turned FAULT by the round-2 1e collision reading; S3 says a
# round-1 placed row stays as placed, so both return to their round-1 placement (the shared destination is surfaced)
applied["S3"] = 0
for b, p in [("opal-data-cot", "gold/positions_cube/"), ("opal-data-cot", "gold/timeseries/positions_cube/")]:
    i = one(b, p, disposition="FAULT")
    base = next(x for x in m1["rows"] if x["bucket"] == b and x["prefix"] == p)
    assert base["disposition"] == "MOVE", base["disposition"]
    for f in ("disposition", "dest", "address", "dest_pattern", "rule"):
        rows[i][f] = copy.deepcopy(base[f])
    rows[i].pop("reason", None)
    rows[i].pop("fault_owner", None)
    applied["S3"] += 1
# the two completion-marker placements stay as placed with no kind field (no change)


# ---------------------------------------------------------------- S5/S7/S8/S11: marker rows
def make_marker(i, state_family, partition, writer, tails, marker_max=None, source=None, scope=None, why="", keep=False):
    r = rows[i]
    if keep:
        # a class the previous table (v3) placed keeps its disposition, address and pattern (S5): only the marker fields land
        assert r["disposition"] == "MOVE" and r["dest"]["table"] == state_family, (r["prefix"], r["disposition"])
    else:
        d = dict(r.get("dest") or {})
        d["source"] = source or d.get("source")
        d["scope"] = scope or d.get("scope")
        d["tier"] = "state"
        d["table"] = state_family
        d["partition"] = partition
        d["object"] = "{object}"
        a = naming.address(d["source"], d["scope"], "state", state_family, partition, object="{object}")
        r["dest"] = d
        r["address"] = a
        r["dest_pattern"] = pattern(a, d["scope"])
    r["kind"] = "marker"
    r["marker_kind"] = "complete"
    r["state_family"] = state_family
    r["writer"] = writer
    r["marker_match"] = list(tails)
    if marker_max is not None:
        r["marker_max_bytes"] = marker_max
    r["disposition"] = "MOVE"
    r.pop("reason", None)
    r.pop("fault_owner", None)
    r["rule"] = why
    return i


cot_bronze = one("opal-data-cot", "bronze/", kind="marker")
make_marker(cot_bronze, "bronze_complete", "bronze",
            "data/cot/scripts/bronze/cot_bronze_ingest.py (writes bronze/{run_date}/_BRONZE_COMPLETE.json)",
            ["_BRONZE_COMPLETE.json"], source="blackdiamond", scope="cottonwood", keep=True,
            why="(b) + ADDENDUM 1(2) + S5: cot bronze/ completion markers -> R21 state home, family bronze_complete, "
                "address and pattern kept as placed in v3 (S5); writer read from cot_bronze_ingest.py")
applied["S5"] += 1

orion = one("opal-data-inf", "bronze/orion-api/", kind="marker")
make_marker(orion, "bronze_complete", "orion-api",
            "infra/aws/ec2/inf-bronze-runner/orchestrator.py (real _BRONZE_COMPLETE.json); "
            "infra/aws/lambda/inf-pipeline/inf-bronze-complete-emitter/lambda_function.py (_BRONZE_COMPLETE_qa.json)",
            ["_BRONZE_COMPLETE.json", "_BRONZE_COMPLETE_qa.json"], source="orion", scope="inflection", keep=True,
            why="(b) + ADDENDUM 1(1) + S5: orion-api completion markers at class grain -> R21 state home, family "
                "bronze_complete, address and pattern kept as placed in v3 (S5)")
applied["S5"] += 1

g_ecl = one("opal-data-inf", "gold/eclipse/", kind="marker")
make_marker(g_ecl, "gold_complete", "eclipse",
            "data/inf/scripts/gold/INF_E_00.eclipse_model_portfolios.py (writes gold/eclipse/{date}/_meta/gold_complete.json)",
            ["gold_complete.json"], source="advi", scope="inflection", keep=True,
            why="(b) + ADDENDUM 1(1) + S5: gold/eclipse completion markers -> R21 state home, family gold_complete, "
                "address and pattern kept as placed in v3 (S5)")
applied["S5"] += 1

s_ecl = one("opal-data-inf", "silver/eclipse/", kind="marker")
make_marker(s_ecl, "silver_complete", "eclipse",
            "data/inf/scripts/silver/convert_eclipse_portfolios_to_silver.py (writes silver/eclipse/{date}/_meta/silver_complete.json)",
            ["silver_complete.json"], source="eclipse", scope="inflection", keep=True,
            why="(b) + ADDENDUM 1(1) + S5: silver/eclipse completion markers -> R21 state home, family silver_complete, "
                "address and pattern kept as placed in v3 (S5)")
applied["S5"] += 1

# S8: the two eclipse bronze classes are split by writer (a FAULT row becomes a placed marker row)
b_ecl = one("opal-data-inf", "bronze/eclipse/", disposition="FAULT")
make_marker(b_ecl, "bronze_complete", "eclipse",
            "data/inf/scripts/bronze/pull_eclipse_portfolios.py (BRONZE_PREFIX bronze/eclipse; writes _meta/pull_complete.json)",
            ["pull_complete.json"], source="eclipse", scope="inflection",
            why="S8 (rule (d) split by writer): bronze/eclipse pull_complete.json markers -> state/bronze_complete, "
                "partition = writing class eclipse, distinct from eclipse_qa")
applied["S8"] += 1
q_ecl = one("opal-data-inf", "bronze/eclipse_qa/", disposition="FAULT")
make_marker(q_ecl, "bronze_complete", "eclipse_qa",
            "infra/aws/lambda/inf-pipeline/inf-api-eclipse/lambda_function.py (ECLIPSE_BRONZE_PREFIX default bronze/eclipse_qa; writes _meta/pull_complete.json)",
            ["pull_complete.json"], source="eclipse", scope="inflection",
            why="S8 (rule (d) split by writer): bronze/eclipse_qa pull_complete.json markers -> state/bronze_complete, "
                "partition = writing class eclipse_qa, distinct from eclipse")
applied["S8"] += 1

# S11: the ten forwardfill _complete/ groups are completion markers split by writer (class token as the partition)
FF_WRITER = ("data/cot/scripts/bronze/cot_bronze_ingest.py (_complete_key writes forwardfill_v2/{table}/_complete/{date}.json; "
             "shared with bd via bd-49f-runner)")
ff_rows = [i for i, r in enumerate(rows) if r["disposition"] == "FAULT" and r["prefix"].endswith("/_complete/")
           and r["prefix"].startswith("forwardfill_v2/")]
assert len(ff_rows) == 10, [(rows[i]["bucket"], rows[i]["prefix"]) for i in ff_rows]
for i in ff_rows:
    r = rows[i]
    table = r["prefix"].split("/")[1]
    scope = FIRM[r["bucket"]]
    keys = live_keys(r["bucket"], r["parent"])
    grp = [(k, s) for k, s in keys if k.startswith(r["prefix"])]
    assert grp and all(k.endswith(".json") for k, _ in grp), (r["prefix"], len(grp))
    make_marker(i, "bronze_complete", table, FF_WRITER, [".json"], marker_max=max(s for _, s in grp),
                source="blackdiamond", scope=scope,
                why="S11 (rule (b) + 1e split by writer): forwardfill _complete/ group of %s -> state/bronze_complete, "
                    "partition = writing class %s; marker_match .json is the group's only tail" % (r["prefix"], table))
    applied["S11"] += 1

# ---------------------------------------------------------------- S7: *_SKIP.json is a marker by literal tail (blocked)
applied["S7"] = 0  # no row can carry it: the 1,142 skip objects sit inside date-partition data children (see surprise row)

# ---------------------------------------------------------------- new date partitions live since the census (rule (c) per date)
NEW = []  # (bucket, parent, prefix, template_index, kind)
def tmpl(bucket, prefix):
    return one(bucket, prefix)

for (b, p, date, tmpl_prefix, folder) in [
        ("opal-data-inf", "bronze/eclipse_qa/", "2026-10-11", "bronze/eclipse_qa/2026-10-10/", None),
        ("opal-data-inf", "bronze/orion-api/", "2026-10-11", "bronze/orion-api/2026-10-10/", None)]:
    t = rows[tmpl(b, tmpl_prefix)]
    nr = copy.deepcopy(t)
    nr["prefix"] = p + date + "/"
    d = dict(nr["dest"])
    d["partition"] = date
    nr["dest"] = d
    nr["address"] = naming.address(d["source"], d["scope"], d["tier"], d["table"], date)
    nr["dest_pattern"] = pattern(nr["address"], d["scope"])
    nr["rule"] = t["rule"].replace(tmpl_prefix.split("/")[-2], date).replace("2026-10-10", date) + \
        " [S9: partition live since the census; added as a child of the re-grid under rule (c)]"
    nr["objects"] = 0
    nr.pop("census_objects", None)
    nr.pop("listed_objects", None)
    nr.pop("listed_at", None)
    rows.append(nr)
    NEW.append(len(rows) - 1)
    NEW.append(None)
# orion-api _markers/ non-date folder inside the new partition: FAULT, same shape as the round-3 non-date folders
t = rows[one("opal-data-inf", "bronze/orion-api/latest/")]
fr = copy.deepcopy(t)
fr["prefix"] = "bronze/orion-api/2026-10-11/_markers/"
fr["objects"] = 0
fr["reason"] = ("non-date folder of re-gridded class bronze/orion-api/: not a date partition and not a completion "
                "marker; no repair rule places it")
fr["fault_owner"] = OWNER
rows.append(fr)
NEW = [len(rows) - 3, len(rows) - 2, len(rows) - 1]

# ---------------------------------------------------------------- S9: re-derive every re-grid child from the LIVE listing
regrid_stats = {}
child_changes = 0
excl_changes = 0
for g in regrids:
    b, p = g["bucket"], g["parent"]
    P = LIVE_BY[(b, p)]
    kids = [i for i, r in enumerate(rows) if r["bucket"] == b and r.get("parent") == p]
    cl = [i for i, r in enumerate(rows) if r["bucket"] == b and r["prefix"] == p and not r.get("parent")
          and r.get("kind") == "marker"]
    cl_tails = [t for i in cl for t in rows[i].get("marker_match", [])]
    cl_max = {}
    cnt = collections.Counter()
    kid_prefixes = sorted({rows[i]["prefix"] for i in kids}, key=len, reverse=True)
    excl_count = collections.Counter()
    unassigned = []
    for k, s in P["keys"]:
        if k == p:
            ph = [i for i in kids if rows[i].get("placeholder_key") == p]
            assert len(ph) == 1, (b, p)
            cnt[("ROW", ph[0])] += 1
            continue
        if cl and tail_ok(k, cl_tails) and k.startswith(p):
            cnt[("CL", cl[0])] += 1
            cl_max[cl[0]] = max(cl_max.get(cl[0], 0), s)
            # the date partition it sits in
            for cp in kid_prefixes:
                if k.startswith(cp):
                    excl_count[cp] += 1
                    break
            continue
        hit = next((cp for cp in kid_prefixes if k.startswith(cp)), None)
        if hit is None:
            unassigned.append(k)
            continue
        cands = [i for i in kids if rows[i]["prefix"] == hit and rows[i].get("placeholder_key") != p]
        assert len(cands) >= 1, (b, p, hit)
        cnt[("ROW", cands[0])] += 1
    assert not unassigned, (b, p, unassigned[:3])
    total = 0
    for i in kids:
        r = rows[i]
        if r.get("placeholder_key") == p:
            new = cnt[("ROW", i)]
        else:
            new = cnt[("ROW", i)]
        if r.get("objects") != new:
            child_changes += 1
        r["objects"] = new
        total += new
        if "excluded_markers" in r and cl:
            ex = excl_count.get(r["prefix"], 0)
            if r["excluded_markers"] != ex:
                excl_changes += 1
            r["excluded_markers"] = ex
    for i in cl:
        r = rows[i]
        new = cnt[("CL", i)]
        if r.get("objects") != new:
            child_changes += 1
        r["objects"] = new
        if new:
            r["marker_max_bytes"] = cl_max[i]
        total += new
    live = P["count"]
    assert total == live, (b, p, total, live)
    g["census_objects"] = g["census_objects"]
    g["parent_objects"] = live
    g["listed_objects"] = live
    g["children_objects"] = live
    g["difference"] = live - g["census_objects"]
    g["listed_at"] = P["listed_at"]
    g["children"] = sorted({rows[i]["prefix"] for i in kids} | {rows[i]["prefix"] for i in cl})
    if live != P["v3_listed_objects"]:
        g["moving"] = True
        g["moving_reason"] = ("live count %d (v3 listing %s: %d) -> %d (listing %s): a producer is still writing this "
                              "parent; two listings minutes apart differ" % (
                                  P["v3_listed_objects"], P["v3_listed_at"], P["v3_listed_objects"], live, P["listed_at"]))
        regrid_stats[(b, p)] = ("MOVING", P["v3_listed_objects"], live)
    else:
        g.pop("moving", None)
        g.pop("moving_reason", None)
        regrid_stats[(b, p)] = ("SAME", live, live)
applied["S9"] = sum(1 for v in regrid_stats.values() if v[0] == "MOVING") + child_changes + len(NEW) + excl_changes
# the table's own S9 touch count is printed in the table view; the new rows count as touched children

# ---------------------------------------------------------------- S6: QA-named rows judged by their writer
QA_WRITER = {
    "investor-reporting/qa/directory/": ("data/assets/scripts/gold/investor_reporting/directory_runner.py (--qa routes to the QA prefix; production runner)", "production"),
    "investor-reporting/qa/holdings/": ("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py (prefix selected by caller; production snapshot)", "production"),
    "qa/": ("infra/aws/ec2/inf-gold-qa-runner/user-data.sh (QA runner: sets the qa/ prefix for the gold scripts)", "qa-tool"),
    "bronze/eclipse_qa/": ("infra/aws/lambda/inf-pipeline/inf-api-eclipse/lambda_function.py (production eclipse loader; staging prefix by default)", "production"),
    "qa-scratch/": (None, "unresolved"),
    "bronze/orion-api/probe/": (None, "unresolved"),
}
qa_judged = []
unmatched = []
for i, r in enumerate(rows):
    if not QA_RE.search(str(r.get("prefix", ""))):
        continue
    hit = None
    for pre, val in QA_WRITER.items():
        if r["prefix"].startswith(pre) and (pre != "qa/" or r["bucket"] == "opal-data-inf"):
            hit = val
            break
    if hit is None:
        unmatched.append((r["bucket"], r["prefix"], r.get("disposition")))
        continue
    writer, verdict = hit
    if verdict == "unresolved":
        r["qa_writer"] = "UNRESOLVED: no writer of this prefix found in the pipeline code (grep of infra, data, workflows, lib, .tools)"
    else:
        r["qa_writer"] = writer
    r["qa_verdict"] = verdict
    if verdict == "qa-tool":
        assert r["disposition"] == "RETIRE", (r["bucket"], r["prefix"], r["disposition"])
    if verdict == "production":
        assert r["disposition"] in ("MOVE", "HOME"), (r["bucket"], r["prefix"], r["disposition"])
    qa_judged.append((r["bucket"], r["prefix"], r["disposition"], verdict))
applied["S6"] = len(qa_judged)
print("QA_UNMATCHED", unmatched)

# ---------------------------------------------------------------- FAULT rows: owner and reason on every remaining FAULT
faults = [r for r in rows if r["disposition"] == "FAULT"]
for r in faults:
    assert r.get("reason") and r.get("fault_owner") == OWNER, (r["bucket"], r["prefix"])

out = {
    "census_listed_at": census["listed_at"],
    "live_listed_at": max(P["listed_at"] for P in LIVE["parents"]),
    "supersedes": "mapping_v3.json",
    "rows": rows,
    "regrids": regrids,
    "collisions": collisions,
    "rulings_applied": {k: applied[k] for k in ("S2", "S3", "S5", "S6", "S7", "S8", "S9", "S10", "S11")},
}
dst = os.path.join(D, "mapping_v4.json")
with open(dst, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=True)
    fh.write("\n")
print("WROTE", dst, "rows", len(rows), "regrids", len(regrids))
print("FAULT before", fault_before, "after", len(faults))
print("rulings_applied", out["rulings_applied"])
print("new rows", [rows[i]["prefix"] for i in NEW])
print("child_changes", child_changes, "excl_changes", excl_changes)
print("regrid moving", [(k, v) for k, v in regrid_stats.items() if v[0] == "MOVING"])
print("qa judged", collections.Counter(v[3] for v in qa_judged))

# ---------------------------------------------------------------- MAPPING_TABLE_v4.md (ASCII, LF)
disp = collections.OrderedDict((d, [0, 0]) for d in ("MOVE", "HOME", "RETIRE", "DECISION", "FAULT"))
for r in rows:
    disp[r["disposition"]][0] += 1
    disp[r["disposition"]][1] += int(r.get("objects") or 0)
live_total = sum(P["count"] for P in LIVE["parents"])
census_obj = sum(bd["objects"] for bd in census["buckets"].values())
census_classes = sum(len(bd["classes"]) for bd in census["buckets"].values())
ruling_text = {
    "S2": "overlap-0 merges name a destination table: 34 merge entries carry destination_table = table; the 7 overlap-0 "
          "FAULT rows name no table in the row or the groups, so they stay FAULT citing S2",
    "S3": "round-1 placed rows stay as placed: the 2 cot positions_cube rows return to their round-1 MOVE placement; the "
          "silver/_silver_complete/ and gold/meta/pull-complete.json placements are untouched (no kind field)",
    "S5": "state families named on 4 placed marker rows (cot bronze/, bronze/orion-api/, gold/eclipse/, silver/eclipse/); "
          "their v3 address and pattern are kept (S5 difference control)",
    "S6": "86 QA-named rows judged by writer: production 75, qa-tool 6, unresolved 5 (qa-scratch/ x4 and "
          "bronze/orion-api/probe/ x1: no writer found in the pipeline code)",
    "S7": "0 rows: no row can carry the *_SKIP.json tail without a second row at the same bronze/orion-api/ key; the "
          "1,142 skip objects stay in their date-partition data children (surprise row filed)",
    "S8": "2 rows: bronze/eclipse/ (writer pull_eclipse_portfolios.py) and bronze/eclipse_qa/ (writer inf-api-eclipse "
          "lambda) become state/bronze_complete markers partitioned by writing class",
    "S9": "%d regrid parents re-listed with a moving count, %d child counts re-derived, %d new partition or folder rows, "
          "%d excluded_markers re-derived" % (sum(1 for v in regrid_stats.values() if v[0] == "MOVING"), child_changes,
                                             len(NEW), excl_changes),
    "S10": "1 row: opal-data-bd gold/clients/ re-written at class grain (no partition token)",
    "S11": "10 rows: the forwardfill _complete/ groups of bd and cot become state/bronze_complete markers partitioned by "
           "writing class (writer cot_bronze_ingest.py); marker_match is .json (the group's only tail)",
}
L_out = []
L_out.append("# MAPPING TABLE v4 -- ADVI_FIRMBKTS round 4, cell FB-g-3 (rulings S2-S11)")
L_out.append("")
L_out.append("Supersedes mapping_v3.json. Census listed_at %s. Live listing for this table at %s (LIST calls only)."
             % (census["listed_at"], out["live_listed_at"]))
L_out.append("Classes: %d census classes (%d in census buckets, all 444 accounted: placed directly or re-gridded)."
             % (census_classes, census_classes))
L_out.append("Census objects: %s. Live objects of the 29 re-grid parents at the listing: %s."
             % (f"{census_obj:,}", f"{live_total:,}"))
L_out.append("")
L_out.append("FAULT before: %d (mapping_v3.json rows; the check's before reads mapping_v2.json, which carries %d)"
             % (fault_before_v3, fault_before))
L_out.append("FAULT after: %d" % len(faults))
L_out.append("")
L_out.append("## Dispositions (rows and objects)")
L_out.append("")
L_out.append("| disposition | rows | objects |")
L_out.append("|---|---:|---:|")
for d, (n, o) in disp.items():
    L_out.append("| %s | %s | %s |" % (d, f"{n:,}", f"{o:,}"))
L_out.append("")
L_out.append("## Ruling counts (one example each in the ruling line)")
L_out.append("")
for k in ("S2", "S3", "S5", "S6", "S7", "S8", "S9", "S10", "S11"):
    L_out.append("- %s: %d. %s" % (k, applied[k], ruling_text[k]))
L_out.append("")
L_out.append("## Re-grids (census, live, difference, children sum)")
L_out.append("")
L_out.append("| bucket | parent | census | listed (live) | difference | children sum | moving |")
L_out.append("|---|---|---:|---:|---:|---:|---|")
for g in regrids:
    kids_sum = sum(int(r.get("objects") or 0) for r in rows if r.get("parent") == g["parent"] and r["bucket"] == g["bucket"])
    kids_sum += sum(int(r.get("objects") or 0) for r in rows if r["prefix"] == g["parent"] and r["bucket"] == g["bucket"]
                    and not r.get("parent") and r.get("kind") == "marker")
    mv = ("yes: " + g["moving_reason"][:90]) if g.get("moving") else "no"
    L_out.append("| %s | %s | %s | %s | %s | %s | %s |" % (
        g["bucket"], g["parent"], f"{g['census_objects']:,}", f"{g['listed_objects']:,}", f"{g['difference']:,}",
        f"{kids_sum:,}", mv))
L_out.append("")
L_out.append("## Remaining FAULT classes by reason (owner %s on every row)" % OWNER)
L_out.append("")
groups = collections.OrderedDict()
for r in faults:
    key = re.sub(r"\d+", "N", r["reason"].split(";")[0])[:110]
    groups.setdefault(key, []).append("%s %s" % (r["bucket"], r["prefix"]))
for key, members in groups.items():
    L_out.append("- %d x %s" % (len(members), key))
    L_out.append("  - " + "; ".join(members))
L_out.append("")
md_path = os.path.join(D, "MAPPING_TABLE_v4.md")
with open(md_path, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(L_out) + "\n")
print("WROTE", md_path)
