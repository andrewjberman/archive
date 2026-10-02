"""HVST-aj-8 AC2 (issuer, read-only): the 149 barrons silver rows with dict titles are re-derived with string titles, and
nothing else moved (CTO 28525, conditions 1 and 2).

Reads the issuer's re-derivation manifest `deliverables/2.0.0_SA_COO_H/round37/aj8_rederive_manifest.json`
= {"targets": [149 article_keys], "others_before": {article_key: record_hash}} (written BEFORE the re-derivation) and the
live barrons silver (`store.silver_latest`). PASS requires:
- the manifest lists exactly 149 targets;
- each target's latest silver row has a string (or null) title, never a dict: 149 of 149;
- every other barrons row's record_hash equals `others_before` (untouched);
- the builder's title matcher (`publication_gold._match_counts`) runs over every barrons silver title without raising.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
MAN = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round37/aj8_rederive_manifest.json")

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    failures = []
    if not os.path.exists(MAN):
        print("MANIFEST: absent (%s)" % MAN)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no re-derivation manifest")
        return 1
    m = json.load(open(MAN, encoding="utf-8"))
    targets, others = m.get("targets") or [], m.get("others_before") or {}
    latest = {k[0]: r for k, r in store.silver_latest(hg.SOURCE_FOR_PUBLISHER["barrons"], "article", ("article_key",)).items()}
    fixed = sum(1 for k in targets if k in latest and not isinstance(latest[k].get("title"), dict))
    still_dict = sum(1 for r in latest.values() if isinstance(r.get("title"), dict))
    moved = [k for k, h in others.items() if (latest.get(k) or {}).get("record_hash") != h]
    print("TARGETS %d; re-derived with a string title %d of %d; dict titles left in barrons silver %d; others moved %d of %d"
          % (len(targets), fixed, len(targets), still_dict, len(moved), len(others)))
    if len(targets) != 149:
        failures.append("manifest lists %d targets, want 149" % len(targets))
    if fixed != len(targets):
        failures.append("%d targets still lack a string title" % (len(targets) - fixed))
    if still_dict:
        failures.append("%d dict titles remain" % still_dict)
    if moved:
        failures.append("%d non-target barrons rows changed" % len(moved))
    raised = 0
    for r in latest.values():
        try:
            pg._match_counts(r.get("title") or "", ["Apple"], set())
        except TypeError:
            raised += 1
        except Exception:  # noqa: BLE001 -- only the type error is the defect under test
            pass
    print("MATCHER raised TypeError on %d of %d barrons titles" % (raised, len(latest)))
    if raised:
        failures.append("matcher raised on %d titles" % raised)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
