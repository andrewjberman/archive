#!/usr/bin/env python3
"""HVST-ad-1 PHASE B: write ONE session bundle Secret, guarded by the CTO half's absent-read.

  python ad1_B_write_one.py <publisher> <secret_name>

Immediately before the single write_session_bundle call, describe_secret must return ResourceNotFound
for the name; if the Secret EXISTS (or the read is any other outcome) the script STOPs and writes nothing.
Prints the returned SHA-256 only -- never a secret value. An AWS refusal is printed and never retried.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[8]
sys.path.insert(0, str(REPO))

import boto3  # noqa: E402

from lib.opal_data_harvest import credentials  # noqa: E402

RUNTIME_ROOT = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"


def main(publisher, name):
    client = boto3.client("secretsmanager", region_name=credentials.REGION)
    try:
        client.describe_secret(SecretId=name)
    except Exception as exc:
        if type(exc).__name__ != "ResourceNotFoundException":
            print("STOP: absent-read of %s was not ResourceNotFound (%s); nothing written" % (name, type(exc).__name__))
            return 2
        print("absent-read %s: ResourceNotFound (immediately before the write)" % name)
    else:
        print("STOP: %s EXISTS; nothing written" % name)
        return 2
    try:
        digest = credentials.write_session_bundle(publisher, name, RUNTIME_ROOT, client=client)
    except Exception as exc:
        print("REFUSED: %s (%s); recorded, not retried" % (type(exc).__name__, exc))
        return 1
    print("write_session_bundle(%s, %s) returned sha256=%s" % (publisher, name, digest))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
