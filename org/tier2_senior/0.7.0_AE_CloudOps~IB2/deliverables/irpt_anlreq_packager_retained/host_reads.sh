set -u
# TO-READ-PACKAGER-RETAINED R1 (READ ONLY, root via SSM). Prints only the closed retained_for_retry fields (timestamp to the minute, class, code); everything else is counted.
UNIT=irpt-analysis-resident.service
J=$(mktemp)
journalctl -u "$UNIT" --since '8 days ago' --no-pager -o short-iso -q > "$J" 2>/dev/null
N=$(wc -l < "$J")
FIRST=$(head -1 "$J" | cut -d' ' -f1)
LAST=$(tail -1 "$J" | cut -d' ' -f1)
P=$(grep -c -E 'python3[.0-9]*\[[0-9]+\]: IRPT_RESIDENT_PACKAGE retained_for_retry' "$J" || true)
Q=$(grep -c -E 'python3[.0-9]*\[[0-9]+\]: IRPT_RESIDENT_POLL retained_for_retry' "$J" || true)
echo "RAW R1 window=$FIRST..$LAST scanned=$N package_retained=$P poll_retained=$Q"
L=$(mktemp)
grep -E 'python3[.0-9]*\[[0-9]+\]: IRPT_RESIDENT_PACKAGE retained_for_retry' "$J" | awk '
{
  ts=substr($1,1,16)
  cls="?"; cod="?"
  if (match($0, /class=[A-Za-z_]+/)) cls=substr($0, RSTART+6, RLENGTH-6)
  if (match($0, /code=([A-Z][A-Z0-9_]*|-)/)) cod=substr($0, RSTART+5, RLENGTH-5)
  print "RAW R1L " ts "Z class=" cls " code=" cod
}' > "$L"
T=$(wc -l < "$L")
if [ "$T" -le 40 ]; then cat "$L"; else head -20 "$L"; echo "RAW R1L-NOTE total=$T printed first 20 and last 20"; tail -20 "$L"; fi
rm -f "$J" "$L"
