"""SSM helper for leg Q' (MDPF_SECCLASS TO-SC-e102b, 0.7.0_AE_CloudOps~SC1). Shell command text only, read from a file.

  python -I e102_ssm.py online <instance> <max_seconds>                    poll PingStatus until Online; prints the time it was first seen
  python -I e102_ssm.py send <instance> <comment> <cmdfile> <out.json>     send ONE AWS-RunShellScript command, poll to a terminal state, save the invocation
  python -I e102_ssm.py list <instance> <since_iso>                        commands sent to the instance since <since_iso> (InvokedAfter filter)
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone

import boto3

TERMINAL = {'Success', 'Failed', 'Cancelled', 'TimedOut', 'Cancelling'}


def _now() -> str:
    return datetime.now(timezone.utc).strftime('%H:%M:%SZ')


def online(inst: str, max_s: int) -> int:
    ssm = boto3.client('ssm')
    t0 = time.time()
    while time.time() - t0 < max_s:
        r = ssm.describe_instance_information(Filters=[{'Key': 'InstanceIds', 'Values': [inst]}])
        rows = r.get('InstanceInformationList', [])
        if rows and rows[0]['PingStatus'] == 'Online':
            print(f'ONLINE at {_now()} (waited {int(time.time() - t0)}s) lastping={rows[0]["LastPingDateTime"].isoformat()}')
            return 0
        time.sleep(3)
    print(f'NOT-ONLINE after {max_s}s at {_now()}')
    return 1


def send(inst: str, comment: str, cmdfile: str, out: str) -> int:
    ssm = boto3.client('ssm')
    text = open(cmdfile, encoding='utf-8').read()
    sent = _now()
    r = ssm.send_command(InstanceIds=[inst], DocumentName='AWS-RunShellScript', Comment=comment,
                         Parameters={'commands': [text], 'executionTimeout': ['3000']}, TimeoutSeconds=60)
    cid = r['Command']['CommandId']
    print(f'SENT {cid} at {sent}')
    time.sleep(2)
    inv = None
    while True:
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=inst)
        except ssm.exceptions.InvocationDoesNotExist:
            time.sleep(2)
            continue
        if inv['Status'] in TERMINAL:
            break
        time.sleep(5)
    inv.pop('ResponseMetadata', None)
    for k in ('ExecutionStartDateTime', 'ExecutionEndDateTime'):
        pass
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(inv, f, indent=1, default=str)
    print(f'DONE {cid} status={inv["Status"]} rc={inv.get("ResponseCode")} start={inv.get("ExecutionStartDateTime")} '
          f'end={inv.get("ExecutionEndDateTime")}')
    so = inv.get('StandardOutputContent', '')
    print('--- stdout (first 2500 / last 2500 chars) ---')
    print(so if len(so) <= 5000 else so[:2500] + '\n...[cut]...\n' + so[-2500:])
    print('--- stderr ---')
    print(inv.get('StandardErrorContent', '')[:1500])
    return 0 if inv['Status'] == 'Success' else 2


def lst(inst: str, since: str) -> int:
    ssm = boto3.client('ssm')
    n = 0
    for page in ssm.get_paginator('list_commands').paginate(InstanceId=inst, Filters=[{'key': 'InvokedAfter', 'value': since}]):
        for c in page['Commands']:
            n += 1
            print(c['CommandId'], c['RequestedDateTime'].isoformat(), c['Status'], c.get('Comment', ''))
    print(f'{n} command(s) since {since}')
    return 0


if __name__ == '__main__':
    a = sys.argv
    if a[1] == 'online':
        sys.exit(online(a[2], int(a[3])))
    if a[1] == 'send':
        sys.exit(send(a[2], a[3], a[4], a[5]))
    sys.exit(lst(a[2], a[3]))
