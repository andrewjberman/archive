#!/usr/bin/env python3
"""check_holes_new_roots -- LGIC_BLANKFIX round 9, cell BF-x-6 (0.9.0_WK_LGIC_BLANKFIX~3).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~3/check_holes_new_roots.py

The roots newly mapped at @1e660e15be (the keys of root_map.json there that its parent lacks) are the population. The check
copies infra/logic/registry/ to a temporary folder, merges the drafted rows of REGISTRY_ROWS_round9.json into the copy
(`_cite` stripped), runs the root check on the real registry (before) and once on the copy (after) for each newly mapped root,
and prints one line per worked root (hole before -> after). The registry itself is never written. Last line:

    NEW-ROOTS-FILL ok=True mapped=N before=N after=N roots_worked=N rows=N refused=0 owned_elsewhere=N

mapped is the number of roots the real root map holds; before/after are the HOLE totals over the newly mapped roots. ok=True
when after < before, no drafted row is refused by the registry's own readers (the validator, the loaders, the grader), the
roots were worked in descending hole order (no newly mapped root left unworked with more holes than a worked one), and every
HOLE line left on a worked root has an OWNED line in HOLES_OWNED_round9.md and every OWNED line matches a hole left.
Python 3.9; ASCII only.
"""
import json
import os
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
import opal_naming_rootmap  # noqa: E402

MAP_COMMIT = "1e660e15be"
ROWS = os.path.join(HERE, "REGISTRY_ROWS_round9.json")
OWNED = os.path.join(HERE, "HOLES_OWNED_round9.md")
REG = opal_naming.REGISTRY_DIR
STRIP = ("_cite",)
KEY_FIELDS = {"bucket", "key", "shape", "canonical", "none_owed", "evidence", "owner", "declared_in", "fills",
              "bucket_per", "bucket_from"}
NAME_FIELDS = {"name", "type", "canonical", "none_owed", "evidence", "owner"}
EVENT_FIELDS = {"name", "type", "canonical", "evidence"}


def _read(path):
    with open(path, "rb") as fh:
        return json.loads(fh.read().decode("utf-8"))


def _write(path, doc):
    with open(path, "wb") as fh:
        fh.write((json.dumps(doc, indent=1, ensure_ascii=True) + "\n").encode("ascii"))


def _text(v):
    return isinstance(v, str) and bool(v.strip())


def _grade_ok(name, typ):
    try:
        return opal_naming.grade(name, typ)[0] == "CONFORMANT"
    except Exception:  # a RaiseDefect is a refusal, whatever its class
        return False


def refuse_key(row, existing):
    if "_cite" not in row or not _text(row["_cite"]):
        return "no _cite"
    extra = set(row) - KEY_FIELDS - set(STRIP)
    if extra:
        return "fields outside row_fields: %s" % sorted(extra)
    if not (_text(row.get("evidence")) and _text(row.get("owner")) and row.get("shape") in ("object", "prefix")):
        return "evidence, owner or shape missing"
    if bool(row.get("canonical")) == bool(row.get("none_owed")):
        return "not exactly one of canonical and none_owed"
    per = bool(row.get("bucket_per") or row.get("bucket_from"))
    if per == bool(row.get("bucket")) or (per and not (row.get("bucket_per") == "firm" and row.get("bucket_from"))):
        return "not exactly one of bucket and (bucket_per 'firm' with bucket_from)"
    ident = ("per:" + row["bucket_from"], row["key"]) if per else (row["bucket"], row["key"])
    if ident in existing:
        return "a ruling for %r already exists" % (ident,)
    if row.get("canonical"):
        c = row["canonical"]
        if per:
            c = c.replace("{scope}", "49financial")
        if "{" in c:
            places = rc.admitted_places(row)
            if not places:
                return "canonical keeps an open place that fills does not explain"
            for p in places:
                c = c.replace("{%s}" % (p,), {"scope": "49financial", "source": "mdpf"}.get(p, "x"))
        if not _grade_ok(c, "S3Key"):
            return "canonical does not grade CONFORMANT as S3Key"
    return None


def refuse_name(row, existing):
    if "_cite" not in row or not _text(row["_cite"]):
        return "no _cite"
    extra = set(row) - NAME_FIELDS - set(STRIP)
    if extra:
        return "fields outside row_fields: %s" % sorted(extra)
    if not (_text(row.get("evidence")) and _text(row.get("owner")) and row.get("name") and row.get("type")):
        return "name, type, evidence or owner missing"
    if bool(row.get("canonical")) == bool(row.get("none_owed")):
        return "not exactly one of canonical and none_owed"
    if (row["name"], row["type"]) in existing:
        return "a ruling for (name, type) already exists"
    if row.get("canonical") and not _grade_ok(row["canonical"], row["type"]):
        return "canonical does not grade CONFORMANT as %s" % row["type"]
    return None


def refuse_event(row, existing):
    if "_cite" not in row or not _text(row["_cite"]):
        return "no _cite"
    extra = set(row) - EVENT_FIELDS - set(STRIP)
    if extra:
        return "fields outside row_fields: %s" % sorted(extra)
    if row.get("type") != "EVENT_RULE" or not _text(row.get("evidence")) or not row.get("name"):
        return "type, name or evidence wrong"
    if (row["name"], row["type"]) in existing:
        return "a rule for (name, type) already exists"
    if not row.get("canonical") or not _grade_ok(row["canonical"], "EVENT_RULE"):
        return "canonical does not grade CONFORMANT as EVENT_RULE"
    if opal_naming_cadence._event_token(row["canonical"]) is None:
        return "canonical has no on-{event} tail"
    return None


def newly_mapped():
    """The root_map keys written at MAP_COMMIT: its file's keys less its parent's."""
    def keys(rev):
        raw = subprocess.check_output(["git", "show", "%s:infra/logic/registry/root_map.json" % rev])
        return set(json.loads(raw.decode("utf-8"))["roots"])
    return sorted(keys(MAP_COMMIT) - keys(MAP_COMMIT + "^"))


def run_roots(roots, map_path, key_rulings, name_rulings):
    """({root: [hole lines]}, {root: hole count}) from check_root over each root, report-only."""
    holes, per = {}, {}
    for r in roots:
        lines = []
        rc.check_root(r, map_path, out=lines.append, report_only=True, key_rulings=key_rulings, name_rulings=name_rulings)
        h = [ln for ln in lines if ln.startswith("HOLE ")]
        holes[r] = h
        per[r] = len(h)
    return holes, per


def owned_lines():
    out = []
    if not os.path.isfile(OWNED):
        return out
    with open(OWNED, "rb") as fh:
        for ln in fh.read().decode("utf-8").splitlines():
            if ln.startswith("OWNED "):
                parts = [p.strip() for p in ln[6:].split("||")]
                if len(parts) >= 4:
                    typ, name = parts[1].split(" ", 1)
                    out.append((parts[0], typ, name, parts[2]))
    return out


def hole_key(root, ln):
    m = rc._LINE_RE.match(ln)
    return (root, m.group("type"), m.group("cur")) if m else (root, "?", ln)


def main():
    problems = []
    doc = _read(ROWS)
    worked = list(doc.get("_worked_roots") or [])
    new_roots = newly_mapped()
    real_map = os.path.join(REG, "root_map.json")
    mapped = len(_read(real_map)["roots"])
    tmp = tempfile.mkdtemp(prefix="holes_new_roots_")
    try:
        reg = os.path.join(tmp, "registry")
        shutil.copytree(REG, reg)
        kr = _read(os.path.join(reg, "key_rulings.json"))
        nr = _read(os.path.join(reg, "name_rulings.json"))
        er = _read(os.path.join(reg, "event_rules.json"))
        rm = _read(os.path.join(reg, "root_map.json"))
        have_k = set((("per:" + r["bucket_from"], r.get("key")) if r.get("bucket_from") else (r.get("bucket"), r.get("key")))
                     for r in kr["key_rulings"])
        have_n = set((r["name"], r["type"]) for r in nr["name_rulings"])
        have_e = set((r["name"], r["type"]) for r in er["rules"])
        refused, rows = 0, 0
        for r in doc.get("key_rulings.json", []):
            why = refuse_key(r, have_k)
            if why:
                refused += 1
                problems.append("REFUSED key %r/%r: %s" % (r.get("bucket"), r.get("key"), why))
                continue
            have_k.add(("per:" + r["bucket_from"], r["key"]) if r.get("bucket_from") else (r["bucket"], r["key"]))
            kr["key_rulings"].append({k: v for k, v in r.items() if k not in STRIP})
            rows += 1
        for r in doc.get("name_rulings.json", []):
            why = refuse_name(r, have_n)
            if why:
                refused += 1
                problems.append("REFUSED name %r/%r: %s" % (r.get("name"), r.get("type"), why))
                continue
            have_n.add((r["name"], r["type"]))
            nr["name_rulings"].append({k: v for k, v in r.items() if k not in STRIP})
            rows += 1
        for r in doc.get("event_rules.json", []):
            why = refuse_event(r, have_e)
            if why:
                refused += 1
                problems.append("REFUSED event %r: %s" % (r.get("name"), why))
                continue
            have_e.add((r["name"], r["type"]))
            er["rules"].append({k: v for k, v in r.items() if k not in STRIP})
            rows += 1
        for root, entry in sorted((doc.get("root_map.json") or {}).items()):
            if root not in rm["roots"]:
                refused += 1
                problems.append("REFUSED root_map %r: the root has no entry to change" % (root,))
                continue
            rm["roots"][root] = {k: v for k, v in entry.items() if k not in STRIP}
            rows += 1
        _write(os.path.join(reg, "key_rulings.json"), kr)
        _write(os.path.join(reg, "name_rulings.json"), nr)
        _write(os.path.join(reg, "event_rules.json"), er)
        _write(os.path.join(reg, "root_map.json"), rm)
        # the registry's own readers over the merged copy: any raise is a refusal of the whole draft
        try:
            refusals, _warn = opal_naming.validate(reg)
            for x in refusals:
                refused += 1
                problems.append("REFUSED registry validate: %s.%s: %s" % x)
            k2 = rc.load_key_rulings(os.path.join(reg, "key_rulings.json"))
            n2 = rc.load_name_rulings(os.path.join(reg, "name_rulings.json"))
            opal_naming_rootmap.load_map(os.path.join(reg, "root_map.json"))
        except Exception as exc:
            refused += 1
            problems.append("REFUSED registry readers: %s: %s" % (type(exc).__name__, exc))
            k2, n2 = rc.load_key_rulings(), rc.load_name_rulings()
        holes_b, per_b = run_roots(new_roots, real_map, None, None)
        saved = opal_naming_cadence._EVENT_RULES
        opal_naming_cadence._EVENT_RULES = os.path.join(reg, "event_rules.json")
        try:
            holes_a, per_a = run_roots(new_roots, os.path.join(reg, "root_map.json"), k2, n2)
        finally:
            opal_naming_cadence._EVENT_RULES = saved
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    before, after = sum(per_b.values()), sum(per_a.values())
    # descending order: the worked roots in the order listed, and no newly mapped root with holes left unworked while
    # holding more holes than a worked one
    order_ok = True
    for i in range(len(worked) - 1):
        if per_b.get(worked[i], -1) < per_b.get(worked[i + 1], -1):
            order_ok = False
            problems.append("order: %s (%s) before %s (%s)" % (worked[i], per_b.get(worked[i]), worked[i + 1],
                                                               per_b.get(worked[i + 1])))
    if worked:
        floor = min(per_b.get(w, 0) for w in worked)
        for r, n in per_b.items():
            if r not in worked and n > floor:
                order_ok = False
                problems.append("order: unworked newly mapped root %s has %d holes, more than the smallest worked root (%d)"
                                % (r, n, floor))
    for w in worked:
        if w not in per_b:
            order_ok = False
            problems.append("worked root %s is not a newly mapped root" % (w,))
    left = set()
    detail = {}
    for w in worked:
        for ln in holes_a.get(w, []):
            k = hole_key(w, ln)
            left.add(k)
            detail[k] = ln
    owned = owned_lines()
    owned_keys = set((o[0], o[1], o[2]) for o in owned)
    undisposed = sorted(left - owned_keys)
    stray = sorted(owned_keys - left)
    for u in undisposed[:10]:
        problems.append("UNDISPOSED hole left on a worked root: %s :: %s" % (u, detail.get(u, "")[:300]))
    for s in stray[:10]:
        problems.append("OWNED line for a hole that is not left: %s" % (s,))
    for w in worked:
        print("ROOT-FILL %s hole %d -> %d" % (w, per_b.get(w, -1), per_a.get(w, -1)))
    rest = ", ".join("%s %d->%d" % (r, per_b[r], per_a[r]) for r in new_roots if r not in worked)
    print("NEWLY-MAPPED-NOT-WORKED " + (rest or "none") + "  (newly mapped at %s: %d roots)" % (MAP_COMMIT, len(new_roots)))
    for p in problems:
        print(p)
    ok = (after < before and refused == 0 and order_ok and not undisposed and not stray and bool(worked))
    print("NEW-ROOTS-FILL ok=%s mapped=%d before=%d after=%d roots_worked=%d rows=%d refused=%d owned_elsewhere=%d" % (
        ok, mapped, before, after, len(worked), rows, refused, len(owned)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
