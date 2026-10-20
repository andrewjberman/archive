"""TCKT_VNEXT round 20 -- R20-REL2: the ticket service release carrying the package route's null pair (pdf_ref and commentary_ref null together,
IRPT_ANLREQ v0.24 FWD-1; the CTO's msgs 11065, 11078 and 11099) is LIVE.

Read-only AWS reads (us-east-1): the Lambda configuration and the live code package. Prints REL2-OK <detail> or REL2-BAD <reason>; exit 0/1.
It compares the live CodeSha256 with the release result file the applier writes, requires the environment unchanged, requires the recorded diff of
the built member against the pre-release live member to be exactly the 11 added lines and 0 removed, and reads the SOURCE inside the live package
for the null-pair rule (the artifact, never the applier's claim alone) and for the earlier same-member fence still being present.

  python r20_rel2_check.py             the live check
  python r20_rel2_check.py --self-test the source scan on a good and bad fixtures (no AWS)
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_rel2/R20_REL2_RESULT.json"
FUNCTION = "opal-ticket-api"
AWS = os.path.abspath(".tools/aws.cmd")
BASELINE = "iRxJZYp6IXEtiXDRMT4R/EOwKvsqh5Id5NNgPcpy3RM="

PAIR_LINES = (
    'null_pair = ("pdf_ref", "commentary_ref")',
    'if k in null_pair and k in body and v is None:',
    'partner = null_pair[1] if k == null_pair[0] else null_pair[0]',
    'if partner not in body:',
    'if body[partner] is None:',
)
I7_SKIP = re.compile(r'for k in PACKAGE_I7_FIELDS:[^\n]*\n\s*if body\[k\] is None:\s*\n\s*continue[^\n]*\n\s*if not _is_i7_canonical\(body\[k\]\):')
FENCE = re.compile(r'req_firm\s*=\s*str\(\(cur\.get\("requester"\) or \{\}\)\.get\("firm"\) or ""\)\s*\n'
                   r'\s*if req_firm != str\(\(cur\.get\("answers"\) or \{\}\)\.get\("firm"\) or ""\):')


def package_source(src):
    m = re.search(r"^def package_ticket\(.*?(?=^def |\Z)", src, re.S | re.M)
    return m.group(0) if m else None


def source_problem(src):
    body = package_source(src)
    if body is None:
        return "package_ticket is absent from the source"
    pos = -1
    for line in PAIR_LINES:   # the five lines of the rule, present and in this order (a plain find, no backtracking)
        pos = body.find(line, pos + 1)
        if pos < 0:
            return "the null-pair rule is absent from package_ticket (line not found in order: %s)" % line
    if not re.match(r"if body\[partner\] is None:[ \t]*\n[ \t]*continue[^\n]*\n[ \t]*return _resp\(400,", body[pos:]):
        return "the null-pair rule has no 400 refusal for a lone null right after the both-null continue"
    if not I7_SKIP.search(body):
        return "the I7 skip for a null member is absent from package_ticket"
    if 'k == "original_ref" and k in body and v is None' not in body:
        return "the original_ref I5' rule is gone from package_ticket"
    if not FENCE.search(src):
        return "the earlier same-member fence is gone from the source"
    return None


def aws(*args):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def result_problem(res):
    for k in ("built_from_sha", "code_sha256_before", "code_sha256_after", "change_ledger", "pair", "env_before", "env_after", "diff_added", "diff_removed"):
        if k not in res or res[k] in (None, "", {}):
            if not (k == "diff_removed" and res.get(k) == 0):
                return "the result file lacks %r" % k
    if res["code_sha256_before"] == res["code_sha256_after"]:
        return "the code hash did not change"
    if res["code_sha256_before"] != BASELINE:
        return "the before-hash is not the pair's baseline (a successor release is a STOP in the pair)"
    if res["env_before"] != res["env_after"]:
        return "the environment changed across the release"
    if res["diff_added"] != 11 or res["diff_removed"] != 0:
        return "the recorded diff is %s added and %s removed, not the pair's 11 and 0" % (res["diff_added"], res["diff_removed"])
    return None


def live():
    try:
        res = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("REL2-BAD cannot read the release result file: %s" % e)
        return 1
    why = result_problem(res)
    if why:
        print("REL2-BAD %s" % why)
        return 1
    try:
        fn = aws("lambda", "get-function", "--function-name", FUNCTION)
        cfg = fn["Configuration"]
        pkg = urllib.request.urlopen(fn["Code"]["Location"], timeout=120).read()
        zf = zipfile.ZipFile(io.BytesIO(pkg))
        names = zf.namelist()
        src = zf.read("lambda_function.py").decode("utf-8")
    except (RuntimeError, KeyError, ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as e:
        print("REL2-BAD live read failed: %s" % e)
        return 1
    if names != ["lambda_function.py"]:
        print("REL2-BAD the live package members are %s, not the one member" % names)
        return 1
    if cfg.get("CodeSha256") != res["code_sha256_after"]:
        print("REL2-BAD live CodeSha256 %s is not the recorded after-hash" % cfg.get("CodeSha256"))
        return 1
    if cfg.get("State") != "Active" or cfg.get("LastUpdateStatus") != "Successful":
        print("REL2-BAD the function is %s / %s" % (cfg.get("State"), cfg.get("LastUpdateStatus")))
        return 1
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    if env != res["env_after"]:
        print("REL2-BAD the live environment differs from the recorded one")
        return 1
    why = source_problem(src)
    if why:
        print("REL2-BAD the live package: %s" % why)
        return 1
    print("REL2-OK code_sha256=%s null_pair=present fence=present env=unchanged members=1" % cfg.get("CodeSha256"))
    return 0


GOOD = '''def package_ticket(event, tid):
    null_pair = ("pdf_ref", "commentary_ref")   # v0.24 FWD-1
    for k in PACKAGE_REF_FIELDS + ("firm",):
        v = body.get(k)
        if k == "original_ref" and k in body and v is None:
            continue
        if k in null_pair and k in body and v is None:
            partner = null_pair[1] if k == null_pair[0] else null_pair[0]
            if partner not in body:
                continue   # refused below
            if body[partner] is None:
                continue   # null together
            return _resp(400, {"error": "x"})
    for k in PACKAGE_I7_FIELDS:   # I7
        if body[k] is None:
            continue   # nothing to test
        if not _is_i7_canonical(body[k]):
            return _resp(400, {"error": "y"})


def attachment_open_ticket(event, tid):
    req_firm = str((cur.get("requester") or {}).get("firm") or "")
    if req_firm != str((cur.get("answers") or {}).get("firm") or ""):
        return _resp(404, {})
'''


def good_result():
    return {"built_from_sha": "abc", "code_sha256_before": BASELINE, "code_sha256_after": "NEW=", "change_ledger": "slug", "pair": "p",
            "env_before": {"A": "1"}, "env_after": {"A": "1"}, "diff_added": 11, "diff_removed": 0}


def self_test():
    if source_problem(GOOD) is not None:
        return "good fixture refused: %s" % source_problem(GOOD)
    muts = {
        "pair rule absent": GOOD.replace("if k in null_pair and k in body and v is None:", "if False:"),
        "pair rule lets a lone null through": GOOD.replace("            return _resp(400, {\"error\": \"x\"})\n", "            continue\n"),
        "I7 skip absent": GOOD.replace("        if body[k] is None:\n            continue   # nothing to test\n", ""),
        "I5' rule gone": GOOD.replace('k == "original_ref" and k in body and v is None', "False"),
        "fence gone": GOOD.replace("if req_firm != str((cur.get(\"answers\") or {}).get(\"firm\") or \"\"):", "if False:"),
        "function absent": "def other():\n    return 1\n",
    }
    for name, src in muts.items():
        if source_problem(src) is None:
            return "source mutant not caught: %s" % name
    if result_problem(good_result()) is not None:
        return "good result refused: %s" % result_problem(good_result())
    rmuts = {
        "same hash": lambda r: r.update(code_sha256_after=BASELINE),
        "not the baseline": lambda r: r.update(code_sha256_before="OTHER="),
        "env changed": lambda r: r.update(env_after={"A": "2"}),
        "extra hunk": lambda r: r.update(diff_added=14),
        "a removed line": lambda r: r.update(diff_removed=1),
        "missing ledger": lambda r: r.pop("change_ledger"),
    }
    for name, mut in rmuts.items():
        r = good_result()
        mut(r)
        if result_problem(r) is None:
            return "result mutant not caught: %s" % name
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = self_test()
        print("R20-REL2-SELFTEST-OK" if why is None else "R20-REL2-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
