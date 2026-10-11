"""ar4_checks.py -- the mechanical checks of IRPT_ANLREQ round 4, workstream Y.

Usage:  python ar4_checks.py <check> --root <workspace root> [--portal <portal root>]

  y41-types   AR-y-41: the three members of persist_inputs.report_index each carry a type the wire generator can render,
              the contract's own test file passes, and it holds the wrong-type refusal test                  -> Y41-TYPES-OK
  y41-keep    AR-y-41: the _contracts folder fails exactly the two ids known at the base, no more           -> Y41-KEEP-OK
  y42-wire    AR-y-42: the portal's wire-regeneration test passes (the committed wire folder equals fresh output) -> Y42-WIRE-OK

--root is REQUIRED (no default: a default that resolves wrongly fails for the wrong reason). Every check prints its token on the
last line, or the token with -FAIL after one FAIL line per problem. The checks write nothing.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
SCHEMA = "docs/contracts/investor-reporting/v1/OwnedAnalysisRequest.schema.json"
TEST = IR + "/_contracts/test_persist_inputs_contract.py"
NEW_TEST = "test_persist_inputs_report_index_wrong_types_refused"
KNOWN_FAILING = 2
WIRE_TEST = "./src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-26.wire-regen.test.ts"
TOKENS = {"y41-types": "Y41-TYPES", "y41-keep": "Y41-KEEP", "y42-wire": "Y42-WIRE"}


def run(cmd, cwd, env=None):
    got = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return got.returncode, (got.stdout or "") + (got.stderr or "")


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def renderable(node):
    return isinstance(node, dict) and any(key in node for key in ("type", "$ref", "const", "enum"))


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    env = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="y", AWS_DEFAULT_REGION="us-east-1")
    problems = []
    if check == "y41-types":
        schema = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
        index = schema["properties"]["persist_inputs"]["properties"]["report_index"]
        objects = [alt for alt in index.get("oneOf", []) if isinstance(alt, dict) and alt.get("type") == "object"]
        if len(objects) != 1:
            return finish(check, ["report_index does not hold exactly one object alternative"])
        members = objects[0].get("properties", {})
        for name in ("report_id", "revision", "retention_ref", "sha256"):
            if not renderable(members.get(name)):
                problems.append("report_index.%s carries no type, $ref, const or enum: %r" % (name, members.get(name)))
        print("report_index members typed: %d of 4" % sum(1 for name in ("report_id", "revision", "retention_ref", "sha256")
                                                          if renderable(members.get(name))))
        if sorted(objects[0].get("required", [])) != ["report_id", "retention_ref", "revision", "sha256"] \
                or objects[0].get("additionalProperties") is not False:
            problems.append("the object alternative's required list or additionalProperties changed")
        text = (root / TEST).read_text(encoding="utf-8")
        if not re.search(r"^def %s\(" % NEW_TEST, text, flags=re.M):
            problems.append("%s holds no test named %s" % (TEST, NEW_TEST))
        rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST], root, env)
        print("\n".join([line for line in out.splitlines() if line.strip()][-1:]))
        if rc != 0:
            problems.append("pytest rc=%d on the contract's test file" % rc)
        return finish(check, problems)
    if check == "y41-keep":
        rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", IR + "/_contracts"], root, env)
        last = [line for line in out.splitlines() if line.strip()][-1:]
        print("\n".join(last))
        found = re.search(r"(\d+) failed", last[0] if last else "")
        failed = int(found.group(1)) if found else (0 if rc == 0 else -1)
        if failed != KNOWN_FAILING:
            problems.append("the _contracts folder fails %d test(s), not the %d known at the base" % (failed, KNOWN_FAILING))
        return finish(check, problems)
    if "--portal" not in argv:
        print(__doc__)
        return 2
    portal = Path(argv[argv.index("--portal") + 1])
    rc, out = run(["bun", "test", WIRE_TEST], portal)
    lines = [line for line in out.splitlines() if line.strip()]
    print("\n".join(lines[-4:]))
    passed = re.search(r"(\d+) pass", out)
    failed = re.search(r"(\d+) fail", out)
    if rc != 0 or not passed or int(passed.group(1)) < 1 or not failed or int(failed.group(1)) != 0:
        problems.append("the wire-regeneration test does not pass (rc=%d)" % rc)
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
