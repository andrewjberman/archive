set -u
# TO-READ-RESOLVE-LIVE R1 (READ ONLY, root via SSM): per-hour counts of closed literals in today's resident journal. No journal line is printed.
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '2026-10-19 00:00:00 UTC' --no-pager -o short-iso -q > "$J" 2>/dev/null
N=$(wc -l < "$J")
FIRST=$(head -1 "$J" | cut -d' ' -f1)
LAST=$(tail -1 "$J" | cut -d' ' -f1)
echo "RAW R1 window=$FIRST..$LAST scanned=$N"
awk '
{
  h = substr($1, 12, 2)
  if (index($0, "IRPT_RESIDENT_POLL handled=") > 0) { polls[h]++; tp++ }
  if (index($0, "IRPT_RESIDENT_POLL handled=0") > 0) { h0++ }
  if (index($0, "IRPT_RESIDENT_POLL retained_for_retry") > 0) { pr++ }
  if (index($0, "IRPT_RESIDENT_RESOLVE") > 0) {
    rs++; rh[h]++
    st = "?"; cd = "?"
    if (match($0, /state=[A-Z_]+/)) st = substr($0, RSTART + 6, RLENGTH - 6)
    if (match($0, /code=[A-Z][A-Z0-9_]*|code=-/)) cd = substr($0, RSTART + 5, RLENGTH - 5)
    pair[st "/" cd]++
  }
  if (index($0, "IRPT_RESIDENT_PACKAGE") > 0) { pk++ }
}
END {
  s = ""
  for (i = 0; i < 24; i++) { hh = sprintf("%02d", i); if (hh in polls) s = s (s == "" ? "" : ",") "h" hh ":" polls[hh] }
  print "RAW R1 polls=" (s == "" ? "none" : s) " total_polls=" tp + 0 " handled0=" h0 + 0 " poll_retained=" pr + 0 " resolve=" rs + 0 " package=" pk + 0
  p = ""
  for (k in pair) p = p (p == "" ? "" : ",") k ":" pair[k]
  print "RAW R1 resolve_pairs=" (p == "" ? "none" : p)
  r = ""
  for (i = 0; i < 24; i++) { hh = sprintf("%02d", i); if (hh in rh) r = r (r == "" ? "" : ",") "h" hh ":" rh[hh] }
  print "RAW R1 resolve_by_hour=" (r == "" ? "none" : r)
}' "$J"
rm -f "$J"
