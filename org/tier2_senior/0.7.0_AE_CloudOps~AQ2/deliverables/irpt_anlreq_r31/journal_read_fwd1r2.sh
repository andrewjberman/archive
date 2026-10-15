#!/bin/bash
# journal_read_fwd1r2.sh -- IRPT_ANLREQ.TO-READ-FWD1R2: READ ONLY journal read of the resident unit.
# It writes no file, restarts nothing, edits nothing. It runs systemctl show and journalctl only.
# Every line it prints passes through redact() first (sed, in this script). Run: bash -s -- [UNTIL] from stdin, or --selftest.
set -u
UNIT=irpt-analysis-resident
SINCE='2026-10-15 16:55:00'
UNTIL="${1:-2026-10-15 17:45:00}"

redact() {
  sed -E \
    -e 's/eyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*/[REDACTED]/g' \
    -e "s/[A-Za-z_]*(password|passwd|token|bearer|authorization|cookie|secret)[A-Za-z_]*([ =:\"']+[^ ,;\"'}]+){0,2}/[REDACTED]/Ig" \
    -e 's/[A-Za-z0-9+\/_=-]{40,}/[REDACTED]/g'
}

if [ "${1:-}" = "--selftest" ]; then
  printf '%s\n' \
    'x Authorization: Bearer abc.def.ghi y' \
    'POST ok password=hunter2 done' \
    'a eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ4In0.c2ln b' \
    'blob QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVowMTIzNDU2Nzg5 end' \
    'Set-Cookie: sid=abcdef; token refreshed' \
    'hdr {"Authorization": "Bearer zzz.yyy.xxx"} end' \
    'bearer=QQQ111 then SECRET: s3cr3tvalue tail' \
    'json {"password":"p4ss w0rd","user":"u"} after' \
    'IRPT_RESIDENT_POLL handled=0 REQ-d47252fe74634d0c5cdd8067 TCK-20261015-944c84f8' | redact
  exit 0
fi

echo "== (a) systemctl show $UNIT"
systemctl show "$UNIT" -p ActiveState -p MainPID -p NRestarts -p ActiveEnterTimestamp | redact
echo "WINDOW since=$SINCE until=$UNTIL"

echo "== (c) IRPT_RESIDENT_POLL lines per 5-minute bucket (handled sum)"
journalctl -u "$UNIT" --since "$SINCE" --until "$UNTIL" -o short-iso --no-pager 2>&1 \
  | grep 'IRPT_RESIDENT_POLL' \
  | awk '{ t=substr($1,12,5); m=substr(t,4,2)+0; b=substr(t,1,3) sprintf("%02d", int(m/5)*5);
           h=0; if (match($0,/handled=[0-9]+/)) h=substr($0,RSTART+8,RLENGTH-8)+0;
           n[b]++; s[b]+=h }
         END { buckets=0; nz=0;
               for (b in n) { buckets++; if (s[b]>0) nz++; printf "BUCKET %s polls=%d handled_sum=%d\n", b, n[b], s[b] }
               printf "BUCKETS total=%d with_handled_gt0=%d\n", buckets, nz }' | sort

FILT='IRPT_RESIDENT|Traceback|Error|ERROR|WARN|commentary|package|packager|attach|REQ-d47252fe74634d0c5cdd8067|TCK-20261015-944c84f8|ready'
TOTAL=$(journalctl -u "$UNIT" --since "$SINCE" --until "$UNTIL" -o cat --no-pager 2>&1 | grep -E "$FILT" | wc -l)
IDLE=$(journalctl -u "$UNIT" --since "$SINCE" --until "$UNTIL" -o cat --no-pager 2>&1 | grep -E "$FILT" | grep -c 'IRPT_RESIDENT_POLL handled=0$')
echo "== (b) FILTERED_TOTAL=$TOTAL IDLE_POLL_LINES(handled=0, excluded below)=$IDLE; lines below are the other filtered lines, 300 chars each, redacted, at most 400 lines, stopped at 17000 bytes"
journalctl -u "$UNIT" --since "$SINCE" --until "$UNTIL" -o short-iso --no-pager 2>&1 \
  | grep -E "$FILT" | grep -v 'IRPT_RESIDENT_POLL handled=0$' | redact | cut -c1-300 | head -400 | head -c 17000
echo
echo "== END"
