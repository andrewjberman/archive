set -u
# IRPT_ANLREQ TO-APPLY-R34C (COO ruling msg 9259): RENAME, never delete, the three leftovers of the failed first send. Runs as root. Stops unless the unit is still r32 (MainPID 1084905).
U=irpt-analysis-resident.service
PID=$(systemctl show -p MainPID --value $U); EXE=$(systemctl show -p ExecStart --value $U | grep -o '/opt/irpt-resident/[^/]*' | head -1)
echo "MOVE unit $(systemctl is-active $U) MainPID=$PID ExecStart root=$EXE NRestarts=$(systemctl show -p NRestarts --value $U)"
if [ "$PID" != "1084905" ] || [ "$EXE" != "/opt/irpt-resident/0485393f3a-r32" ] || [ "$(systemctl is-active $U)" != "active" ]; then echo "MOVE STOP: the unit is not r32 with MainPID 1084905; nothing renamed"; exit 9; fi
S=$(date -u +%Y%m%dT%H%M%SZ)
A=/opt/irpt-resident/0485393f3a-r34c
B=/opt/investor-reporting-ycharts/ycharts_session.js.before-0485393f3a-r34c
C=/tmp/irpt-resident-0485393f3a-r34c.tar.gz
for p in "$A" "$B" "$C"; do
  [ -e "$p" ] || { echo "MOVE STOP: $p absent; nothing renamed"; exit 9; }
  [ -e "$p.moved-aside-$S" ] && { echo "MOVE STOP: target exists for $p; nothing renamed"; exit 9; }
done
echo "MOVE LIST (rename only, stamp $S):"
for p in "$A" "$B" "$C"; do echo "MOVE   $p  ->  $p.moved-aside-$S"; done
for p in "$A" "$B" "$C"; do mv "$p" "$p.moved-aside-$S" && echo "MOVE done $p" || echo "MOVE FAIL $p"; done
for p in "$A" "$B" "$C"; do echo "MOVE after: $p exists=$([ -e "$p" ] && echo yes || echo no); moved copy exists=$([ -e "$p.moved-aside-$S" ] && echo yes || echo no)"; done
echo "MOVE moved root file count outside pydeps: $(find "$A.moved-aside-$S" -type f -not -path '*/pydeps/*' | wc -l)"
echo "MOVE moved kept copy sha256: $(sha256sum "$B.moved-aside-$S" | cut -c1-16); tar sha256: $(sha256sum "$C.moved-aside-$S" | cut -c1-64)"
echo "MOVE unit after: $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U)"
