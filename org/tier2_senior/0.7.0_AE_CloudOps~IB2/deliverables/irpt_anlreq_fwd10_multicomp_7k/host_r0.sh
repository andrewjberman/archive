set -u
# TO-RUN-COMMENTARY-E2E R0 host reads (READ ONLY, root via SSM): the running release root and the last YCharts call line time. Tokens and timestamps only; no journal line is printed.
UNIT=irpt-analysis-resident.service
EXEC=$(systemctl show -p ExecStart --value "$UNIT" | tr ' ;' '\n\n' | grep -m1 'resident_main.py')
ROOT=${EXEC%/ycharts/generate/resident_main.py}
echo "RAW R0 resident_root=$(basename "$ROOT") active=$(systemctl is-active "$UNIT")"
J=$(mktemp)
journalctl -u "$UNIT" --since '9 days ago' --no-pager -o short-iso -q > "$J" 2>/dev/null
echo "RAW R0 journal_lines_9d=$(wc -l < "$J")"
# distinct log tokens that mention ycharts (token = the first UPPER_SNAKE word after the process id), with count and the last UTC time
grep -i 'ycharts' "$J" | awk '{ t="?"; if (match($0, /\]: [A-Z][A-Z0-9_]+/)) t=substr($0, RSTART+3, RLENGTH-3); c[t]++; last[t]=substr($1,1,19) } END { for (k in c) print "RAW R0 ycharts_token " k " count=" c[k] " last=" last[k] "Z" }' | sort | head -20
rm -f "$J"
