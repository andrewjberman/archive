set -u
# IRPT_ANLREQ TO-RUN-FWD1 window 3, AMENDMENT 2 (b): ONE bounded READ-ONLY journal read of the resident unit for the probe window (10:29:50Z to 10:32:30Z). Filter: checker / TICKER_CHECK_FAILED / YFINANCE lines. Every password, token, Authorization, cookie and base64 blob of 40 or more characters is replaced by [REDACTED]; at most 200 lines of 300 characters. No restart, no edit, no install, no network call.
U=irpt-analysis-resident.service
J=$(journalctl -u $U --since '2026-10-16 10:29:50' --until '2026-10-16 10:32:30' --no-pager -o short-iso 2>&1)
echo "JRN window lines total: $(printf '%s\n' "$J" | grep -c .)"
echo "JRN window IRPT_RESIDENT_POLL lines: $(printf '%s\n' "$J" | grep -c IRPT_RESIDENT_POLL)"
M=$(printf '%s\n' "$J" | grep -i -E 'check|TICKER_CHECK_FAILED|YFINANCE|yfinance' || true)
echo "JRN matching lines (checker, TICKER_CHECK_FAILED, YFINANCE): $(printf '%s\n' "$M" | grep -c .)"
printf '%s\n' "$M" | /usr/bin/python3.12 -c "
import re, sys
n = 0
for line in sys.stdin:
    line = line.rstrip('\n')
    if not line.strip():
        continue
    line = re.sub(r'(?i)(authorization|bearer|cookie|set-cookie|password|passwd|token|secret)[^ ,;]*[ =:]+[^ ,;]+', '[REDACTED]', line)
    line = re.sub(r'[A-Za-z0-9+/=_-]{40,}', '[REDACTED]', line)
    print('JRN ' + line[:300])
    n += 1
    if n >= 200:
        break
"
