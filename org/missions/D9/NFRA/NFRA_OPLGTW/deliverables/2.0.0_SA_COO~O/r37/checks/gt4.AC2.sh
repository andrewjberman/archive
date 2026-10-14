#!/usr/bin/env bash
# OPLGTW gt4 AC2 (round-37 G1-TYPED, FWD-22): research, filing analysis and peers/scores for ASML against the REAL bucket.
# The probe runs the tool function itself against the REAL bucket with the box's credentials and an Opal stand-in
# principal, then re-derives the answer independently (gt_probe_lib: boto3 + pyarrow, no tool under test).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
CK="$(dirname "$0")"; CK="$(cd "$CK" && pwd)"
res=$(CKDIR="$(native "$CK")" timeout 110 python - <<'EOF'
import os, sys
sys.path.insert(0, os.environ["CKDIR"])
import gt_probe_lib as P
ok = False
try:
    c = P.setup()

    from app import harvest_research as h
    key = P.asml_key(c)
    r = h.harvest_get_research(key)
    f = h.harvest_get_filing_analysis(key)
    p = h.harvest_get_peers_and_scores(key)
    def empty(d):
        body = {k: v for k, v in d.items() if k not in ("as_of", "source_keys", "denominator", "absent_reason", "truncated", "projected_to_bytes")}
        return not any(body.values())
    nonempty = sum(1 for d in (r, f, p) if not empty(d))
    explained = all((not empty(d)) or bool(d.get("absent_reason")) for d in (r, f, p))
    print("ASML: research %s, filing analysis %s, peers/scores %s; non-empty %d of 3 (want >= 2); every empty one names why %s; envelope on all three %s"
          % ("body" if not empty(r) else "empty", "body" if not empty(f) else "empty", "body" if not empty(p) else "empty", nonempty, explained, all(P.envelope_ok(x) for x in (r, f, p))))
    ok = bool(key) and nonempty >= 2 and explained and all(P.envelope_ok(x) for x in (r, f, p))

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
