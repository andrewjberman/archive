#!/usr/bin/env bash
# OPLGTW nw1 AC2 (round-37 G1-TYPED, FWD-22): the five news tools called for real against the live DynamoDB tables and the portal singletons.
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

    import os
    os.environ["NEWS_ARTICLES_TABLE"] = "opal-news-articles"
    os.environ["NEWS_TRENDING_TABLE"] = "opal-news-trending-daily"
    os.environ["NEWS_KEYWORD_TABLE"] = "opal-keyword-intelligence"
    import datetime as dt
    from types import SimpleNamespace
    import boto3
    import app.harvest_read as hr
    from app import news_typed as h
    d = boto3.client("dynamodb", region_name="us-east-1")
    def cnt(table, key_name, key_val, idx=None):
        kw = {"TableName": table, "Select": "COUNT", "KeyConditionExpression": "#k = :v", "ExpressionAttributeNames": {"#k": key_name}, "ExpressionAttributeValues": {":v": {"S": key_val}}}
        if idx:
            kw["IndexName"] = idx
        n = 0
        while True:
            r = d.query(**kw); n += r["Count"]
            if "LastEvaluatedKey" not in r:
                return n
            kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    # a recent weekday with articles: walk back from today
    day = None
    for back in range(1, 8):
        cand = (dt.date.today() - dt.timedelta(days=back)).isoformat()
        if cnt("opal-news-articles", "article_date", cand) > 0:
            day = cand; break
    s = h.news_search_articles(date_from=day, date_to=day, limit=5)
    pdc = (s.get("per_day_counts") or {})
    tool_n = pdc.get(day) if isinstance(pdc, dict) else None
    indep_n = cnt("opal-news-articles", "article_date", day) if day else None
    arts = s.get("articles") or []
    long_ref = h.news_search_articles(date_from="2026-01-01", date_to="2026-03-01")
    t = h.news_trending_topics()
    tdate = (t.get("date") or (t.get("topics") or [{}])[0].get("date") or "")
    topics = t.get("topics") or []
    m = h.news_market_mood()
    k = h.news_keyword_intelligence(date=day) if day else {}
    nk = h.news_keyword_intelligence()
    sec = h.news_for_security(ticker="ASML")
    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    non_opal = all((fn() or {}).get("code") in ("typed_opal_only", "harvest_opal_only") for fn in (lambda: h.news_search_articles(date_from=day, date_to=day), h.news_market_mood))
    cap_ok = long_ref.get("code") == "harvest_bad_argument"
    neither_ok = nk.get("code") == "harvest_bad_argument"
    shape = all(P.envelope_ok(x) for x in (s, t, m, sec))
    mood_ok = bool(m.get("source_keys")) and len(m.get("source_keys")) == 2
    sec_labels = all(r.get("match") == "text" for r in (sec.get("fallback") or sec.get("text_matches") or []))
    print("news: day %s count tool %s vs independent %s; articles %d (want 1-5); 15+ day window refused %s; trending topics %d (want >= 1); mood reads %s keys; neither-keyword refused %s; for_security answered %s with fallback rows labelled text %s; envelope on all %s; non-Opal refused %s"
          % (day, tool_n, indep_n, len(arts), cap_ok, len(topics), len(m.get("source_keys") or []), neither_ok, isinstance(sec, dict) and bool(sec), sec_labels, shape, non_opal))
    ok = bool(day) and tool_n == indep_n and 1 <= len(arts) <= 5 and cap_ok and len(topics) >= 1 and mood_ok and neither_ok and shape and non_opal and isinstance(sec, dict) and sec_labels

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
