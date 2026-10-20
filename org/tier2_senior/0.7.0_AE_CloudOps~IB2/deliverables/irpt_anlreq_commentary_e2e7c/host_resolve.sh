set -u
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-20 18:56:41' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW RES first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1) scanned=$(wc -l < "$J") resolve_lines=$(grep -c RESOLVE "$J" || true) state_lines=$(grep -c 'IRPT_RESIDENT_RESOLVE state=' "$J" || true)"
rm -f "$J"
