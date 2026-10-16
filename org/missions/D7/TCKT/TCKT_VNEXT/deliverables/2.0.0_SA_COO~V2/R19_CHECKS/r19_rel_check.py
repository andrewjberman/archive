"""TCKT_VNEXT round 19 -- R19-REL: the ticket service release for rows S134 items 1-3 is LIVE and reads back as built.

Read-only AWS read (us-east-1) of the Lambda configuration. Prints REL-OK <detail> or REL-BAD <reason>; exit 0/1.
It compares the live configuration with the release result file the applier writes and with the contract values
(decomposition R19, CONTRACT item 5), never with the applier's own claim alone.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_rel/R19_REL_RESULT.json"
MIG = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_mig/R19_MIG_RESULT.json"
FUNCTION = "opal-ticket-api"
AWS = os.path.abspath(".tools/aws.cmd")
INTAKE_FIRMS = "49financial,inflection,cottonwood"


def aws(*args):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def main():
    try:
        res = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("REL-BAD cannot read the release result file: %s" % e)
        return 1
    for k in ("code_sha256_before", "code_sha256_after", "change_ledger", "pair", "mig_result"):
        if not res.get(k):
            print("REL-BAD the result file lacks %r" % k)
            return 1
    if res["code_sha256_before"] == res["code_sha256_after"]:
        print("REL-BAD the code hash did not change")
        return 1
    if not os.path.exists(MIG):
        print("REL-BAD the migration result file is absent: the release must follow the migration")
        return 1
    try:
        cfg = aws("lambda", "get-function-configuration", "--function-name", FUNCTION)
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as e:
        print("REL-BAD live read failed: %s" % e)
        return 1
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    if cfg.get("CodeSha256") != res["code_sha256_after"]:
        print("REL-BAD live CodeSha256 %s is not the recorded after-hash" % cfg.get("CodeSha256"))
        return 1
    try:
        contacts = json.loads(env.get("CLIENT_NOTICE_CONTACT_MAP", ""))
    except ValueError:
        print("REL-BAD CLIENT_NOTICE_CONTACT_MAP is absent or not JSON")
        return 1
    if not isinstance(contacts, dict):
        print("REL-BAD CLIENT_NOTICE_CONTACT_MAP is not a JSON object")
        return 1
    if env.get("ANALYST_INTAKE_ALLOWED_FIRMS") != INTAKE_FIRMS:
        print("REL-BAD ANALYST_INTAKE_ALLOWED_FIRMS is not exactly the three served firms")
        return 1
    print("REL-OK code_sha256=%s contact_map_firms=%d intake_firms=3" % (cfg.get("CodeSha256"), len(contacts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
