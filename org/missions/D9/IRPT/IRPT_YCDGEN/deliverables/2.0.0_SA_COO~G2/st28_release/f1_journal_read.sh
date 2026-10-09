J=$(journalctl -u irpt-analysis-resident.service --since "2026-10-09 09:12:00" --no-pager -o short-iso 2>&1)
echo "journal lines since 09:12: $(echo "$J" | wc -l)"
echo "YCHARTS markers (vendor/session/transport): $(echo "$J" | grep -ciE 'ycharts|vendor|session_|transport|capture')"
echo "OPAL markers: $(echo "$J" | grep -ciE 'opal')"
echo "--- last 40 lines (closed codes only by construction) ---"
echo "$J" | tail -40 | cut -c1-220
echo "--- service ---"
systemctl show irpt-analysis-resident.service -p ActiveState -p SubState -p ExecMainStartTimestamp -p NRestarts
