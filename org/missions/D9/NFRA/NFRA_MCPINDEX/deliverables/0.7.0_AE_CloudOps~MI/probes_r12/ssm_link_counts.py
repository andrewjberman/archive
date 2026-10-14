"""ssm_link_counts.py <out.txt>: READ-ONLY. Ships link_counts_host.py plus the CUT's reader and catalog to the
gateway host via SSM AWS-RunShellScript (base64), runs them under the host venv as ec2-user against
/opt/opal-gateway (the LIVE side) and the two /tmp copies (the CUT side), writes stdout, removes the /tmp files.
Writes nothing to /opt/opal-gateway and opens no socket. MX-r-12 PHASE A, amendment A1.
"""

import base64
import json
import os
import subprocess
import sys
import tempfile
import time

WS = os.getcwd()
AWS = os.path.join(WS, ".tools", "aws")
INSTANCE = "i-07dccb1615503ac99"
CUT_GW = "C:/tmp/mx-dep-r12/infra/aws/ec2/opal-gateway"
PROBE = os.path.join(
    WS, "org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables",
    "0.7.0_AE_CloudOps~MI", "probes_r12", "link_counts_host.py",
)


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


cmd = (
    "echo " + b64(PROBE) + " | base64 -d > /tmp/r12_lc.py; "
    "echo " + b64(os.path.join(CUT_GW, "app", "admin_gateway_breakdown.py")) + " | base64 -d > /tmp/r12_cut_reader.py; "
    "echo " + b64(os.path.join(CUT_GW, "app", "refs", "DATA_CATALOG.yaml")) + " | base64 -d > /tmp/r12_cut_catalog.yaml; "
    "chmod 644 /tmp/r12_lc.py /tmp/r12_cut_reader.py /tmp/r12_cut_catalog.yaml; "
    "cd /opt/opal-gateway && sudo -u ec2-user ./.venv/bin/python /tmp/r12_lc.py "
    "/opt/opal-gateway/app/admin_gateway_breakdown.py /opt/opal-gateway/app/refs/DATA_CATALOG.yaml "
    "/tmp/r12_cut_reader.py /tmp/r12_cut_catalog.yaml 2>&1; "
    "rm -f /tmp/r12_lc.py /tmp/r12_cut_reader.py /tmp/r12_cut_catalog.yaml"
)

params = os.path.join(tempfile.mkdtemp(), "params.json")
json.dump({"commands": [cmd]}, open(params, "w", encoding="utf-8"))


def run(args):
    return subprocess.run(
        ["bash", AWS] + args, capture_output=True, text=True, encoding="utf-8", timeout=90
    ).stdout.strip()


cid = run([
    "ssm", "send-command", "--instance-ids", INSTANCE, "--document-name", "AWS-RunShellScript",
    "--parameters", "file://" + params, "--query", "Command.CommandId", "--output", "text",
])
st = ""
for _ in range(40):
    time.sleep(4)
    st = run([
        "ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INSTANCE,
        "--query", "Status", "--output", "text",
    ])
    if st in ("Success", "Failed", "Cancelled", "TimedOut"):
        break
out = run([
    "ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INSTANCE,
    "--query", "StandardOutputContent", "--output", "text",
])
open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(out.replace("\r", "") + "\n")
print("ssm command", cid, "status", st, "bytes", len(out))
