"""IRPT_DASHBD round 82 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 5955: the two tokens accepted, TIMING_END removed.

Cell DB-b-157: the proposal record carries the ruled class set -- the TIMING axis holds three values, TIMING_END is listed as
retired beside the two RECONCILES tokens, and the record states the classes as RULED.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB82-1-AC1  ~121/TIMING_CLASSES_PROPOSAL.json: the TIMING axis's values are exactly TIMING_START, TIMING_MID and
              TIMING_NOT_DETERMINED; new_tokens holds 5 tokens and not TIMING_END; token_census holds one entry per new token;
              no placement cell names TIMING_END and the cells still sum to 51 with uncovered 0; retired_tokens lists
              RECONCILES_YES, RECONCILES_NO and TIMING_END, each {token, retired_by, why}; ruled {by, accepted_axis
              "RESTATED_CLOSE", served_relabelled false}.
"""
import json
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
TIMING = ["TIMING_MID", "TIMING_NOT_DETERMINED", "TIMING_START"]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB82"))
        sys.exit(1)

    if cid != "DB82-1-AC1":
        fail("unknown criterion %r" % cid)
    p = root / (M + "0.9.0_WK_IRPT_DASHBD~121/TIMING_CLASSES_PROPOSAL.json")
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    axes = r.get("axes") or []
    tim = [a for a in axes if "TIMING" in str(a.get("name") or "").upper()]
    if len(axes) != 2 or len(tim) != 1 or sorted(str(v) for v in (tim[0].get("values") or [])) != TIMING:
        fail("the TIMING axis does not hold exactly the three ruled values: %r" % [a.get("values") for a in tim])
    new = [str(t) for t in (r.get("new_tokens") or [])]
    if len(new) != 5 or "TIMING_END" in new:
        fail("new_tokens %r" % new)
    tc = r.get("token_census") or []
    if sorted(str(t.get("token")) for t in tc) != sorted(new):
        fail("token_census does not hold one entry per new token")
    pl = r.get("placement") or {}
    cells = pl.get("cells") or []
    if pl.get("total") != 51 or pl.get("uncovered") != 0 or sum(c.get("segments", 0) for c in cells) != 51:
        fail("placement does not place 51 of 51")
    if any(str(v) == "TIMING_END" for c in cells for k, v in c.items() if k != "of_which"):
        fail("a placement cell still names TIMING_END")
    rt = r.get("retired_tokens") or []
    if sorted(str(x.get("token")) for x in rt) != ["RECONCILES_NO", "RECONCILES_YES", "TIMING_END"] \
            or any(not str(x.get("retired_by") or "").strip() or not str(x.get("why") or "").strip() for x in rt):
        fail("retired_tokens must list the three retired tokens, each with retired_by and why")
    ru = r.get("ruled") or {}
    if not str(ru.get("by") or "").strip() or ru.get("accepted_axis") != "RESTATED_CLOSE" or ru.get("served_relabelled") is not False:
        fail("ruled %r" % ru)
    print("OK: TIMING holds three values; 5 tokens censused; TIMING_END and the two RECONCILES tokens are listed retired; 51 of 51 placed")
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
