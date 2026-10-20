set -u
J=$(mktemp)
journalctl -u irpt-analysis-resident.service --since '2026-10-20 08:02:20' --until '2026-10-20 08:06:00' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW N first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1) scanned=$(wc -l < "$J")"
grep -E 'IRPT_RESIDENT_PACKAGE|PACKAGER|HOP_FAILURE|retained_for_retry|ClientError|Traceback' "$J" | cut -c1-600 | sed 's/^/RAW L /'
rm -f "$J"
