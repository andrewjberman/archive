J=$(journalctl -u irpt-analysis-resident.service --since "2026-10-09 12:00:00" --no-pager -o short-iso 2>&1)
echo "journal lines since 12:00: $(echo "$J" | wc -l)"
echo "YCHARTS markers (vendor/session/transport/capture): $(echo "$J" | grep -ciE 'ycharts_vendor|vendor|session_|transport|capture')"
echo "--- non-idle lines ---"
echo "$J" | grep -v 'POLL handled=0' | tail -30 | cut -c1-240
