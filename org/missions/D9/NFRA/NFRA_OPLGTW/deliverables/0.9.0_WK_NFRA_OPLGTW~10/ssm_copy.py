"""NFRA_OPLGTW OG-v-6 step 6 -- the copy of record in SSM (pattern of row NFRA_OPLGTW-S50).

Writes the salt and every plaintext answer as SecureString under
/opal/nfra_oplgtw/ogv6/seal_v2_YYYYMMDD/{<question id>..., SALT} (YYYYMMDD = the sealing run's UTC date,
read from SEALED_EXPECTED_V2.json), reads each back with --with-decryption and compares its sha256 with
the local bytes. Prints only names, byte lengths and equality booleans -- never a value. Values reach the
CLI through a short-lived file under this worktree's .scratch (a path without a space), removed at once.
Writes SSM_COPY_RECORD.json (names, lengths, booleans). Only ssm PutParameter / GetParameter under
/opal/nfra_oplgtw/ogv6/ are run.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import og_v6_common as C  # noqa: E402

EXPECTED_DIR = os.path.join(C.SEALED_DIR, "expected")
SCRATCH = os.path.join(C.REPO_ROOT, ".scratch", "ssmval")
RECORD = os.path.join(C.CELL_DIR, "SSM_COPY_RECORD.json")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main():
    with open(C.SEALED_PATH, "r", encoding="utf-8") as fh:
        sealed = json.load(fh)
    prefix = sealed["ssm_copy_of_record"]["prefix"]
    assert prefix.startswith("/opal/nfra_oplgtw/ogv6/")
    names = sealed["ssm_copy_of_record"]["names"]
    os.makedirs(SCRATCH, exist_ok=True)
    rows = []
    for name in names:
        with open(os.path.join(EXPECTED_DIR, name + ".txt"), "rb") as fh:
            local = fh.read()
        tmp = os.path.join(SCRATCH, "v.txt")
        with open(tmp, "wb") as fh:
            fh.write(local)
        try:
            C.aws(["ssm", "put-parameter", "--name", prefix + name, "--type", "SecureString",
                   "--value", "file://" + tmp.replace("\\", "/"), "--description",
                   "NFRA_OPLGTW OG-v-6 sealed question set v2 copy of record"])
        finally:
            os.remove(tmp)
        back = json.loads(C.aws(["ssm", "get-parameter", "--name", prefix + name, "--with-decryption",
                                 "--query", "Parameter", "--output", "json"]))
        val = back["Value"].encode("ascii")
        rows.append({"name": prefix + name, "type": back.get("Type"), "local_bytes": len(local),
                     "ssm_bytes": len(val), "sha256_equal": sha(local) == sha(val)})
        print(f"{prefix + name}: type={back.get('Type')} local_bytes={len(local)} "
              f"ssm_bytes={len(val)} equal={sha(local) == sha(val)}")
    ok = all(r["sha256_equal"] and r["type"] == "SecureString" for r in rows)
    with open(RECORD, "w", encoding="ascii") as fh:
        json.dump({"cell": "OG-v-6", "prefix": prefix, "parameters": rows, "all_equal": ok}, fh, indent=2)
        fh.write("\n")
    try:
        os.rmdir(SCRATCH)
    except OSError:
        pass
    print("OK" if ok else "FAIL", len(rows), "parameters")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
