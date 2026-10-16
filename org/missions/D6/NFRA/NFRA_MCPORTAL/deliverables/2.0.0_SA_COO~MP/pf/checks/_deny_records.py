"""MP-v-2 gate read (the issuer's, READ-ONLY): do the email_deny records exist for the named accounts?
Ruling: CTO msg 35204 (@e511fa0194): (b) removes the records of andrew@opalinvest.com and opalbloomberg@opalinvest.com only; alyssa@opalinvest.com stays.
Prints counts and yes/no only: never a key, a digest, an email's record body, a tenant id or an object id.
usage: python _deny_records.py   (run from any cwd; resolves the repo from this file's location)
exit 0 when the table scan is complete (the verdict is the printed lines), 2 when it is not."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, *([".."] * 9)))      # checks > pf > 2.0.0_SA_COO~MP > deliverables > NFRA_MCPORTAL > NFRA > D6 > missions > org > workspace root
sys.path.insert(0, os.path.join(WS, "infra", "aws", "ec2", "opal-gateway"))
from app import access_state as acs  # noqa: E402

ACCOUNTS = [("andrew@opalinvest.com", "removed by (b)"), ("opalbloomberg@opalinvest.com", "removed by (b)"),
            ("alyssa@opalinvest.com", "must stay")]
want = {e: acs.email_deny_key(e).pk for e, _ in ACCOUNTS}
aws = os.path.join(WS, ".tools", "aws.cmd") if os.name == "nt" else os.path.join(WS, ".tools", "aws")
tmp = os.path.join(os.environ.get("TMPDIR", os.environ.get("TEMP", "/tmp")), "_deny_records_key.json")


def main():
    pks, start, pages = set(), None, 0
    while True:
        cmd = [aws, "dynamodb", "scan", "--table-name", "gateway-access-state-table", "--region", "us-east-1",
               "--projection-expression", "#p", "--expression-attribute-names", '{"#p":"pk"}',
               "--filter-expression", "begins_with(#p, :x)", "--expression-attribute-values", '{":x":{"S":"POLICY#EMAILDENY#"}}',
               "--no-paginate", "--output", "json"]
        if start:
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(start))
            cmd += ["--exclusive-start-key", "file://" + tmp.replace("\\", "/")]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if out.returncode != 0:
            print("SCAN FAILED rc=%d: %s" % (out.returncode, out.stderr.strip()[:160]))
            return 2
        d = json.loads(out.stdout)
        pages += 1
        pks.update(it["pk"]["S"] for it in d.get("Items", []))
        start = d.get("LastEvaluatedKey")
        if not start or pages >= 60:
            break
    if os.path.exists(tmp):
        os.remove(tmp)
    complete = not start
    print("emaildeny scan: pages=%d records=%d complete=%s" % (pages, len(pks), "yes" if complete else "NO"))
    for e, note in ACCOUNTS:
        print("%s: deny record %s (%s)" % (e, "PRESENT" if want[e] in pks else "absent", note))
    return 0 if complete else 2


if __name__ == "__main__":
    sys.exit(main())
