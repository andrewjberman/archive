"""IRPT_ANLREQ TO-RUN-RESIDUE-DELETE-7E7J steps T and D (applier 0.7.0_AE_CloudOps~IB2).

  python delete_pass.py t    step T: assume role 0 and delete the manifest's FIRST entry alone by exact key and VersionId; 204 expected; head-object by VersionId: 404 expected
  python delete_pass.py d    step D: the remaining 28 entries (chunk 0 rest, chunk 1, chunk 2; 12 / 12 / 5), each in the matching assumed-role session; each delete 204, each read 404;
                             then every manifest key's versions and delete markers read EMPTY (one exact key at a time)

The role credentials live in memory only (never printed, never written). Every delete names a manifest entry's exact key and VersionId; nothing is ever listed to decide a delete.
The audit key is deleted only after its versions are re-read as exactly the two named ones. Any result other than 204 then 404 is a STOP with the remaining entries untouched.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
MANIFEST = ROOT / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/synthetic_residue_delete_list_supplement_runs7e_7j_20261021.json"
ROLE_ARN = "arn:aws:iam::313476888478:role/irpt-residue-delete-%d-role"
BUCKET = "opal-data-irpt"
REGION = "us-east-1"
RESULTS = HERE / "delete_results.json"
lines = []


def say(x):
    lines.append(x)
    print(x, flush=True)


def client_for(n):
    sts = boto3.client("sts", region_name=REGION)
    last = None
    for _ in range(12):
        try:
            c = sts.assume_role(RoleArn=ROLE_ARN % n, RoleSessionName="ib2-residue-%d" % n, DurationSeconds=900)["Credentials"]
            return boto3.client("s3", region_name=REGION, aws_access_key_id=c["AccessKeyId"], aws_secret_access_key=c["SecretAccessKey"], aws_session_token=c["SessionToken"])
        except ClientError as e:
            last = e.response["Error"]["Code"]
            time.sleep(5)
    raise SystemExit("STOP assume-role of role %d failed: %s" % (n, last))


def head_code(s3, key, vid):
    try:
        s3.head_object(Bucket=BUCKET, Key=key, VersionId=vid)
        return 200
    except ClientError as e:
        return int(e.response["ResponseMetadata"]["HTTPStatusCode"])


def versions_of(s3, key):
    out = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=key):
        out += [("V", v["VersionId"]) for v in pg.get("Versions", []) if v["Key"] == key]
        out += [("M", m["VersionId"]) for m in pg.get("DeleteMarkers", []) if m["Key"] == key]
    return out


def delete_one(rs3, plain, idx, o):
    key, vid = o["key"], o["version_id"]
    try:
        r = rs3.delete_object(Bucket=BUCKET, Key=key, VersionId=vid)
        code = int(r["ResponseMetadata"]["HTTPStatusCode"])
    except ClientError as e:
        code = int(e.response["ResponseMetadata"]["HTTPStatusCode"])
    read = head_code(plain, key, vid)
    say("ENTRY %02d role=%d run=%s family=%s key=...%s version=%s delete=%d read=%d" % (idx, idx // 12 if idx < 24 else 2, o["run"], o["family_dir"], key[-24:], vid[:8], code, read))
    return code == 204 and read == 404


def main(mode):
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))["objects"]
    assert len(man) == 29
    plain = boto3.client("s3", region_name=REGION)
    role_of = [0] * 12 + [1] * 12 + [2] * 5
    if mode == "t":
        s3 = client_for(0)
        ok = delete_one(s3, plain, 0, man[0])
        say("T first delete %s" % ("204 and ABSENT (read 404)" if ok else "FAIL"))
        RESULTS.write_text(json.dumps({"t_ok": ok, "done": [0] if ok else []}), encoding="ascii")
        return 0 if ok else 3
    state = json.loads(RESULTS.read_text(encoding="ascii"))
    assert state["t_ok"] and state["done"] == [0], "step T did not pass"
    sessions = {}
    # the audit key: re-read exactly its two named versions before any delete of it
    audit = [o for o in man if o["family_dir"] == "analysis_audit"]
    akey = {o["key"] for o in audit}
    assert len(akey) == 1
    cur = sorted(v for t, v in versions_of(plain, audit[0]["key"]) if t == "V")
    markers = [1 for t, _ in versions_of(plain, audit[0]["key"]) if t == "M"]
    if cur != sorted(o["version_id"] for o in audit) or markers:
        say("D FAIL the audit key does not hold exactly its two named versions (versions %d, markers %d); no delete" % (len(cur), len(markers)))
        return 4
    done = list(state["done"])
    for i in range(1, 29):
        n = role_of[i]
        if n not in sessions:
            sessions[n] = client_for(n)
        if not delete_one(sessions[n], plain, i, man[i]):
            say("D STOP at entry %d: not 204 then 404; remaining entries untouched" % i)
            RESULTS.write_text(json.dumps({"t_ok": True, "done": done, "stopped_at": i}), encoding="ascii")
            return 5
        done.append(i)
        RESULTS.write_text(json.dumps({"t_ok": True, "done": done}), encoding="ascii")
    say("D %d of 29 versions deleted and read ABSENT (204 then 404 each)" % len(done))
    keys = sorted({o["key"] for o in man})
    empty = 0
    for k in keys:
        v = versions_of(plain, k)
        empty += 0 if v else 1
        if v:
            say("D key still lists versions or markers: ...%s count=%d" % (k[-24:], len(v)))
    say("D %d of %d manifest keys list EMPTY (versions and delete markers)" % (empty, len(keys)))
    say("D audit key versions: %s" % versions_of(plain, audit[0]["key"]))
    return 0 if empty == len(keys) else 6


if __name__ == "__main__":
    rc = main(sys.argv[1])
    (HERE / ("results_%s.txt" % sys.argv[1])).write_text("\n".join(lines) + "\n", encoding="ascii", errors="replace", newline="\n")
    sys.exit(rc)
