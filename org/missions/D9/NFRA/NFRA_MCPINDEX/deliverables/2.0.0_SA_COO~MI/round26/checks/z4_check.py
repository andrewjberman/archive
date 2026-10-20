"""z4_check.py <z4.AC1|z4.AC2> <coverage_two.json>: the round-26 (workstream GATEWAY) criteria of cell MX-z-4, run from the repository root.
Prints a DENOMINATOR line, one line per arm, then ARMS and RESULT: PASS|FAIL. ASCII only; python 3.9.
Contract: decompositions/NFRA_MCPINDEX_DECOMP.round26-GATEWAY.md section R26.3 (Z4 COVERAGE TWO).
AC1: shape and coverage (exactly the two refused tools opal_describe and opal_discover, once each, schema, disposition, row versus c shape),
with planted mutants that must be refused.
AC2: grounding (a row item: a new unique entity, bucket/prefix overlapping an s3 source of the tool, a vendor in the vocabulary; every item: a
reason of at least eight ASCII words and a cite that resolves; an entity a reason names must exist in the catalog), with planted mutants
that must be refused. Mutants are planted from the data present: when the file holds no row item, a c item is turned into a row-form item."""
import copy
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
R26 = os.path.normpath(os.path.join(HERE, ".."))
DELIV = os.path.normpath(os.path.join(R26, ".."))
DELIV = os.path.dirname(DELIV)
EVID25 = os.path.join(DELIV, "2.0.0_SA_COO~MI", "round25", "evidence")
REFUSALS = os.path.join(EVID25, "COVERAGE_r25_candidate_c.json")
CATALOG = os.path.join("infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
SCHEMA = "gateway_coverage_two/1"
EXTRA_VENDORS = ("opal", "ycharts", "microsoft", "bloomberg", "other")
SECTION_NAMES = ("portal_datasets", "silver_datasets", "harvest_datasets")
ENTITY_PREFIXES = ("portal_", "opal_data_", "harvest_", "dynamodb_", "silver_")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def is_ascii(text):
    return all(ord(ch) < 128 for ch in text)


def load_refusals():
    doc = jload(REFUSALS)
    return sorted(r["subject"] for r in doc["refusals"] if r.get("class") == "tool_member_b")


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
        for key in ("tool", "disposition", "reason", "cite"):
            if not isinstance(it.get(key), str) or not it.get(key).strip():
                out.append("%s: %s missing or not a non-empty string" % (tool, key))
        if it.get("disposition") not in ("row", "c"):
            out.append("%s: disposition %r not row|c" % (tool, it.get("disposition")))
        elif it["disposition"] == "row" and not isinstance(it.get("row"), dict):
            out.append("%s: disposition row needs a row object" % tool)
        elif it["disposition"] == "c" and it.get("row") is not None:
            out.append("%s: disposition c needs row null" % tool)
    out += ["%s appears %d times" % (t, n) for t, n in seen.items() if n > 1]
    out += ["tool %s has no item" % t for t in refused if t not in seen]
    out += ["tool %s is not a refusal of the coverage file" % t for t in sorted(seen, key=str) if t not in refused]
    if not is_ascii(json.dumps(doc, ensure_ascii=False)):
        out.append("the file holds a non-ASCII character")
    return out


def named_entities_missing(reason, entities, tools):
    """Entity-looking tokens of a reason (portal_/opal_data_/harvest_/dynamodb_/silver_ prefixes) that are neither a catalog entity, a tool nor a section name."""
    bad = []
    for tok in re.findall(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", reason or ""):
        if tok.startswith(ENTITY_PREFIXES) and tok not in entities and tok not in tools and tok not in SECTION_NAMES:
            bad.append(tok)
    return bad


def problems_ac2(doc, sources, entities, vendors):
    out, ents = [], {}
    for it in doc.get("items", []):
        tool = it.get("tool")
        reason = it.get("reason") or ""
        if words(reason) < 8 or not is_ascii(reason):
            out.append("%s: reason is under eight ASCII words" % tool)
        for tok in named_entities_missing(reason, entities, sources):
            out.append("%s: the reason names %s, which is no catalog entity" % (tool, tok))
        if not cite_resolves(it.get("cite")):
            out.append("%s: cite %r does not resolve" % (tool, it.get("cite")))
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
    add("a foreign tool", lambda d: d["items"][0].update(tool="no_such_tool_in_the_refusals"))
    add("a wrong schema", lambda d: d.update(schema="gateway_coverage_two/0"))
    add("a bad disposition", lambda d: d["items"][0].update(disposition="maybe"))
    add("a row item without a row object", lambda d: d["items"][0].update(disposition="row", row=None))
    add("a c item that carries a row", lambda d: d["items"][0].update(disposition="c", row={"entity": "x"}))
    add("a non-ASCII reason", lambda d: d["items"][0].update(reason="cafe" + chr(233) + " reason that is long enough to count here ok"))
    return m


def row_form(item, entities):
    """A valid-looking row-form copy of an item, built from the data present (a c item turned into a row)."""
    probe = copy.deepcopy(item)
    probe["disposition"] = "row"
    probe["row"] = {"entity": "z4_probe_row_that_is_new", "bucket": "opal-data-portal-v2", "prefix": "served/", "vendor": "opal", "firm": "none"}
    return probe


def mutants_ac2(doc, entities):
    """(label, mutated doc, fragment of the refusal line the mutant must produce)."""
    m = []

    def add(label, edit, expect):
        d = copy.deepcopy(doc)
        edit(d)
        m.append((label, d, expect))

    r = first(doc, "row")
    if r is None and doc["items"]:
        # no row item present: plant the row-form mutants from a copy of the first item turned into a row
        def make_row(d):
            d["items"][0] = row_form(d["items"][0], entities)
        r = 0
        base_edit = make_row
    else:
        def base_edit(d):
            return None

    def on_row(edit):
        def go(d):
            base_edit(d)
            edit(d["items"][r]["row"])
        return go

    if r is not None:
        add("an entity already in the catalog", on_row(lambda row: row.update(entity=sorted(entities)[0])), "already in the catalog")
        add("a bucket no source names", on_row(lambda row: row.update(bucket="bucket-that-no-source-names")), "overlaps no s3 source")
        add("a vendor outside the vocabulary", on_row(lambda row: row.update(vendor="zzz_vendor")), "not in the vocabulary")
        if len(doc["items"]) > 1:
            def twin(d):
                base_edit(d)
                other = 1 if r == 0 else 0
                d["items"][other] = row_form(d["items"][other], entities)
                d["items"][other]["row"]["entity"] = d["items"][r]["row"]["entity"]
            add("two items with one entity", twin, "used by")
    if doc["items"]:
        i = len(doc["items"]) - 1
        add("a three-word reason", lambda d: d["items"][i].update(reason="too short"), "under eight")
        add("a cite to a missing file", lambda d: d["items"][i].update(cite="app/no_such_file_anywhere.py:3"), "does not resolve")
        add("a cite past the end of the file", lambda d: d["items"][i].update(cite="app/tools.py:99999999"), "does not resolve")
        add("a reason that names an entity the catalog lacks",
            lambda d: d["items"][i].update(reason=d["items"][i]["reason"] + " and the rows portal_no_such_entity_zz cover it"), "no catalog entity")
    return m


def run(cid, path):
    refused = load_refusals()
    sources = load_sources()
    entities, vendors = load_catalog()
    print("DENOMINATOR: %d tool(s) in scope: the tool_member_b refusals of COVERAGE_r25_candidate_c.json (%s); %d catalog entities, %d tools with a traced source set"
          % (len(refused), ", ".join(refused), len(entities), len(sources)))
    if not path or not os.path.isfile(path):
        arm("the deliverable exists", False, "absent: %s" % path)
        return
    try:
        doc = jload(path)
    except ValueError as exc:
        arm("the deliverable is JSON", False, str(exc))
        return
    if cid == "z4.AC1":
        real = problems_ac1(doc, refused)
        arm("schema, items, disposition, row versus c shape and the two refused tools exactly once each", not real, "; ".join(real[:4]))
        arm("only the 2 tools of the refusal file are present (%d items)" % len(doc.get("items", [])), len(doc.get("items", [])) == len(refused) and not real)
        if doc.get("items"):
            for label, mut in mutants_ac1(doc):
                arm("planted mutant refused: %s" % label, bool(problems_ac1(mut, refused)))
    else:
        base = problems_ac1(doc, refused)
        arm("AC1 shape holds (the grounding below reads items)", not base, "; ".join(base[:3]))
        real = problems_ac2(doc, sources, entities, vendors)
        arm("every reason is long and names real entities, every cite resolves; a row item has a new unique entity, a bucket/prefix overlapping an s3 source and a vendor in the vocabulary",
            not real, "; ".join(real[:4]))
        n_row = sum(1 for it in doc.get("items", []) if it.get("disposition") == "row")
        print("  info rows=%d c=%d" % (n_row, len(doc.get("items", [])) - n_row))
        if not base:
            for label, mut, expect in mutants_ac2(doc, entities):
                found = [x for x in problems_ac2(mut, sources, entities, vendors) if expect in x]   # refused for the planted defect itself
                arm("planted mutant refused: %s" % label, bool(found))


if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in ("z4.AC1", "z4.AC2"):
        print("usage: z4_check.py <z4.AC1|z4.AC2> <coverage_two.json>")
        sys.exit(9)
    run(cid, sys.argv[2] if len(sys.argv) > 2 else None)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
