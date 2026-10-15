"""t1_check.py -- grades MX-c-18 / T1 (nl_tags on every catalog row; the empty ones derived and marked inferred), run from the repo root.

  python t1_check.py ac1   the emitted catalog: EVERY row of silver_datasets, portal_datasets and harvest_datasets carries a non-empty nl_tags list;
                           prints the denominator (N of N)
  python t1_check.py ac2   against the BASE catalog (the live one, git ref BASE_REF): a row whose base nl_tags were non-empty keeps them byte-equal and
                           carries no nl_tags_basis; a row whose base nl_tags were empty or absent now has non-empty nl_tags and nl_tags_basis == inferred;
                           the inferred set is exactly the rows that were empty (44 expected, printed)
  python t1_check.py ac3   the derivation: workflows/atom_decomposition/derive_nl_tags.py derive_tags(entity, business_meaning, example_questions) is
                           deterministic, and for every inferred row it reproduces the row's tags exactly, 3 to 6 tags, each tag 2 to 5 lowercase ASCII
                           words, no duplicate tag, every word drawn from the row's OWN entity, business_meaning or example_questions

The catalog is infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml, or T1_CATALOG (a planted copy); the derive module is the one in
workflows/atom_decomposition, or T1_DERIVE (a planted reference module file). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "1b18b94979"
CATALOG = "infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
NEW = os.environ.get("T1_CATALOG") or CATALOG
DERIVE = os.environ.get("T1_DERIVE") or os.path.join("workflows", "atom_decomposition", "derive_nl_tags.py")
SECTIONS = ("silver_datasets", "portal_datasets", "harvest_datasets")
TAG = re.compile(r"^[a-z0-9]+( [a-z0-9]+){1,4}$")


def load(path):
    with open(path, encoding="ascii") as fh:
        return yaml.safe_load(fh)


def base_catalog():
    r = subprocess.run(["git", "show", "%s:%s" % (BASE_REF, CATALOG)], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        print("ERROR: git show %s:%s rc %d" % (BASE_REF, CATALOG, r.returncode))
        sys.exit(9)
    p = os.path.join(tempfile.mkdtemp(prefix="t1_"), "base.yaml")
    open(p, "wb").write(r.stdout)
    return load(p)


def rows(cat):
    out = {}
    for sec in SECTIONS:
        for r in cat.get(sec) or []:
            if isinstance(r, dict) and r.get("entity"):
                out[r["entity"]] = r
    return out


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def ac1():
    new = rows(load(NEW))
    have = sum(1 for r in new.values() if isinstance(r.get("nl_tags"), list) and r["nl_tags"] and all(isinstance(t, str) and t.strip() for t in r["nl_tags"]))
    print("DENOMINATOR rows %d; with a non-empty nl_tags %d of %d" % (len(new), have, len(new)))
    for e in sorted(e for e, r in new.items() if not r.get("nl_tags"))[:5]:
        print("  empty: %s" % e)
    return report([("every row carries non-empty nl_tags (%d of %d)" % (have, len(new)), len(new) > 0 and have == len(new))])


def ac2():
    base, new = rows(base_catalog()), rows(load(NEW))
    res = []
    empty_before = sorted(e for e, r in base.items() if not r.get("nl_tags"))
    inferred_now = sorted(e for e, r in new.items() if r.get("nl_tags_basis") == "inferred")
    print("DENOMINATOR base rows %d, new rows %d; empty in the base %d; marked inferred now %d" % (len(base), len(new), len(empty_before), len(inferred_now)))
    res.append(("the row sets are equal", sorted(base) == sorted(new)))
    res.append(("the inferred set is exactly the rows that were empty (%d)" % len(empty_before), inferred_now == empty_before and len(empty_before) > 0))
    kept = [e for e in base if e not in empty_before and e in new]
    same = [e for e in kept if new[e].get("nl_tags") == base[e].get("nl_tags") and "nl_tags_basis" not in new[e]]
    res.append(("%d of %d rows that had tags keep them byte-equal and carry no nl_tags_basis" % (len(same), len(kept)), len(same) == len(kept) and bool(kept)))
    filled = [e for e in empty_before if e in new and new[e].get("nl_tags")]
    res.append(("%d of %d empty rows now have tags" % (len(filled), len(empty_before)), len(filled) == len(empty_before)))
    return report(res)


def words(text):
    return set(re.findall(r"[a-z0-9]+", str(text).lower()))


def ac3():
    spec = importlib.util.spec_from_file_location("t1_derive", DERIVE)
    if not os.path.exists(DERIVE):
        print("ERROR: %s absent" % DERIVE)
        return report([("derive_nl_tags.py exists", False)])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    new = rows(load(NEW))
    inferred = sorted(e for e, r in new.items() if r.get("nl_tags_basis") == "inferred")
    bad = []
    for e in inferred:
        r = new[e]
        qs = list(r.get("example_questions") or [])
        meaning = (r.get("property") or {}).get("meaning") or r.get("business_meaning") or ""
        a = mod.derive_tags(e, meaning, qs)
        b = mod.derive_tags(e, meaning, qs)
        tags = r.get("nl_tags") or []
        own = words(e) | words(meaning) | words(" ".join(qs))
        why = None
        if a != b:
            why = "not deterministic"
        elif a != tags:
            why = "does not reproduce the row's tags"
        elif not 3 <= len(tags) <= 6:
            why = "%d tags" % len(tags)
        elif len(set(tags)) != len(tags):
            why = "duplicate tag"
        elif not all(TAG.match(t) for t in tags):
            why = "a tag is not 2 to 5 lowercase ASCII words"
        elif not all(set(t.split()) <= own for t in tags):
            why = "a tag word is not drawn from the row's own text"
        if why:
            bad.append("%s: %s" % (e, why))
    print("DENOMINATOR inferred rows %d; bad %d" % (len(inferred), len(bad)))
    for b in bad[:5]:
        print("  BAD %s" % b)
    return report([("derive_tags reproduces and satisfies the rules on %d of %d inferred rows" % (len(inferred) - len(bad), len(inferred)), bool(inferred) and not bad)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
