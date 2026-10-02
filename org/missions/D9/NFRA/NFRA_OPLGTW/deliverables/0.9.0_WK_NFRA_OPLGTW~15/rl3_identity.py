"""OG-rl-3 PHASE A step 6: prove the identity the live deploy-to-ec2.sh needs (OG_TAXSMA_WORKBOOK_IDENTITY) equals the host's
current TAXSMA_WORKBOOK_IDENTITY, by sha256 computed host-side. Prints MATCH / DIFFER only (plus the 12-char hash prefix is NOT printed).

usage: python rl3_identity.py check          # the PHASE A proof
       eval "$(python rl3_identity.py export)"   # PHASE B: exports OG_TAXSMA_WORKBOOK_IDENTITY into the deploying shell, never printed

The value is values.tenant_id + "/" + values["opalbloomberg@opalinvest.com"] from %LOCALAPPDATA%/opal/og-principals/part_d_20260930.json.
.env is never sourced (row Z-S32): the host program parses the one named key and prints a boolean."""
import base64
import hashlib
import json
import os
import subprocess
import sys
import time

INST = "i-07dccb1615503ac99"
PARTD = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-principals", "part_d_20260930.json")


def identity():
    v = json.load(open(PARTD, encoding="utf-8"))["values"]
    return v["tenant_id"] + "/" + v["opalbloomberg@opalinvest.com"]


def aws(a):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + a, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    mode = sys.argv[1]
    ident = identity()
    if mode == "export":
        print("export OG_TAXSMA_WORKBOOK_IDENTITY='%s'" % ident)
        return 0
    want = hashlib.sha256(ident.encode("utf-8")).hexdigest()
    prog = "\n".join([
        "import hashlib, re",
        "val = None",
        "for line in open('/opt/opal-gateway/.env', encoding='utf-8'):",
        "    m = re.match(r'^TAXSMA_WORKBOOK_IDENTITY=(.*)$', line.rstrip(chr(10)))",
        "    if m: val = m.group(1).strip().strip(chr(34))",
        "got = hashlib.sha256(val.encode('utf-8')).hexdigest() if val is not None else 'ABSENT'",
        "print('IDENTITY_SHA256 ' + ('MATCH' if got == '@@W@@' else 'DIFFER'))".replace("@@W@@", want),
    ]) + "\n"
    b64 = base64.b64encode(prog.encode("ascii")).decode("ascii")
    params = json.dumps({"commands": ["echo %s | base64 -d > /tmp/og_rl3_id.py" % b64, "python3.11 /tmp/og_rl3_id.py", "rm -f /tmp/og_rl3_id.py"]})
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_rl3_id_params.json")
    open(pf, "w", encoding="utf-8", newline="\n").write(params)
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript", "--comment", "OG-rl-3 identity hash compare",
             "--parameters", "file://" + pf.replace("\\", "/"), "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    if r.returncode != 0:
        print("SEND FAIL", r.stderr.strip()[:200])
        return 2
    cid = r.stdout.strip()
    st = ""
    for _ in range(40):
        time.sleep(3)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST, "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
    os.remove(pf)
    print("ssm %s status=%s" % (cid, st))
    print(out.strip())
    return 0 if "MATCH" in out and "DIFFER" not in out else 1


sys.exit(main())
