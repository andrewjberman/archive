# The FINAL rank_universe_20261008.json and rank_universe_identity_20261008.json are built by 0.9.0_WK_AMGT_HARVST~121/bn1_names_made_whole.py in ONE run; this script is kept as the record of how they were first made, and re-running it reverts the final files.
"""HVST-bm-2: the stored company names cut at 30 characters, printed, and the cut ones repaired in the NEW identity file.

LOCAL only: reads the round-47 identity file, the bm-1 identity file and snapshot, `lib/research/identity/registrations.json`,
and calls the gold side's own functions (`lib.research.harvest.universe_securities`: `suffix_fragment`,
`cut_legal_name_fragment`, `clean_legal_name`, `suffix_forms`, `LEGAL_NAME_EXACT_LENGTH`) and the collector's own
`publishers.slug_query` / `slug_queries`. No network, no job, no config change. The ONLY file written is
`rank_universe_identity_20261008.json` (beside this script); the round-47 files and `config.json` are read, never written.

The BEFORE set is idempotent: a record is taken from the round-47 identity file when its key is there, else from the new
file (the 8 records bm-1 added, none of which this cell touches), so a re-run reads the same values.

Repair rule, in order, for a record whose stored company is CUT (ends in a suffix fragment, by the gold side's function):
  A. a STORED source carries a fuller name for that exact key (the pool record's name with its ticker tail removed, or
     `registrations.json` `identity.name`) that is LONGER than the stored value and begins with it (case/punctuation
     folded): the record takes it, status DERIVED;
  B. else the fragment is dropped (`cut_legal_name_fragment`), status DERIVED;
  C. else the value stays and is listed `CUT, NOT REPAIRED`.
A 30-character value with NO fragment is classed by FORM: WHOLE when it ends in a whole listed corporate suffix
(`suffix_forms` non-empty), else CUT WITH NO SUFFIX FRAGMENT. Neither is repaired unless rule A finds a stored name.
Aliases are rebuilt by `build_rank_identity.py`'s rule for a non-pilot record: the company alone. sa_symbol, ticker,
key and pool_name are never touched.
"""

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
sys.path.insert(0, ROOT)

from lib.opal_data_harvest import publishers  # noqa: E402
from lib.research.harvest import universe_securities as gold  # noqa: E402

DELIV = os.path.join(ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables")
R47_IDENTITY = os.path.join(DELIV, "2.0.0_SA_COO_H", "round47", "rank_universe_identity_20261005.json")
NEW_IDENTITY = os.path.join(HERE, "rank_universe_identity_20261008.json")
NEW_SNAPSHOT = os.path.join(HERE, "rank_universe_20261008.json")
REGISTRATIONS = os.path.join(ROOT, "lib", "research", "identity", "registrations.json")
BUILDER = os.path.join(DELIV, "0.9.0_WK_AMGT_HARVST~94", "build_rank_identity.py")
PILOT_EVIDENCE = "config.json pilot_securities"


def _load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _builder():
    spec = importlib.util.spec_from_file_location("build_rank_identity", BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fold(text):
    return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()


def before_records():
    """(ordered list of BEFORE records, round-47 key set): round-47's record where the key is there, else the new file's."""
    r47 = {r["security_key"]: r for r in _load(R47_IDENTITY)["records"]}
    new = _load(NEW_IDENTITY)["records"]
    return [r47.get(r["security_key"], r) for r in new], set(r47)


def stored_names(record, entry, registrations, clean_company):
    """[(source, name)] the stored sources give for this exact key."""
    out = []
    if entry:
        cleaned = clean_company(entry["name"], entry["ticker"])
        out.append(("pool record name (rank_universe_20261008.json entries[].name, trailing ticker removed)", cleaned))
    reg = registrations.get(record["security_key"])
    if reg and (reg.get("identity") or {}).get("name"):
        out.append(("lib/research/identity/registrations.json identity.name", reg["identity"]["name"]))
    return out


def completion(value, candidates):
    """The first candidate that is a COMPLETION of `value`: longer and begins with it (folded). (source, name) or None."""
    for source, name in candidates:
        if len(_fold(name)) > len(_fold(value)) and _fold(name).startswith(_fold(value)):
            return source, name
    return None


def classify(value):
    """('CUT', fragment) | ('CUT_NO_FRAGMENT', reason) | ('WHOLE', reason)."""
    fragment = gold.suffix_fragment(value)
    if fragment is not None:
        return "CUT", fragment
    if gold.suffix_forms(value):
        return "WHOLE", "ends in a whole listed corporate suffix (suffix_forms %r)" % (gold.suffix_forms(value),)
    return "CUT_NO_FRAGMENT", ("%d characters, ends in no whole corporate suffix and no suffix fragment; last word %r"
                               % (len(value), value.split()[-1]))


def rebuilt(record, new_company, how, source):
    rec = json.loads(json.dumps(record))
    rec["company"] = {"value": new_company, "status": "DERIVED",
                      "evidence": ("HVST-bm-2: %s; stored value %r (%d characters, the identity record's cut length) was %s"
                                   % (how, record["company"]["value"], len(record["company"]["value"]), source))}
    rec["aliases"] = {"value": [new_company], "status": "DERIVED",
                      "evidence": "the repaired company name alone (build_rank_identity.py rule for a non-pilot record)"}
    return rec


def analyse():
    """Pure: everything the printout and the plants need. Writes nothing."""
    builder = _builder()
    before, r47_keys = before_records()
    entries = {e["security_key"]: e for e in _load(NEW_SNAPSHOT)["entries"]}
    registrations = {r["security_key"]: r for r in _load(REGISTRATIONS)["registrations"]}
    after = []
    rows, repaired, not_repaired = [], [], []
    for record in before:
        value = record["company"]["value"]
        new = record
        if len(value) == gold.LEGAL_NAME_EXACT_LENGTH:
            kind, detail = classify(value)
            candidates = stored_names(record, entries.get(record["security_key"]), registrations, builder.clean_company)
            found = completion(value, candidates)
            row = {"security_key": record["security_key"], "value": value, "kind": kind, "detail": detail,
                   "candidates": candidates, "completion": found, "action": "unchanged"}
            is_pilot = (record["aliases"].get("evidence") or "").startswith(PILOT_EVIDENCE)
            if kind in ("CUT", "CUT_NO_FRAGMENT") and not is_pilot:
                if found:
                    new = rebuilt(record, found[1], "a stored source gives the full name for this exact key", "completed from " + found[0])
                    row["action"] = "REPAIRED (stored full name)"
                elif kind == "CUT":
                    name, fragment = gold.cut_legal_name_fragment(value, value)
                    new = rebuilt(record, name, "suffix fragment %r dropped by universe_securities.cut_legal_name_fragment" % fragment,
                                  "cut inside a corporate suffix, no stored source carries a fuller name")
                    row["action"] = "REPAIRED (fragment %r dropped)" % fragment
                else:
                    not_repaired.append(row)
                    row["action"] = "CUT, NOT REPAIRED"
            elif kind in ("CUT", "CUT_NO_FRAGMENT"):
                not_repaired.append(row)
                row["action"] = "CUT, NOT REPAIRED (pilot record, config.json owns it)"
            rows.append(row)
            if new is not record:
                repaired.append({"security_key": record["security_key"], "before": record, "after": new, "row": row})
        after.append(new)
    repaired_keys = {r["security_key"] for r in repaired}
    changed = [a["security_key"] for a, b in zip(after, before) if a != b]
    other = [k for k in changed if k not in repaired_keys]
    return {"before": before, "after": after, "rows": rows, "repaired": repaired, "not_repaired": not_repaired,
            "other_changed": other, "r47_keys": r47_keys}


def _refuse_live_collector_pointer(path):
    """Row AMGT_HARVST-Z-W120-S3, disarmed by row AMGT_HARVST-Z-S105 (2.0.0_SA_COO~H): a file that
    lib/opal_data_harvest/config.json names is the LIVE collector list, and re-running this record script would silently
    revert the repairs made to it after this script ran. Writing it is refused."""
    root = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(root, "lib", "opal_data_harvest", "config.json")):
        parent = os.path.dirname(root)
        if parent == root:
            return
        root = parent
    with open(os.path.join(root, "lib", "opal_data_harvest", "config.json"), encoding="utf-8") as handle:
        config = json.load(handle)
    target = os.path.normcase(os.path.abspath(path))
    for value in config.values():
        if isinstance(value, str) and target == os.path.normcase(os.path.abspath(os.path.join(root, value))):
            raise SystemExit("REFUSED: %s is a live collector pointer in config.json (row AMGT_HARVST-Z-W120-S3)" % path)


def write_identity(result):
    _refuse_live_collector_pointer(NEW_IDENTITY)
    doc = _load(NEW_IDENTITY)
    if [r["security_key"] for r in doc["records"]] != [r["security_key"] for r in result["after"]]:
        raise SystemExit("ERROR: record order or keys differ from the file being rewritten")
    doc["records"] = result["after"]
    doc["bm2_repair"] = {"cell": "HVST-bm-2", "author": "0.9.0_WK_AMGT_HARVST~120",
                         "repaired": sorted(r["security_key"] for r in result["repaired"]),
                         "rule": "bm2_truncated_names.py rule A (stored full name), then B (suffix fragment dropped), else unchanged"}
    with open(NEW_IDENTITY, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(doc, indent=2, ensure_ascii=True) + "\n")


def _verdict(row, source, name):
    if (source, name) == row["completion"]:
        return "[COMPLETES THE VALUE]"
    if name == row["value"]:
        return "[same as the stored value, not a fuller name]"
    return "[not a completion: %s than the stored value]" % ("shorter" if len(name) < len(row["value"]) else "different")


def main():
    result = analyse()
    rows = result["rows"]
    print("DENOMINATOR: identity records %d, company values of exactly %d characters %d"
          % (len(result["before"]), gold.LEGAL_NAME_EXACT_LENGTH, len(rows)))
    for row in rows:
        if row["kind"] == "CUT":
            cut = "CUT (suffix_fragment -> %r)" % row["detail"]
            second = "n/a (a suffix fragment was found)"
        else:
            cut = "not cut by suffix_fragment (None)"
            second = ("CUT WITH NO SUFFIX FRAGMENT: " if row["kind"] == "CUT_NO_FRAGMENT" else "WHOLE: ") + row["detail"]
        stored = "; ".join("%s = %r %s" % (s, n, _verdict(row, s, n)) for s, n in row["candidates"]) or "none"
        print("%s | stored %r | %s | %s | stored sources: %s | action: %s"
              % (row["security_key"], row["value"], cut, second, stored, row["action"]))
    print("REPAIRED: %d" % len(result["repaired"]))
    for item in result["repaired"]:
        b, a, key = item["before"], item["after"], item["security_key"]
        print("  %s" % key)
        print("    company  before %r (%s) -> after %r (%s)" % (b["company"]["value"], b["company"]["status"],
                                                               a["company"]["value"], a["company"]["status"]))
        print("    company evidence: %s" % a["company"]["evidence"])
        print("    aliases  before %r -> after %r" % (b["aliases"]["value"], a["aliases"]["value"]))
        print("    slug_query  before %r -> after %r" % (publishers.slug_query(b["company"]["value"]),
                                                       publishers.slug_query(a["company"]["value"])))
        print("    slug_queries  before %r -> after %r"
              % (publishers.slug_queries({"company": b["company"]["value"], "aliases": b["aliases"]["value"]}),
                 publishers.slug_queries({"company": a["company"]["value"], "aliases": a["aliases"]["value"]})))
    print("CUT, NOT REPAIRED: %d" % len(result["not_repaired"]))
    for row in result["not_repaired"]:
        print("  %s | %r | %s" % (row["security_key"], row["value"], row["detail"]))
    print("OTHER RECORDS CHANGED: %d%s" % (len(result["other_changed"]), " " + repr(result["other_changed"]) if result["other_changed"] else ""))
    repaired_keys = [r["security_key"] for r in result["repaired"]]
    if len(rows) > 0 and "AIG_US_Equity" in repaired_keys and not result["other_changed"]:
        write_identity(result)
        print("REPAIR OK")
    else:
        why = ("k=0" if not rows else "AIG_US_Equity not repaired" if "AIG_US_Equity" not in repaired_keys
               else "other records changed %r" % result["other_changed"])
        print("REPAIR FAIL: " + why)
        sys.exit(1)


if __name__ == "__main__":
    main()
