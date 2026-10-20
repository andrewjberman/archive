set -u
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-19 23:09:30' --until '2026-10-19 23:12:00' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW N first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1) scanned=$(wc -l < "$J") resolve=$(grep -c IRPT_RESIDENT_RESOLVE "$J" || true) retained=$(grep -c RETAINED "$J" || true) nc=$(grep -c NEEDS_CORRECTION "$J" || true) tnf=$(grep -c TICKER_NOT_FOUND "$J" || true) unres=$(grep -c UNRESOLVED "$J" || true) kat=$(grep -c KEPT_AS_TYPED "$J" || true)"
grep IRPT_RESIDENT_RESOLVE "$J" | awk '{ s="?"; c="?"; if (match($0, /state=[A-Z_]+/)) s=substr($0, RSTART+6, RLENGTH-6); if (match($0, /code=[A-Z][A-Z0-9_]*|code=-/)) c=substr($0, RSTART+5, RLENGTH-5); print "RAW P " s "/" c }' | sort | uniq -c | awk '{print "RAW PAIR " $4 " " $1}'
rm -f "$J"
