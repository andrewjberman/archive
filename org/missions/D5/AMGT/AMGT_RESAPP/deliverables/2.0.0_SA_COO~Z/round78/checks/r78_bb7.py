"""AMGT_RESAPP round 78 -- AMGT-bb-7: the stored name list carries each record's legal name, and name search reads it.

CTO round-78 ruling, "bb-7, name search": "Not the copied file. The pool carries each record's legal name at its next
mint, under a re-mint pair like today's, and name search reads the pool." (This file replaces the check of the refused
draft, which copied another project's file.)

  --crit AC1|AC2|AC3 --where local
  --crit READ --where local          (the measure alone; always exit 0)

NOTHING IS WRITTEN TO THE STORE. Every criterion builds the document IN MEMORY, exactly as the mint would
(`crosswalk.build_crosswalk` over the registrations file, the newest retained universe object, the research folders and
the served object as `served`), and compares it with the served object `crosswalk/v1/<newest>.json`. The stores are
read; no object is put.

THE ORACLE (this file's own, independent of the builder). A record's legal name is, in this order:
  1. the name its own registration stored: `identity.name` on the record (Bloomberg NAME);
  2. the name a retained universe object `universe/v1/<date>.json` carries for its key on an entry whose `source` is
     "holding" (the holdings line's own company name); the newest object that carries one wins;
  3. none: the record has no legal name stored anywhere (its research folder name is not a legal name).

AC1 (build; FAILS at the base): the in-memory build carries the legal name.
    C1 every record carries `legal_name`, an object with exactly `value`, `status`, `evidence`;
    C2 the value on every record equals the oracle's; a named record reads status MEASURED with an evidence sentence
       naming its source (`identity.name` or the `universe/v1/` object); an unnamed one reads value null, status ABSENT;
       200 or more records are named (the base oracle reads 211 of 243), the unnamed are printed;
    C3 `denominators.with_legal_name` equals the named count and the document passes the write-time schema check;
    C4 lib/research/identity/tests/test_crosswalk_legal_name.py exists and passes.
AC2 (build; FAILS at the base): name search, pointed at that in-memory document, reads the legal name.
    C1 "apple" lists AAPL_US_Equity as "Apple Inc", "microsoft" lists MSFT_US_Equity as "Microsoft Corp", "airbnb"
       lists ABNB_US_Equity; each answer is `candidates`, never `exact`;
    C2 every stored name of every record (its research folder name, its registered name, its oracle legal name), typed
       whole, lists that record (the count is printed against the record count);
    C3 lib/research/api/tests/test_name_search.py holds test_a_legal_name_lists_its_company and the file passes.
AC3 (BOUND; PASSES at the base and after): nothing that exists today moves.
    C1 the in-memory build holds exactly the served object's keys, and on every record every field other than
       `legal_name` equals the served record's;
    C2 every top-level field equals the served object's, other than the fields in MOVING (the read clock, the counts of
       the live research directory, and the one added count);
    C3 a build that is NOT handed legal names carries `legal_name` on 0 records and no `with_legal_name` count (the
       default document is the one built today);
    C4 on the in-memory document every stored key still passes through name search as `exact`, and "lenovo" still
       lists 992_HK_Equity under its folder name;
    C5 the existing test files of the two packages still pass.
Verdict: R78 BB7 <CRIT> SERVED: YES|NO (exit 0|1). READ prints R78 BB7 READ: DONE.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
import tempfile

BUCKET = "opal-data-harvest"
UNIVERSE_RE = re.compile(r"^universe/v1/\d{4}-\d{2}-\d{2}\.json$")
NEW_FIELD = "legal_name"
NEW_COUNT = "with_legal_name"
BUILDER_LOADER = "universe_names"
NAMED_FLOOR = 200
ID_TESTS = "lib/research/identity/tests"
ID_NEW_TEST = "lib/research/identity/tests/test_crosswalk_legal_name.py"
NS_TEST = "lib/research/api/tests/test_name_search.py"
NS_TEST_NAME = "test_a_legal_name_lists_its_company"
# Top-level paths allowed to differ from the served object (AC3 C2). The first is the build's read clock; the next
# three are functions of the live research directory at the moment of the build; the last is the one added count.
MOVING = (
    ("research_universe", "read_at"),
    ("research_universe", "folders"),
    ("denominators", "research_folders_live"),
    ("coverage_vintage", "snapshot_stale_against_live"),
    ("denominators", NEW_COUNT),
)
QUERIES = (("apple", "AAPL_US_Equity", "Apple Inc"), ("microsoft", "MSFT_US_Equity", "Microsoft Corp"),
           ("airbnb", "ABNB_US_Equity", None))


def _client():
    import boto3

    return boto3.client("s3", region_name="us-east-1")


def holding_names(client):
    """({key: (name, object key)}, [object keys]) -- the oracle's rule 2, read from every retained universe object."""
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="universe/v1/"):
        keys.extend(o["Key"] for o in page.get("Contents", []) if UNIVERSE_RE.match(o["Key"]))
    out = {}
    for key in sorted(keys):
        document = json.loads(client.get_object(Bucket=BUCKET, Key=key)["Body"].read())
        for entry in document.get("names") or []:
            name = entry.get("name")
            if entry.get("source") == "holding" and entry.get("security_key") and isinstance(name, str) and name.strip():
                out[entry["security_key"]] = (name.strip(), key)
    return out, sorted(keys)


def registered_name(record):
    identity = record.get("identity")
    name = identity.get("name") if isinstance(identity, dict) else None
    return name.strip() if isinstance(name, str) and name.strip() else None


def oracle(records, holdings):
    """{record index: (value or None, rule)} over `records`."""
    out = {}
    for i, record in enumerate(records):
        own = registered_name(record)
        held = holdings.get(record.get("security_key"))
        if own:
            out[i] = (own, "identity.name")
        elif held:
            out[i] = (held[0], held[1])
        else:
            out[i] = (None, "none")
    return out


def build(with_names=True):
    """(served document, served key, in-memory build, whether the builder was handed legal names)."""
    from lib.research.identity import crosswalk

    served, served_key = crosswalk._read_pool_latest()
    universe, universe_source = crosswalk.load_identity_universe()
    folders, root = crosswalk._research_folders_for_disclosure()
    kwargs = dict(identity_universe=universe, identity_source=universe_source, research_folders=folders,
                  research_root=root, served=copy.deepcopy(served))
    handed = False
    loader = getattr(crosswalk, BUILDER_LOADER, None)
    if with_names and callable(loader):
        kwargs["legal_names"] = loader(universe, universe_source)
        handed = True
    document = crosswalk.build_crosswalk(served["as_of"], **kwargs)
    return served, served_key, document, handed


def search_on(document):
    """name_search.resolve_query bound to `document` (a temporary local copy; the pool is not read)."""
    from lib.research.api import name_search
    from lib.research.identity import crosswalk

    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(document, handle)
    handle.close()
    os.environ[crosswalk.ENV_CROSSWALK] = handle.name
    crosswalk._CACHE.clear()
    crosswalk._RESOLVED_FROM.clear()
    return name_search.resolve_query, handle.name


def lists(fn, typed, key):
    """True when the search, given `typed`, answers with `key` (as a candidate, or as the exact record)."""
    answer = fn(typed)
    return answer.get("security_key") == key or any(
        c.get("security_key") == key for c in (answer.get("candidates") or []))


def pytest_run(paths):
    env = {k: v for k, v in os.environ.items() if k != "AMGT_CROSSWALK_PATH"}
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider"] + list(paths),
                       capture_output=True, timeout=1500, env=env)
    tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1].strip()
    return p.returncode == 0 and " passed" in tail and "failed" not in tail and "error" not in tail, tail


def strip_moving(document):
    out = copy.deepcopy(document)
    for outer, inner in MOVING:
        if isinstance(out.get(outer), dict):
            out[outer].pop(inner, None)
    out.pop("records", None)
    return out


def measure():
    served, served_key, document, handed = build()
    records = document["records"]
    holdings, universe_keys = holding_names(_client())
    want = oracle(records, holdings)
    keys = [r.get("security_key") for r in records]
    in_pool = {k for k in keys if k}
    print("   served object %s; records %d; in-memory build records %d; builder handed legal names: %s" % (
        served_key, len(served["records"]), len(records), "yes" if handed else "no (the builder offers none)"))
    folder = sum(1 for r in records if (r.get("source_row") or {}).get("folder"))
    own = sum(1 for r in records if registered_name(r))
    either = sum(1 for r in records if (r.get("source_row") or {}).get("folder") or registered_name(r))
    print("   records with a research folder name %d; with a registered name %d; with either %d of %d" % (
        folder, own, either, len(records)))
    print("   retained universe objects %d %s; keys they name on a holding entry %d, of which in this build %d" % (
        len(universe_keys), universe_keys, len(holdings), len(set(holdings) & in_pool)))
    by_rule = {}
    for value, rule in want.values():
        by_rule[rule] = by_rule.get(rule, 0) + 1
    named = sum(1 for value, _rule in want.values() if value)
    print("   oracle legal names %d of %d, by source %s" % (named, len(records), json.dumps(by_rule, sort_keys=True)))
    unnamed = [keys[i] for i, (value, _rule) in sorted(want.items()) if not value]
    print("   no legal name stored anywhere: %d %s" % (len(unnamed), unnamed))
    carrying = sum(1 for r in records if isinstance(r.get(NEW_FIELD), dict) and r[NEW_FIELD].get("value"))
    print("   in-memory build: records with a non-empty %s.value %d of %d" % (NEW_FIELD, carrying, len(records)))
    return served, document, handed, want


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3", "READ"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    served, document, handed, want = measure()
    records = document["records"]
    keys = [r.get("security_key") for r in records]
    named = [i for i, (value, _rule) in sorted(want.items()) if value]

    if a.crit == "READ":
        fn, _path = search_on(document)
        for q, _key, _name in QUERIES:
            r = fn(q)
            print("   %r: status %s candidates %s reason %r" % (
                q, r.get("status"), [(c.get("security_key"), c.get("name")) for c in (r.get("candidates") or [])][:5],
                r.get("reason")))
        print("R78 BB7 READ: DONE")
        return 0

    if a.crit == "AC1":
        from lib.research.identity import crosswalk

        shaped = [i for i, r in enumerate(records)
                  if isinstance(r.get(NEW_FIELD), dict) and sorted(r[NEW_FIELD]) == ["evidence", "status", "value"]]
        clause("C1 every record carries %s with value, status, evidence" % NEW_FIELD, len(shaped) == len(records),
               "%d of %d" % (len(shaped), len(records)))
        wrong = []
        for i, record in enumerate(records):
            cell = record.get(NEW_FIELD) if isinstance(record.get(NEW_FIELD), dict) else {}
            value, rule = want[i]
            evidence = str(cell.get("evidence") or "")
            if value:
                good = (cell.get("value") == value and cell.get("status") == "MEASURED"
                        and (rule if rule == "identity.name" else "universe/v1/") in evidence)
            else:
                good = cell.get("value", "") is None and cell.get("status") == "ABSENT" and bool(evidence.strip())
            if not good:
                wrong.append(keys[i])
        clause("C2 every record's legal name equals the oracle's, with its source stated; %d or more are named"
               % NAMED_FLOOR, not wrong and len(named) >= NAMED_FLOOR,
               "%d of %d agree; named %d; first disagreeing %s" % (len(records) - len(wrong), len(records), len(named),
                                                                    wrong[:8]))
        count = (document.get("denominators") or {}).get(NEW_COUNT)
        try:
            crosswalk._validate_document_against_schema(document)
            schema_note = "passes"
        except ValueError as err:
            schema_note = str(err)[:200]
        clause("C3 the named count is stated and the document passes the write-time schema check",
               count == len(named) and schema_note == "passes" and handed,
               "%s %r against %d named; schema: %s" % (NEW_COUNT, count, len(named), schema_note))
        if os.path.isfile(ID_NEW_TEST):
            passed, tail = pytest_run([ID_NEW_TEST])
        else:
            passed, tail = False, "the file does not exist"
        clause("C4 %s exists and passes" % ID_NEW_TEST, passed, tail)
        return verdict(a, ok)

    if a.crit == "AC2":
        fn, _path = search_on(document)
        good = []
        for q, key, name in QUERIES:
            r = fn(q)
            cands = r.get("candidates") or []
            hit = next((c for c in cands if c.get("security_key") == key), None)
            print("   %r: status %s candidates %s" % (q, r.get("status"),
                                                      [(c.get("security_key"), c.get("name")) for c in cands][:5]))
            good.append(r.get("status") == "candidates" and not r.get("security_key") and hit is not None
                        and (name is None or hit.get("name") == name))
        clause("C1 apple, microsoft and airbnb list their companies by company name, never as exact", all(good))
        have, lack, asked = [], [], 0
        for i, record in enumerate(records):
            typed = [n for n in ((record.get("source_row") or {}).get("folder"), registered_name(record), want[i][0])
                     if n and keys[i]]
            if not typed:
                continue
            asked += len(typed)
            (have if all(lists(fn, n, keys[i]) for n in typed) else lack).append(keys[i])
        clause("C2 every stored name (folder, registered, legal), typed whole, lists its own record",
               have and not lack, "%d of %d records, %d names typed, of %d records in all; not listed %s" % (
                   len(have), len(have) + len(lack), asked, len(records), lack[:12]))
        text = open(NS_TEST, encoding="utf-8").read() if os.path.isfile(NS_TEST) else ""
        passed, tail = pytest_run([NS_TEST])
        clause("C3 the test file holds %s and passes" % NS_TEST_NAME, ("def %s(" % NS_TEST_NAME) in text and passed,
               tail)
        return verdict(a, ok)

    # AC3, the bound
    served_by_key = {r.get("security_key"): r for r in served["records"]}
    built_by_key = {r.get("security_key"): r for r in records}
    moved = {}
    for key, record in built_by_key.items():
        other = served_by_key.get(key)
        if other is None:
            continue
        for field in sorted(set(record) | set(other)):
            if field != NEW_FIELD and record.get(field, "<absent>") != other.get(field, "<absent>"):
                moved.setdefault(field, []).append(key)
    same_keys = set(built_by_key) == set(served_by_key) and len(records) == len(served["records"])
    clause("C1 the same keys, and every existing field of every record equals the served record's",
           same_keys and not moved,
           "keys %d built, %d served, only built %s, only served %s; fields that moved %s" % (
               len(built_by_key), len(served_by_key), sorted(set(built_by_key) - set(served_by_key), key=str)[:5],
               sorted(set(served_by_key) - set(built_by_key), key=str)[:5],
               {f: len(k) for f, k in sorted(moved.items())}))
    top_built, top_served = strip_moving(document), strip_moving(served)
    top_moved = sorted(k for k in set(top_built) | set(top_served) if top_built.get(k) != top_served.get(k))
    listed = [".".join(p) for p in MOVING
              if (document.get(p[0]) or {}).get(p[1], "<absent>") != (served.get(p[0]) or {}).get(p[1], "<absent>")]
    clause("C2 every top-level field equals the served object's, other than the listed moving ones", not top_moved,
           "moved outside the list %s; listed ones that moved %s" % (top_moved, listed))
    _served, _key, plain, _handed = build(with_names=False)
    with_field = sum(1 for r in plain["records"] if NEW_FIELD in r)
    clause("C3 a build not handed legal names carries none", with_field == 0
           and NEW_COUNT not in (plain.get("denominators") or {}),
           "%d of %d records carry %s" % (with_field, len(plain["records"]), NEW_FIELD))
    fn, _path = search_on(document)
    stored = [k for k in keys if k]
    miss = [k for k in stored if not (fn(k).get("status") == "exact" and fn(k).get("security_key") == k)]
    lenovo = fn("lenovo")
    kept = any(c.get("security_key") == "992_HK_Equity" and c.get("name") == "Lenovo 992 HK"
               for c in (lenovo.get("candidates") or []))
    clause("C4 every stored key passes through as exact, and lenovo lists under its folder name",
           stored and not miss and kept and lenovo.get("status") == "candidates",
           "%d of %d exact; lenovo %s" % (len(stored) - len(miss), len(stored),
                                         [(c.get("security_key"), c.get("name")) for c in
                                          (lenovo.get("candidates") or [])][:3]))
    os.environ.pop("AMGT_CROSSWALK_PATH", None)
    existing = [ID_TESTS, NS_TEST]
    passed, tail = pytest_run(existing)
    clause("C5 the two packages' test files pass", passed, tail)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB7 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
