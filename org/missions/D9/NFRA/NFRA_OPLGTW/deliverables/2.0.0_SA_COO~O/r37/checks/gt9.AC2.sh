#!/usr/bin/env bash
# OPLGTW OG-gt-9 AC2 (round-37 G1-FIX, FWD-22): the REAL bucket. harvest_search_articles for ASML (its newest article is the anchor, so
# the window holds data whatever today's date) answers inside 40 s BOTH with no window (limit 5; the unpruned probe took 46.8 s) and
# with the 7 days ending at the newest article (15.9 s unpruned); the windowed answer carries sentiment for at least one article, the
# envelope is whole, and the denominator names partitions read of partitions total. ALB idle timeout is 60 s.
# (The pruning premise -- no sentiment row predates its article's fetch -- is measured by the worker and reported as a count.)
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
CK="$(dirname "$0")"; CK="$(cd "$CK" && pwd)"
res=$(CKDIR="$(native "$CK")" timeout 115 python - <<'EOF'
import os, sys, time
sys.path.insert(0, os.environ["CKDIR"])
import gt_probe_lib as P
ok = False
try:
    c = P.setup()
    from app import harvest_press as h
    import datetime as dt
    key = P.asml_key(c)
    t0 = time.time()
    s0 = h.harvest_search_articles(key, limit=5)
    el0 = time.time() - t0
    a0 = s0.get("articles") or []
    newest = str(a0[0]["published_utc"])[:10] if a0 else None
    frm = (dt.date.fromisoformat(newest) - dt.timedelta(days=6)).isoformat() if newest else None
    t0 = time.time()
    s = h.harvest_search_articles(key, from_day=frm, to_day=newest, limit=20) if newest else {}
    el = time.time() - t0
    arts = s.get("articles") or []
    scored = [a for a in arts if a.get("sentiment_label") is not None]
    den = str(s.get("denominator"))
    print("search ASML: no window %d article(s) in %.1f s (want < 50); 7d ending at the newest (%s) %d article(s), %d with a sentiment label, in %.1f s (want < 40); denominator names partitions read %s; envelope whole %s"
          % (len(a0), el0, newest, len(arts), len(scored), el, "partitions" in den, P.envelope_ok(s0) and P.envelope_ok(s)))
    ok = bool(key) and bool(a0) and el0 < 50 and len(arts) >= 1 and len(scored) >= 1 and el < 40 and "partitions" in den and P.envelope_ok(s0) and P.envelope_ok(s)
except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
