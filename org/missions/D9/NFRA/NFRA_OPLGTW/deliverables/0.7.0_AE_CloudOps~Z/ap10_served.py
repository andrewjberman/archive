"""OG-ap-10 PHASE B2 step 6 -- the SERVED read, through the INSTALLED code on the host.

usage:  python ap10_served.py <out.json>

Writes W/AP10_SERVED.json = {"body": {...}} with the five fields the order names:
  tool_takes_extension, market_update_root_equals_address, bad_extension_refused,
  objects_written, fee_root_unchanged.

NO REAL .pptx PUT. The first real deck is ADVI_BILLING's (dell2) use, so this reads the installed
code's own contract and writes nothing: `objects_written` is 0 BY CONSTRUCTION (no put_object call
is made anywhere in this program) and is corroborated afterwards by a caller-side S3 list.

WHY ONLY A BOOLEAN CROSSES FOR THE ROOTS. The order says to compare the value on the host and print
only the boolean. This program never prints either root: it sha256s the host's .env value and
compares that digest to one computed in the repo from `lib.opal_naming address()`, which is passed
in. So the comparison is exact, and no S3 address or .env value leaves the host in the output.

WHY THE BAD-EXTENSION ARM IS SOUND. site_to_s3._pair() raises SiteToS3Refused for any extension
outside PAIRS, and it is reached BEFORE the Graph fetch -- so the refusal is genuinely pre-read,
not a late failure after bytes moved. This program proves the ordering two ways: _pair(".docx")
alone raises, and the full entry function called with extension=".docx" raises the SAME refusal
while being handed a token and ids that would fail loudly if any fetch had been attempted.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time

INST = "i-07dccb1615503ac99"
HERE = os.path.dirname(os.path.abspath(__file__))

HOST_PROG = r'''
import hashlib, inspect, json, os, sys
sys.path.insert(0, "/opt/opal-gateway")
R = {}

def dig(s):
    return hashlib.sha256((s or "").encode("utf-8")).hexdigest()

# --- the two roots, read from the INSTALLED .env; only digests are kept ------------------
env = {}
try:
    import re as _re
    with open("/opt/opal-gateway/.env", encoding="utf-8") as fh:
        for ln in fh:
            # EXACTLY ap10_verify.py's capture: the RAW value after '=', quotes and all. A
            # different normalisation here would make the two instruments' digests
            # incomparable, which is the bug this line replaced.
            m = _re.match(r"^([A-Z0-9_]+)=(.*)$", ln.rstrip("\n").rstrip("\r"))
            if m:
                env[m.group(1)] = m.group(2)
    R["env_read"] = True
except Exception as e:
    R["env_read"] = False
    R["env_error"] = type(e).__name__

mu = env.get("ADVI_MARKET_UPDATE_S3_ROOT", "")
fee = env.get("ADVI_FEE_STATEMENT_S3_ROOT", "")
R["market_update_root_present"] = bool(mu)
R["market_update_root_digest"] = dig(mu) if mu else None
R["fee_root_present"] = bool(fee)
R["fee_root_digest"] = dig(fee) if fee else None
R["market_update_root_shape_ok"] = mu.endswith("/bronze/market_update/")

# --- the tool signature, from the INSTALLED app.tools -----------------------------------
os.environ.setdefault("MOCK_GRAPH", "1")
try:
    from app import tools as T
    fn = getattr(T, "copy_site_file_to_s3", None)
    if fn is None:
        R["tool_takes_extension"] = False
        R["tool_present"] = False
    else:
        R["tool_present"] = True
        params = list(inspect.signature(fn).parameters)
        R["tool_params"] = params
        R["tool_takes_extension"] = "extension" in params
except Exception as e:
    R["tool_takes_extension"] = False
    R["tool_import_error"] = type(e).__name__ + ": " + str(e)[:200]

# --- the bad-extension arm: refused BEFORE any read -------------------------------------
try:
    from app.integrations.advi_billing import site_to_s3 as S
    R["pairs_admitted"] = sorted(getattr(S, "PAIRS", {}))
    # (a) the guard itself
    try:
        S._pair(".docx")
        R["pair_docx_raised"] = False
    except Exception as e:
        R["pair_docx_raised"] = type(e).__name__ == "SiteToS3Refused"
        R["pair_docx_error"] = str(e)[:160]
    # (b) the full entry function, handed credentials that would fail LOUDLY if it ever fetched
    def _never(*a, **k):
        raise AssertionError("REACHED THE NETWORK -- the refusal was NOT pre-read")
    try:
        S.copy_site_file_to_s3("sentinel-token-not-a-real-token", "sentinel-site", "sentinel-item",
                               "2026-10-12", extension=".docx", graph_call=_never, s3_client=None)
        R["entry_docx_raised"] = False
    except AssertionError as e:
        R["entry_docx_raised"] = False
        R["entry_docx_reached_network"] = True
        R["entry_docx_error"] = str(e)[:160]
    except Exception as e:
        R["entry_docx_raised"] = type(e).__name__ == "SiteToS3Refused"
        R["entry_docx_error"] = type(e).__name__ + ": " + str(e)[:160]
        R["entry_docx_reached_network"] = False
    # (c) the .pptx pair is admitted and keys on date=, with the quarter arg NOT naming the key
    try:
        p = S._pair(".pptx")
        R["pptx_partition_label"] = getattr(p, "partition_label", None)
    except Exception as e:
        R["pptx_partition_label"] = "ERR:" + type(e).__name__
except Exception as e:
    R["site_to_s3_import_error"] = type(e).__name__ + ": " + str(e)[:200]

R["objects_written"] = 0   # BY CONSTRUCTION: this program calls no put_object
print("SERVEDJSON " + json.dumps(R))
'''


def aws(args):
    return subprocess.run(["bash", "-c", 'aws "$@"', "x"] + args,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def ssm_run(commands, comment, polls=60, wait=3):
    pf = os.path.join(os.environ.get("TEMP", "/tmp"), "og_ap10_served_%d.json" % os.getpid())
    with open(pf, "w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(json.dumps({"commands": commands, "executionTimeout": ["1800"]}))
    r = aws(["ssm", "send-command", "--instance-ids", INST, "--document-name", "AWS-RunShellScript",
             "--comment", comment, "--parameters", "file://" + pf.replace(chr(92), "/"),
             "--region", "us-east-1", "--query", "Command.CommandId", "--output", "text"])
    os.remove(pf)
    if r.returncode != 0:
        print("SEND FAIL " + r.stderr.strip()[:300])
        sys.exit(2)
    cid = r.stdout.strip()
    st = ""
    for _ in range(polls):
        time.sleep(wait)
        st = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST,
                  "--region", "us-east-1", "--query", "Status", "--output", "text"]).stdout.strip()
        if st in ("Success", "Failed", "Cancelled", "TimedOut"):
            break
    out = aws(["ssm", "get-command-invocation", "--command-id", cid, "--instance-id", INST,
               "--region", "us-east-1", "--query", "StandardOutputContent", "--output", "text"]).stdout
    print("ssm %s status=%s" % (cid, st))
    return st, out.replace(chr(13), ""), cid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    a = ap.parse_args()

    expect_mu = open(os.path.join(HERE, "ap10_expected_root_sha.txt"), encoding="utf-8").read().strip()
    expect_fee_addr = open(os.path.join(HERE, "ap10_expected_fee_sha.txt"), encoding="utf-8").read().strip()

    # fee_root_unchanged means UNCHANGED ACROSS THIS DEPLOY, not "equals an address() I recomputed".
    # The first version of this program asserted the latter and read FALSE on a deploy that had
    # changed nothing -- the wrong oracle, not a regression. The sound comparison is this host's
    # CURRENT digest against the SAME host's digest in the before-state read, both sha256 of the raw
    # .env value, which is also what ap10_verify.py compared when it read "changed []" over 53 keys.
    before_state = os.path.join(HERE, "ap10_state_before.json")
    B = json.load(open(before_state, encoding="utf-8"))
    fee_before = (B.get("env_hashes") or {}).get("ADVI_FEE_STATEMENT_S3_ROOT")

    b64 = base64.b64encode(HOST_PROG.encode("utf-8")).decode("ascii")
    tmp = "/tmp/og_ap10_served_%d.py" % os.getpid()
    st, out, cid = ssm_run(["echo %s | base64 -d > %s" % (b64, tmp),
                            "/opt/opal-gateway/.venv/bin/python " + tmp, "rm -f " + tmp,
                            "echo LEFTOVER=$(ls /tmp/og_ap10_served_* 2>/dev/null | wc -l)"],
                           "OG-ap-10 served read")
    line = [x for x in out.split(chr(10)) if x.startswith("SERVEDJSON ")]
    if st != "Success" or not line:
        print("SERVED READ FAILED")
        print(out[-900:])
        sys.exit(2)
    print([x for x in out.split(chr(10)) if x.startswith("LEFTOVER=")])
    H = json.loads(line[0][len("SERVEDJSON "):])

    body = {
        "tool_takes_extension": bool(H.get("tool_takes_extension")),
        "market_update_root_equals_address": bool(
            H.get("market_update_root_digest") and H["market_update_root_digest"] == expect_mu),
        "bad_extension_refused": bool(H.get("pair_docx_raised")) and bool(H.get("entry_docx_raised")),
        "objects_written": H.get("objects_written"),
        "fee_root_unchanged": bool(
            H.get("fee_root_digest") and fee_before and H["fee_root_digest"] == fee_before),
    }
    rec = {
        "body": body,
        "method": ("one SSM read through the INSTALLED code at /opt/opal-gateway; no real .pptx put, "
                   "no put_object call anywhere in the program"),
        "ssm_command_id": cid,
        "root_comparison": ("sha256 of the host's .env value against sha256 of lib.opal_naming "
                            "address() output computed in the repo; NEITHER value is printed here"),
        "market_update_root_shape_ok": H.get("market_update_root_shape_ok"),
        "pairs_admitted": H.get("pairs_admitted"),
        "pptx_partition_label": H.get("pptx_partition_label"),
        "bad_extension_detail": {
            "guard_pair_docx_raised_SiteToS3Refused": H.get("pair_docx_raised"),
            "entry_fn_docx_raised_SiteToS3Refused": H.get("entry_docx_raised"),
            "entry_fn_reached_the_network": H.get("entry_docx_reached_network"),
            "note": ("the entry call was handed a sentinel token and a `call` that RAISES if used, "
                     "so a refusal that happened after a fetch would surface as "
                     "AssertionError, not SiteToS3Refused"),
            "error": H.get("entry_docx_error"),
        },
        "tool_params": H.get("tool_params"),
        "fee_root_detail": {
            "predicate": "UNCHANGED across this deploy (host digest now == host digest in the before-state)",
            "digest_now_equals_before": bool(
                H.get("fee_root_digest") and fee_before and H["fee_root_digest"] == fee_before),
            "corroborated_by": ("ap10_verify.py's 'every .env value digest unchanged' limb, which read "
                                "equal 53 of 53, changed [] -- the fee root is one of those 53"),
            "ALSO_OBSERVED_not_a_trigger": (
                "The live fee root does NOT equal address('sharepoint','transcripts','bronze',"
                "'fee_statement','quarter=X') minus its partition: sha256 %s (live, unchanged) vs %s "
                "(that address call). This is RECORDED, NOT asserted as a defect -- this seat may "
                "simply have used the wrong arguments for the fee pair, and OG-ap-10 neither sets nor "
                "reads that root. It is named so nobody later reads this file's True as a claim that "
                "the fee root matches the builder." % (str(H.get("fee_root_digest"))[:16],
                                                      expect_fee_addr[:16])),
        },
    }
    json.dump(rec, open(a.out, "w", encoding="utf-8"), indent=1)
    print(json.dumps(body, indent=1))
    ok = (body["tool_takes_extension"] and body["market_update_root_equals_address"]
          and body["bad_extension_refused"] and body["objects_written"] == 0
          and body["fee_root_unchanged"])
    print("SERVED %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


sys.exit(main())
