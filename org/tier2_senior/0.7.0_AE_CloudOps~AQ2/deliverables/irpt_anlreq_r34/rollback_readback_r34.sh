set -u
# IRPT_ANLREQ TO-APPLY-R34B step 9 (amendment 1): the READ-ONLY read-back after scripts/rollback_r34.sh. Sent as the SSM command text. No write.
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
UNIT=irpt-analysis-resident.service
RUN=$(systemctl show $UNIT -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1)
echo "RB at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "RB running root $RUN (want $R/0485393f3a-r32) active=$(systemctl is-active $UNIT) restarts=$(systemctl show $UNIT -p NRestarts --value) since=$(systemctl show $UNIT -p ActiveEnterTimestamp --value) mainpid=$(systemctl show $UNIT -p MainPID --value)"
echo "RB producer list line: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py) (want andrew@opalinvest.com and fwd1-staff-r41b@opal.invalid, as at P1)"
echo "RB worker sha256 $(sha256sum $RUN/ycharts/generate/resident_worker.py | cut -d' ' -f1) (want 7bab7930b418866d5a9906cf56b70fa4750ebe0b69279d8fcc7fbc67e98f6d53, as at P1)"
echo "RB members that release 34 changed or added, read at the running root (the P1 values; an added member must be absent):"
for ent in \
  "intake/portfolio.py ba04b49bbb087f602701eeab5de79affc460f308eed15e05977bd88bb05e4d04" \
  "intake/uploads.py 48211e08e459fe3a3a1d87663abce6c67caa90c1c50f50e4b93d48ed7514629d" \
  "intake/yfinance_check.py ABSENT" \
  "ops/status.py 87048c7f4d00ba33c87de1a223a36b53e3487ed7414d613ee744984bcaef6030" \
  "reports/resident_installed.py 0271bde8483b20aa7ea3ad55aecf1dfd4d7ecb09d3ee04b6d2dfd4155fa907ae" \
  "ycharts/research/opal_producer.py adc8ca8b7f86d54ea2df3828faa977574aac68e6baf7151460da64b34d6acc9e" \
  "ycharts/research/swap_pass.py ABSENT" \
  "ycharts/research/swap_pool.json ABSENT" \
  "ycharts/research/yahoo_history_days.py ABSENT" \
  "ycharts/session/resident_session.py ea9d7ea9c21794d19ca50a49a96511077a0802bd2c0c944f31696eb5796a6242"; do
  set -- $ent
  if [ -f $RUN/$1 ]; then GOT=$(sha256sum $RUN/$1 | cut -d' ' -f1); else GOT=ABSENT; fi
  echo "RB member $1 sha256 $GOT (want $2) $([ "$GOT" = "$2" ] && echo MATCH || echo MISMATCH)"
done
echo "RB bindings: opal_swap_pool key present in the running root's bindings: $(python3.12 -c "import json;print('opal_swap_pool' in json.load(open('$RUN/reports/resident_bindings.json')))") (want False); opal_pricing enabled: $(python3.12 -c "import json;print(json.load(open('$RUN/reports/resident_bindings.json'))['opal_pricing']['enabled'])") (want False)"
echo "RB r34 root kept on the host: $(test -d $R/0485393f3a-r34 && echo yes || echo no) (want yes, no delete); r32 receipt copy present: $(test -f $R/cutover_receipt.0485393f3a-r32.json && echo yes || echo no)"
echo "RB receipt: $(python3.12 -c "import json;r=json.load(open('$R/cutover_receipt.json'));print(r.get('package_root'),r.get('package_manifest_sha256','')[:16],r.get('ledger'))") (want /opt/irpt-resident/0485393f3a-r32 and irpt-resident-r32-20261015)"
echo "RB library $(sha256sum $H/ycharts_session.js | cut -d' ' -f1) (want a1c2880169c5f7996cc7c5880e4fe36db90f0a2c1f5a1cd01e0d1d8153544841)"
echo "RB queue visible/in-flight: $(aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text) (want 0 0, as at P1)"
echo "RB journal 60s: polls=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c IRPT_RESIDENT_POLL) tracebacks=$(journalctl -u $UNIT --since '-60 s' --no-pager | grep -c Traceback)"
echo "RB NO SIGN-IN since the rollback start: journal lines naming a capture, an eviction or a session refresh = $(journalctl -u $UNIT --since "$(systemctl show $UNIT -p ActiveEnterTimestamp --value)" --no-pager | grep -c -i -E 'capture|EVICTION|session_refresh|SIGNED_OUT|NO_AUTHENTICATED') (expect 0)"
