"""TCKT_VNEXT round 7 -- R7-nr-3: the four direct-invoke arms read as the pair expects, and no address is in the file.

Prints NR3-ARMS-OK or NR3-ARMS-FAIL <reason>; exit 0/1.
"""
import json
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r7_nr2/RESULT.json"
EXPECT = {"N1": 200, "N2": 403, "N3": 200, "N4": 403}


def main():
    try:
        raw = open(RES, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, ValueError) as e:
        print("NR3-ARMS-FAIL cannot read the result file: %s" % e)
        return 1
    if "@" in raw:
        print("NR3-ARMS-FAIL the file holds an address")
        return 1
    arms = doc.get("arms") or {}
    bad = [k for k, v in EXPECT.items() if (arms.get(k) or {}).get("function_status") != v]
    if bad:
        print("NR3-ARMS-FAIL arm(s) not as expected: %s" % bad)
        return 1
    print("NR3-ARMS-OK N1=200 N2=403 N3=200 N4=403")
    return 0


if __name__ == "__main__":
    sys.exit(main())
