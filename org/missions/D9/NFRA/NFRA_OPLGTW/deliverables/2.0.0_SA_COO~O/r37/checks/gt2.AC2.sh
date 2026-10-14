#!/usr/bin/env bash
# OPLGTW gt2 AC2 (round-37 G1-TYPED, FWD-22): chatter, search and article against the REAL bucket, with the newest-part control.
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

    from app import harvest_press as h
    import datetime as dt
    key = P.asml_key(c)
    today = dt.date.today(); frm = (today - dt.timedelta(days=30)).isoformat(); to = today.isoformat()
    ch = h.harvest_get_chatter(key, frm, to)
    daily = ch.get("daily") or []
    newest = P.newest_part(c, "amgt/harvest/gold/chatter_daily/")
    src = [k for k in (ch.get("source_keys") or []) if "chatter_daily" in k]
    tbl = P.read_table(c, newest, ["security_key", "day", "articles_total"]).to_pylist()
    want = sum((r["articles_total"] or 0) for r in tbl if r["security_key"] == key and frm <= str(r["day"]) <= to)
    got = sum((r.get("articles_total") or 0) for r in daily)
    st = all("data_status" in r for r in daily)
    s = h.harvest_search_articles(key, limit=5)
    arts = s.get("articles") or []
    a = h.harvest_get_article(arts[0]["article_key"], arts[0]["publisher"]) if arts else {}
    print("chatter: days %d, data_status on every day %s; source chatter_daily keys %s, equal to the independent newest part %s; sum articles_total tool %d vs independent %d; search %d article(s) (want 1-5); article text withheld by default %s"
          % (len(daily), st, len(src), src == [newest], got, want, len(arts), bool(a) and "text" not in a and "body_blocks" not in a))
    ok = bool(key) and len(daily) <= 31 and st and src == [newest] and got == want and 1 <= len(arts) <= 5 and bool(a) and "text" not in a and "body_blocks" not in a and all(P.envelope_ok(x) for x in (ch, s, a))

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
