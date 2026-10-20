"""z1_check.py <z1.AC1|z1.AC2> [uncatalogued_rows.json]: the round-26 (workstream GATEWAY) criteria of cell MX-z-1, run from the repository root.
Prints a DENOMINATOR line, one line per arm, then ARMS and RESULT: PASS|FAIL. ASCII only; python 3.9.
Contract: decompositions/NFRA_MCPINDEX_DECOMP.round26-GATEWAY.md section R26.3 (Z1 UNCATALOGUED ROWS).
AC1: shape and coverage (exactly the 15 live-extra census tables, once each, keyed by bucket and prefix, order, schema, disposition,
     the no-reason rule for three live tables), with planted mutants that must be refused.
AC2: grounding (a row item has a new unique entity and its item's bucket, prefix and table, a vendor in the vocabulary; every item has a reason of
     8 words or more and evidence that resolves), with planted mutants that must be refused.
Every mutant is planted into a clean synthetic document built from the census, so each runs whatever the deliverable holds."""
import copy
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
R26 = os.path.normpath(os.path.join(HERE, ".."))
DELIV = os.path.normpath(os.path.join(R26, "..", ".."))
CENSUS = os.path.join(DELIV, "4.0.0_SA_CRO~Y", "census.json")
CATALOG = os.path.join("infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
DEFAULT = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "0.9.0_WK_NFRA_MCPINDEX~90", "uncatalogued_rows.json")
SCHEMA = "gateway_uncatalogued_rows/1"
EXTRA_VENDORS = ("opal", "ycharts", "microsoft", "bloomberg", "other")
FIRST = ("opal-data-inf", "silver/transactions/")
NO_REASON = (("opal-data-inf", "silver/transactions/"), ("opal-data-inf", "silver/orion-rest/transactions/"), ("opal-data-bd", "silver/realized/"))
ENTITY_RE = re.compile(r"^[a-z0-9_]+$")
OK, BAD = [], []


def arm(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  -- " + detail) if (detail and not cond) else ""))


def jload(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return json.load(fh)


def is_ascii(text):
    return isinstance(text, str) and all(ord(ch) < 128 for ch in text)


def words(text):
    return len([w for w in re.split(r"\s+", text.strip()) if w]) if isinstance(text, str) else 0


def load_census():
    """(expected list of (bucket, prefix, table) in contract order, set of all (bucket, prefix) of the census)."""
    entries = jload(CENSUS)
    extra = [(e["bucket"], e["prefix"], e["table"]) for e in entries if e.get("src") == "live-extra"]
    first = [t for t in extra if (t[0], t[1]) == FIRST]
    rest = sorted((t for t in extra if (t[0], t[1]) != FIRST), key=lambda t: (t[0], t[1]))
    return first + rest, {(e["bucket"], e["prefix"]) for e in entries}


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


def evidence_problem(ev, census_keys):
    """None when the evidence entry resolves, else the reason it does not."""
    if not isinstance(ev, str) or not ev.strip():
        return "an evidence entry is empty or not a string"
    if not is_ascii(ev):
        return "evidence %r is not ASCII" % ev
    if "#" in ev:
        path, key = ev.split("#", 1)
        if os.path.basename(path.replace("\\", "/")) != "census.json":
            return "evidence %r: only census.json#<bucket>/<prefix> takes a #" % ev
        bucket, _, prefix = key.partition("/")
        if (bucket, prefix) not in census_keys:
            return "evidence %r names no census entry" % ev
        return None
    m = re.match(r"^(.+):([0-9]+)$", ev)
    if not m:
        return "evidence %r is neither <path>:<line> nor census.json#<bucket>/<prefix>" % ev
    path, line = m.group(1).replace("\\", "/"), int(m.group(2))
    if os.path.isabs(path) or ".." in path.split("/"):
        return "evidence path %r is absolute or climbs out" % path
    for cand in (path, os.path.join(GW, path)):
        if os.path.isfile(cand):
            with open(cand, encoding="utf-8", errors="replace") as fh:
                n = sum(1 for _ in fh)
            return None if 1 <= line <= n else "evidence line %d is outside %s (%d lines)" % (line, path, n)
    return "evidence file %r does not exist" % path


def problems_ac1(doc, expected):
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        return ["schema is not %s" % SCHEMA]
    items = doc.get("items")
    if not isinstance(items, list):
        return ["items is not a list"]
    out, seen, table_of = [], {}, {(b, p): t for b, p, t in expected}
    for it in items:
        if not isinstance(it, dict):
            out.append("an item is not an object")
            continue
        key = (it.get("bucket"), it.get("prefix"))
        seen[key] = seen.get(key, 0) + 1
        for field in ("table", "bucket", "prefix", "reason"):
            if not isinstance(it.get(field), str) or not it[field].strip():
                out.append("%s: %s missing or not a non-empty string" % (key, field))
        if key in table_of and it.get("table") != table_of[key]:
            out.append("%s: table %r is not the census's %r" % (key, it.get("table"), table_of[key]))
        disp = it.get("disposition")
        if disp not in ("row", "reason"):
            out.append("%s: disposition %r is not row|reason" % (key, disp))
        elif disp == "row" and not isinstance(it.get("row"), dict):
            out.append("%s: disposition row needs a row object" % (key,))
        elif disp == "reason" and it.get("row") is not None:
            out.append("%s: disposition reason needs row null" % (key,))
        if disp == "reason" and key in NO_REASON:
            out.append("%s: a reason item is not allowed for this live table" % (key,))
    out += ["%s appears %d times" % (k, n) for k, n in seen.items() if n > 1]
    out += ["table %s has no item" % (k,) for k in table_of if k not in seen]
    out += ["item %s is not a live-extra table of the census" % (k,) for k in seen if k not in table_of]
    keys = [(it.get("bucket"), it.get("prefix")) for it in items if isinstance(it, dict)]
    want = [(b, p) for b, p, _ in expected]
    if sorted(keys) == sorted(want) and keys != want:
        out.append("the items are not in contract order (inf silver/transactions first, then sorted by bucket and prefix)")
    if not is_ascii(json.dumps(doc, ensure_ascii=False)):
        out.append("the file holds a non-ASCII character")
    return out


def problems_ac2(doc, entities, vendors, census_keys):
    out, ents = [], {}
    if not isinstance(doc, dict):
        return ["the document is not an object"]
    for it in doc.get("items") or []:
        if not isinstance(it, dict):
            continue
        key = (it.get("bucket"), it.get("prefix"))
        if it.get("disposition") == "row":
            row = it.get("row") or {}
            for field in ("entity", "bucket", "prefix", "vendor", "firm", "table"):
                if not isinstance(row.get(field), str) or (field != "firm" and not row[field].strip()):
                    out.append("%s: row.%s is not a string" % (key, field))
            ent = row.get("entity") if isinstance(row.get("entity"), str) else ""
            if not ENTITY_RE.match(ent):
                out.append("%s: entity %r is not lower-case words with underscores" % (key, ent))
            if ent in entities:
                out.append("%s: entity %s is already in the catalog" % (key, ent))
            ents[ent] = ents.get(ent, 0) + 1
            for field in ("bucket", "prefix", "table"):
                if row.get(field) != it.get(field):
                    out.append("%s: row.%s %r is not the item's %r" % (key, field, row.get(field), it.get(field)))
            if row.get("vendor") not in vendors:
                out.append("%s: vendor %r is not in the vocabulary" % (key, row.get("vendor")))
        reason = it.get("reason")
        if words(reason) < 8 or not is_ascii(reason):
            out.append("%s: reason is under eight words or not ASCII" % (key,))
        ev = it.get("evidence")
        if not isinstance(ev, list) or not ev:
            out.append("%s: evidence is not a non-empty list" % (key,))
        else:
            for e in ev:
                why = evidence_problem(e, census_keys)
                if why:
                    out.append("%s: %s" % (key, why))
    out += ["entity %s used by %d items" % (e, n) for e, n in ents.items() if n > 1]
    return out


def synthetic(expected, entities):
    """A clean document built from the census alone: a row for every table but the meta folder, a reason for it."""
    items = []
    for bucket, prefix, table in expected:
        base = "z1syn_" + re.sub(r"[^a-z0-9]+", "_", (bucket + "_" + prefix).lower()).strip("_")
        evid = ["census.json#%s/%s" % (bucket, prefix)]
        if table == "meta":
            items.append({"table": table, "bucket": bucket, "prefix": prefix, "disposition": "reason", "row": None,
                          "reason": "a meta folder that holds no data table, so no catalog row describes it", "evidence": evid})
        else:
            items.append({"table": table, "bucket": bucket, "prefix": prefix, "disposition": "row",
                          "row": {"entity": base, "bucket": bucket, "prefix": prefix, "vendor": "orion", "firm": "inflection", "table": table},
                          "reason": "a live advisor table of the Orion and Eclipse producer output kept in this bucket", "evidence": evid})
    assert not any(it["row"] and it["row"]["entity"] in entities for it in items if it["row"])
    return {"schema": SCHEMA, "items": items}


def run_mutants(fn, good, mutants):
    arm("control: a clean synthetic document passes", fn(good) == [], "; ".join(fn(good))[:300])
    for name, mut in mutants:
        d = copy.deepcopy(good)
        mut(d)
        arm("planted mutant refused: %s" % name, bool(fn(d)))


def pick(doc, key):
    for it in doc["items"]:
        if (it["bucket"], it["prefix"]) == key:
            return it
    raise KeyError(key)


def first_with_row(doc, skip=()):
    for it in doc["items"]:
        if it["disposition"] == "row" and (it["bucket"], it["prefix"]) not in skip:
            return it
    raise KeyError("no row item")


def load_deliverable(path):
    if not path or not os.path.isfile(path):
        return None, "deliverable %s absent" % path
    try:
        return jload(path), None
    except (ValueError, OSError) as exc:
        return None, "deliverable %s unreadable: %s" % (path, exc)


def ac1(path):
    expected, _ = load_census()
    entities, _ = load_catalog()
    print("DENOMINATOR: %d live-extra table(s) of the census in scope (src live-extra of 4.0.0_SA_CRO~Y/census.json); first item opal-data-inf silver/transactions/; "
          "11 planted mutants" % len(expected))
    arm("the census holds 15 live-extra tables and the first is inf silver/transactions/", len(expected) == 15 and (expected[0][0], expected[0][1]) == FIRST,
        "read %d" % len(expected))
    good = synthetic(expected, entities)

    def fn(d):
        return problems_ac1(d, expected)

    def drop(d):
        d["items"].pop()

    def twice(d):
        d["items"].append(copy.deepcopy(d["items"][3]))

    def foreign(d):
        d["items"][2]["bucket"] = "opal-data-nowhere"

    def swap_first(d):
        d["items"][0], d["items"][1] = d["items"][1], d["items"][0]

    def reason_for(key):
        def mut(d):
            it = pick(d, key)
            it.update(disposition="reason", row=None, reason="no row is written because the table is judged to be a copy of something else here")
        return mut

    run_mutants(fn, good, [
        ("a table dropped", drop),
        ("a table twice", twice),
        ("a foreign table (bucket not in the census)", foreign),
        ("a wrong schema", lambda d: d.update(schema="gateway_uncatalogued_rows/0")),
        ("a bad disposition", lambda d: d["items"][1].update(disposition="maybe")),
        ("a table name altered", lambda d: d["items"][2].update(table="not_the_census_table")),
        ("the first item moved off inf silver/transactions/", swap_first),
        ("a reason for inf silver/transactions/", reason_for(("opal-data-inf", "silver/transactions/"))),
        ("a reason for orion-rest/transactions/", reason_for(("opal-data-inf", "silver/orion-rest/transactions/"))),
        ("a reason for bd realized/", reason_for(("opal-data-bd", "silver/realized/"))),
        ("a non-ASCII reason", lambda d: d["items"][4].update(reason="a live table with caf" + chr(233) + " style text that is long enough to count")),
    ])
    doc, err = load_deliverable(path)
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = fn(doc)
    arm("the deliverable holds exactly the 15 census tables once each, in order, with schema, disposition and the no-reason rule", not probs, "; ".join(probs)[:600])


def ac2(path):
    expected, census_keys = load_census()
    entities, vendors = load_catalog()
    doc, err = load_deliverable(path)
    n = len(doc.get("items", [])) if isinstance(doc, dict) and isinstance(doc.get("items"), list) else 0
    print("DENOMINATOR: %d item(s) in the deliverable to ground against %d catalog entities, %d census entries and %d vendors in the vocabulary; "
          "12 planted mutants" % (n, len(entities), len(census_keys), len(vendors)))
    good = synthetic(expected, entities)

    def fn(d):
        return problems_ac2(d, entities, vendors, census_keys)

    def row_field(field, value):
        def mut(d):
            first_with_row(d)["row"][field] = value
        return mut

    def repeat_entity(d):
        rows = [it for it in d["items"] if it["disposition"] == "row"]
        rows[1]["row"]["entity"] = rows[0]["row"]["entity"]

    run_mutants(fn, good, [
        ("an entity already in the catalog", row_field("entity", sorted(entities)[0])),
        ("an entity used twice", repeat_entity),
        ("a row bucket altered", row_field("bucket", "opal-data-nowhere")),
        ("a row prefix altered", row_field("prefix", "silver/not_this_prefix/")),
        ("a row table altered", row_field("table", "not_the_table")),
        ("a vendor outside the vocabulary", row_field("vendor", "zzz_vendor")),
        ("a three-word reason", lambda d: d["items"][0].update(reason="too short here")),
        ("a non-ASCII reason", lambda d: d["items"][0].update(reason="a live advisor table with caf" + chr(233) + " style text long enough to count")),
        ("evidence naming a missing file", lambda d: d["items"][0].update(evidence=["workflows/gateway_battery/no_such_file_z1.py:1"])),
        ("evidence past the end of the file", lambda d: d["items"][0].update(evidence=["workflows/gateway_battery/routing_table.py:999999"])),
        ("evidence naming a census entry that does not exist", lambda d: d["items"][0].update(evidence=["census.json#opal-data-inf/silver/no_such_table/"])),
        ("no evidence", lambda d: d["items"][0].update(evidence=[])),
    ])
    if err:
        arm("deliverable present and readable", False, err)
        return
    probs = fn(doc)
    arm("every row item is grounded (new unique entity, the item's bucket, prefix and table, a vocabulary vendor) and every item has a long ASCII reason and evidence that resolves",
        not probs, "; ".join(probs)[:600])


CHECKS = {"z1.AC1": ac1, "z1.AC2": ac2}

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else ""
    if cid not in CHECKS:
        print("usage: z1_check.py <%s> [uncatalogued_rows.json]" % "|".join(sorted(CHECKS)))
        sys.exit(9)
    CHECKS[cid](sys.argv[2] if len(sys.argv) > 2 else DEFAULT)
    print("ARMS: %d ok, %d failed" % (len(OK), len(BAD)))
    print("RESULT: %s" % ("PASS" if OK and not BAD else "FAIL"))
    sys.exit(0 if OK and not BAD else 1)
