"""TCKT_VNEXT round 9 -- R9-st-3: the five direct-invoke arms read as the pair expects, and no address is in the file.

Prints ST3-ARMS-OK or ST3-ARMS-FAIL <reason>; exit 0/1.
"""
import json
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r9_st2/RESULT.json"
EXPECT = {"S1": 200, "S2": 403, "S3": 403, "S4": 200, "S5": 403}


def main():
    try:
        raw = open(RES, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, ValueError) as e:
        print("ST3-ARMS-FAIL cannot read the result file: %s" % e)
        return 1
    if "@" in raw:
        print("ST3-ARMS-FAIL the file holds an address")
        return 1
    arms = doc.get("arms") or {}
    bad = [k for k, v in EXPECT.items() if (arms.get(k) or {}).get("function_status") != v]
    if bad:
        print("ST3-ARMS-FAIL arm(s) not as expected: %s" % bad)
        return 1
    print("ST3-ARMS-OK S1=200 S2=403 S3=403 S4=200 S5=403")
    return 0


if __name__ == "__main__":
    sys.exit(main())
