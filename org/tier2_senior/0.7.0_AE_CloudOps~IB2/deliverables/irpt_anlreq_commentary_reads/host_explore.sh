set -u
# TO-READ-RESIDENT-COMMENTARY exploration (READ ONLY, root via SSM): names only, never a value. Writes nothing.
UNIT=irpt-analysis-resident.service
EXEC=$(systemctl show -p ExecStart --value "$UNIT" | tr ' ;' '\n\n' | grep -m1 'resident_main.py')
ROOT=${EXEC%/ycharts/generate/resident_main.py}
echo "EXPLORE exec_path_present=$([ -n "$EXEC" ] && echo yes || echo no) root_basename=$(basename "$ROOT")"
echo "EXPLORE active=$(systemctl is-active "$UNIT") since=$(systemctl show -p ActiveEnterTimestamp --value "$UNIT")"
echo "EXPLORE root top-level names:"; ls -1 "$ROOT" | head -40
echo "EXPLORE pin/manifest/build-like names (depth 2):"; find "$ROOT" -maxdepth 2 \( -iname '*pin*' -o -iname '*manifest*' -o -iname '*BUILD*' -o -iname 'SHA256SUMS*' -o -iname 'RELEASE*' -o -iname 'VERSION*' \) -not -path '*/__pycache__/*' | sed "s#^$ROOT/##" | head -20
echo "EXPLORE releases dir names:"; ls -1 /opt/irpt-resident | head -20
echo "EXPLORE unit Environment KEY NAMES:"; systemctl show -p Environment --value "$UNIT" | tr ' ' '\n' | sed 's/=.*//' | sort -u | head -40
echo "EXPLORE unit EnvironmentFiles (paths):"; systemctl show -p EnvironmentFiles --value "$UNIT" | head -3
echo "EXPLORE journal bounds: $(journalctl -u "$UNIT" --since '7 days ago' --no-pager -q 2>/dev/null | wc -l) lines"
