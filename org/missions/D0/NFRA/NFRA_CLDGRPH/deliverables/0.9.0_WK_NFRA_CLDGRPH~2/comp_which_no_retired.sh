#!/bin/bash
# E1-AC2 -- DOES A REFRESH PHRASING STILL ROUTE TO A RETIRED ENTRY?
#
# THE THREE PHRASINGS ARE NOT CHOSEN, THEY ARE INHERITED. Each is the vocabulary the manifest
# ITSELF used to route to the two refresh entries, quoted from the entries' own `notes:` and
# `use_case:` before this order rewrote them (graph-call-manifest.yaml @de466829e0 :220/:228/:234):
#   "my graph is behind"                                     (cloud.refresh.incremental)
#   "full rebuild / ground-truth reset of the local projection" (cloud.refresh.full)
#   "MSTR startup graph warm"                                (cloud.refresh.full)
# Asking comp-which a phrasing invented for the test would measure the test.
#
# WHAT IS SCORED: the WHOLE answer, stdout and stderr together, for four tokens -- `cloud.refresh`,
# `--mode`, `--db-path`, `kuzu_nessie_db`. Any one of them in the answer is a route back and the
# phrasing FAILS. The answer is printed VERBATIM under each phrasing, so a reader grades the same
# bytes the score did.
#
# THE CONTROL EXISTS BECAUSE A SILENT comp-which SCORES A PERFECT ZERO. A router that crashed,
# hung, or answered nothing contains none of the four tokens and would read as three clean routes.
# So a FOURTH phrasing -- one with no refresh vocabulary at all -- is asked, and the control fires
# only when comp-which (a) emitted a MATCHES block, (b) named a rank-1 tool, and (c) that tool
# RESOLVES through the manifest's own tools_index to a LIVE entry id, which is printed.
#
# WHY THE ID IS RESOLVED RATHER THAN READ OFF THE ANSWER: comp-which's human answer names a TOOL
# and a CALL and never prints a manifest entry id (measured 2026-09-09 across five phrasings). The
# id therefore comes from the manifest's own tools_index row for the rank-1 tool, and the entry it
# names is checked to be status-canonical -- resolution through the registry, not a guess.
#
# NOTE ON THE INSTRUMENT, RECORDED BECAUSE IT LIMITS THE READING: comp-which prints
# `ALARM: POTION semantic embedder unavailable -> falling back to lexical relevance` on this box
# (a vendored-tokenizer hash mismatch, FAIL-CLOSED, pre-existing at HEAD and untouched by this
# order). Routing here is therefore LEXICAL. The curated-route table this criterion is about is
# matched lexically in both modes, so the reading holds; a semantic run is not re-measured here.
#
# Exit: 0 = three clean routes and the control fired; 1 = a retired route or a dead control;
#       2 = BLOCKED (comp-which or the manifest could not be run/read).
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2

OUT=".scratch/e1ac2"
rm -rf "$OUT" && mkdir -p "$OUT" || exit 2

P1="my graph is behind"
P2="full rebuild / ground-truth reset of the local projection"
P3="MSTR startup graph warm"
CTRL="what breaks if I change this bucket"

i=0
for q in "$P1" "$P2" "$P3" "$CTRL"; do
  i=$((i + 1))
  timeout 120 python .tools/comp-which "$q" > "$OUT/a$i.txt" 2>&1
  rc=$?
  echo "$rc" > "$OUT/rc$i.txt"
  if [ "$rc" -eq 124 ]; then
    echo "BLOCKED: comp-which timed out (rc 124) on phrasing $i: $q"
    exit 2
  fi
done

python - <<'PY'
import re
import sys

try:
    import yaml
except ImportError as exc:
    print("BLOCKED: PyYAML unavailable (%s)" % exc)
    sys.exit(2)

PHRASINGS = [
    ("my graph is behind", "cloud.refresh.incremental use_case, manifest @de466829e0"),
    ("full rebuild / ground-truth reset of the local projection",
     "cloud.refresh.full use_case, manifest @de466829e0"),
    ("MSTR startup graph warm", "cloud.refresh.full notes, manifest @de466829e0"),
]
CONTROL = "what breaks if I change this bucket"
RETIRED_TOKENS = ("cloud.refresh", "--mode", "--db-path", "kuzu_nessie_db")

with open("org/modules/graph/graph-call-manifest.yaml", encoding="utf-8") as fh:
    DOC = yaml.safe_load(fh)
LIVE = {str(e.get("id")): e for e in (DOC.get("entries") or [])
        if isinstance(e, dict) and str(e.get("status") or "") != "retired"}
TOOLS_INDEX = DOC.get("tools_index") or {}


def answer(i):
    with open(".scratch/e1ac2/a%d.txt" % i, encoding="utf-8", errors="replace") as fh:
        return fh.read()


print("RETIRED_TOKEN_SET=%s  (any one of these in an answer is a route back)"
      % ", ".join(repr(t) for t in RETIRED_TOKENS))

bad = 0
for i, (q, provenance) in enumerate(PHRASINGS, start=1):
    text = answer(i)
    hits = [t for t in RETIRED_TOKENS if t in text]
    verdict = "ROUTES BACK: %s" % ", ".join(hits) if hits else "clean"
    if hits:
        bad += 1
    print("\n--- PHRASING %d (%s)\n    %r\n    %s" % (i, provenance, q, verdict))
    for line in text.splitlines():
        print("      | %s" % line)

print("\nRETIRED_ROUTES=%d of %d" % (bad, len(PHRASINGS)))

# --- the control ---------------------------------------------------------------------------------
ctext = answer(4)
print("\n--- CONTROL PHRASING (no refresh vocabulary)\n    %r" % CONTROL)
for line in ctext.splitlines():
    print("      | %s" % line)

m = re.search(r"^\s*1\.\s+score\s+[0-9.]+\s+(\S+)", ctext, re.M)
rank1 = m.group(1) if m else None
has_matches = "MATCHES (top" in ctext
entry_ids = [str(e) for e in ((TOOLS_INDEX.get(rank1) or {}).get("entries") or [])] if rank1 else []
live_ids = [e for e in entry_ids if e in LIVE]

if not (has_matches and rank1 and live_ids):
    print("WHICH_PROBE_CONTROL=DEAD -- matches_block=%s rank1=%r live_entry_ids=%r. A comp-which"
          " that answered nothing contains none of the four tokens either, so the three zeros"
          " above would be a false clean." % (has_matches, rank1, live_ids))
    sys.exit(1)
print("WHICH_PROBE_CONTROL=FIRED -- comp-which answered, ranked %r at rank 1, and that tool"
      " resolves through the manifest's own tools_index to LIVE entry id(s) %s (status %s). The"
      " router ran and can answer, so the zeros above are measurements."
      % (rank1, ", ".join(live_ids), LIVE[live_ids[0]].get("status")))

sys.exit(1 if bad else 0)
PY
