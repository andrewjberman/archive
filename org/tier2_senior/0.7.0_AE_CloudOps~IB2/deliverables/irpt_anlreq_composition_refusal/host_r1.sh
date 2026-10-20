set -u
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-20 02:33:30' --until '2026-10-20 02:50:30' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW N first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1) scanned=$(wc -l < "$J") refused=$(grep -c COMPOSITION-REFUSED "$J" || true) retained=$(grep -c retained_for_retry "$J" || true) submissionrefused=$(grep -c SubmissionRefused "$J" || true)"
grep -o 'COMPOSITION-REFUSED step=[0-9]* error_class=[A-Za-z_]*' "$J" | sed 's/^/RAW C /'
rm -f "$J"
