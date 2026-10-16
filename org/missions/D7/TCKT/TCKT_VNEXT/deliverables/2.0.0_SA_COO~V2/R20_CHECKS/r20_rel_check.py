"""TCKT_VNEXT round 20 -- R20-REL: the ticket service release carrying the open route's same-member fence (row C-S11) is LIVE.

Read-only AWS reads (us-east-1): the Lambda configuration and the live code package. Prints REL-OK <detail> or REL-BAD <reason>;
exit 0/1. It compares the live CodeSha256 with the release result file the applier writes, keeps the two R19 environment values
as they were, and reads the SOURCE inside the live package for the fence (the artifact, never the applier's claim alone).

  python r20_rel_check.py             the live check
  python r20_rel_check.py --self-test the source scan on a good and two bad fixtures (no AWS)
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_rel/R20_REL_RESULT.json"
FUNCTION = "opal-ticket-api"
AWS = os.path.abspath(".tools/aws.cmd")
INTAKE_FIRMS = "49financial,inflection,cottonwood"

FENCE = re.compile(
    r'req_firm\s*=\s*str\(\(cur\.get\("requester"\) or \{\}\)\.get\("firm"\) or ""\)\s*\n'
    r'\s*if req_firm != str\(\(cur\.get\("answers"\) or \{\}\)\.get\("firm"\) or ""\):\s*\n'
    r'\s*return _resp\(404, \{"error": f"ticket \{tid\} carries no attachment"\}\)\s*\n'
    r'\s*firm = req_firm\s*\n')


def open_route_source(src):
    """The text of attachment_open_ticket, or None."""
    m = re.search(r"^def attachment_open_ticket\(.*?(?=^def |\Z)", src, re.S | re.M)
    return m.group(0) if m else None


def fence_problem(src):
    body = open_route_source(src)
    if body is None:
        return "attachment_open_ticket is absent from the source"
    if not FENCE.search(body):
        return "the same-member fence is absent from attachment_open_ticket"
    if re.search(r'^\s*firm\s*=\s*str\(\(cur\.get\("answers"\)', body, re.M):
        return "firm is still read from answers.firm"
    return None


def aws(*args):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def live():
    try:
        res = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("REL-BAD cannot read the release result file: %s" % e)
        return 1
    for k in ("built_from_sha", "code_sha256_before", "code_sha256_after", "change_ledger", "pair"):
        if not res.get(k):
            print("REL-BAD the result file lacks %r" % k)
            return 1
    if res["code_sha256_before"] == res["code_sha256_after"]:
        print("REL-BAD the code hash did not change")
        return 1
    try:
        fn = aws("lambda", "get-function", "--function-name", FUNCTION)
        cfg = fn["Configuration"]
        pkg = urllib.request.urlopen(fn["Code"]["Location"], timeout=120).read()
        src = zipfile.ZipFile(io.BytesIO(pkg)).read("lambda_function.py").decode("utf-8")
    except (RuntimeError, KeyError, ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as e:
        print("REL-BAD live read failed: %s" % e)
        return 1
    if cfg.get("CodeSha256") != res["code_sha256_after"]:
        print("REL-BAD live CodeSha256 %s is not the recorded after-hash" % cfg.get("CodeSha256"))
        return 1
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    try:
        contacts = json.loads(env.get("CLIENT_NOTICE_CONTACT_MAP", ""))
    except ValueError:
        print("REL-BAD CLIENT_NOTICE_CONTACT_MAP is absent or not JSON")
        return 1
    if not isinstance(contacts, dict) or env.get("ANALYST_INTAKE_ALLOWED_FIRMS") != INTAKE_FIRMS:
        print("REL-BAD the two R19 environment values changed")
        return 1
    why = fence_problem(src)
    if why:
        print("REL-BAD the live package: %s" % why)
        return 1
    print("REL-OK code_sha256=%s fence=present env=unchanged" % cfg.get("CodeSha256"))
    return 0


GOOD = '''def attachment_open_ticket(event, tid):
    att = cur.get("attachment")
    req_firm = str((cur.get("requester") or {}).get("firm") or "")
    if req_firm != str((cur.get("answers") or {}).get("firm") or ""):
        return _resp(404, {"error": f"ticket {tid} carries no attachment"})
    firm = req_firm
    return 1


def other():
    return 2
'''
BAD_OLD = GOOD.replace('    if req_firm != str((cur.get("answers") or {}).get("firm") or ""):\n'
                       '        return _resp(404, {"error": f"ticket {tid} carries no attachment"})\n', "").replace(
    "    firm = req_firm\n", '    firm = str((cur.get("answers") or {}).get("firm") or "")\n')


def self_test():
    if fence_problem(GOOD) is not None:
        return "good fixture refused: %s" % fence_problem(GOOD)
    if fence_problem(BAD_OLD) is None:
        return "the old source was not caught"
    if fence_problem("def nothing(): pass\n") is None:
        return "a missing function was not caught"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = self_test()
        print("R20-REL-SELFTEST-OK" if why is None else "R20-REL-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
