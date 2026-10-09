#!/usr/bin/env python3
"""check_entries_land_round8 -- LGIC_BLANKFIX round 8, cell BF-w-4.

For each drafted root-map entry in MAP_ENTRIES_round8.json (next to this file): merge that entry ALONE into a temporary
copy of the CURRENT infra/logic/registry/root_map.json and call lib/opal_naming_rootmap.load_map on it. The entry
  LANDS    when it carries no UNDECIDED value and the loader accepts it,
  is HELD  when it carries an UNDECIDED value (the fields are named) and every field it does decide passes the loader's
           own field checks (system, source and scope are tested one by one),
  is REFUSED when it carries none and the loader refuses it, or a decided field of a held entry fails its check.
Then every landing entry is merged into ONE temporary map and the `all` command (opal_naming_rootcheck.all_roots) runs on it once.
The registry is read, never written; the `_cite` object of an entry is the worker's record and is stripped before the merge,
so the loader sees exactly the entry the registry would hold.

One line per root (verdict, root, undecided fields), then the ALL-ROOTS line of the merged run, and last:
  ENTRIES-LAND ok=True entries=N land=N held=N refused=0 undecided_fields=N merged_ok=True
ok is True when refused == 0, land + held == entries, entries equals the number of entries the round-7 file left held (an
UNDECIDED value) and the roots are the same set, and the merged run is ok with no stopped root.

Python 3.9 syntax; ASCII only; no dependency beyond lib/.
"""
import copy
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRIES_FILE = os.path.join(HERE, "MAP_ENTRIES_round8.json")
ROUND7_FILE = os.path.join(HERE, "MAP_ENTRIES_round7.json")
UNDECIDED = "UNDECIDED"


def repo_root():
    """The worktree root: the nearest ancestor of this file that holds lib/opal_naming.py."""
    cur = HERE
    while True:
        if os.path.isfile(os.path.join(cur, "lib", "opal_naming.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            raise SystemExit("no lib/opal_naming.py above %s" % HERE)
        cur = parent


def undecided_fields(entry):
    """The names of the entry's fields whose value is UNDECIDED (a bare value, or an element of a list value)."""
    out = []
    for key, val in entry.items():
        if key == "_cite":
            continue
        if val == UNDECIDED or (isinstance(val, list) and UNDECIDED in val):
            out.append(key)
    return out


def clean(entry):
    return dict((k, v) for k, v in entry.items() if k != "_cite")


def decided_field_error(rm, name, ent):
    """"" or the loader's refusal of a field a HELD entry does decide (system, source, scope; one by one)."""
    if ent.get("names") == "none":
        return ""
    try:
        if ent.get("system") != UNDECIDED:
            rm._check_system(name, "system", ent.get("system"))
        if ent.get("source") != UNDECIDED:
            rm._check_source(name, "source", ent.get("source"))
        if ent.get("scope") != UNDECIDED:
            src = ent.get("source")
            rm._check_scope(name, "scope", ent.get("scope"), None if src == UNDECIDED else src)
    except ValueError as exc:
        return str(exc)
    return ""


def write_map(base_doc, entries, path):
    doc = copy.deepcopy(base_doc)
    doc.setdefault("roots", {})
    for root, ent in entries:
        doc["roots"][root] = clean(ent)
    with open(path, "wb") as fh:
        fh.write(json.dumps(doc, indent=1, ensure_ascii=True).encode("utf-8"))


def main():
    root = repo_root()
    sys.path.insert(0, os.path.join(root, "lib"))
    import opal_naming_rootcheck as rc  # noqa: E402
    import opal_naming_rootmap as rm  # noqa: E402

    with open(ENTRIES_FILE, "rb") as fh:
        entries = json.loads(fh.read().decode("utf-8"))["roots"]
    base_path = os.path.join(root, "infra", "logic", "registry", "root_map.json")
    with open(base_path, "rb") as fh:
        base_doc = json.loads(fh.read().decode("utf-8"))
    with open(ROUND7_FILE, "rb") as fh:
        round7 = json.loads(fh.read().decode("utf-8"))["roots"]
    held7 = sorted(k for k, v in round7.items() if undecided_fields(v))

    tmp = tempfile.mkdtemp(prefix="bfv5_")
    land, held, refused, fields_total = [], 0, 0, 0
    try:
        for name, ent in entries.items():
            und = undecided_fields(ent)
            if und:
                bad = decided_field_error(rm, name, ent)
                if bad:
                    refused += 1
                    print("REFUSED %s %s" % (name, bad))
                    continue
                held += 1
                fields_total += len(und)
                print("HELD    %s undecided=%s" % (name, ",".join(und)))
                continue
            path = os.path.join(tmp, "one.json")
            write_map(base_doc, [(name, ent)], path)
            try:
                rm.load_map(path)
            except ValueError as exc:
                refused += 1
                print("REFUSED %s %s" % (name, exc))
                continue
            land.append((name, ent))
            print("LANDS   %s undecided=none" % name)

        merged_path = os.path.join(tmp, "merged.json")
        write_map(base_doc, land, merged_path)
        lines = []
        rc_code = rc.all_roots(merged_path, out=lines.append)
        all_line = [ln for ln in lines if ln.startswith("ALL-ROOTS ")]
        stopped = [ln for ln in lines if ln.startswith("ROOT ") and "STOPPED" in ln]
        for ln in stopped:
            print(ln)
        print(all_line[-1] if all_line else "ALL-ROOTS missing")
        merged_ok = bool(all_line) and all_line[-1].startswith("ALL-ROOTS ok=True ") and rc_code == 0 and not stopped
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    n = len(entries)
    same_roots = sorted(entries) == held7
    if not same_roots:
        print("ROOTS-DIFFER missing=%s extra=%s" % (sorted(set(held7) - set(entries)), sorted(set(entries) - set(held7))))
    ok = refused == 0 and len(land) + held == n and n == len(held7) and same_roots and merged_ok
    print("ENTRIES-LAND ok=%s entries=%d land=%d held=%d refused=%d undecided_fields=%d merged_ok=%s"
          % (ok, n, len(land), held, refused, fields_total, merged_ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
