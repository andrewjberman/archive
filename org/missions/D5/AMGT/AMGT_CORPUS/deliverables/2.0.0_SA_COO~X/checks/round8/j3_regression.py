"""AMGT_CORPUS round 8 -- j3_AC3's comparator. Read-only (cases-report reads landed raw; it writes nothing).

Runs `model_block_pull cases-report` over the 97 model-block keys in batches of 3 and compares each key's Base-case
status and ratio against the issuer's base-state log taken at the cut (evidence/r8_base_cases_report_all_20260928T234706Z.log,
rule case_rule.py @b56fef3032). A key SERVED at the base that reads anything else now is UNSERVED; a key SERVED in both whose
ratio differs is RATIO_MOVED. A key that moves ABSENT -> SERVED is the cell's intended effect and is only counted.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = os.path.join(HERE, "model_block_keys_97.txt")
BASE = os.path.join(HERE, "..", "..", "evidence", "r8_base_cases_report_all_20260928T234706Z.log")
LINE = re.compile(r"^cases (\S+) base (\S+) ratio (\S+) ")


def _load(lines):
    out = {}
    for line in lines:
        m = LINE.match(line.strip())
        if m:
            out[m.group(1)] = (m.group(2), m.group(3))
    return out


def main():
    base = _load(open(BASE, encoding="utf-8"))
    keys = [k.strip() for k in open(KEYS, encoding="utf-8") if k.strip()]
    now = {}
    for i in range(0, len(keys), 3):
        tickers = [k.replace("_", " ") for k in keys[i:i + 3]]
        proc = subprocess.run(
            [sys.executable, "-m", "integrations.bloomberg.research.model_block_pull", "cases-report", "--securities"] + tickers,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        now.update(_load(proc.stdout.splitlines()))
    served_base = [k for k in keys if base.get(k, ("", ""))[0] == "SERVED"]
    unserved = [k for k in served_base if now.get(k, ("MISSING", ""))[0] != "SERVED"]
    ratio_moved = [k for k in served_base if k not in unserved and now[k][1] != base[k][1]]
    newly_served = [k for k in keys if base.get(k, ("", ""))[0] != "SERVED" and now.get(k, ("", ""))[0] == "SERVED"]
    missing = [k for k in keys if k not in now]
    for k in unserved:
        print("unserved %s base %s now %s" % (k, base[k], now.get(k)))
    for k in ratio_moved:
        print("ratio_moved %s base %s now %s" % (k, base[k][1], now[k][1]))
    print("newly_served %d %s" % (len(newly_served), " ".join(newly_served)))
    print("j3 keys_read %d of %d unserved_vs_base %d of %d ratio_moved_vs_base %d"
          % (len(keys) - len(missing), len(keys), len(unserved), len(served_base), len(ratio_moved)))


if __name__ == "__main__":
    main()
