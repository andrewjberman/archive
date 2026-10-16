set -u
# IRPT_ANLREQ TO-RUN-FWD1 window 3, AMENDMENT 8 (e) F12 / F10: ONE bounded READ-ONLY journal read of the resident unit for the run window (@SINCE@ to @UNTIL@ UTC: the run's first upload to its last answer plus 4 minutes). Filter: checker, TICKER_CHECK_FAILED, YFINANCE_CHECK_FAILED, 429, rate, timeout, queue, worker, RESOLVE, WAF_CHALLENGE, ATTENTION, yfinance, yahoo, swap. Every password, token, Authorization, cookie and base64 blob of 40 or more characters is replaced by [REDACTED]; at most 200 lines of 300 characters. No restart, no edit, no network call apart from the SQS count read.
U=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
J=$(journalctl -u $U --utc --since '@SINCE@' --until '@UNTIL@' --no-pager 2>&1)
echo "RJ window lines total: $(printf '%s\n' "$J" | grep -c .); first: $(printf '%s\n' "$J" | grep -m1 . | cut -c1-40); last: $(printf '%s\n' "$J" | grep . | tail -1 | cut -c1-40)"
echo "RJ WAF_CHALLENGE lines in the window: $(printf '%s\n' "$J" | grep -c WAF_CHALLENGE)"
echo "RJ RESOLVE_RETRY_EXHAUSTED lines in the window: $(printf '%s\n' "$J" | grep -c RESOLVE_RETRY_EXHAUSTED)"
echo "RJ ATTENTION lines in the window: $(printf '%s\n' "$J" | grep -c ATTENTION)"
echo "RJ POLL lines: $(printf '%s\n' "$J" | grep -c IRPT_RESIDENT_POLL); RESOLVE lines: $(printf '%s\n' "$J" | grep -c IRPT_RESIDENT_RESOLVE)"
echo "RJ yfinance or yahoo or swap lines: $(printf '%s\n' "$J" | grep -i -c -E 'yfinance|yahoo|swap')"
M=$(printf '%s\n' "$J" | grep -i -E 'checker|TICKER_CHECK_FAILED|YFINANCE_CHECK_FAILED|429|rate|timeout|queue|worker|RESOLVE|WAF_CHALLENGE|ATTENTION|yfinance|yahoo|swap' || true)
echo "RJ matching lines: $(printf '%s\n' "$M" | grep -c .)"
printf '%s\n' "$M" | /usr/bin/python3.12 -c "
import re, sys
n = 0
for line in sys.stdin:
    line = line.rstrip('\n')
    if not line.strip():
        continue
    line = re.sub(r'(?i)(authorization|bearer|cookie|set-cookie|password|passwd|token|secret)[^ ,;]*[ =:]+[^ ,;]+', '[REDACTED]', line)
    line = re.sub(r'[A-Za-z0-9+/=_-]{40,}', '[REDACTED]', line)
    print('RJ ' + line[:300])
    n += 1
    if n >= 200:
        break
"
echo "RJ tracebacks in the window: $(printf '%s\n' "$J" | grep -c Traceback)"
echo "RJ queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "RJ unit $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U) ActiveEnter=$(systemctl show -p ActiveEnterTimestamp --value $U)"
