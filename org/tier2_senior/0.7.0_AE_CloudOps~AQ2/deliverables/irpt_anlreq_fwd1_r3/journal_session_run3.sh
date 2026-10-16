set -u
# IRPT_ANLREQ TO-RUN-FWD1 window 3, AMENDMENT 5 ADDENDUM (2): ONE bounded READ-ONLY journal read of the resident unit for 13:28Z to 13:45Z, filtered for capture, refresh, session, BROWSER_ATTENTION, WAF and challenge lines. Every password, token, Authorization, cookie and base64 blob of 40 or more characters is replaced by [REDACTED]; at most 200 lines of 300 characters. No restart, no edit, no network call.
U=irpt-analysis-resident.service
J=$(journalctl -u $U --utc --since '2026-10-16 13:28:00' --until '2026-10-16 13:45:00' --no-pager 2>&1)
echo "SES window lines total: $(printf '%s\n' "$J" | grep -c .); first: $(printf '%s\n' "$J" | grep -m1 . | cut -c1-40); last: $(printf '%s\n' "$J" | grep . | tail -1 | cut -c1-40)"
M=$(printf '%s\n' "$J" | grep -i -E 'capture|refresh|session|BROWSER_ATTENTION|WAF|challenge' || true)
echo "SES matching lines: $(printf '%s\n' "$M" | grep -c .)"
printf '%s\n' "$M" | /usr/bin/python3.12 -c "
import re, sys
n = 0
for line in sys.stdin:
    line = line.rstrip('\n')
    if not line.strip():
        continue
    line = re.sub(r'(?i)(authorization|bearer|cookie|set-cookie|password|passwd|token|secret)[^ ,;]*[ =:]+[^ ,;]+', '[REDACTED]', line)
    line = re.sub(r'[A-Za-z0-9+/=_-]{40,}', '[REDACTED]', line)
    print('SES ' + line[:300])
    n += 1
    if n >= 200:
        break
"
echo "SES unit $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U)"
