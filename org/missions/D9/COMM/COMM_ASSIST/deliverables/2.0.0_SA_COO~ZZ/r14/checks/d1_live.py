"""COMM_ASSIST round 14 CA-f-1 AC1: the round-13 package is LIVE, read from AWS, never from a report.

PASS needs all of:
  1. both functions (handler, ingress) carry the same CodeSha256, different from the pre-state SFSTGBQX... (the NFRA_CTLPLN
     TO-APPLY-31 package, built at bde0c0fc90);
  2. the zip the ingress function SERVES (get-function Code.Location, downloaded) hashes to that CodeSha256, and its two
     round-13 files, data/transcripts/scripts/teams_chat/mail_requests.py and channel_mentions.py, are byte-identical (LF) to
     the pin's (git show PIN:<path>);
  3. the SERVED code, imported from the extracted zip, refuses a sixth client firm: firm_domains() on a synthetic registry
     carrying the five plus a sixth returns exactly the five.
Prints one line per check and RESULT: PASS|FAIL. Read-only: get calls and one download.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r14/checks/d1_live.py
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

PIN = "2fd32e12c2"
PRE = "SFSTGBQX3r49t2YXSrN+6t6Ekmz1NrpxkjX09VHLZEM="
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
FILES = ["data/transcripts/scripts/teams_chat/mail_requests.py", "data/transcripts/scripts/teams_chat/channel_mentions.py"]
FIVE = {"cottonwood", "inflection", "49financial", "alongside", "opal"}

PROBE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import mail_requests as m
def firm(k): return {"key": k, "class": "FIRM", "tenant": {"kind": "client", "email_domain": k + ".test"}}
def party(k): return {"party": k, "considered": True, "email_domains": [{"domain": k + ".test", "claim": "measured"}]}
reg = {"scopes": {"scopes": [firm("cottonwood"), firm("inflection"), firm("49financial"), firm("sixthfirm")]},
       "mail_parties": {"mail_parties": [party("alongside"), party("opal")]}}
print(json.dumps(sorted(m.firm_domains(reg))))
'''


def root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                          encoding="utf-8").stdout.strip()


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return None, ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1]
    return json.loads(r.stdout), None


def main():
    os.chdir(root())
    ok = True
    shas = []
    for fn in FUNCS:
        cfg, err = aws("lambda", "get-function-configuration", "--function-name", fn)
        sha = (cfg or {}).get("CodeSha256")
        shas.append(sha)
        print("CHECK %s CodeSha256=%s LastModified=%s %s" % (fn, sha, (cfg or {}).get("LastModified"), err or ""))
    c1 = bool(shas[0]) and shas[0] == shas[1] and shas[0] != PRE
    print("CHECK both functions on one package, not the pre-state: %s" % c1)
    ok &= c1

    fn_doc, err = aws("lambda", "get-function", "--function-name", FUNCS[1])
    url = ((fn_doc or {}).get("Code") or {}).get("Location")
    data = urllib.request.urlopen(url, timeout=60).read() if url else b""
    served = base64.b64encode(hashlib.sha256(data).digest()).decode() if data else None
    c2a = bool(served) and served == shas[1]
    print("CHECK served zip hash equals CodeSha256: %s (%s bytes)" % (c2a, len(data)))
    ok &= c2a

    same = True
    tmp = tempfile.mkdtemp(prefix="comm_r14_d1_")
    if data:
        zipfile.ZipFile(io.BytesIO(data)).extractall(tmp)
    for path in FILES:
        pin_bytes = subprocess.run(["git", "show", "%s:%s" % (PIN, path)], capture_output=True).stdout.replace(b"\r\n", b"\n")
        fp = os.path.join(tmp, *path.split("/"))
        live_bytes = open(fp, "rb").read() if os.path.isfile(fp) else b""
        eq = bool(pin_bytes) and live_bytes == pin_bytes
        print("CHECK served %s == pin %s: %s" % (path, PIN, eq))
        same &= eq
    ok &= same

    keys = None
    if data:
        # cwd=tmp: run from the repo root, `-c` puts the repo first on sys.path and the probe imports the REPO's module
        r = subprocess.run([sys.executable, "-c", PROBE, tmp], capture_output=True, text=True, encoding="utf-8", cwd=tmp)
        try:
            keys = set(json.loads((r.stdout or "").strip().splitlines()[-1]))
        except Exception:  # noqa: BLE001 -- a failed probe reads as a FAIL with its stderr shown
            print("ERROR: probe failed: %s" % (r.stderr or "")[-300:])
    c3 = keys == FIVE
    print("CHECK served code refuses a sixth firm: %s (keys %s)" % (c3, sorted(keys) if keys is not None else None))
    ok &= c3

    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
