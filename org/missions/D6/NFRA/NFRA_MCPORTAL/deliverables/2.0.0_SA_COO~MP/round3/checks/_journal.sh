#!/usr/bin/env bash
# _journal.sh -- sourced by v1.AC1/v1.AC2. Reads the window [t0, t1] the worker recorded in
# org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~3/v1_run.json ({"t0": ISO-UTC, "t1": ISO-UTC}),
# then pulls the gateway's OWN access-log lines for that window over SSM (server-side record; never the worker's
# self-report). Client addresses are replaced on the host before the output leaves it. Sets $J (the lines) and $WIN.
AWS="$(pwd)/.tools/aws"; I=i-07dccb1615503ac99
# MP_V1_RUN overrides the window file ONLY for the issuer's dry-run controls at the cut; the criterion never sets it.
RUN="${MP_V1_RUN:-org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/0.9.0_WK_NFRA_MCPORTAL~3/v1_run.json}"
WIN=$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d['t0'],d['t1'])" "$RUN" 2>/dev/null | tr -d '\r')
[ -n "$WIN" ] || { echo "no window: $RUN missing or unreadable"; echo "RESULT: FAIL"; exit 1; }
set -- $WIN; T0="$1"; T1="$2"
TJ="${TMPDIR:-/tmp}/mp_v1_j_$$"; mkdir -p "$TJ"
python - "$TJ/params.json" "$T0" "$T1" <<'EOF'
import json, sys
since, until = sys.argv[2].replace('T', ' ').rstrip('Z'), sys.argv[3].replace('T', ' ').rstrip('Z')
cmd = ('journalctl -u opal-gateway --no-pager -o cat --utc --since "%s" --until "%s" | grep -E "HTTP/1.1\\" [0-9]{3}" '
       '| sed -E "s/[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+:[0-9]+/IP/g"') % (since, until)
json.dump({"commands": ["TZ=UTC " + cmd]}, open(sys.argv[1], "w", encoding="utf-8"))
EOF
cid=$(timeout 40 "$AWS" ssm send-command --instance-ids $I --document-name AWS-RunShellScript --parameters "file://$(cygpath -w "$TJ/params.json")" --query Command.CommandId --output text 2>&1 | tr -d '\r')
st=""; for i in 1 2 3 4 5 6 7 8 9 10; do st=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query Status --output text 2>/dev/null | tr -d '\r'); [ "$st" = Success ] || [ "$st" = Failed ] && break; sleep 3; done
J=$(timeout 20 "$AWS" ssm get-command-invocation --command-id "$cid" --instance-id $I --query StandardOutputContent --output text 2>/dev/null | tr -d '\r')
rm -rf "$TJ"
echo "window $T0 .. $T1; ssm command=${cid:-NONE} status=${st:-NONE}; access-log lines in window=$(printf '%s\n' "$J" | grep -c 'HTTP/1.1')"
[ "$st" = Success ] || { echo "RESULT: FAIL"; exit 1; }
