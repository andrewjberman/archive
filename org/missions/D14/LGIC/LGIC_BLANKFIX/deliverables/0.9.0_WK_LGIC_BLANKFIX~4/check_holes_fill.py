#!/usr/bin/env python3
"""check_holes_fill -- LGIC_BLANKFIX round 8, cell BF-w-3 (0.9.0_WK_LGIC_BLANKFIX~4).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~4/check_holes_fill.py

Copies infra/logic/registry/ to a temporary folder, merges the drafted rows of REGISTRY_ROWS_round8.json into the copy
(`_cite` stripped), runs the all-roots check on the real registry (before) and on the copy (after), and prints one line
per worked root (hole before -> after). The registry itself is never written. Last line:

    HOLES-FILL ok=True before=N after=N roots_worked=N rows=N refused=0 owned_elsewhere=N

before/after are the all-mapped-roots HOLE totals. ok=True when after < before, no drafted row is refused by the
registry's own readers (the validator, the three loaders, the grader), the roots were worked in descending hole order,
and every HOLE line left on a worked root has an OWNED line in HOLES_OWNED_round8.md. Python 3.9; ASCII only.
"""
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
import opal_naming_rootmap  # noqa: E402

ROWS = os.path.join(HERE, "REGISTRY_ROWS_round8.json")
OWNED = os.path.join(HERE, "HOLES_OWNED_round8.md")
REG = opal_naming.REGISTRY_DIR
STRIP = ("_cite",)
KEY_FIELDS = {"bucket", "key", "shape", "canonical", "none_owed", "evidence", "owner", "declared_in", "fills",
              "bucket_per", "bucket_from"}
NAME_FIELDS = {"name", "type", "canonical", "none_owed", "evidence", "owner"}
EVENT_FIELDS = {"name", "type", "canonical", "evidence"}
_ROOT_LINE = re.compile(r"^ROOT (?P<root>\S+) \| ROOTCHECK .*? hole=(?P<hole>\d+) \|")


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
            # an open place is admitted only where fills explains every place (the registry's own reading)
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


def estate(map_path, key_rulings, name_rulings, holes_out):
    """(per-root hole counts, total line fields) from one all-roots run; holes_out gets {root: [(type, name, line)]}."""
    def run_one(key, mp, out=print, report_only=True):
        lines = []
        rc.check_root(key, mp, out=lines.append, report_only=True, key_rulings=key_rulings, name_rulings=name_rulings)
        for ln in lines:
            if ln.startswith("HOLE "):
                m = rc._LINE_RE.match(ln)
                holes_out.setdefault(key, []).append(
                    (m.group("type"), m.group("cur"), ln) if m else ("?", ln, ln))
            out(ln)
    lines = []
    rc.all_roots(map_path, out=lines.append, run_one=run_one)
    per = {}
    for ln in lines:
        m = _ROOT_LINE.match(ln)
        if m:
            per[m.group("root")] = int(m.group("hole"))
    last = lines[-1]
    fields = dict(p.split("=", 1) for p in last.split()[1:] if "=" in p)
    return per, fields, lines


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


def main():
    problems = []
    doc = _read(ROWS)
    worked = list(doc.get("_worked_roots") or [])
    tmp = tempfile.mkdtemp(prefix="holes_fill_")
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
            e = {k: v for k, v in entry.items() if k not in STRIP}
            rm["roots"][root] = e
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
        # before: the real registry
        holes_b, holes_a = {}, {}
        per_b, f_b, _lb = estate(os.path.join(REG, "root_map.json"), None, None, holes_b)
        # after: the copy (the event rules are read from the copy by the cadence reader)
        saved = opal_naming_cadence._EVENT_RULES
        opal_naming_cadence._EVENT_RULES = os.path.join(reg, "event_rules.json")
        try:
            per_a, f_a, _la = estate(os.path.join(reg, "root_map.json"), k2, n2, holes_a)
        finally:
            opal_naming_cadence._EVENT_RULES = saved
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    before, after = int(f_b["hole"]), int(f_a["hole"])
    # descending order: the worked roots in the order listed, no unworked root with a larger count than a worked one
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
                problems.append("order: unworked root %s has %d holes, more than the smallest worked root (%d)" % (r, n, floor))
    for w in worked:
        if w not in per_b:
            order_ok = False
            problems.append("worked root %s is not a mapped root" % (w,))
    owned = owned_lines()
    left = set()
    for w in worked:
        for (typ, name, _ln) in holes_a.get(w, []):
            left.add((w, typ, name))
    owned_keys = set((o[0], o[1], o[2]) for o in owned)
    undisposed = sorted(left - owned_keys)
    stray = sorted(owned_keys - left)
    detail = dict(((w, t, n), ln) for w in worked for (t, n, ln) in holes_a.get(w, []))
    for u in undisposed[:10]:
        problems.append("UNDISPOSED hole left on a worked root: %s :: %s" % (u, detail.get(u, "")[:300]))
    for s in stray[:10]:
        problems.append("OWNED line for a hole that is not left: %s" % (s,))
    for w in worked:
        print("ROOT-FILL %s hole %d -> %d" % (w, per_b.get(w, -1), per_a.get(w, -1)))
    moved = ", ".join("%s %d->%d" % (r, per_b[r], per_a.get(r, -1)) for r in sorted(per_b)
                      if r not in worked and per_a.get(r) != per_b[r])
    print("OTHER-ROOTS-MOVED " + (moved or "none"))
    print("ESTATE mapped_roots=%s items_before=%s items_after=%s uncounted_before=%s uncounted_after=%s "
          "stale_hints_before=%s stale_hints_after=%s" % (f_b["mapped"], f_b["items"], f_a["items"], f_b["uncounted"],
                                                         f_a["uncounted"], f_b["stale_hints"], f_a["stale_hints"]))
    for p in problems:
        print(p)
    ok = (after < before and refused == 0 and order_ok and not undisposed and not stray and bool(worked)
          and f_b["ok"] == "True" and f_a["ok"] == "True"
          and int(f_a["stale_hints"]) <= int(f_b["stale_hints"]) and f_a["items"] == f_b["items"])
    print("HOLES-FILL ok=%s before=%d after=%d roots_worked=%d rows=%d refused=%d owned_elsewhere=%d" % (
        ok, before, after, len(worked), rows, refused, len(owned)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
