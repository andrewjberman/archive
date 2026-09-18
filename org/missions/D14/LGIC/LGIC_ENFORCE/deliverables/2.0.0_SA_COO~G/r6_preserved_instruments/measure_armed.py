# PRESERVED BY 2.0.0_SA_COO~G AT THE DRAIN OF LGIC_ENFORCE.TO-EN-s-32-r6, UNMODIFIED BELOW THIS HEADER.
# ORIGIN: measure_armed.py of worktree .worktrees/wk-lgic-enforce-6-1, authored by 0.9.0_WK_LGIC_ENFORCE~1, NEVER COMMITTED
#   and about to be deleted with that worktree.
# WHY: DISARM_SWEEP_R6.json's own denominators.instrument field cites ".scratch/measure_armed.py" as the
#   SECOND, deliberately different reader whose agreement with check_en_r6.py's armed_population() is the
#   cell's corroboration claim. An untracked instrument makes that claim UNVERIFIABLE the moment the
#   worktree is removed -- the record would cite an instrument nobody can run.
# NOT CLAIMED: that this seat has re-run or reviewed the logic below. It is preserved VERBATIM as evidence,
#   and its own sha1 under git hash-object is recorded in the commit that adds it.
# THIS COPY IS NOT ON ANY EXECUTION PATH. No criterion invokes it.
#!/usr/bin/env python3
"""My own re-derivation of LGIC_ENFORCE's ARMED population.

A DIFFERENT instrument than check_en_r6.py's armed_population(): this walks the
channel with os.walk and scans fences LINE BY LINE rather than glob + a single
re.finditer over the whole file. Same predicate (R-46 as corrected, R-42 owner
order), independently coded, so a disagreement between the two is a finding
rather than a restatement.

Usage: python .scratch/measure_armed.py <repo_root> <dump_path>
"""
import json
import os
import sys

ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"


def fences(text):
    """Every ```json fence body, found by a LINE scan (not one regex over the file)."""
    bodies = []
    buf = None
    for line in text.split("\n"):
        s = line.strip()
        if buf is None:
            if s.startswith("```json"):
                buf = []
            continue
        if s.startswith("```"):
            bodies.append("\n".join(buf))
            buf = None
            continue
        buf.append(line)
    return bodies


def walk_channel(repo):
    base = os.path.join(repo, ROOT, "surprise-channel")
    files = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            if fn.endswith(".md"):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def owner_of(r):
    cands = [r.get("disarm_owner")]
    dz = r.get("disarm")
    cands.append(dz.get("owner") if isinstance(dz, dict) else None)
    cands.append(r.get("owner"))
    for v in cands:
        if str(v or "").strip():
            return str(v).strip()
    return "<NO OWNER FIELD>"


def closing_clock(doc, r):
    if "REMEDIATION" not in doc.upper():
        return None
    rem = r.get("remediation")
    if isinstance(rem, dict) and str(rem.get("state") or "").upper() == "REMEDIATED":
        return "remediation.state=REMEDIATED"
    dz = r.get("disarm")
    if (isinstance(dz, dict)
            and str(dz.get("state") or "").upper() == "DISARMED"
            and str(dz.get("at") or "").strip()):
        return "disarm DISARMED at %s" % dz.get("at")
    return None


def main():
    repo = sys.argv[1]
    dump = sys.argv[2]
    pairs = []
    per_file = []
    for path in walk_channel(repo):
        text = open(path, encoding="utf-8", errors="replace").read()
        doc = os.path.basename(path)
        n_f, n_r, n_bad = 0, 0, 0
        for body in fences(text):
            n_f += 1
            try:
                d = json.loads(body)
            except ValueError:
                n_bad += 1
                continue
            for r in (d if isinstance(d, list) else [d]):
                if isinstance(r, dict) and r.get("id"):
                    pairs.append((doc, r))
                    n_r += 1
        per_file.append((doc, n_f, n_r, n_bad))

    byid = {}
    for doc, r in pairs:
        byid.setdefault(r["id"], []).append((doc, r))

    still, closed = {}, {}
    for rid, rows in sorted(byid.items()):
        if not any(str(r.get("hazard_standing")) == "ARMED" for _d, r in rows):
            continue
        why = None
        for doc, r in rows:
            why = closing_clock(doc, r)
            if why:
                break
        if why:
            closed[rid] = why
        else:
            first = next(r for _d, r in rows if str(r.get("hazard_standing")) == "ARMED")
            still[rid] = owner_of(first)

    print("INSTRUMENT: .scratch/measure_armed.py (os.walk + line-scanned fences)")
    print("documents scanned: %d" % len(per_file))
    for doc, n_f, n_r, n_bad in per_file:
        print("  %-42s fences=%-3d rows=%-4d unparseable=%d" % (doc, n_f, n_r, n_bad))
    print("OCCURRENCES (rows with an id, never deduped): %d" % len(pairs))
    print("DISTINCT IDS: %d" % len(byid))
    print("ARMED IDS (any occurrence hazard_standing==ARMED): %d" % (len(still) + len(closed)))
    print("CLOSED BY A REMEDIATION CLOCK: %d" % len(closed))
    print("STILL ARMED: %d" % len(still))
    counts = {}
    for o in still.values():
        counts[o] = counts.get(o, 0) + 1
    print("OWNERS OF THE STILL-ARMED (disarm_owner -> disarm.owner -> owner):")
    for o in sorted(counts, key=lambda k: (-counts[k], k)):
        print("  %-20s %d" % (o, counts[o]))

    payload = {
        "occurrences": len(pairs),
        "distinct_ids": len(byid),
        "armed_ids": len(still) + len(closed),
        "closed": closed,
        "still_armed_owners": still,
        "owner_counts": counts,
        "rows": {rid: [{"doc": d, "row": r} for d, r in byid[rid]] for rid in still},
    }
    with open(dump, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    print("DUMP: %s" % dump)
    return 0


if __name__ == "__main__":
    sys.exit(main())
