"""AMGT_RESAPP round 77 -- cell AMGT-ba-7 (CTO ADDENDUM 1 @3bad4be9e0; row Z-W20-S8): each name's passage set lists
the filing sections it covers and the sections it does not.

The cell builds `lib/research/filings/section_coverage.py`:
  wanted_items(form)                                   -> [(key, item label), ...] the sections a filing of that form is read for
  coverage_from_source(source, passage_map=None)       -> the coverage block, from one stored source object (pure)
  read_section_coverage(security_key, pool_client, bucket) -> the same block for a name's newest stored source object
The block: {"sections": [{"key","item","chars","full_chars","share","truncated","passages"}],
            "not_covered": [{"key","item","reason"}], "passages_outside_sections", "source": {"form","filing_date",
            "accession"}, "reason"}. `reason` is None when a source is read, and a plain sentence when none is.

  AC1  the block equals the stored facts on every resolved source object (fixture), with the specimens named
  AC2  the seam: `read_section_coverage` over the REAL stored objects of every covered name (read-only)
  AC3  the wanted sections equal the producer's own table; reasons are plain; stdlib-only at module scope

  python r77_ba7.py --crit AC1|AC2|AC3 [--where local]
Prints PASS / FAIL clause lines and `R77 BA7 <crit> SERVED: YES|NO`; exit 0 on YES.
"""
import argparse
import ast
import collections
import concurrent.futures
import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "r77_ba7_fixture.json")
MODULE = "lib.research.filings.section_coverage"
BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate",
          "stage", "input ledger")
STDLIB_OK = {"__future__", "json", "re", "typing", "collections", "itertools", "functools", "dataclasses", "enum",
             "string", "time"}

_OK = [True]


def clause(name, passed, detail=""):
    print(("PASS " if passed else "FAIL ") + name + ((" " + str(detail)) if detail != "" else ""))
    if not passed:
        _OK[0] = False


def verdict(crit):
    print("R77 BA7 %s SERVED: %s" % (crit, "YES" if _OK[0] else "NO"))
    return 0 if _OK[0] else 1


def plain(reason):
    low = str(reason).lower()
    return (isinstance(reason, str) and 20 <= len(reason) <= 240 and reason[0].isupper() and reason.rstrip().endswith(".")
            and all(ord(ch) < 128 for ch in reason) and not any(word in low for word in BANNED) and "_" not in reason)


def expected(entry, wanted):
    """The block's facts, read off ONE stored source object and its passage map; nothing typed."""
    source = entry["source"]
    excerpt = source.get("excerpt") or {}
    keys = list(excerpt.get("item_keys") or [])
    items = list(excerpt.get("items") or [])
    passages = entry.get("passage_map")
    by_item = collections.Counter(str(p.get("location") or "").split(" / ")[0].upper() for p in passages or [])
    sections = []
    for key, item in zip(keys, items):
        sections.append({"key": key, "item": item, "chars": excerpt["item_chars"][key],
                         "full_chars": excerpt["item_full_chars"][key], "truncated": key in (excerpt.get("truncated_items") or []),
                         "passages": by_item.get(item.upper(), 0) if passages is not None else None})
    missing = [(key, label) for key, label in wanted if key not in keys]
    outside = (len(passages) - sum(s["passages"] for s in sections)) if passages is not None else None
    return sections, missing, outside


def compare(block, entry, wanted):
    """The differences between a block and the stored facts, as short strings."""
    out = []
    sections, missing, outside = expected(entry, wanted)
    got = block.get("sections") or []
    if [s.get("key") for s in got] != [s["key"] for s in sections]:
        out.append("section keys %s != %s" % ([s.get("key") for s in got], [s["key"] for s in sections]))
        return out
    for have, want in zip(got, sections):
        for field in ("item", "chars", "full_chars", "truncated", "passages"):
            if have.get(field) != want[field]:
                out.append("%s.%s %r != %r" % (want["key"], field, have.get(field), want[field]))
        share = have.get("share")
        ratio = (want["chars"] / want["full_chars"]) if want["full_chars"] else None
        if ratio is not None and not (isinstance(share, (int, float)) and abs(share - ratio) < 0.005):
            out.append("%s.share %r != %.3f" % (want["key"], share, ratio))
    not_covered = block.get("not_covered") or []
    if [(n.get("key"), n.get("item")) for n in not_covered] != missing:
        out.append("not_covered %s != %s" % ([(n.get("key"), n.get("item")) for n in not_covered], missing))
    for entry_nc in not_covered:
        if not plain(entry_nc.get("reason")):
            out.append("not_covered.%s reason not plain: %r" % (entry_nc.get("key"), entry_nc.get("reason")))
    if block.get("passages_outside_sections") != outside:
        out.append("passages_outside_sections %r != %r" % (block.get("passages_outside_sections"), outside))
    src = block.get("source") or {}
    for field in ("form", "filing_date", "accession"):
        if src.get(field) != entry["source"].get(field):
            out.append("source.%s %r != %r" % (field, src.get(field), entry["source"].get(field)))
    if block.get("reason") is not None:
        out.append("reason should be None on a read source: %r" % block.get("reason"))
    return out


def crit_ac1(mod):
    with open(FIXTURE, encoding="utf-8") as handle:
        fx = json.load(handle)
    resolved = fx["resolved"]
    print("   fixture captured %s: covered names %d; stored source objects resolved %d, not resolved %d, none %d" % (
        fx["captured_at"], fx["covered_names"], fx["counts"]["resolved"], fx["counts"]["not_resolved"], fx["counts"]["no_source_object"]))
    bad = {}
    blocks = {}
    for key, entry in sorted(resolved.items()):
        block = mod.coverage_from_source(entry["source"], entry["passage_map"])
        blocks[key] = block
        diffs = compare(block, entry, mod.wanted_items(entry["source"].get("form")))
        if diffs:
            bad[key] = diffs[:3]
    clause("C1 the block equals the stored facts on every resolved source object", not bad and len(resolved) > 0,
           "%d of %d equal; e.g. %s" % (len(resolved) - len(bad), len(resolved), json.dumps(bad)[:300] if bad else "[]"))
    baba = blocks.get("BABA_US_Equity") or {}
    shares = {s.get("key"): s for s in baba.get("sections") or []}
    clause("C2 the specimen (BABA): both sections are listed as cut short, with how much of each is kept",
           set(shares) == {"risk", "mdna"} and all(s.get("truncated") is True for s in shares.values())
           and abs((shares.get("risk") or {}).get("share", 9) - 70000 / 350005) < 0.005
           and abs((shares.get("mdna") or {}).get("share", 9) - 80000 / 131933) < 0.005,
           {k: (v.get("chars"), v.get("full_chars"), v.get("share")) for k, v in shares.items()})
    for key in ("ASML_NA_Equity", "PBR_US_Equity"):
        nc = (blocks.get(key) or {}).get("not_covered") or []
        clause("C3 %s lists the operating review as NOT covered, by its item name" % key,
               [n.get("key") for n in nc] == ["mdna"] and "Item 5" in str(nc[0].get("item")), [(n.get("key"), n.get("item")) for n in nc])
    hal = (blocks.get("HAL_US_Equity") or {}).get("not_covered") or []
    clause("C4 HAL lists the risk factors as NOT covered", [n.get("key") for n in hal] == ["risk"], [(n.get("key"), n.get("item")) for n in hal])
    asml = blocks.get("ASML_NA_Equity") or {}
    clause("C5 a passage outside every named section is counted, not dropped (ASML NA: 1)", asml.get("passages_outside_sections") == 1,
           asml.get("passages_outside_sections"))
    no_map = mod.coverage_from_source(resolved["BA_US_Equity"]["source"], None)
    clause("C6 with no passage map the sections are still listed and the passage counts read None",
           [s.get("key") for s in no_map.get("sections") or []] == ["risk", "mdna"]
           and all(s.get("passages") is None for s in no_map.get("sections") or []) and no_map.get("passages_outside_sections") is None, "")
    for key, entry in sorted(fx["not_resolved_specimen"].items()):
        block = mod.coverage_from_source(entry["source"], None)
        clause("C7 a name with no filing read (%s) serves no sections and a plain reason" % key,
               not block.get("sections") and not block.get("not_covered") and plain(block.get("reason")), repr(block.get("reason")))
    for odd in (None, {}, {"status": "RESOLVED"}):
        block = mod.coverage_from_source(odd, None)
        clause("C8 a missing or empty source object (%r) serves a plain reason and never raises" % (odd,),
               isinstance(block, dict) and not block.get("sections") and plain(block.get("reason")), repr(block.get("reason")))


def crit_ac2(mod):
    import boto3

    from lib.research.coverage import pool_reader
    from lib.research.coverage.covered_universe import covered_security_keys

    with open(FIXTURE, encoding="utf-8") as handle:
        fx = json.load(handle)
    keys = sorted(covered_security_keys())
    client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))

    def one(key):
        try:
            return key, mod.read_section_coverage(key, lambda: client, pool_reader.POOL_BUCKET), None
        except Exception as err:  # noqa: BLE001 -- the reader must never raise
            return key, None, "%s: %s" % (type(err).__name__, err)

    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        got = list(pool.map(one, keys))
    raised = [(k, e) for k, _b, e in got if e]
    clause("C1 the reader raised on no covered name", not raised and len(keys) > 0, "%d names; raised %s" % (len(keys), raised[:2]))
    with_sections = sorted(k for k, b, _e in got if b and b.get("sections"))
    with_reason = [k for k, b, _e in got if b and not b.get("sections")]
    not_plain = [k for k, b, _e in got if b and not b.get("sections") and not plain(b.get("reason"))]
    print("   covered names %d: a filing read on %d, a plain reason on %d" % (len(keys), len(with_sections), len(with_reason)))
    clause("C2 every covered name serves either its sections or a plain reason", len(with_sections) + len(with_reason) == len(keys) and not not_plain,
           "not plain: %s" % not_plain[:3])
    partial = sorted(k for k, b, _e in got if b and b.get("not_covered"))
    short = sorted(k for k, b, _e in got if b and any(s.get("truncated") for s in b.get("sections") or []))
    print("   a section NOT covered on %d %s; a section cut short on %d %s" % (len(partial), partial, len(short), short))
    clause("C3 the names with a filing read are at least the fixture's (the store only grows)", set(fx["resolved"]) <= set(with_sections),
           "missing %s" % sorted(set(fx["resolved"]) - set(with_sections)))
    blocks = {k: b for k, b, _e in got if b}
    same = []
    for key, entry in sorted(fx["resolved"].items()):
        block = blocks.get(key) or {}
        if (block.get("source") or {}).get("accession") != entry["source"].get("accession"):
            continue  # a newer filing has been stored since the fixture; the pure arm is AC1
        diffs = compare(block, entry, mod.wanted_items(entry["source"].get("form")))
        same.append((key, diffs))
    differing = {k: d[:2] for k, d in same if d}
    clause("C4 on every name whose stored filing is the fixture's, the read block equals the stored facts", same and not differing,
           "%d of %d equal; e.g. %s" % (len(same) - len(differing), len(same), json.dumps(differing)[:240] if differing else "[]"))
    planted = one("R77_PLANT_NO_SUCH_Equity")
    clause("C5 control: a name the store does not hold serves a plain reason, not an error",
           planted[2] is None and not (planted[1] or {}).get("sections") and plain((planted[1] or {}).get("reason")), repr((planted[1] or {}).get("reason")))


def crit_ac3(mod):
    from lib.research.filings import document, fetch

    produced = {form: [(key, document._10K_20F_PATTERNS[form][key][0]) for key in fetch.EXCERPT_ITEMS[form]]
                for form in sorted(fetch.EXCERPT_ITEMS)}
    for form, want in produced.items():
        have = [tuple(pair) for pair in mod.wanted_items(form)]
        clause("C1 the wanted sections of a %s equal the producer's own table" % form, have == want, "%s vs %s" % (have, want))
    clause("C2 a form the producer does not cut has no wanted sections, and says so without raising",
           list(mod.wanted_items("R77-NO-SUCH-FORM")) == [] and list(mod.wanted_items(None)) == [], "")
    path = getattr(mod, "__file__", "") or ""
    with open(path, encoding="utf-8") as handle:
        source = handle.read()
    tree = ast.parse(source)
    top = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            top.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            top.add((node.module or "").split(".")[0])
    clause("C3 the module imports only the standard library at module scope (the Lambda imports it; its package holds no filing fetch stack)",
           top <= STDLIB_OK, sorted(top - STDLIB_OK))
    nested = sorted({n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
                    {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
    clause("C4 no import anywhere in the module reaches the fetch or document layer, a vendor or the network",
           not any(re.search(r"(filings\.fetch|filings\.document|battery|analyze|requests|urllib|anthropic|fitz)", name) for name in nested), nested)
    clause("C5 the module is ASCII", all(ord(ch) < 128 for ch in source), "")
    with open(FIXTURE, encoding="utf-8") as handle:
        fx = json.load(handle)
    reasons = []
    for entry in fx["resolved"].values():
        reasons += [n.get("reason") for n in mod.coverage_from_source(entry["source"], entry["passage_map"]).get("not_covered") or []]
    for entry in fx["not_resolved_specimen"].values():
        reasons.append(mod.coverage_from_source(entry["source"], None).get("reason"))
    reasons.append(mod.coverage_from_source(None, None).get("reason"))
    clause("C6 every reason the module gives is plain words", reasons and all(plain(r) for r in reasons), [r for r in reasons if not plain(r)][:2])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    try:
        mod = importlib.import_module(MODULE)
    except Exception as err:  # noqa: BLE001 -- an absent or broken module is the FAIL this check reports
        clause("the module %s imports" % MODULE, False, "%s: %s" % (type(err).__name__, err))
        return verdict(a.crit)
    missing = [n for n in ("wanted_items", "coverage_from_source", "read_section_coverage") if not callable(getattr(mod, n, None))]
    if missing:
        clause("the module exports wanted_items, coverage_from_source and read_section_coverage", False, missing)
        return verdict(a.crit)
    try:
        {"AC1": crit_ac1, "AC2": crit_ac2, "AC3": crit_ac3}[a.crit](mod)
    except Exception as err:  # noqa: BLE001 -- an instrument error is a FAIL with its cause, never a traceback
        clause("the check ran to the end", False, "%s: %s" % (type(err).__name__, err))
    return verdict(a.crit)


if __name__ == "__main__":
    sys.exit(main())
