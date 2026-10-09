journalctl -u irpt-analysis-resident.service --since "2026-10-09 09:12:00" --until "2026-10-09 09:28:40" --no-pager -o short-iso 2>&1 | grep -v 'POLL handled=0' | cut -c1-260
