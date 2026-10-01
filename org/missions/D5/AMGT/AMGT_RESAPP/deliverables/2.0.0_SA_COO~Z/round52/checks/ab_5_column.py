"""AMGT_RESAPP round 52, AMGT-ab-5 -- a driver point verifies ONLY against its OWN column (CTO round-51 ruling 7, row Z-W185-S1).
Through the ONE verification path (`analyze._apply_point_verification`, which the fresh two-pass run and the stored-object reverify
share), on a planted columnar table -- header run 2023/2024/2025, a row label, then 100/200/300 one per line:
  (a) the PLANT {period 2025, value 200} (2024's number) must be HELD, never verified -- at the cut the last-located period's block
      runs to the excerpt's end, so 200 verifies inside the 2025 block;
  (b) the CONTROL {2023: 100, 2024: 200, 2025: 300} (each in its own column) must verify 3 of 3, each span covering its own number.
usage: python <this>   (from the repo root; no I/O)"""
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.filings import analyze  # noqa: E402

EXCERPT = "Net sales by year\n2023\n2024\n2025\nNet sales\n100\n200\n300\nOther text follows here.\n"


def run(points):
    kept, held = analyze._apply_point_verification(
        [{"period": p, "value": v} for p, v in points], EXCERPT, [], anchor=0)
    return ({k["period"]: EXCERPT[k["span"][0]:k["span"][1]] for k in kept if k.get("span")},
            [h["period"] for h in held])


def main():
    v_plant, h_plant = run([("2025", 200)])
    print("(a) plant 2025=200 (2024's column): verified %s, held %s" % (v_plant, h_plant))
    v_ctl, h_ctl = run([("2023", 100), ("2024", 200), ("2025", 300)])
    print("(b) control own columns: verified %s, held %s" % (v_ctl, h_ctl))
    ok_a = "2025" not in v_plant and "2025" in h_plant
    ok_b = v_ctl == {"2023": "100", "2024": "200", "2025": "300"} and not h_ctl
    print("A DRIVER POINT VERIFIES ONLY AGAINST ITS OWN COLUMN: %s" % ("YES" if ok_a and ok_b else "NO"))
    return 0 if ok_a and ok_b else 1


if __name__ == "__main__":
    sys.exit(main())
