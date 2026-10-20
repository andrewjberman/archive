#!/usr/bin/env bash
# OPLGTW OG-nf-1 AC1 (round 47, H2 / Z-S414): news_for_security (app/news_typed.py) no longer answers 0 mentions with no reason for an active name.
# API seam fixed by the order: a module function news_typed._security_name(ticker_or_key) -> Optional[str] (the company name for a ticker, or None); the fallback text search runs for the
# ticker text AND the name, in that order, through _search_core; the body carries fallback_terms (list), fallback_name_absent_reason (str or None), mention_index_lag_days (int or None),
# and each fallback row carries match_term (the term that found it); a zero answer's absent_reason names the mention index's newest partition date and every term searched.
# Probe: the index read, the name resolver, the articles table and the search core are replaced by fakes; today is 2026-10-16 and the index's newest partition is 2026-10-08.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && MOCK_GRAPH=1 timeout 110 python3 -I - <<'EOF'
import sys, datetime as dt
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import news_typed as nt
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
KEY = nt.MENTION_PREFIX + "date=2026-10-08/part-0.parquet"
state = {"rows": [], "by_term": {}, "searched": [], "name": "Nvidia"}
nt.admit_scope = lambda *a, **k: None
nt.ts.newest_part = lambda scope, prefix: KEY
nt.ts.read_parquet = lambda scope, key, columns=None: (list(state["rows"]), len(state["rows"]), 0)
nt.ts.audit_ok = lambda *a, **k: None
nt._today = lambda: dt.date(2026, 10, 16)
nt._table = lambda which: "articles_tbl"
nt._security_name = lambda ticker_or_key: state["name"] if hasattr(nt, "_security_name") else None
def core(table, d0, d1, text, source, label, limit):
    state["searched"].append(text)
    return {"returned": [dict(r) for r in state["by_term"].get(text, [])]}
nt._search_core = core
def art(n):
    return {"published": "2026-10-1%d" % n, "source": "s", "title": "Nvidia story %d" % n, "url": "https://example.invalid/%d" % n}
def run():
    state["searched"] = []
    return nt.news_for_security(ticker="NVDA", window_days=7)
try:
    if not hasattr(nt, "_security_name"):
        say("seam: news_typed._security_name exists", False)
    state.update(rows=[], by_term={"NVDA": [], "Nvidia": [art(1), art(2)]}, name="Nvidia")
    r = run()
    say("name search found 2 rows although the ticker text found none", len(r.get("fallback") or []) == 2 and all(x.get("match_term") == "Nvidia" for x in r.get("fallback") or []), "fallback %s" % len(r.get("fallback") or []))
    say("fallback_terms is the ticker then the name", r.get("fallback_terms") == ["NVDA", "Nvidia"], "terms %r searched %r" % (r.get("fallback_terms"), state["searched"]))
    say("rows found: no absent_reason", r.get("absent_reason") is None, "absent_reason %r" % (r.get("absent_reason"),))
    state.update(by_term={"NVDA": [art(3)], "Nvidia": [art(3), art(4)]})
    r = run()
    say("a row found by both terms is listed once", len(r.get("fallback") or []) == 2, "fallback %s" % len(r.get("fallback") or []))
    state.update(by_term={"NVDA": [], "Nvidia": []})
    r = run()
    reason = r.get("absent_reason") or ""
    say("zero answer: absent_reason names the partition date and every term", "2026-10-08" in reason and "NVDA" in reason and "Nvidia" in reason, "reason %r" % reason[:160])
    say("zero answer: mention_index_lag_days is 8, fallback empty", r.get("mention_index_lag_days") == 8 and r.get("fallback") == [], "lag %r" % (r.get("mention_index_lag_days"),))
    state.update(name=None, by_term={"NVDA": [art(5)]})
    r = run()
    say("name unresolved: terms are the ticker only, the reason is stated", r.get("fallback_terms") == ["NVDA"] and isinstance(r.get("fallback_name_absent_reason"), str) and r["fallback_name_absent_reason"], "terms %r reason %r" % (r.get("fallback_terms"), r.get("fallback_name_absent_reason")))
    mention = {"security_key": "NVDA_US_Equity", "published_utc": "2026-10-15T12:00:00Z", "publisher": "p", "title": "t", "url": "u", "signal_tier": 1, "mention_count": 1,
               "mention_in_title": True, "sentiment_finbert_label": "positive", "sentiment_finbert_score": 0.9}
    state.update(rows=[mention], name="Nvidia", by_term={"NVDA": [], "Nvidia": []})
    r = run()
    say("control: an index mention is still served, absent_reason None", len(r.get("mentions") or []) == 1 and r.get("absent_reason") is None, "mentions %s" % len(r.get("mentions") or []))
except Exception as exc:
    print("probe raised %s: %s" % (type(exc).__name__, str(exc)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
