"""CA-i-12 AC2: the round-17 package is LIVE, read from AWS, never from a report.

PASS needs all of:
  1. both functions (handler, ingress) carry the same CodeSha256, different from the pre-state nIQW...;
  2. the zip the ingress function SERVES (get-function Code.Location, downloaded) hashes to that CodeSha256, and its four round-17 files are byte-identical (LF) to the pin's;
  3. BOTH functions' environment carries MUSE_ANSWER_PUBKEY whose `ssh-keygen -lf` fingerprint is the record's, and MAIL_BEARER_SECRET and SMS_ORIGINATION are unchanged;
  4. the SERVED code, imported from the extracted zip, behaves (and, from CA-i-10: a payload without version is refused, a seq is carried, the acted-set guard exists): tenant.ROUTES has muse.reply; muse_verify.verify accepts a real `ssh-keygen -Y sign` signature made with a
     throwaway key it is given as the pinned key and refuses a second key's signature; bus_send's message carries from_tailnet=ldo-001.
Prints one line per check and RESULT: PASS|FAIL. Read-only: get calls and one download.
"""
import base64
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PIN = "8a480805e5"
PRE = "lRKObLMbn1kTWSXtohLxZ33HYVq7aBd1o/fjLfaA1Rw="
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
FILES = ["data/transcripts/scripts/teams_chat/tenant.py", "data/transcripts/scripts/teams_chat/muse_verify.py",
         "data/transcripts/scripts/teams_chat/mail_requests.py", "data/transcripts/scripts/teams_chat/assist.py"]   # tenant.py is the changed one; the other three must stay the first deploy's bytes
FP = "SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ"
MAIL_ARN = "arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/mail/commassist-bearer-cPYbR3"
SMS = "arn:aws:sms-voice:us-east-1:313476888478:phone-number/phone-0e98f7739a16415c83d951336a7da12a"

PROBE = r'''
import json, os, subprocess, sys, tempfile
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import assist as a, tenant as t, muse_verify as mv
out = {"route": "muse.reply" in t.ROUTES}
with tempfile.TemporaryDirectory() as d:
    def key(n):
        k = os.path.join(d, n)
        subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", k], check=True, capture_output=True)
        return k, " ".join(open(k + ".pub").read().split()[:2])
    k1, p1 = key("one"); k2, p2 = key("two")
    msg = b'{"tag":"C1","action":"send","notes":"","version":1}'
    def sign(k):
        f = os.path.join(d, "m_" + os.path.basename(k)); open(f, "wb").write(msg)
        subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", k, "-n", "muse-answer@opal", f], check=True, capture_output=True)
        return open(f + ".sig").read()
    out["accepts"] = mv.verify(p1, "muse-answer@opal", msg, sign(k1))[0]
    out["refuses"] = not mv.verify(p1, "muse-answer@opal", msg, sign(k2))[0]
sent = []
class Sqs:
    def get_queue_url(self, QueueName): return {"QueueUrl": "https://sqs.example.invalid/0/" + QueueName}
    def send_message(self, **kw): sent.append(kw); return {"MessageId": "m"}
a.aws = lambda svc: Sqs()
a.bus_send(sorted(a.DEVICES)[0], "a bid", {"type": "job.bid", "job": "J0"})
out["stamp"] = (sent[0]["MessageAttributes"].get("from_tailnet") or {}).get("StringValue")
out["no_version_refused"] = t._muse_fields(json.dumps({"tag": "C1", "action": "send", "notes": ""})) is None
f = t._muse_fields(json.dumps({"tag": "C1", "action": "send", "notes": "", "version": 1, "seq": 4}))
out["seq_carried"] = bool(f) and f.get("seq") == 4
out["acted_guard"] = "sent" in getattr(t, "MUSE_ACTED", ())
print(json.dumps(out))
'''


def root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8").stdout.strip()


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    if r.returncode != 0:
        return None, ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1]
    return json.loads(r.stdout), None


def fingerprint(line):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "k.pub"
        p.write_text((line or "") + "\n", encoding="ascii")
        out = subprocess.run(["ssh-keygen", "-lf", str(p)], capture_output=True, text=True).stdout
    return (out.split() + ["", ""])[1]


def main():
    os.chdir(root())
    ok = True
    shas, envs = [], []
    for fn in FUNCS:
        cfg, err = aws("lambda", "get-function-configuration", "--function-name", fn)
        shas.append((cfg or {}).get("CodeSha256"))
        envs.append(((cfg or {}).get("Environment") or {}).get("Variables") or {})
        print("CHECK %s CodeSha256=%s LastModified=%s %s" % (fn, shas[-1], (cfg or {}).get("LastModified"), err or ""))
    c1 = bool(shas[0]) and shas[0] == shas[1] and shas[0] != PRE
    print("CHECK both functions on one package, not the pre-state: %s" % c1)
    ok &= c1

    doc, err = aws("lambda", "get-function", "--function-name", FUNCS[1])
    url = ((doc or {}).get("Code") or {}).get("Location")
    data = urllib.request.urlopen(url, timeout=60).read() if url else b""
    served = base64.b64encode(hashlib.sha256(data).digest()).decode() if data else None
    c2 = bool(served) and served == shas[1]
    tmp = tempfile.mkdtemp(prefix="comm_r17_i4_")
    if data:
        zipfile.ZipFile(io.BytesIO(data)).extractall(tmp)
    same = True
    for path in FILES:
        pin_bytes = subprocess.run(["git", "show", "%s:%s" % (PIN, path)], capture_output=True).stdout.replace(b"\r\n", b"\n")
        fp = os.path.join(tmp, *path.split("/"))
        eq = bool(pin_bytes) and os.path.isfile(fp) and open(fp, "rb").read() == pin_bytes
        print("CHECK served %s == pin %s: %s" % (path, PIN, eq))
        same &= eq
    print("CHECK served zip hash equals CodeSha256: %s (%s bytes); four files equal the pin: %s" % (c2, len(data), same))
    ok &= c2 and same

    c3 = True
    for fn, env in zip(FUNCS, envs):
        good = (fingerprint(env.get("MUSE_ANSWER_PUBKEY")) == FP and env.get("MAIL_BEARER_SECRET") == MAIL_ARN
                and env.get("SMS_ORIGINATION") == SMS)
        print("CHECK %s environment: muse key fingerprint, mail secret and sms origination as recorded: %s" % (fn, good))
        c3 &= good
    ok &= c3

    probe = None
    if data:
        r = subprocess.run([sys.executable, "-c", PROBE, tmp], capture_output=True, text=True, encoding="utf-8", cwd=tmp, timeout=100)
        try:
            probe = json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:  # noqa: BLE001 -- a failed probe reads as a FAIL with its stderr shown
            print("ERROR: probe failed: %s" % (r.stderr or "")[-300:])
    c4 = bool(probe) and probe.get("route") is True and probe.get("accepts") is True and probe.get("refuses") is True and probe.get("stamp") == "ldo-001" and probe.get("no_version_refused") is True and probe.get("seq_carried") is True and probe.get("acted_guard") is True
    print("CHECK served code: muse.reply routed, real signature accepted, other key refused, bus send stamped ldo-001: %s (%s)" % (c4, probe))
    ok &= c4

    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
