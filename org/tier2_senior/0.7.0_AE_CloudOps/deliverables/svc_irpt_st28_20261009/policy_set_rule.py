import argparse
import copy
import hashlib
import json
from pathlib import Path


def _as_sorted_list(value):
    return sorted(value if isinstance(value, list) else [value])


def normalize(policy):
    normalized = copy.deepcopy(policy)
    for statement in normalized.get("Statement", []):
        principal = statement.get("Principal")
        if isinstance(principal, dict) and "AWS" in principal:
            principal["AWS"] = _as_sorted_list(principal["AWS"])
        arn_not_equals = statement.get("Condition", {}).get("ArnNotEquals")
        if isinstance(arn_not_equals, dict) and "aws:PrincipalArn" in arn_not_equals:
            arn_not_equals["aws:PrincipalArn"] = _as_sorted_list(
                arn_not_equals["aws:PrincipalArn"]
            )
    return normalized


def canonical_bytes(policy):
    return json.dumps(
        normalize(policy), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("live")
    parser.add_argument("expected")
    parser.add_argument("output")
    parser.add_argument("--label", required=True)
    args = parser.parse_args()

    live = json.loads(Path(args.live).read_text(encoding="utf-8-sig"))
    expected = json.loads(Path(args.expected).read_text(encoding="utf-8-sig"))
    live_bytes = canonical_bytes(live)
    expected_bytes = canonical_bytes(expected)
    verdict = {
        "label": args.label,
        "set_rule_equal": live_bytes == expected_bytes,
        "live_canonical_sha256": hashlib.sha256(live_bytes).hexdigest(),
        "expected_canonical_sha256": hashlib.sha256(expected_bytes).hexdigest(),
        "live_statement_sids": [s.get("Sid") for s in live.get("Statement", [])],
        "expected_statement_sids": [s.get("Sid") for s in expected.get("Statement", [])],
    }
    Path(args.output).write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verdict, indent=2))
    raise SystemExit(0 if verdict["set_rule_equal"] else 1)


if __name__ == "__main__":
    main()
