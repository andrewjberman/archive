"""CA-p-2 AC1 (and, with P2_MODE=live, AC2): the package that ships is the live package plus CA-p-1, and nothing else moves.

equiv (default): the BUILT package (a detached worktree at N2_PIN with `bash infra/aws/lambda/teams-chat-assist/build.sh` run in
  it: dist/pkg) is compared with the zip the live ingress function serves NOW. Arms:
  (a) the file sets are equal (no file only in one of them);
  (b) the files that differ are exactly CHANGED (mail_requests.py) plus, at most, the FOREIGN set (files other seats
      changed between the live pin 1aa63bde67 and P2_PIN, set measured at the first pre-flight, see FOREIGN), printed;
  (c) the built mail_requests.py is byte-equal to the pin's (LF);
  (d) the 17-probe battery of check_l4_equiv.py (S3 addresses for five chats and the mail parties) gives identical output from
      the built package and the live zip (the foreign rows move no address the assistant forms);
  (e) the issuer's P1 arms (r22/checks/check_p1_self_mail.py, P1_ROOT = the built package) read 6 of 6.
live (N2_MODE=live): both functions carry ONE CodeSha256, not PRE; the served zip hashes to it; the served file set equals the
  pin's build list above; the served mail_requests.py equals the pin's; both environments carry INGRESS_MARK_MODE=enforce and
  exactly the fifteen key names recorded; the P1 arms read 6 of 6 against the SERVED zip; the 17 probes equal the PRE package's.
Prints:  P2-EQUIV|P2-LIVE ok=<True|False> differ=<n> foreign=<n> probes=<n> same=<n> p1=<k of 6> reason=<text>
Needs: env P2_PIN; for equiv a detached worktree at N2_PIN with build.sh run in it. Read-only: get-function and downloads.
Finds the repository from the current directory's git toplevel, never from this file's location.
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

PIN = os.environ.get("P2_PIN", "")
MODE = os.environ.get("P2_MODE", "equiv")
PRE = "RoH5DIiH/lWEutB+Qb3CswFUB402LhOjbx6P5sbk2DE="     # the CA-n-2 package, built at 1aa63bde67, live at this write
FUNCS = ["teams-global-chat-assist-handler-lambda", "teams-global-chat-assist-ingress-lambda"]
CHANGED = "data/transcripts/scripts/teams_chat/mail_requests.py"
REG = "infra/logic/registry/"
FOREIGN = sorted([REG + "exemptions.json", REG + "legacy_addresses.json", "lib/opal_naming.py", "org/standards/NAMING_SCHEMA.json"])   # measured 2026-10-19 on the pin e6c37673c8 against the live CA-n-2 package
KEYS = sorted(["GATEWAY_BASE", "IGNORE_NAMES", "INGRESS_MARK_MODE", "LDO_ALARM_PREFIX", "LDO_ALARM_ROLE_ARN", "LDO_ARCHIVE_BUCKET",
               "LDO_DEDUP_DAYS", "LDO_ID", "LDO_KMS_KEY_ARN", "LDO_MAILBOX_ARN", "LDO_MAILBOX_URL", "LDO_TABLE",
               "MAIL_BEARER_SECRET", "MUSE_ANSWER_PUBKEY", "SMS_ORIGINATION"])
P1 = "org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r22/checks/check_p1_self_mail.py"

PROBE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
from data.transcripts.scripts.teams_chat import assist as a, mail_requests as mr
out = {"BUCKET": a.BUCKET}
try:
    out["firms"] = json.dumps({k: sorted(v) if isinstance(v, (list, set, tuple)) else v for k, v in mr.firm_domains().items()}, sort_keys=True, default=str)
except Exception as exc:
    out["firms"] = "ERR %s" % type(exc).__name__
for i, cid in enumerate(["19:abc@unq.gbl.spaces", "19:meeting_XYZ@thread.v2", "eod:2026-10-13", "job:J290", "mail:owner"]):
    out["state_%d" % i] = a.state_key("x_%d.json" % i)
    out["silver_%d" % i] = a.silver_key(cid, "context.md")
    out["bronze_%d" % i] = a.bronze_key(cid, {"created": "2026-10-13T20:13:51Z", "id": "m%d" % i})
print(json.dumps(out, sort_keys=True))
'''


def root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip() or os.getcwd()


ROOT = root()


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, cwd=ROOT).stdout


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--region", "us-east-1", "--output", "json"], capture_output=True, text=True,
                       encoding="utf-8", timeout=90)
    return json.loads(r.stdout) if r.returncode == 0 else None


def pinned_worktree():
    block = []
    for line in git("worktree", "list", "--porcelain").decode("utf-8", "replace").splitlines() + [""]:
        if line:
            block.append(line)
            continue
        head = next((b[5:] for b in block if b.startswith("HEAD ")), "")
        if "detached" in block and PIN and head.startswith(PIN):
            return next(b[9:] for b in block if b.startswith("worktree "))
        block = []
    return None


def files_of(path):
    out = {}
    for base, dirs, names in os.walk(path):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in names:
            if not n.endswith(".pyc"):
                p = os.path.join(base, n)
                out[os.path.relpath(p, path).replace(os.sep, "/")] = Path(p).read_bytes()
    return out


def zip_files(data):
    zf = zipfile.ZipFile(io.BytesIO(data))
    return {i.filename: zf.read(i.filename) for i in zf.infolist() if not i.is_dir()}, zf


def probe(path):
    r = subprocess.run([sys.executable, "-c", PROBE, path], capture_output=True, text=True, cwd=path, timeout=100)
    return json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip() else {"ERROR": (r.stderr or "")[-200:]}


def p1(path):
    env = dict(os.environ, P1_ROOT=path)
    r = subprocess.run([sys.executable, os.path.join(ROOT, P1)], capture_output=True, text=True, cwd=ROOT, env=env, timeout=120)
    last = (r.stdout.strip().splitlines() or [""])[-1]
    return last.split("arms=")[-1] if "arms=" in last else "ERROR " + (r.stderr or "")[-120:]


def live_zip(func):
    doc = aws("lambda", "get-function", "--function-name", func)
    url = ((doc or {}).get("Code") or {}).get("Location")
    if not url:
        raise RuntimeError("could not read %s's code location" % func)
    return doc, urllib.request.urlopen(url, timeout=60).read()


def main():
    differ_n = probes = same = 0
    foreign, n1_read, why = [], "-", ""
    tag = "P2-LIVE" if MODE == "live" else "P2-EQUIV"
    try:
        if not PIN:
            raise RuntimeError("P2_PIN is not set")
        pin_cm = git("show", "%s:%s" % (PIN, CHANGED)).replace(b"\r\n", b"\n")
        if not pin_cm:
            raise RuntimeError("the pin %s holds no %s" % (PIN, CHANGED))
        problems = []
        if MODE == "live":
            docs = [live_zip(f) for f in FUNCS]
            hashes = [d["Configuration"]["CodeSha256"] for d, _ in docs]
            if len(set(hashes)) != 1 or hashes[0] == PRE:
                problems.append("hashes %s: want one, not PRE" % hashes)
            data = docs[1][1]
            if base64.b64encode(hashlib.sha256(data).digest()).decode() != hashes[1]:
                problems.append("the served zip does not hash to its CodeSha256")
            for d, _ in docs:
                env = (d["Configuration"].get("Environment") or {}).get("Variables") or {}
                if env.get("INGRESS_MARK_MODE") != "enforce" or sorted(env) != KEYS:
                    problems.append("%s: mode %s, key names %s" % (d["Configuration"]["FunctionName"],
                                                                   env.get("INGRESS_MARK_MODE"), sorted(env)))
            new, zf = zip_files(data)
            if new.get(CHANGED, b"").replace(b"\r\n", b"\n") != pin_cm:
                problems.append("(c) the served mail_requests.py is not the pin's")
            with tempfile.TemporaryDirectory() as tmp:
                zf.extractall(tmp)
                n1_read = p1(tmp)
                served_p = probe(tmp)
            pre_p = json.loads(os.environ.get("P2_PRE_PROBES", "null") or "null")
            if pre_p:
                probes = len(served_p)
                same = sum(1 for k in served_p if served_p[k] == pre_p.get(k))
                if probes != 17 or same != probes:
                    problems.append("(d) probes %d, same %d" % (probes, same))
            else:
                probes = len(served_p)
                same = probes if "ERROR" not in served_p else 0
                if probes != 17 or "ERROR" in served_p:
                    problems.append("(d) served probes: %s" % str(served_p)[:120])
        else:
            wt = pinned_worktree()
            if not wt:
                raise RuntimeError("no detached worktree at the pin %s" % PIN)
            pkg = Path(wt) / "infra" / "aws" / "lambda" / "teams-chat-assist" / "dist" / "pkg"
            if not pkg.is_dir():
                raise RuntimeError("no built package at %s" % pkg)
            _, data = live_zip(FUNCS[1])
            live, zf = zip_files(data)
            built = files_of(str(pkg))
            only = sorted(set(live) ^ set(built))
            if only:
                problems.append("(a) files in one only: %s" % only[:6])
            differ = sorted(n for n in set(live) & set(built) if live[n] != built[n])
            differ_n = len(differ)
            foreign = [n for n in differ if n in FOREIGN]
            other = [n for n in differ if n not in FOREIGN and n != CHANGED]
            if CHANGED not in differ or other:
                problems.append("(b) differ %s: want mail_requests.py plus at most the foreign set" % differ[:8])
            if foreign:
                print("FOREIGN packaged files that differ (%d): %s" % (len(foreign), foreign))
            if built.get(CHANGED, b"").replace(b"\r\n", b"\n") != pin_cm:
                problems.append("(c) the built mail_requests.py is not the pin's")
            with tempfile.TemporaryDirectory() as tmp:
                zf.extractall(tmp)
                live_p, built_p = probe(tmp), probe(str(pkg))
            print("PRE-PROBES %s" % json.dumps(live_p, sort_keys=True))
            if "ERROR" in live_p or "ERROR" in built_p:
                problems.append("(d) probe failed: live=%s built=%s" % (str(live_p)[:120], str(built_p)[:120]))
            else:
                probes = len(built_p)
                same = sum(1 for k in built_p if built_p[k] == live_p.get(k))
                if probes != 17 or same != probes:
                    problems.append("(d) probes %d, same %d" % (probes, same))
            n1_read = p1(str(pkg))
        if n1_read != "6 of 6":
            problems.append("(e) P1 arms %s" % n1_read)
        why = "; ".join(problems)
    except Exception as exc:  # noqa: BLE001 -- any failure reads as ok=False with its reason
        why = "%s: %s" % (type(exc).__name__, str(exc)[:240])
    print("%s ok=%s differ=%d foreign=%d probes=%d same=%d p1=%s reason=%s"
          % (tag, not why, differ_n, len(foreign), probes, same, n1_read, why or "none"))
    return 0 if not why else 1


if __name__ == "__main__":
    sys.exit(main())
