"""w5_check.py <w5.AC1|w5.AC2> <coverage_rows.json>: the round-24 (workstream GATEWAY) criteria of cell MX-w-5, run from the repository root.
Prints a DENOMINATOR line, one line per arm, then ARMS and RESULT: PASS|FAIL. ASCII only; python 3.9.
Contract: decompositions/NFRA_MCPINDEX_DECOMP.round24-GATEWAY.md section R24.3 (W5 COVERAGE ROWS).
AC1: shape and coverage (exactly the 36 refused tools, once each, owner, disposition, schema), with planted mutants that must be refused.
AC2: grounding (row items overlap a traced s3 source, entity new and unique, vendor in the vocabulary; c items give a long reason and a cite that
resolves), with planted mutants that must be refused."""
import copy
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
R24 = os.path.normpath(os.path.join(HERE, ".."))
DELIV = os.path.normpath(os.path.join(R24, "..", ".."))
EVID = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round23", "evidence")
REFUSALS = os.path.join(EVID, "COVERAGE_after_apply_20261019.json")
CATALOG = os.path.join("infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
SCHEMA = "gateway_coverage_rows/1"
EXTRA_VENDORS = ("opal", "ycharts", "microsoft", "bloomberg", "other")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def is_ascii(text):
    return all(ord(ch) < 128 for ch in text)


def load_refusals():
    doc = jload(REFUSALS)
    return {r["subject"]: r["detail"] for r in doc["refusals"] if r.get("class") == "tool_member_b"}


def load_sources():
    by_tool = {}
    for path in sorted(glob.glob(os.path.join(DELIV, "0.9.0_WK_NFRA_MCPINDEX~7[1-6]", "source_sets_*.json"))):
        for entry in jload(path).get("tools", []):
            by_tool.setdefault(entry["tool"], []).extend(entry.get("sources", []))
    return by_tool


def load_catalog():
    with open(CATALOG, encoding="utf-8", errors="replace") as fh:
        cat = yaml.safe_load(fh)
    entities, vendors = set(), set(EXTRA_VENDORS)
    for key in ("silver_datasets", "portal_datasets", "harvest_datasets"):
        for row in cat.get(key) or []:
            entities.add(row["entity"])
            if row.get("vendor"):
                vendors.add(row["vendor"])
    return entities, vendors


def overlap(bucket, prefix, src):
    if src.get("kind") != "s3" or src.get("bucket") != bucket:
        return False
    other = src.get("prefix") or ""
    return prefix.startswith(other) or other.startswith(prefix)


def cite_resolves(cite):
    m = re.match(r"^(.+):(\d+)$", cite or "")
    if not m:
        return False
    rel, num = m.group(1).replace("\\", "/"), int(m.group(2))
    for cand in (rel, os.path.join(GW, rel)):
        if os.path.isfile(cand):
            with open(cand, encoding="utf-8", errors="replace") as fh:
                return 1 <= num <= sum(1 for _ in fh)
    return False


def words(text):
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def problems_ac1(doc, refused):
    out = []
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    items = doc.get("items")
    if not isinstance(items, list):
        return ["items is not a list"]
    seen = {}
    for it in items:
        if not isinstance(it, dict):
            out.append("an item is not an object")
            continue
        tool = it.get("tool")
        seen[tool] = seen.get(tool, 0) + 1
        for key in ("tool", "owner", "disposition", "reason", "cite"):
            if not isinstance(it.get(key), str) or not it.get(key).strip():
                out.append("%s: %s missing or not a non-empty string" % (tool, key))
        if it.get("disposition") not in ("row", "c"):
            out.append("%s: disposition %r not row|c" % (tool, it.get("disposition")))
        elif it["disposition"] == "row" and not isinstance(it.get("row"), dict):
            out.append("%s: disposition row needs a row object" % tool)
        elif it["disposition"] == "c" and it.get("row") is not None:
            out.append("%s: disposition c needs row null" % tool)
        if tool in refused and it.get("owner") != refused[tool]:
            out.append("%s: owner %r is not the refusal detail %r" % (tool, it.get("owner"), refused[tool]))
    out += ["%s appears %d times" % (t, n) for t, n in seen.items() if n > 1]
    out += ["tool %s has no item" % t for t in sorted(refused) if t not in seen]
    out += ["tool %s is not a refusal of the coverage file" % t for t in sorted(seen) if t not in refused]
    if not is_ascii(json.dumps(doc, ensure_ascii=False)):
        out.append("the file holds a non-ASCII character")
    return out


def problems_ac2(doc, sources, entities, vendors):
    out, ents = [], {}
    for it in doc.get("items", []):
        tool = it.get("tool")
        if it.get("disposition") == "row":
            row = it.get("row") or {}
            for key in ("entity", "bucket", "prefix", "vendor", "firm"):
                if not isinstance(row.get(key), str):
                    out.append("%s: row.%s is not a string" % (tool, key))
            ent = row.get("entity") if isinstance(row.get("entity"), str) else ""
            if not re.match(r"^[a-z0-9_]+$", ent):
                out.append("%s: entity %r is not lower-case words with underscores" % (tool, ent))
            if ent in entities:
                out.append("%s: entity %s is already in the catalog" % (tool, ent))
            ents[ent] = ents.get(ent, 0) + 1
            b, p = row.get("bucket") or "", row.get("prefix") or ""
            if not any(overlap(b, p, s) for s in sources.get(tool, [])):
                out.append("%s: bucket/prefix %s %s overlaps no s3 source of the tool" % (tool, b, p))
            if row.get("vendor") not in vendors:
                out.append("%s: vendor %r is not in the vocabulary" % (tool, row.get("vendor")))
        elif it.get("disposition") == "c":
            reason = it.get("reason") or ""
            if words(reason) < 8 or not is_ascii(reason):
                out.append("%s: reason is under eight ASCII words" % tool)
            if not cite_resolves(it.get("cite")):
                out.append("%s: cite %r does not resolve" % (tool, it.get("cite")))
        if not re.match(r"^.+:\d+$", it.get("cite") or ""):
            out.append("%s: cite %r is not <path>:<line>" % (tool, it.get("cite")))
    out += ["entity %s used by %d items" % (e, n) for e, n in ents.items() if n > 1]
    return out


def first(doc, disposition):
    for i, it in enumerate(doc["items"]):
        if it.get("disposition") == disposition:
            return i
    return None


def mutants_ac1(doc):
    m = []

    def add(label, edit):
        d = copy.deepcopy(doc)
        edit(d)
        m.append((label, d))

    add("a tool dropped", lambda d: d["items"].pop())
    add("a tool twice", lambda d: d["items"].append(copy.deepcopy(d["items"][0])))
    add("a wrong owner", lambda d: d["items"][0].update(owner="NOT_THE_OWNER"))
    add("a foreign tool", lambda d: d["items"][0].update(tool="no_such_tool_in_the_refusals"))
    add("a wrong schema", lambda d: d.update(schema="gateway_coverage_rows/0"))
    add("a bad disposition", lambda d: d["items"][0].update(disposition="maybe"))
    add("a non-ASCII reason", lambda d: d["items"][0].update(reason="cafe" + chr(233) + " reason that is long enough to count here ok"))
    return m


def mutants_ac2(doc, entities):
    m = []

    def add(label, edit):
        d = copy.deepcopy(doc)
        edit(d)
        m.append((label, d))

    r = first(doc, "row")
    if r is not None:
        add("an entity already in the catalog", lambda d: d["items"][r]["row"].update(entity=sorted(entities)[0]))
        add("a bucket no source names", lambda d: d["items"][r]["row"].update(bucket="bucket-that-no-source-names"))
        add("a vendor outside the vocabulary", lambda d: d["items"][r]["row"].update(vendor="zzz_vendor"))
        others = [i for i, it in enumerate(doc["items"]) if it.get("disposition") == "row" and i != r]
        spare = first(doc, "c")
        if others:
            add("two items with one entity", lambda d: d["items"][others[0]]["row"].update(entity=d["items"][r]["row"]["entity"]))
        elif spare is not None:
            # the data holds one row item: turn a c item into a copy of it so the repeated-entity rule is still exercised
            add("two items with one entity", lambda d: d["items"][spare].update(disposition="row", row=copy.deepcopy(d["items"][r]["row"])))
    c = first(doc, "c")
    if c is not None:
        add("a three-word reason", lambda d: d["items"][c].update(reason="too short"))
        add("a cite to a missing file", lambda d: d["items"][c].update(cite="app/no_such_file_anywhere.py:3"))
        add("a cite past the end of the file", lambda d: d["items"][c].update(cite="app/tools.py:99999999"))
    return m


def run(cid, path):
    refused = load_refusals()
    sources = load_sources()
    entities, vendors = load_catalog()
    print("DENOMINATOR: %d tool(s) in scope: the tool_member_b refusals of COVERAGE_after_apply_20261019.json; %d catalog entities, %d tools with a traced source set"
          % (len(refused), len(entities), len(sources)))
    if not path or not os.path.isfile(path):
        arm("the deliverable exists", False, "absent: %s" % path)
        return
    try:
        doc = jload(path)
    except ValueError as exc:
        arm("the deliverable is JSON", False, str(exc))
        return
    if cid == "w5.AC1":
        real = problems_ac1(doc, refused)
        arm("schema, items, owner, disposition and the 36 refused tools exactly once each", not real, "; ".join(real[:4]))
        arm("only the 36 tools of the refusal file are present (%d items)" % len(doc.get("items", [])), len(doc.get("items", [])) == len(refused) and not real)
        if doc.get("items"):
            for label, mut in mutants_ac1(doc):
                arm("planted mutant refused: %s" % label, bool(problems_ac1(mut, refused)))
    else:
        base = problems_ac1(doc, refused)
        arm("AC1 shape holds (the grounding below reads items)", not base, "; ".join(base[:3]))
        real = problems_ac2(doc, sources, entities, vendors)
        arm("row items grounded (new unique entity, bucket/prefix overlap a traced s3 source, vendor in vocabulary); c items give a long reason and a cite that resolves",
            not real, "; ".join(real[:4]))
        n_row = sum(1 for it in doc.get("items", []) if it.get("disposition") == "row")
        print("  info rows=%d c=%d" % (n_row, len(doc.get("items", [])) - n_row))
        if not base:
            for label, mut in mutants_ac2(doc, entities):
                found = problems_ac2(mut, sources, entities, vendors)
                if label == "two items with one entity":
                    found = [x for x in found if "used by" in x]   # refused for the repeated entity, not for another reason
                arm("planted mutant refused: %s" % label, bool(found))


if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in ("w5.AC1", "w5.AC2"):
        print("usage: w5_check.py <w5.AC1|w5.AC2> <coverage_rows.json>")
        sys.exit(9)
    run(cid, sys.argv[2] if len(sys.argv) > 2 else None)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
