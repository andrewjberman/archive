"""TO-APPLY-WS2WS3 AC1 -- the five live rivalfunds Lambdas run exactly the packages built in the deploy tree.

    python ws23_deploy_check.py [<deploy tree, default C:/tmp/rv-ws23-dell1>]

For each of the five functions: base64(sha256(<tree>/.runtime/rivalfunds-build/zips/<key>.zip)) must equal the live
`CodeSha256` (boto3 get_function_configuration, read-only), State Active, LastUpdateStatus Successful, MemorySize 3008.
A missing zip or a failed read is a failure, never a pass. Prints one line per function and the result.
"""
import base64
import hashlib
import pathlib
import sys

import boto3

TREE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "C:/tmp/rv-ws23-dell1")
ZIPS = TREE / ".runtime" / "rivalfunds-build" / "zips"
FUNCS = ["etfs-rivalfunds-daily-lambda", "etfs-rivalfunds-fetch-holdings-lambda", "rivalfunds-build-silver-lambda",
         "rivalfunds-build-canonical-shape-lambda", "rivalfunds-publish-page-lambda"]
lam = boto3.client("lambda", region_name="us-east-1")
zips = sorted(ZIPS.glob("*.zip")) if ZIPS.is_dir() else []
built = {base64.b64encode(hashlib.sha256(z.read_bytes()).digest()).decode(): z.name for z in zips}
print(f"deploy tree {TREE}: {len(zips)} built zip(s)")
fails = []
for fn in FUNCS:
    try:
        c = lam.get_function_configuration(FunctionName=fn)
    except Exception as ex:  # noqa: BLE001 -- a failed read is a failure
        fails.append(f"{fn}: READ FAILED {type(ex).__name__}")
        continue
    sha, ok_state = c["CodeSha256"], (c["State"], c["LastUpdateStatus"], c["MemorySize"]) == ("Active", "Successful", 3008)
    print(f"{fn}: CodeSha256 {sha[:12]} LastModified {c['LastModified']} built-zip {built.get(sha, 'NONE')} "
          f"state {c['State']}/{c['LastUpdateStatus']}/{c['MemorySize']}")
    if sha not in built:
        fails.append(f"{fn}: live code is not one of the built packages")
    if not ok_state:
        fails.append(f"{fn}: state/update/memory not Active/Successful/3008")
for f in fails:
    print("FAIL:", f)
print(f"WS23 DEPLOY RESULT: {'PASS' if not fails else 'FAIL'} {len(fails)} failures")
sys.exit(1 if fails else 0)
