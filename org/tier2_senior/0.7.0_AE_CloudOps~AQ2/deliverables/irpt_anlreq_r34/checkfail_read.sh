set -u
# IRPT_ANLREQ TO-READ-CHECKFAIL (0.7.0_AE_CloudOps~AQ2): READ ONLY. Six sections about the resident unit. Writes nothing, calls nothing, prints no secret.
U=irpt-analysis-resident.service
echo "SECTION UNIT"
systemctl show $U -p MainPID -p User -p Group -p ActiveEnterTimestamp -p NRestarts -p WorkingDirectory -p ExecStart; echo "UNIT rc of systemctl show: $?"
PID=$(systemctl show -p MainPID --value $U)
USR=$(systemctl show -p User --value $U); [ -z "$USR" ] && USR=$(stat -c %U /proc/$PID)
echo "UNIT MainPID now $PID, process owner $(stat -c %U /proc/$PID), unit User field '$(systemctl show -p User --value $U)'"
echo "SECTION SANDBOX"
systemctl show $U -p Environment -p EnvironmentFiles -p ProtectHome -p ProtectSystem -p PrivateTmp -p PrivateNetwork -p ReadWritePaths -p ReadOnlyPaths -p InaccessiblePaths -p IPAddressAllow -p IPAddressDeny -p RestrictAddressFamilies -p NoNewPrivileges -p DynamicUser; echo "SANDBOX rc: $?"
EF=$(systemctl show -p EnvironmentFiles --value $U | sed 's/ (.*//' | tr -d '-')
if [ -n "$EF" ] && [ -r "$EF" ]; then echo "SANDBOX EnvironmentFiles $EF NAMES only:"; cut -d= -f1 "$EF" | sed 's/^/SANDBOXNAME /'; else echo "SANDBOX no readable EnvironmentFiles path named ($EF)"; fi
echo "SECTION PROCENV"
for V in HOME USER LOGNAME PYTHONPATH XDG_CACHE_HOME TMPDIR PATH HTTP_PROXY HTTPS_PROXY NO_PROXY YF_CACHE_DIR; do
  L=$(tr '\0' '\n' < /proc/$PID/environ | grep -m1 "^$V=" || true)
  if [ -n "$L" ]; then echo "$L"; else echo "$V=ABSENT"; fi
done
echo "PROCENV cwd: $(ls -ld /proc/$PID/cwd | sed 's/.* -> /-> /') ; $(ls -ld "$(readlink /proc/$PID/cwd)" | cut -c1-120)"
echo "SECTION CACHE"
H=$(tr '\0' '\n' < /proc/$PID/environ | grep -m1 '^HOME=' | cut -d= -f2-); [ -z "$H" ] && H=$(getent passwd "$USR" | cut -d: -f6)
echo "CACHE user $USR home $H"
for P in "$H" "$H/.cache" "$H/.cache/py-yfinance"; do
  if [ -e "$P" ]; then echo "CACHE $(ls -ld "$P" | cut -c1-110); writable by $USR: $(sudo -u "$USR" test -w "$P" && echo yes || echo no)"; else echo "CACHE $P ABSENT"; fi
done
for V in XDG_CACHE_HOME TMPDIR; do
  P=$(tr '\0' '\n' < /proc/$PID/environ | grep -m1 "^$V=" | cut -d= -f2-)
  if [ -n "$P" ]; then echo "CACHE $V=$P $(ls -ld "$P" 2>&1 | cut -c1-100); writable by $USR: $(sudo -u "$USR" test -w "$P" && echo yes || echo no)"; else echo "CACHE $V not set in the process"; fi
done
echo "CACHE df:"; df -Pk "$H" /tmp | tail -2
echo "SECTION PYPATH"
R=$(systemctl show -p ExecStart --value $U | grep -o '/opt/irpt-resident/[^/]*' | head -1)
echo "PYPATH running root $R"
LAUNCH=$(systemctl show -p ExecStart --value $U | grep -o '/opt/irpt-resident/[^ ;]*resident_main.py' | head -1)
for F in "$R/ycharts/session/resident_session.py" "$R/ycharts/generate/resident_worker.py" "$LAUNCH"; do
  N=$(grep -n pydeps "$F" 2>/dev/null | cut -c1-240); if [ -n "$N" ]; then echo "PYPATH $F:"; echo "$N" | sed 's/^/PYPATH   /'; else echo "PYPATH $F: none"; fi
done
echo "PYPATH $(ls -ld /opt/investor-reporting-ycharts/pydeps | cut -c1-110); readable by $USR: $(sudo -u "$USR" test -r /opt/investor-reporting-ycharts/pydeps && echo yes || echo no)"
echo "SECTION JOURNAL"
J=$(journalctl -u $U --utc --since '2026-10-16 10:15:00' --until '2026-10-16 10:40:00' --no-pager 2>&1)
echo "JOURNAL window lines: $(printf '%s\n' "$J" | grep -c .); first: $(printf '%s\n' "$J" | grep -m1 . | cut -c1-40); last: $(printf '%s\n' "$J" | grep . | tail -1 | cut -c1-40)"
M=$(printf '%s\n' "$J" | grep -i -E -B2 -A2 'Traceback|Error|Exception|yfinance|checker|CHECK_FAILED|CheckerUnavailable|ErrorFrame|permission|sqlite|peewee|cache|timeout|429|403|curl|ssl|resolve|network' || true)
if [ -z "$M" ]; then echo "NO_MATCH window_lines=$(printf '%s\n' "$J" | grep -c .)"; else printf '%s\n' "$M" | cut -c1-400 | sed 's/^/JRN /'; fi
