"""FB-k-4 read-only helper: summarise saved `aws lambda get-function-configuration` JSON files.

Prints, per file: function name, runtime, role name, timeout, memory, last modified, the environment
variable NAMES, and a value ONLY where the variable name marks a bucket, region, table or queue
(no secret, credential or id value is printed). Read-only: it opens the files it is given and nothing else.

Usage: python -I planinv_fb_k4_lambda_summary.py <cfg.json> [<cfg.json> ...]
"""
import json
import re
import sys

VALUE_KEY = re.compile(r"BUCKET|REGION|TABLE|QUEUE", re.I)
SECRET_KEY = re.compile(r"SECRET|TOKEN|PASS|KEY|CRED|SALT|JWT", re.I)


def summarise(path):
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    print("FUNCTION %s" % cfg.get("FunctionName"))
    print("  runtime=%s role=%s timeout=%s memory=%s modified=%s" % (
        cfg.get("Runtime"), (cfg.get("Role") or "").split("/")[-1], cfg.get("Timeout"),
        cfg.get("MemorySize"), cfg.get("LastModified")))
    print("  env_names=%d" % len(env))
    for k in sorted(env):
        if VALUE_KEY.search(k) and not SECRET_KEY.search(k):
            print("    %s=%s" % (k, env[k]))
        else:
            print("    %s (value not printed)" % k)


def main(paths):
    for p in paths:
        summarise(p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
