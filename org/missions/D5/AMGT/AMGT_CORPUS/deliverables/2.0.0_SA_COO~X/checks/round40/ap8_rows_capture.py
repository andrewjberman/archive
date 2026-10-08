"""AMGT_CORPUS round 40, CRPS-ap-8 FWD-20 -- capture, per served name, the fiscal-year mnemonics its served Model payload carries
a value for, and the ones the served check face REFUSES. Read-only (the served read path, scoped_amgt.read_thesis_bundle (the /thesis payload the page reads)); writes ONE
json file beside this script for ap8_rows_census.cjs. No Bloomberg call, no S3 write.

  python ap8_rows_capture.py        (PYTHONPATH=. from the repository root)
"""
import datetime
import json
import os
import sys

from lib.research.api import scoped_amgt as s
from lib.research.corpus import dossier
from lib.research.harvest import store

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ap8_rows_capture.json")


def main():
    keys = dossier._resolved_security_keys(client=store._default_client())
    out = {"_note": "AMGT_CORPUS round 40 ap-8 issuer capture through scoped_amgt.read_thesis_bundle (the /thesis payload the page reads), %s; per key: the fiscal-year "
                    "mnemonics with at least one non-null value, and those whose figures the served check face refuses"
                    % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "keys": {}}
    errors = 0
    for key in keys:
        try:
            bundle = s.read_thesis_bundle(key)
        except Exception as exc:  # noqa: BLE001 -- printed and counted, never a silent drop
            errors += 1
            print("READ-ERROR %s %s" % (key, type(exc).__name__))
            continue
        model = bundle.get("model") or {}
        # the page's join (portal figureIdentity.ts figureId / checkFor): "<scope>:<mnemonic>:<fiscal_year>"
        refusing = {c.get("figure_id") for c in (bundle.get("check_face") or model.get("check_face") or [])
                    if c.get("verdict") == "REFUSE"}
        have, refused = set(), set()
        for fig in model.get("fiscal_year_figures") or bundle.get("fiscal_year_figures") or []:
            mnem = fig.get("mnemonic")
            if not mnem:
                continue
            if fig.get("value") is not None:
                have.add(mnem)
            if "%s:%s:%s" % (fig.get("scope") or "unknown", mnem, fig.get("fiscal_year")) in refusing:
                refused.add(mnem)
        out["keys"][key] = {"fiscal_mnemonics": sorted(have), "refused_mnemonics": sorted(refused)}
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("captured keys %d of %d (errors %d) -> %s" % (len(out["keys"]), len(keys), errors, OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
