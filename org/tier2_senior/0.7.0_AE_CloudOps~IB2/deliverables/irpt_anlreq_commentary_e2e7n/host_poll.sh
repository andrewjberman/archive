set -u
UNIT=irpt-analysis-resident.service
SINCE='2026-10-21 15:04:36'
journalctl -u "$UNIT" --since "$SINCE" --no-pager -o short-iso -q 2>/dev/null | grep -E 'IRPT_RESIDENT_POLL retained_for_retry' | sed -E 's/^([0-9T:-]{19}).*retained_for_retry /RAW PR \1Z /' | cut -c1-220
