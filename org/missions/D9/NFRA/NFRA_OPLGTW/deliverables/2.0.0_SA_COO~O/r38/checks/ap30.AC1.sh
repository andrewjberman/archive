#!/usr/bin/env bash
# OPLGTW OG-ap-30 AC1 (round 38, reverse the browser side effect of OG-mg-1's email_deny records, PHASE A, before any write):
#  - the ask NEVER_WIDEN_ASK_OG-ap-30.md exists with three half headings (CTO, COO, CVO), names exactly andrew@opalinvest.com and opalbloomberg@opalinvest.com as the write set, names alyssa@opalinvest.com only as UNTOUCHED, and carries no other e-mail address;
#  - the before-record DENY_BEFORE_OG-ap-30.json lists write_set exactly [andrew, opalbloomberg], writes 2, one sha256 per item for all three labels, email_deny_total_before 3;
#  - the LIVE table (strongly consistent) still holds all three records active, and the live total equals the record's (the pre-act state).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="${AP30_W_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1}"
ASK="$W/NEVER_WIDEN_ASK_OG-ap-30.md"; REC="$W/DENY_BEFORE_OG-ap-30.json"
[ -f "$ASK" ] && [ -f "$REC" ] || { echo "the ask or DENY_BEFORE_OG-ap-30.json is absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$ASK")" "$(native "$REC")" <<'PYEOF'
import json, re, sys
ask = open(sys.argv[1], encoding="utf-8").read()
rec = json.load(open(sys.argv[2], encoding="utf-8"))
halves = all(re.search(r"(?mi)^#+ .*%s" % h, ask) for h in ("CTO", "COO", "CVO"))
emails = set(e.lower() for e in re.findall(r"[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", ask))
allowed = {"andrew@opalinvest.com", "opalbloomberg@opalinvest.com", "alyssa@opalinvest.com"}
other = sorted(emails - allowed)
names = {"andrew@opalinvest.com", "opalbloomberg@opalinvest.com"} <= emails
untouched = bool(re.search(r"(?is)alyssa@opalinvest\.com.{0,200}untouched|untouched.{0,200}alyssa@opalinvest\.com", ask))
ws = rec.get("write_set")
items = rec.get("items") or {}
shas = all(isinstance(items.get(k, {}).get("sha256"), str) and len(items[k]["sha256"]) == 64 for k in ("andrew", "opalbloomberg", "alyssa"))
ok = (halves and names and untouched and not other and ws == ["andrew", "opalbloomberg"] and rec.get("writes") == 2
      and shas and rec.get("email_deny_total_before") == 3)
print("ask: three half headings %s; names the two write-set e-mails %s; alyssa named as untouched %s; other e-mail addresses %d (want 0)" % (
      "yes" if halves else "no", "yes" if names else "no", "yes" if untouched else "no", len(other)))
print("record: write_set %s (want [andrew, opalbloomberg]); writes %s (want 2); item sha256 for all three %s; email_deny_total_before %s (want 3)" % (
      ws, rec.get("writes"), "yes" if shas else "no", rec.get("email_deny_total_before")))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
live="${AP30_LIVE_OVERRIDE:-$(timeout 100 python "$(native "$(dirname "$0")/_deny.py")" live | tr -d '\r')}"
want="live_read=ok andrew_present=yes andrew_active=yes opalbloomberg_present=yes opalbloomberg_active=yes alyssa_present=yes alyssa_active=yes email_deny_total=3"
printf '%s\n' "$res" | sed '$d'
echo "live table now: $live"
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && [ "$live" = "$want" ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
