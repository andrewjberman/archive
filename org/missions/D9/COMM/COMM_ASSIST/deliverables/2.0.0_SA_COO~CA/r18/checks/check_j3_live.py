"""CA-j-3 AC2: the round-18 package, the ingress-mark secret and INGRESS_MARK_MODE=record are LIVE, read from AWS, never from a report.

PASS needs all of:
  1. both functions carry the same CodeSha256, different from the pre-state (PRE);
  2. the zip the ingress function SERVES hashes to that CodeSha256 and its files (tenant.py, ingress_mark.py, NAMES.json, assist.py, mail_requests.py, muse_verify.py) are byte-identical (LF) to J3_PIN's;
  3. BOTH environments carry INGRESS_MARK_MODE == "record", and MUSE_ANSWER_PUBKEY (fingerprint as recorded), MAIL_BEARER_SECRET and SMS_ORIGINATION unchanged;
  4. the secret teams/global/ingress-mark exists and has a current VERSION (describe-secret; its value is NEVER read), and for each function's execution role
     iam simulate-principal-policy says secretsmanager:GetSecretValue on that secret is allowed;
  5. the SERVED code, imported from the extracted zip: stamp/verify round-trip "ok" with a throwaway secret, a tampered payload reads "bad-mark", an unset mode is off, "record" and "enforce" parse, a typo raises;
     the secret NAME comes from the NAMES row.
Prints one line per check and RESULT: PASS|FAIL. Read-only: get/describe/simulate calls and one download. Needs env J3_PIN.
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

PIN = os.environ.get("J3_PIN", "")
PRE = "sWltfUwyJQpANEhbY+KFkszo8ScLKEIi7Lm4qyUNWrM="
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
FILES = ["data/transcripts/scripts/teams_chat/tenant.py", "data/transcripts/scripts/teams_chat/ingress_mark.py", "data/transcripts/scripts/teams_chat/NAMES.json",
         "data/transcripts/scripts/teams_chat/assist.py", "data/transcripts/scripts/teams_chat/mail_requests.py", "data/transcripts/scripts/teams_chat/muse_verify.py"]
FP = "SHA256:oq0WqfmN1I15uxqNGuoN64t+SubEBfmPINUyLgqFBRQ"
MAIL_ARN = "arn:aws:secretsmanager:us-east-1:313476888478:secret:gateway/mail/commassist-bearer-cPYbR3"
SMS = "arn:aws:sms-voice:us-east-1:313476888478:phone-number/phone-0e98f7739a16415c83d951336a7da12a"
SECRET = "teams/global/ingress-mark"

PROBE = r'''
import datetime, json, os, sys
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import assist as a, ingress_mark as im, tenant as t
out = {"name": a.NAMES["secrets"].get("ingress_mark")}
now = datetime.datetime(2026, 10, 14, 4, 0, tzinfo=datetime.timezone.utc)
p = im.stamp("throwaway-secret", "obj", "sms.reply", {"tag": "C1", "action": "send"}, now)
out["roundtrip"] = im.verify("throwaway-secret", "obj", "sms.reply", p, now) == "ok"
q = dict(p, action="drop")
out["tamper"] = im.verify("throwaway-secret", "obj", "sms.reply", q, now) == "bad-mark"
os.environ.pop("INGRESS_MARK_MODE", None)
out["unset_off"] = t._mark_mode() == "off"
os.environ["INGRESS_MARK_MODE"] = "record"
out["record"] = t._mark_mode() == "record"
os.environ["INGRESS_MARK_MODE"] = "enforce"
out["enforce"] = t._mark_mode() == "enforce"
os.environ["INGRESS_MARK_MODE"] = "enfroce"
try:
    t._mark_mode()
    out["typo_raises"] = False
except ValueError:
    out["typo_raises"] = True
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
    if not PIN:
        print("ERROR: J3_PIN is not set")
        print("RESULT: FAIL")
        return 1
    shas, envs, roles = [], [], []
    for fn in FUNCS:
        cfg, err = aws("lambda", "get-function-configuration", "--function-name", fn)
        shas.append((cfg or {}).get("CodeSha256"))
        envs.append(((cfg or {}).get("Environment") or {}).get("Variables") or {})
        roles.append((cfg or {}).get("Role"))
        print("CHECK %s CodeSha256=%s LastModified=%s %s" % (fn, shas[-1], (cfg or {}).get("LastModified"), err or ""))
    c1 = bool(shas[0]) and shas[0] == shas[1] and shas[0] != PRE
    print("CHECK both functions on one package, not the pre-state: %s" % c1)
    ok &= c1

    doc, err = aws("lambda", "get-function", "--function-name", FUNCS[1])
    url = ((doc or {}).get("Code") or {}).get("Location")
    data = urllib.request.urlopen(url, timeout=60).read() if url else b""
    served = base64.b64encode(hashlib.sha256(data).digest()).decode() if data else None
    c2 = bool(served) and served == shas[1]
    tmp = tempfile.mkdtemp(prefix="comm_r18_j3_")
    if data:
        zipfile.ZipFile(io.BytesIO(data)).extractall(tmp)
    same = True
    for path in FILES:
        pin_bytes = subprocess.run(["git", "show", "%s:%s" % (PIN, path)], capture_output=True).stdout.replace(b"\r\n", b"\n")
        fp = os.path.join(tmp, *path.split("/"))
        eq = bool(pin_bytes) and os.path.isfile(fp) and open(fp, "rb").read() == pin_bytes
        print("CHECK served %s == pin %s: %s" % (path, PIN, eq))
        same &= eq
    print("CHECK served zip hash equals CodeSha256: %s (%s bytes); %d files equal the pin: %s" % (c2, len(data), len(FILES), same))
    ok &= c2 and same

    c3 = True
    for fn, env in zip(FUNCS, envs):
        good = (env.get("INGRESS_MARK_MODE") == "record" and fingerprint(env.get("MUSE_ANSWER_PUBKEY")) == FP
                and env.get("MAIL_BEARER_SECRET") == MAIL_ARN and env.get("SMS_ORIGINATION") == SMS)
        print("CHECK %s environment: INGRESS_MARK_MODE=record, muse key fingerprint, mail secret and sms origination as recorded: %s" % (fn, good))
        c3 &= good
    ok &= c3

    sec, err = aws("secretsmanager", "describe-secret", "--secret-id", SECRET)
    arn = (sec or {}).get("ARN")
    stages = [s for v in ((sec or {}).get("VersionIdsToStages") or {}).values() for s in v]
    c4 = bool(arn) and "AWSCURRENT" in stages
    print("CHECK secret %s exists with a current version (value not read): %s %s" % (SECRET, c4, err or ""))
    for fn, role in zip(FUNCS, roles):
        sim, err = aws("iam", "simulate-principal-policy", "--policy-source-arn", role or "none", "--action-names", "secretsmanager:GetSecretValue",
                       "--resource-arns", arn or "none")
        allowed = bool(sim) and all(r.get("EvalDecision") == "allowed" for r in sim.get("EvaluationResults", [])) and bool(sim.get("EvaluationResults"))
        print("CHECK %s role may read the secret (simulate): %s %s" % (fn, allowed, err or ""))
        c4 &= allowed
    ok &= c4

    probe = None
    if data:
        r = subprocess.run([sys.executable, "-c", PROBE, tmp], capture_output=True, text=True, encoding="utf-8", cwd=tmp, timeout=100)
        try:
            probe = json.loads((r.stdout or "").strip().splitlines()[-1])
        except Exception:  # noqa: BLE001 -- a failed probe reads as a FAIL with its stderr shown
            print("ERROR: probe failed: %s" % (r.stderr or "")[-300:])
    keys = ("roundtrip", "tamper", "unset_off", "record", "enforce", "typo_raises")
    c5 = bool(probe) and probe.get("name") == SECRET and all(probe.get(k) is True for k in keys)
    print("CHECK served code: secret name from the NAMES row, mark round trip, tamper refused, modes parse, typo raises: %s (%s)" % (c5, probe))
    ok &= c5

    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
