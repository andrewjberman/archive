set -u
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-08 00:00:00' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW J first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1) scanned=$(wc -l < "$J") hits=$(grep -c 'REQ-8966d24ffefa1c28269ef26c' "$J" || true)"
rm -f "$J"
