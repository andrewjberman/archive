set -u
# READ ONLY: the resident journal lines of this run's window that name the packager outcome or the retention refusal (no payload, cut to 300 chars)
UNIT=irpt-analysis-resident.service
journalctl -u "$UNIT" --since '2026-10-20 23:35:47' --no-pager -o short-iso -q 2>/dev/null | grep -E 'IRPT_RESIDENT_PACKAGE|Retention|RETENTION|retained_for_retry|Traceback|Error' | cut -c1-300 | head -40
echo "RAW END"
