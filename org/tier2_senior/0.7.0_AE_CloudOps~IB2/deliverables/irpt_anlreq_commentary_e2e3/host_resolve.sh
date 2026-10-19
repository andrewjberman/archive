set -u
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-19 14:31:14' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW RES first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1) scanned=$(wc -l < "$J") resolve_lines=$(grep -c RESOLVE "$J" || true)"
rm -f "$J"
