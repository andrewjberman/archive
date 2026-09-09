#!/bin/bash
# E1-AC1 -- DOES THE MANIFEST STILL ROUTE BACK TO THE RETIRED LOCAL SURFACE?
#
# THE INSTRUMENT IS A YAML WALK, NEVER A TEXT SWEEP. A text sweep over this file cannot tell a
# LIVE ROUTE from a RETIRED RECORD, and the whole point of the retired-alias convention is that
# the record KEEPS the retired words so the retirement stays legible. Grep counts the words; this
# counts the ROUTES. So every predicate below is asked of a PARSED entry: its `status`, its
# `tool`, its `mode`, its `canonical_call` -- fields, not lines.
#
# WHAT "A ROUTE BACK" MEANS HERE, STATED BEFORE IT IS COUNTED (two disjunctive limbs):
#   (a) the entry's `canonical_call` names a flag the thin client REFUSES -- `--mode auto|inc|full`
#       or `--db-path`. Exercised at this cut: `python infra/aws/globgrph/kuzu_cli.py --mode full
#       "<q>"` prints `kuzu_cli.py: error: unrecognized arguments: --mode`.
#   (b) the entry is a REBUILD OF THE LOCAL STORE: tool comp-kuzu with mode `rebuild`. The
#       narrowing matters -- 45 other live entries carry mode `rebuild` legitimately (comp-build's
#       trace cache, comp-aws derive's cloud producer), and a predicate that counted `rebuild`
#       alone would convict the whole manifest of a defect that belongs to one tool.
#
# THE CANDIDATE SET IS THE LIVE ONE. An entry with `status: retired` has LEFT the routing candidate
# set by the file's own convention (see the per-entry schema at the head of the manifest) and is
# scored separately, by name, as a RECORD -- printed, never dropped. A retirement you cannot see
# is indistinguishable from a deletion, and this cell's bound is that records STAY.
#
# THREE CONTROLS, BECAUSE A ZERO HAS MORE THAN ONE CAUSE:
#   ROUTE_PROBE_CONTROL   -- a PLANTED entry carrying BOTH limbs, held in a temp string in this
#     file and never in a tracked one, fed through the SAME predicate in the SAME process. It must
#     be CAUGHT on both limbs. Without it, a predicate that matched nothing (a mistyped field name,
#     a walk over the wrong key) prints a perfect zero over the whole manifest.
#   ROUTE_NEGATIVE_CONTROL -- a PLANTED LIVE READ entry (`comp-kuzu "<Cypher>"`, mode query) fed
#     through the same predicate. It must NOT be caught. Without it, a predicate that matched
#     EVERYTHING would satisfy the first control and still read as a finding rather than a fact.
#   RETIRED_RESOLUTION    -- each retired record's `superseded_by` is resolved against the LIVE
#     entry ids. A successor that names nothing, or names another retired entry, is a dead pointer
#     and scores the record UNRESOLVED. "It has a successor field" is not "it has a successor".
#
# AN UNSCOPED RE-READ RUNS BESIDE THE SCOPED ONE. The criterion scopes tools_index to the comp-kuzu
# row; a check scoped to one member cannot see a defect the members SHARE, so every tools_index row
# is re-read for the same two flags and the count is printed whether it is zero or not.
#
# Exit: 0 = no live route back, both records resolve, all controls behaved.
#       1 = a live route back, an unresolved record, or a misbehaving control.
#       2 = BLOCKED (the manifest could not be read or parsed).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

python - <<'PY'
import re
import sys

try:
    import yaml
except ImportError as exc:
    print("BLOCKED: PyYAML unavailable (%s) -- a YAML criterion cannot be scored by a text sweep"
          % exc)
    sys.exit(2)

MANIFEST = "org/modules/graph/graph-call-manifest.yaml"
REFUSED_FLAG = re.compile(r"--mode\s+(auto|inc|full)|--mode\b|--db-path\b")
LOCAL_STORE = re.compile(r"kuzu_nessie_db")
RETIRED_IDS = ("cloud.refresh.full", "cloud.refresh.incremental")

try:
    with open(MANIFEST, encoding="utf-8") as fh:
        DOC = yaml.safe_load(fh)
except OSError as exc:
    print("BLOCKED: %s could not be read (%s)" % (MANIFEST, exc))
    sys.exit(2)
except yaml.YAMLError as exc:
    print("BLOCKED: %s failed to PARSE (%s) -- an unparseable manifest yields zero entries, which"
          " is a perfect score for the wrong reason" % (MANIFEST, exc))
    sys.exit(2)

ENTRIES = [e for e in (DOC.get("entries") or []) if isinstance(e, dict)]
TOOLS_INDEX = DOC.get("tools_index") or {}


def route_back(entry):
    """Every reason this entry routes back to the retired local surface. [] = it does not."""
    why = []
    call = str(entry.get("canonical_call") or "")
    if REFUSED_FLAG.search(call):
        why.append("canonical_call names a flag the client refuses")
    if LOCAL_STORE.search(call):
        why.append("canonical_call names the retired local store")
    if str(entry.get("tool") or "").strip() == "comp-kuzu" \
            and str(entry.get("mode") or "").strip() == "rebuild":
        why.append("mode is a rebuild of the local comp-kuzu store")
    return why


live = [e for e in ENTRIES if str(e.get("status") or "") != "retired"]
retired = [e for e in ENTRIES if str(e.get("status") or "") == "retired"]
live_ids = {str(e.get("id")) for e in live}

print("MANIFEST_ENTRIES_TOTAL=%d  (live %d + retired %d)" % (len(ENTRIES), len(live), len(retired)))
print("ROUTE_BACK_PREDICATE=(a) canonical_call names --mode/--db-path or the retired local store,"
      " OR (b) tool==comp-kuzu AND mode==rebuild. Asked of PARSED FIELDS, never of lines.")

offenders = [(str(e.get("id")), route_back(e)) for e in live]
offenders = [(i, w) for i, w in offenders if w]
for eid, why in offenders:
    print("  ROUTES BACK  %-42s %s" % (eid, "; ".join(why)))
print("LIVE_ROUTES_BACK=%d of %d" % (len(offenders), len(live)))

# --- the two retired records ---------------------------------------------------------------------
resolved = 0
for eid in RETIRED_IDS:
    rec = next((e for e in ENTRIES if str(e.get("id")) == eid), None)
    if rec is None:
        print("  RECORD MISSING  %s -- a retired entry is KEPT as a record, never deleted" % eid)
        continue
    status = str(rec.get("status") or "")
    succ = str(rec.get("superseded_by") or "")
    has_prose = bool(str(rec.get("retired") or "").strip()) and bool(str(rec.get("why") or "").strip())
    ok = status == "retired" and succ in live_ids and has_prose
    print("  RETIRED-RECORD  %-30s status=%s superseded_by=%s -> %s   retired+why prose=%s"
          % (eid, status or "(none)", succ or "(none)",
             "LIVE ENTRY" if succ in live_ids else "DEAD POINTER", "yes" if has_prose else "NO"))
    if ok:
        resolved += 1
print("RETIRED_RECORDS=%d of %d" % (resolved, len(RETIRED_IDS)))

# --- the tools_index comp-kuzu row (scoped), then every row (unscoped) -----------------------------
row = TOOLS_INDEX.get("comp-kuzu") or {}
subs = [str(x) for x in (row.get("subcommands") or [])]
ents = [str(x) for x in (row.get("entries") or [])]
bad = []
for s in subs:
    if REFUSED_FLAG.search(s):
        bad.append("subcommand %r" % s)
for e in ents:
    if e in RETIRED_IDS or e not in live_ids:
        bad.append("entry %r (retired or not a live id)" % e)
for b in bad:
    print("  TOOLS_INDEX comp-kuzu carries %s" % b)
print("TOOLS_INDEX_FLAGS=%d of %d   (subcommands %d + entries %d)"
      % (len(bad), len(subs) + len(ents), len(subs), len(ents)))

unscoped = []
for tool, r in sorted(TOOLS_INDEX.items()):
    if not isinstance(r, dict):
        continue
    for s in (r.get("subcommands") or []):
        if REFUSED_FLAG.search(str(s)):
            unscoped.append("%s:%s" % (tool, s))
    for e in (r.get("entries") or []):
        if str(e) in RETIRED_IDS:
            unscoped.append("%s:%s" % (tool, e))
for u in unscoped:
    print("  UNSCOPED RE-READ hit: %s" % u)
print("TOOLS_INDEX_FLAGS_UNSCOPED=%d of %d row(s)  (a check scoped to one member cannot see a"
      " defect the members share -- this is the same predicate over the whole population)"
      % (len(unscoped), len(TOOLS_INDEX)))

# --- control 1: a planted route back MUST be caught, on BOTH limbs ---------------------------------
PLANTED = yaml.safe_load(
    "id: planted.refresh.local\n"
    "use_case: planted\n"
    'canonical_call: \'comp-kuzu --mode full [--db-path PATH] "<Cypher>"\'\n'
    "tool: comp-kuzu\n"
    "mode: rebuild\n"
    "status: canonical\n")
caught = route_back(PLANTED)
if len(caught) < 2:
    print("ROUTE_PROBE_CONTROL=DEAD -- the planted route-back entry yielded %r (want both limbs);"
          " the zero above measures a broken predicate, not a clean manifest" % (caught,))
    sys.exit(1)
print("ROUTE_PROBE_CONTROL=FIRED -- a PLANTED entry carrying both limbs, held only in this script"
      " and fed through the SAME predicate in-process, was caught on %d limb(s): %s"
      % (len(caught), "; ".join(caught)))

# --- control 2: a planted LIVE READ must NOT be caught ---------------------------------------------
BENIGN = yaml.safe_load(
    "id: planted.read.served\n"
    "use_case: planted\n"
    'canonical_call: \'comp-kuzu "<Cypher>" [--json] [--limit N]\'\n'
    "tool: comp-kuzu\n"
    "mode: query\n"
    "status: canonical\n")
benign = route_back(BENIGN)
if benign:
    print("ROUTE_NEGATIVE_CONTROL=DEAD -- a plain served READ was scored as a route back %r; a"
          " predicate that matches everything is not a measurement" % (benign,))
    sys.exit(1)
print("ROUTE_NEGATIVE_CONTROL=FIRED -- a PLANTED live served read scored 0, so the predicate"
      " discriminates rather than convicts")

bad_total = len(offenders) + len(bad) + len(unscoped) + (len(RETIRED_IDS) - resolved)
sys.exit(1 if bad_total else 0)
PY
