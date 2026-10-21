set -u
UNIT=irpt-analysis-resident.service
SINCE='2026-10-21 14:43:44'
journalctl -u "$UNIT" --since "$SINCE" --no-pager -o short-iso -q 2>/dev/null | grep -E 'IRPT_RESIDENT_PACKAGE (outcome=|retained_for_retry)' | awk '{ts=substr($1,1,19); l=$0; m=""; if (match(l, /outcome=[A-Z_]+/)) m=substr(l,RSTART,RLENGTH); else if (match(l, /retained_for_retry class=[A-Za-z_]+ code=([A-Z][A-Z0-9_]*|-)/)) m=substr(l,RSTART,RLENGTH); if (m!="") print "RAW P4 " ts "Z " m}'
