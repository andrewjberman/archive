set -u
# TO-READ-RESIDENT-COMMENTARY R1, R2, R3 (READ ONLY, root via SSM). Counts, booleans and key names only. Writes nothing. Never prints a value or a journal line.
UNIT=irpt-analysis-resident.service
EXEC=$(systemctl show -p ExecStart --value "$UNIT" | tr ' ;' '\n\n' | grep -m1 'resident_main.py')
ROOT=${EXEC%/ycharts/generate/resident_main.py}
REL=$(basename "$ROOT")

# ---- R1: the release the RUNNING service loaded, and booleans on its INSTALLED producer and packager
SUMS=$(sha256sum "$ROOT/SHA256SUMS" | cut -c1-64)
PROD=$(find "$ROOT" -maxdepth 4 -name opal_producer.py -not -path '*/__pycache__/*' | head -1)
PACK=$(find "$ROOT" -maxdepth 4 -name opal_packager.py -not -path '*/__pycache__/*' | head -1)
yn() { [ "${1:-0}" -ge 1 ] && echo yes || echo no; }
c1=$([ -n "$PROD" ] && grep -c 'def produce_commentary_pdf' "$PROD" || echo 0)
c2=$([ -n "$PROD" ] && grep -c 'def package_logical_id' "$PROD" || echo 0)
c3=$([ -n "$PACK" ] && grep -c 'produce_commentary_pdf' "$PACK" || echo 0)
echo "RAW R1 release=$REL sums_sha256=$SUMS producer_found=$([ -n "$PROD" ] && echo yes || echo no) packager_found=$([ -n "$PACK" ] && echo yes || echo no) produce_commentary_pdf=$(yn "$c1") package_logical_id=$(yn "$c2") packager_calls_commentary_pdf=$(yn "$c3")"

# ---- R2: the journal of the last 7 days (counts of literal substrings only)
J=$(mktemp)
journalctl -u "$UNIT" --since '7 days ago' --no-pager -o short-iso -q > "$J" 2>/dev/null
N=$(wc -l < "$J")
FIRST=$(head -1 "$J" | cut -d' ' -f1)
LAST=$(tail -1 "$J" | cut -d' ' -f1)
cnt() { grep -c -F -- "$1" "$J" || true; }
CODES=$(grep -o 'PackagerRefused[^A-Z]*[A-Z][A-Z0-9_]\{3,\}' "$J" | sed 's/.*[^A-Z0-9_]\([A-Z][A-Z0-9_]\{3,\}\)$/\1/' | sort | uniq -c | awk '{printf "%s%s:%s", (n++?",":""), $2, $1}')
echo "RAW R2 window=$FIRST..$LAST scanned=$N skipped_not_requested=$(cnt 'IRPT_RESIDENT_READY_SIGNAL skipped=COMMENTARY_NOT_REQUESTED') skipped_no_ticket=$(cnt 'IRPT_RESIDENT_READY_SIGNAL skipped=NO_TICKET') send_failed=$(cnt 'ANALYSIS_READY_SEND_FAILED') packager_refused=$(cnt 'PackagerRefused') codes=${CODES:-none} d47252fe=$(cnt 'REQ-d47252fe74634d0c5cdd8067') d6231c01=$(cnt 'REQ-d6231c013ae90519c67d18e9')"
rm -f "$J"

# ---- R3: the service environment, KEY NAMES with a set/unset boolean (from the unit, its drop-ins and the live process); never a value
PID=$(systemctl show -p MainPID --value "$UNIT")
NAMES=$( { systemctl show -p Environment --value "$UNIT" | tr ' ' '\n' | grep '=' ; systemctl cat "$UNIT" | grep -E '^\s*Environment=' | sed 's/^\s*Environment=//' | tr ' ' '\n' | tr -d '"' | grep '=' ; tr '\0' '\n' < /proc/$PID/environ ; } | awk -F= 'NF>=1 && $1!="" {name=$1; val=substr($0, length(name)+2); if (!(name in seen) || (val!="" )) seen[name]=(val==""?"unset":"set")} END {for (k in seen) print k"="seen[k]}')
want=""
for k in IRPT_ANALYSIS_READY_QUEUE_URL; do v=$(echo "$NAMES" | grep -m1 "^$k=" | cut -d= -f2); want="${want}${k}=${v:-absent};"; done
cm=$(echo "$NAMES" | grep 'COMMENTARY_READY' | sed 's/^\([^=]*\)=\(.*\)$/\1=\2/' | sort)
if [ -n "$cm" ]; then for l in $cm; do want="${want}${l};"; done; else want="${want}COMMENTARY_READY*=absent;"; fi
echo "RAW R3 resident_env ${want}"
echo "RAW R3 env key names total: $(echo "$NAMES" | wc -l)"
