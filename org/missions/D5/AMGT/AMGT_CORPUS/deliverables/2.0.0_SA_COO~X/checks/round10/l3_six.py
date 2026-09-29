"""AMGT_CORPUS round 10 -- l3_AC2's checker. Read-only; writes nothing.

For the six names whose scenario table round 9 could not read (row Z-W1-S12), resolves the three case fields through the
SAME resolver build() calls (`dossier._resolve_case_field`) and classifies each name:
  body_names       -- all three cases served with values;
  absent_specific  -- served ABSENT with a reason that is NOT round 9's generic value-count message;
  absent_generic   -- still served ABSENT with "... carries <n> values, expected 3 x <k>" (the round-9 state).
Prints one line per name and the summary.
"""
import re

from lib.research.corpus import dossier
from lib.research.harvest import store

SIX = ("8035_JP_Equity", "BZLFY_US_Equity", "HEI_US_Equity", "SNPS_US_Equity", "TSM_US_Equity", "V_US_Equity")
GENERIC = re.compile(r"carries \d+ values, expected 3 x \d+")


def main():
    client = store._default_client()
    body = specific = generic = 0
    for key in SIX:
        _items, pick_a, pick_b = dossier._picked_reports(key, client)
        label_a = dossier._period_label(pick_a)
        label_b = dossier._period_label(pick_b)
        fields = {}
        for case_name, names in dossier.CASE_SECTION_NAMES.items():
            fields[case_name], _state = dossier._resolve_case_field(case_name, names, pick_a, pick_b, label_a, label_b)
        served = [c for c, f in fields.items() if f.get("value") is not None]
        reasons = sorted({f.get("absent") or "" for f in fields.values() if f.get("value") is None})
        if len(served) == 3:
            body += 1
            cls = "body"
        elif reasons and all(r and not GENERIC.search(r) for r in reasons):
            specific += 1
            cls = "absent_specific"
        else:
            generic += 1
            cls = "absent_generic"
        print("l3 %s %s served %d reason %s" % (key, cls, len(served), " | ".join(reasons)[:200]))
    print("l3 names %d body_names %d absent_specific %d absent_generic %d sum %d"
          % (len(SIX), body, specific, generic, body + specific + generic))


if __name__ == "__main__":
    main()
