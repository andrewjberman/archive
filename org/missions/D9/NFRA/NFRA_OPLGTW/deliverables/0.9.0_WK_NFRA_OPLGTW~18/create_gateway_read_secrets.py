"""OG-pr-1 (NFRA_OPLGTW.TO-OG-pr-1): create the three gateway read secrets, out of band, so no value enters TF state.

Secrets (us-east-1):
  gateway/transcripts/bearer   -- secrets.token_hex(32)
  gateway/mail/bearer          -- secrets.token_hex(32)
  gateway/principals/rosters   -- JSON {"master_admin": "<tid>/<oid>", "write_capable": "<tid>/<oid>,<tid>/<oid>"}
                                  built from the site-Z Part D file (PART_D_RECORD_20260930.md).

Every value is built in memory. Prints ONLY each ARN and the roster pair counts -- never a value.
Refuses (exit 2, nothing created) if a secret of any of the three names already exists.

usage: python create_gateway_read_secrets.py [--dry-run] [<part_d_json_path>]
  --dry-run  builds and shape-checks the values, prints counts, touches no AWS API.
"""
import json
import os
import re
import secrets
import sys

REGION = "us-east-1"
ORDER = "NFRA_OPLGTW.TO-OG-pr-1 (principal-rosters-secret)"
BEARERS = ["gateway/transcripts/bearer", "gateway/mail/bearer"]
ROSTERS = "gateway/principals/rosters"
GUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
ADMIN_KEY = "andrew@opalinvest.com"
WRITE_KEYS = ["alyssa@opalinvest.com", "opalbloomberg@opalinvest.com"]


def build_rosters(path):
    with open(path, encoding="utf-8") as f:
        vals = json.load(f)["values"]
    tid = vals["tenant_id"]
    oids = [vals[ADMIN_KEY]] + [vals[k] for k in WRITE_KEYS]
    if not all(GUID.match(x) for x in [tid] + oids) or len(set([tid] + oids)) != 4:
        raise SystemExit("ERROR: Part D file values are not 4 distinct GUIDs")
    master = "%s/%s" % (tid, vals[ADMIN_KEY])
    write = ",".join("%s/%s" % (tid, vals[k]) for k in WRITE_KEYS)
    return json.dumps({"master_admin": master, "write_capable": write}), 1, len(WRITE_KEYS)


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if not a.startswith("--")]
    path = args[0] if args else os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-principals", "part_d_20260930.json")
    values = {n: secrets.token_hex(32) for n in BEARERS}
    values[ROSTERS], n_master, n_write = build_rosters(path)
    print("roster pair counts: master %d write %d" % (n_master, n_write))
    if dry:
        print("dry-run: 3 values built in memory, no AWS call")
        return 0
    import boto3
    from botocore.exceptions import ClientError
    sm = boto3.client("secretsmanager", region_name=REGION)
    for n in values:
        try:
            sm.describe_secret(SecretId=n)
            print("REFUSED: secret %s already exists; nothing created" % n)
            return 2
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceNotFoundException":
                raise
    for n, v in values.items():
        r = sm.create_secret(Name=n, SecretString=v, Description="Gateway read secret created by %s" % ORDER)
        print("created %s %s" % (n, r["ARN"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
