set -u
# TO-READ-RESOLVE-LIVE R1 extension (READ ONLY): the UTC minute of each IRPT_RESIDENT_RESOLVE and poll retained_for_retry line today, with the closed state/code words only.
UNIT=irpt-analysis-resident.service
journalctl -u "$UNIT" --since '2026-10-19 00:00:00 UTC' --no-pager -o short-iso -q 2>/dev/null | awk '
index($0, "IRPT_RESIDENT_RESOLVE") > 0 {
  st = "?"; cd = "?"
  if (match($0, /state=[A-Z_]+/)) st = substr($0, RSTART + 6, RLENGTH - 6)
  if (match($0, /code=[A-Z][A-Z0-9_]*|code=-/)) cd = substr($0, RSTART + 5, RLENGTH - 5)
  print "RAW RESOLVE " substr($1, 1, 19) "Z " st "/" cd
}
index($0, "IRPT_RESIDENT_POLL retained_for_retry") > 0 {
  cl = "?"; cd = "?"
  if (match($0, /class=[A-Za-z_]+/)) cl = substr($0, RSTART + 6, RLENGTH - 6)
  if (match($0, /code=[A-Z][A-Z0-9_]*|code=-/)) cd = substr($0, RSTART + 5, RLENGTH - 5)
  print "RAW POLLRETAINED " substr($1, 1, 19) "Z class=" cl " code=" cd
}'
