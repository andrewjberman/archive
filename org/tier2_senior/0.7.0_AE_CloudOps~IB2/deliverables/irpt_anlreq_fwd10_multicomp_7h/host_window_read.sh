set -u
# READ ONLY: the resident journal of the 7h window by closed token (no payload, line heads cut to 200 chars), and the unit state
UNIT=irpt-analysis-resident.service
echo "RAW unit active=$(systemctl is-active $UNIT) restarts=$(systemctl show -p NRestarts --value $UNIT) since=$(systemctl show -p ActiveEnterTimestamp --value $UNIT)"
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-21 02:11:00' --until '2026-10-21 02:45:00' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW lines=$(wc -l < "$J") first=$(head -1 "$J" | cut -d' ' -f1) last=$(tail -1 "$J" | cut -d' ' -f1)"
awk '{ t="?"; if (match($0, /\]: [A-Z][A-Z0-9_]+/)) t=substr($0, RSTART+3, RLENGTH-3); c[t]++ } END { for (k in c) print "RAW token " k " count=" c[k] }' "$J" | sort
grep -E 'Traceback|Error|retained_for_retry|REFUSED|Refused|FAILED|LEASE|BUDGET|WINDOW' "$J" | cut -c1-200 | head -20
rm -f "$J"
echo "RAW END"
