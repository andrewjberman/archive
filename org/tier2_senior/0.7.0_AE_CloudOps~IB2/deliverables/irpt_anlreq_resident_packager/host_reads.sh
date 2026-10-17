set -u
# TO-READ-RESIDENT-PACKAGER R1 and R2 (READ ONLY, root via SSM). Names, booleans and counts only. Writes nothing. Never prints a binding value, a queue URL or a journal line.
UNIT=irpt-analysis-resident.service
EXEC=$(systemctl show -p ExecStart --value "$UNIT" | tr ' ;' '\n\n' | grep -m1 'resident_main.py')
ROOT=${EXEC%/ycharts/generate/resident_main.py}
BF=$(find "$ROOT" -maxdepth 4 -name resident_bindings.json -not -path '*/__pycache__/*' | head -1)
RI=$(find "$ROOT" -maxdepth 4 -name resident_installed.py -not -path '*/__pycache__/*' | head -1)
echo "RAW R1 bindings_found=$([ -n "$BF" ] && echo yes || echo no) beside_resident_installed=$([ -n "$BF" ] && [ "$(dirname "$BF")" = "$(dirname "$RI")" ] && echo yes || echo no)"
if [ -n "$BF" ]; then
python3.12 - "$BF" <<'PYEOF'
import json, sys
doc = json.load(open(sys.argv[1], encoding="utf-8"))
def st(k):
    if k not in doc:
        return "absent"
    v = doc[k]
    return "set" if (v not in (None, "", {}, [])) else "unset"
def last(u):
    return str(u).rstrip("/").rsplit("/", 1)[-1] if isinstance(u, str) else ""
cm = "yes" if last(doc.get("commentary_ready_queue_url")) == "outlook-global-commentary-draft-commentary-ready-queue" else "no"
am = "yes" if last(doc.get("analysis_ready_queue_url")) == "outlook-global-commentary-draft-analysis-ready-queue" else "no"
print("RAW R1 keys=%s analysis_ready_queue_url=%s commentary_ready_queue_url=%s packager=%s commentary_queue_name_match=%s analysis_queue_name_match=%s" % (
    ",".join(sorted(doc)), st("analysis_ready_queue_url"), st("commentary_ready_queue_url"), st("packager"), cm, am))
PYEOF
fi

J=$(mktemp)
journalctl -u "$UNIT" --since '7 days ago' --no-pager -o short-iso -q > "$J" 2>/dev/null
N=$(wc -l < "$J")
FIRST=$(head -1 "$J" | cut -d' ' -f1)
LAST=$(tail -1 "$J" | cut -d' ' -f1)
cnt() { grep -c -F -- "$1" "$J" || true; }
OUT=$(grep -o 'IRPT_RESIDENT_PACKAGE outcome=[A-Z][A-Z0-9_]*' "$J" | sed 's/.*outcome=//' | sort | uniq -c | awk '{printf "%s%s:%s", (n++?",":""), $2, $1}')
echo "RAW R2 window=$FIRST..$LAST scanned=$N package_outcomes=$(cnt 'IRPT_RESIDENT_PACKAGE outcome=') outcome_codes=${OUT:-none} ready_queue_unset=$(cnt 'ANALYSIS_READY_QUEUE_UNSET') ready_signals=$(cnt 'IRPT_RESIDENT_READY_SIGNAL') d47252fe=$(cnt 'REQ-d47252fe74634d0c5cdd8067')"
rm -f "$J"
