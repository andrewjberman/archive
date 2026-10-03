"""DB10-1-AC3 -- the readiness cell builds and uploads NOTHING: the three reporting functions' artifact fields in the map are the
ones the issuance commit carried (the build, upload and deploy are the issuer's P-2 packet).

Grades: for irpt-reporting-gold-lambda, -publish-lambda and -read-lambda, artifact_s3_key and artifact_sha256 in
infra/aws/lambda/ci/lambda-source-map.json equal the values below (read from the map at the issuance base, 2026-10-03).
Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
BASE = {
    "irpt-reporting-gold-lambda": ("investor-reporting/irpt-reporting-gold-lambda.zip", "RLOFPe0lYEBKKvQw69r8oqB5DeCfnZMBeukFJ0AZzN8="),
    "irpt-reporting-publish-lambda": ("investor-reporting/irpt-reporting-publish-lambda.zip", "gZM/pgyLqFICfadTwYF5VkNQDwhoFJbR2YGmjsmbzis="),
    "irpt-reporting-read-lambda": ("investor-reporting/irpt-reporting-read-lambda.zip", "dKMqVbKWyZJV+0txPH16QGwLoC/HfsyGHoOdo1lGuS8="),
}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    f = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"]
    for name, (key, sha) in BASE.items():
        got = (f.get(name, {}).get("artifact_s3_key"), f.get(name, {}).get("artifact_sha256"))
        if got != (key, sha):
            print("FAIL: %s artifact fields moved: %s" % (name, got))
            print("DB10-1-AC3 FAIL")
            sys.exit(1)
    print("OK: 3 of 3 reporting artifacts unchanged (nothing built or uploaded)")
    print("DB10-1-AC3 PASS")


if __name__ == "__main__":
    main()
