"""OPLGTW OG-da-1 AC2: the LIVE data_refresh Lambda runs box/sitez HEAD's lambda_function.py, byte for byte.

  python da1_live.py <function_name> <repo_root>

Reads the function (aws lambda get-function), downloads its Code.Location zip, and compares lambda_function.py with
infra/aws/lambda/data_refresh/lambda_function.py at the repo root; prints the live CodeSha256, State and
LastUpdateStatus. The function name is read from the deploy path (Terraform) and passed in by the check.
"""
import io
import json
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    fn, root = argv[1], Path(argv[2])
    shim = root / ".tools" / ("aws.cmd" if sys.platform == "win32" else "aws")
    try:
        p = subprocess.run([str(shim), "lambda", "get-function", "--function-name", fn, "--region", "us-east-1",
                            "--output", "json"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=100)
        d = json.loads(p.stdout)
        data = urllib.request.urlopen(d["Code"]["Location"], timeout=60).read()
        z = zipfile.ZipFile(io.BytesIO(data))
        live = z.read("lambda_function.py") if "lambda_function.py" in z.namelist() else b""
    except Exception as exc:  # the instrument's own failure is a FAIL, never a pass
        print("instrument failure: %s" % type(exc).__name__)
        print("RESULT: FAIL")
        return 1
    head = (root / "infra/aws/lambda/data_refresh/lambda_function.py").read_bytes()
    cfg = d["Configuration"]
    same = live == head
    print("function %s: lambda_function.py equal-to-HEAD=%s; CodeSha256=%s State=%s LastUpdateStatus=%s"
          % (fn, same, cfg.get("CodeSha256"), cfg.get("State"), cfg.get("LastUpdateStatus")))
    ok = same and cfg.get("State") == "Active" and cfg.get("LastUpdateStatus") == "Successful"
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
