set -u
# IRPT_ANLREQ TO-RUN-FWD1 window 3, AMENDMENT 6 (d): ONE bounded READ-ONLY journal read of the resident unit for 14:21:45Z to 14:34:25Z (first SET 3 post to the last answer 14:30:25Z plus 4 minutes), plus the queue counts and the restart count. Filter: checker, TICKER_CHECK_FAILED, YFINANCE_CHECK_FAILED, 429, rate, timeout, queue, worker, RESOLVE and WAF_CHALLENGE lines. Every password, token, Authorization, cookie and base64 blob of 40 or more characters is replaced by [REDACTED]; at most 200 lines of 300 characters. No restart, no edit, no network call apart from the SQS count read.
U=irpt-analysis-resident.service
Q=https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation
J=$(journalctl -u $U --utc --since '2026-10-16 14:21:45' --until '2026-10-16 14:34:25' --no-pager 2>&1)
echo "S3J window lines total: $(printf '%s\n' "$J" | grep -c .); first: $(printf '%s\n' "$J" | grep -m1 . | cut -c1-40); last: $(printf '%s\n' "$J" | grep . | tail -1 | cut -c1-40)"
echo "S3J WAF_CHALLENGE lines in the window: $(printf '%s
' "$J" | grep -c WAF_CHALLENGE)"
echo "S3J POLL lines: $(printf '%s\n' "$J" | grep -c IRPT_RESIDENT_POLL); RESOLVE lines: $(printf '%s\n' "$J" | grep -c IRPT_RESIDENT_RESOLVE)"
M=$(printf '%s\n' "$J" | grep -i -E 'checker|TICKER_CHECK_FAILED|YFINANCE_CHECK_FAILED|429|rate|timeout|queue|worker|RESOLVE|WAF_CHALLENGE' || true)
echo "S3J matching lines: $(printf '%s\n' "$M" | grep -c .)"
printf '%s\n' "$M" | /usr/bin/python3.12 -c "
import re, sys
n = 0
for line in sys.stdin:
    line = line.rstrip('\n')
    if not line.strip():
        continue
    line = re.sub(r'(?i)(authorization|bearer|cookie|set-cookie|password|passwd|token|secret)[^ ,;]*[ =:]+[^ ,;]+', '[REDACTED]', line)
    line = re.sub(r'[A-Za-z0-9+/=_-]{40,}', '[REDACTED]', line)
    print('S3J ' + line[:300])
    n += 1
    if n >= 200:
        break
"
echo "S3J tracebacks in the window: $(printf '%s\n' "$J" | grep -c Traceback)"
echo "S3J queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url $Q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
echo "S3J unit $(systemctl is-active $U) MainPID=$(systemctl show -p MainPID --value $U) NRestarts=$(systemctl show -p NRestarts --value $U) ActiveEnter=$(systemctl show -p ActiveEnterTimestamp --value $U)"
