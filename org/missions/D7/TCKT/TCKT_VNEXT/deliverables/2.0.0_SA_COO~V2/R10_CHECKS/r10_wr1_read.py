"""TCKT_VNEXT round 10 -- R10-wr-1: the read of who writes the disabled tooling row has its four parts, a verdict from
the closed set, every cited path exists, and no address is in the file.

Prints WR1-READ-OK <detail> or WR1-READ-FAIL <reason>; exit 0/1.
"""
import json
import os
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r10_wr1/WHO_WRITES_THE_DISABLED_TOOLING_ROW_20261012.json"
KEYS = {"row_changes", "profile_row_writers", "sign_in_activity", "workspace_mentions", "verdict", "what_was_not_read", "claim"}
VERDICTS = {"A_TOOL_REWRITES_ITS_OWN_ROW", "A_SIGN_IN_ATTEMPT_WRITES_THE_ROW", "ANOTHER_WRITER", "NOT_DETERMINED"}


def main():
    try:
        raw = open(RES, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, ValueError) as e:
        print("WR1-READ-FAIL cannot read the result file: %s" % e)
        return 1
    if "@" in raw:
        print("WR1-READ-FAIL the file holds an address")
        return 1
    missing = sorted(KEYS - set(doc))
    if missing:
        print("WR1-READ-FAIL missing key(s): %s" % missing)
        return 1
    if doc["verdict"] not in VERDICTS:
        print("WR1-READ-FAIL verdict not in the closed set")
        return 1
    writers = doc["profile_row_writers"]
    if not isinstance(writers, list) or not writers:
        print("WR1-READ-FAIL profile_row_writers is empty")
        return 1
    absent = [w.get("where") for w in writers if not os.path.exists(str(w.get("where", "")).split(":")[0])]
    if absent:
        print("WR1-READ-FAIL writer path(s) absent: %s" % absent[:4])
        return 1
    if doc["claim"] not in ("measured", "inferred"):
        print("WR1-READ-FAIL claim must be measured or inferred")
        return 1
    print("WR1-READ-OK verdict=%s writers=%d" % (doc["verdict"], len(writers)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
