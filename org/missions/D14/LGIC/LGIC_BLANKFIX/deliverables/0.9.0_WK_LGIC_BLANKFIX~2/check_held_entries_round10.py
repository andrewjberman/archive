#!/usr/bin/env python3
"""check_held_entries_round10 -- LGIC_BLANKFIX round 10, cell BF-y-3 (0.9.0_WK_LGIC_BLANKFIX~2).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~2/check_held_entries_round10.py

The nine roots round 8 held are ruled by 4.0.0_SA_CRO in org/tier1_exec/4.0.0_SA_CRO/deliverables/ROOT_MAP_ROUND10_RULINGS_20261009.md:
seven take an entry (MAP_ENTRIES_round10.json "roots"), two are retired ("retire", 0 resources). This check

  1. copies infra/logic/registry/ to a temporary folder (the registry itself is never written);
  2. loads every entry ALONE into a copy of the root map and calls opal_naming_rootmap.load_map (LANDS or REFUSED);
  3. compares each entry's four defaults with the ruling's table, and re-measures each entry's exceptions with opal_naming.grade
     (every name whose canonical form leads with a systems.json key other than the default is listed, and every listed one does);
  4. merges the entries and the rows of REGISTRY_ROWS_round10.json (`_cite` stripped) into the copy, each row through the same
     refusals the registry's own readers make;
  5. applies the retirements to the copy: the files of the retired roots leave the file list the scope reads, as `git rm` would;
  6. runs the `all` command (opal_naming_rootcheck.all_roots) ONCE against the copy, with the copy's rulings and event rules;
  7. reads the ALL-ROOTS line of the round-9 close (mapped_before, hole_before) and each root's hole count there.

Last line:  HELD-ENTRIES ok=True entries=N land=N refused=0 retired=N mapped_before=N mapped_after=N hole_before=N hole_after=N
ok is True when refused == 0, every ruled root lands, the retired roots leave the denominator (roots_total falls by exactly the number
retired and no root is unmapped), no root of the 78 mapped before has a HOLE that it did not have before, every HOLE left on a newly mapped
root has an OWNED line in HOLES_OWNED_round10.md (and every OWNED line matches a HOLE left), and the merged run prints ok=True with
no stopped root. Python 3.9; ASCII only.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"]).decode("ascii").strip()
os.chdir(REPO)
sys.path.insert(0, os.path.join(REPO, "lib"))

import opal_naming  # noqa: E402
import opal_naming_cadence  # noqa: E402
import opal_naming_rootcheck as rc  # noqa: E402
import opal_naming_rootmap as rm  # noqa: E402
import opal_naming_scope  # noqa: E402

ENTRIES = os.path.join(HERE, "MAP_ENTRIES_round10.json")
ROWS = os.path.join(HERE, "REGISTRY_ROWS_round10.json")
OWNED = os.path.join(HERE, "HOLES_OWNED_round10.md")
BASE_RUN = os.path.join(HERE, "..", "2.0.0_SA_COO~B1", "ALL_ROOTS_round9.txt")
ROUND9_CHECK = os.path.join(HERE, "..", "0.9.0_WK_LGIC_BLANKFIX~3", "check_holes_new_roots.py")
REG = opal_naming.REGISTRY_DIR
TF = "infra/aws/terraform/"
STRIP = ("_cite",)

# The ruling's tables (ROOT_MAP_ROUND10_RULINGS_20261009.md R10-1..R10-3): root -> (system, scope, source, fills)
RULED = {
    "shared-infra": ("cloudops", "global", "cloudops", []),
    "astn-pipeline": ("news", "global", "news", []),
    "mdpf-pipeline": ("mdpf", "global", "mdpf", ["system"]),
    "etfs-reports": ("etfs", "global", "etfs", ["system"]),
    "etfs-canon": ("etfs", "global", "etfs", ["system"]),
    "etfs-netassets": ("etfs", "global", "etfs", ["system"]),
    "harvest": ("harvest", "global", "harvest", ["system"]),
}
RETIRED = ("canonical-schwab-si2-schedule", "opal-assets-absence")


def _load_round9():
    spec = importlib.util.spec_from_file_location("check_holes_new_roots_r9", ROUND9_CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    os.chdir(REPO)
    return mod


R9 = _load_round9()
_read, _write = R9._read, R9._write


def clean(d):
    return dict((k, v) for k, v in d.items() if k not in STRIP)


def base_numbers():
    """(mapped, total, hole, {root: hole}) from the round-9 close."""
    with open(BASE_RUN, "rb") as fh:
        text = fh.read().decode("utf-8")
    last = [ln for ln in text.splitlines() if ln.startswith("ALL-ROOTS ")][-1]
    f = dict(p.split("=", 1) for p in last.split()[1:] if "=" in p)
    per = {}
    for ln in text.splitlines():
        m = re.match(r"^ROOT (\S+) \| ROOTCHECK .* hole=(\d+) \| COMPLETED$", ln)
        if m:
            per[m.group(1)] = int(m.group(2))
    return int(f["mapped"]), int(f["roots_total"]), int(f["hole"]), per


def measure_exceptions(root, default, map_path):
    """{(name, type): lead} for every name of the root whose canonical form (or its own name, when conformant) leads with a
    systems.json key other than `default`. S3Key and SECRET lead with a source, not a system, and are not measured."""
    keys = set(s["key"] for s in opal_naming._systems(opal_naming._registry()))
    items = opal_naming_scope.root_names(TF + root, map_path)[0]
    out = {}
    for it in items:
        if it["type"] in ("S3Key", "SECRET"):
            continue
        try:
            _v, canon = opal_naming.grade(it["current"], it["type"])
        except Exception:
            continue
        lead = (canon or it["current"]).split("-")[0]
        if lead in keys and lead != default:
            out[(it["current"], it["type"])] = lead
    return out


def owned_lines():
    out = []
    if os.path.isfile(OWNED):
        with open(OWNED, "rb") as fh:
            for ln in fh.read().decode("utf-8").splitlines():
                if ln.startswith("OWNED "):
                    parts = [p.strip() for p in ln[6:].split("||")]
                    if len(parts) >= 4:
                        typ, name = parts[1].split(" ", 1)
                        out.append((parts[0], typ, name, parts[2]))
    return out


def main():
    problems = []
    ent_doc = _read(ENTRIES)
    entries = ent_doc["roots"]
    retire = [r["root"] for r in ent_doc.get("retire", [])]
    rows = _read(ROWS)
    mapped_b, total_b, hole_b, per_b = base_numbers()
    tmp = tempfile.mkdtemp(prefix="held_entries_r10_")
    refused, rows_n = 0, 0
    try:
        reg = os.path.join(tmp, "registry")
        shutil.copytree(REG, reg)
        base_map = _read(os.path.join(reg, "root_map.json"))
        # 2. each entry alone
        land = 0
        for name, ent in sorted(entries.items()):
            one = os.path.join(tmp, "one.json")
            doc = json.loads(json.dumps(base_map))
            doc["roots"][name] = clean(ent)
            _write(one, doc)
            try:
                rm.load_map(one)
                land += 1
                print("LANDS   %s" % name)
            except ValueError as exc:
                refused += 1
                problems.append("REFUSED entry %s: %s" % (name, exc))
                print("REFUSED %s %s" % (name, exc))
        # 3. the ruling's table, and the exceptions re-measured
        for name, (sysn, scope, src, fills) in RULED.items():
            ent = entries.get(name)
            if ent is None:
                refused += 1
                problems.append("RULED root %s has no entry" % name)
                continue
            got = (ent.get("system"), ent.get("scope"), ent.get("source"), ent.get("fills"))
            if got != (sysn, scope, src, fills):
                refused += 1
                problems.append("entry %s %r differs from the ruling %r" % (name, got, (sysn, scope, src, fills)))
        extra = set(entries) - set(RULED)
        if extra:
            refused += 1
            problems.append("entries for roots the ruling does not name: %s" % sorted(extra))
        if sorted(retire) != sorted(RETIRED):
            refused += 1
            problems.append("retire list %s differs from the ruling %s" % (sorted(retire), sorted(RETIRED)))
        # 4. merge entries and rows
        merged = json.loads(json.dumps(base_map))
        for name, ent in entries.items():
            if name in merged["roots"]:
                refused += 1
                problems.append("REFUSED entry %s: the root is already mapped" % name)
            merged["roots"][name] = clean(ent)
        merged_map = os.path.join(reg, "root_map.json")
        _write(merged_map, merged)
        for name, (sysn, _s, _c, _f) in RULED.items():
            if name not in entries:
                continue
            listed = dict(((e["name"], e["type"]), e["system"]) for e in entries[name].get("exceptions", []))
            measured = measure_exceptions(name, sysn, merged_map)
            miss = sorted(set(measured) - set(listed))
            wrong = sorted(k for k in listed if measured.get(k) != listed[k])
            print("EXCEPTIONS %s listed=%d measured=%d" % (name, len(listed), len(measured)))
            if miss or wrong:
                refused += 1
                problems.append("exceptions of %s: unlisted %s; listed but not measured %s" % (name, miss[:5], wrong[:5]))
        kr = _read(os.path.join(reg, "key_rulings.json"))
        nr = _read(os.path.join(reg, "name_rulings.json"))
        er = _read(os.path.join(reg, "event_rules.json"))
        have_k = set((("per:" + r["bucket_from"], r.get("key")) if r.get("bucket_from") else (r.get("bucket"), r.get("key")))
                     for r in kr["key_rulings"])
        have_n = set((r["name"], r["type"]) for r in nr["name_rulings"])
        have_e = set((r["name"], r["type"]) for r in er["rules"])
        for r in rows.get("key_rulings.json", []):
            why = R9.refuse_key(r, have_k)
            if why:
                refused += 1
                problems.append("REFUSED key %r/%r: %s" % (r.get("bucket"), r.get("key"), why))
                continue
            have_k.add((r["bucket"], r["key"]))
            kr["key_rulings"].append(clean(r))
            rows_n += 1
        for r in rows.get("name_rulings.json", []):
            why = R9.refuse_name(r, have_n)
            if why:
                refused += 1
                problems.append("REFUSED name %r/%r: %s" % (r.get("name"), r.get("type"), why))
                continue
            have_n.add((r["name"], r["type"]))
            nr["name_rulings"].append(clean(r))
            rows_n += 1
        for r in rows.get("event_rules.json", []):
            why = R9.refuse_event(r, have_e)
            if why:
                refused += 1
                problems.append("REFUSED event %r: %s" % (r.get("name"), why))
                continue
            have_e.add((r["name"], r["type"]))
            er["rules"].append(clean(r))
            rows_n += 1
        _write(os.path.join(reg, "key_rulings.json"), kr)
        _write(os.path.join(reg, "name_rulings.json"), nr)
        _write(os.path.join(reg, "event_rules.json"), er)
        try:
            refusals, _warn = opal_naming.validate(reg)
            for x in refusals:
                refused += 1
                problems.append("REFUSED registry validate: %s.%s: %s" % x)
            k2 = rc.load_key_rulings(os.path.join(reg, "key_rulings.json"))
            n2 = rc.load_name_rulings(os.path.join(reg, "name_rulings.json"))
            rm.load_map(merged_map)
        except Exception as exc:
            refused += 1
            problems.append("REFUSED registry readers: %s: %s" % (type(exc).__name__, exc))
            k2, n2 = rc.load_key_rulings(), rc.load_name_rulings()
        # the live denominator before the retirements (it can differ from the round-9 close: a root added since is not this cell's)
        covered = set(opal_naming_scope._map_key_root(k) for k in base_map["roots"])
        live_total_b = len(opal_naming_scope._roots())
        gone_keys = set(TF + r for r in list(entries) + list(retire))
        expect_unmapped = sorted(r for r in opal_naming_scope._roots() if r not in covered and r not in gone_keys)
        # 5. the retirements: the files of the retired roots leave the file list the scope reads
        gone = [f for f in opal_naming_scope._files() if any(f.startswith(TF + r + "/") for r in retire)]
        opal_naming_scope._CACHE["files"] = [f for f in opal_naming_scope._files() if f not in set(gone)]
        opal_naming_scope._CACHE.pop("roots", None)
        opal_naming_scope._CACHE.pop("dirs", None)
        print("RETIRED %s: %d tracked files leave the file list" % (", ".join(retire), len(gone)))
        # 6. the all command, once, on the copy
        seen = {}

        def run_one(key, map_path, out=print, report_only=True):
            lines = []
            try:
                return rc.check_root(key, map_path, out=lines.append, report_only=True, key_rulings=k2, name_rulings=n2)
            finally:
                seen[key] = list(lines)
                for ln in lines:
                    out(ln)

        saved = opal_naming_cadence._EVENT_RULES
        opal_naming_cadence._EVENT_RULES = os.path.join(reg, "event_rules.json")
        out_lines = []
        try:
            rc.all_roots(merged_map, out=out_lines.append, run_one=run_one)
        finally:
            opal_naming_cadence._EVENT_RULES = saved
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    all_line = [ln for ln in out_lines if ln.startswith("ALL-ROOTS ")]
    f = dict(p.split("=", 1) for p in all_line[-1].split()[1:] if "=" in p) if all_line else {}
    print(all_line[-1] if all_line else "ALL-ROOTS missing")
    stopped = [ln for ln in out_lines if ln.startswith("ROOT ") and "STOPPED" in ln]
    for ln in stopped:
        problems.append(ln[:300])
    mapped_a = int(f.get("mapped", -1))
    total_a = int(f.get("roots_total", -1))
    hole_a = int(f.get("hole", -1))
    merged_ok = bool(all_line) and all_line[-1].startswith("ALL-ROOTS ok=True ") and not stopped
    if not merged_ok:
        problems.append("the merged run did not print ok=True")
    # the retired roots leave the denominator, and nothing is unmapped
    unmapped_a = sorted(ln.split()[1] for ln in out_lines if ln.startswith("UNMAPPED "))
    print("DENOMINATOR round-9 close roots_total=%d; live before the retirements roots_total=%d; after roots_total=%d unmapped=%s" % (
        total_b, live_total_b, total_a, unmapped_a or "none"))
    if total_a != live_total_b - len(retire) or unmapped_a != expect_unmapped:
        problems.append("denominator: roots_total %d (live before %d, retired %d), unmapped %s expected %s" % (
            total_a, live_total_b, len(retire), unmapped_a, expect_unmapped))
    # no HOLE on a root mapped before is added
    per_a = dict((k, sum(1 for ln in v if ln.startswith("HOLE "))) for k, v in seen.items())
    added = sorted(k for k in per_b if per_a.get(k, 0) > per_b[k])
    for k in added:
        problems.append("HOLE added on a root mapped before: %s %d -> %d" % (k, per_b[k], per_a.get(k, 0)))
    # every HOLE left on a newly mapped root is owned, and every OWNED line is a HOLE left
    left, detail = set(), {}
    for root in entries:
        for ln in seen.get(root, []):
            if ln.startswith("HOLE "):
                m = rc._LINE_RE.match(ln)
                k = (root, m.group("type"), m.group("cur")) if m else (root, "?", ln)
                left.add(k)
                detail[k] = ln
    owned = owned_lines()
    owned_keys = set((o[0], o[1], o[2]) for o in owned)
    undisposed = sorted(left - owned_keys)
    stray = sorted(owned_keys - left)
    for u in undisposed[:12]:
        problems.append("UNDISPOSED hole on a newly mapped root: %s :: %s" % (u, detail.get(u, "")[:260]))
    for s in stray[:12]:
        problems.append("OWNED line for a hole that is not left: %s" % (s,))
    for root in sorted(entries):
        hb = per_a.get(root, -1)
        print("ROOT-HOLES %s hole_after=%d (owned %d)" % (root, hb, sum(1 for o in owned if o[0] == root)))
    print("ROWS merged=%d (key_rulings %d, name_rulings %d, event_rules %d) owned_elsewhere=%d" % (
        rows_n, len(rows.get("key_rulings.json", [])), len(rows.get("name_rulings.json", [])), len(rows.get("event_rules.json", [])), len(owned)))
    for p in problems:
        print(p)
    ok = (refused == 0 and land == len(entries) == len(RULED) and merged_ok and not added and not undisposed and not stray
          and total_a == live_total_b - len(retire) and unmapped_a == expect_unmapped and mapped_a == mapped_b + len(entries) and not stopped)
    print("HELD-ENTRIES ok=%s entries=%d land=%d refused=%d retired=%d mapped_before=%d mapped_after=%d hole_before=%d hole_after=%d" % (
        ok, len(entries), land, refused, len(retire), mapped_b, mapped_a, hole_b, hole_a))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
