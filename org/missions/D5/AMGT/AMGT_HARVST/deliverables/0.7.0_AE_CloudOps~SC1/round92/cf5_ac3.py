"""HVST-cf-5 AMENDMENT 3 (msg 7852): the controlled AC3 comparison. READ ONLY, run from the pinned worktree
(C:/tmp/cf5-build at 04be089e13). ASCII only. NOTHING is written (dossier.build only; write_one is never called).

  python -u cf5_ac3.py <SECURITY_KEY>

Builds the dossier of one security in memory TWICE, with the same code and the same inputs:
  A) as now: substrate resolves the new version-2 fund form;
  B) with substrate._fund_form_member patched to return the member the substrate returned BEFORE the cf-5 writes
     (cf5_before.out step 0 iv): CPA -> the stale version-1 IDVZ object b5b15d3bf826322f.json, current False; UNH -> absent.
Then diffs the two previews: every `fields` key, and every top-level key.
"""
from __future__ import annotations

import json
import os
import sys

WT = r"C:\tmp\cf5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import dossier, substrate  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BEFORE = {
    "CPA_US_Equity": {
        "content_sha256": "577ec13815e284a07a0435d54d03d4ea40d3dfca6d94d8ea543f5c2c62866937",
        "current": False,
        "inputs_count": 37,
        "method_version": "1",
        "uri": "s3://opal-data-harvest/amgt/harvest/gold/research-fund-form/fund=idvz/b5b15d3bf826322f.json",
    },
    "UNH_US_Equity": {"absent": "continuation's fund_of_record is absent"},
}


def main(sk):
    client = store._default_client()
    original = substrate._fund_form_member
    print("=== AC3 controlled comparison for %s ===" % sk)
    a = dossier.build(sk, client=client)
    print("A (as now) built: as_of=%s content_sha256=%s fund_form_ref=%s" % (
        a.get("as_of"), a.get("content_sha256"), json.dumps(a["fields"].get("fund_form_ref"), sort_keys=True)))
    substrate._fund_form_member = lambda continuation_document, client_: dict(BEFORE[sk])
    try:
        b = dossier.build(sk, client=client)
    finally:
        substrate._fund_form_member = original
    print("B (member patched to the BEFORE value) built: as_of=%s content_sha256=%s fund_form_ref=%s" % (
        b.get("as_of"), b.get("content_sha256"), json.dumps(b["fields"].get("fund_form_ref"), sort_keys=True)))
    fa, fb = a["fields"], b["fields"]
    fdiff = [k for k in sorted(set(fa) | set(fb)) if fa.get(k) != fb.get(k)]
    tdiff = [k for k in sorted((set(a) | set(b)) - {"fields"}) if a.get(k) != b.get(k)]
    print("FIELDS differing between A and B: %s" % (fdiff if fdiff else "NONE"))
    print("TOP-LEVEL keys differing between A and B: %s" % (tdiff if tdiff else "NONE"))
    if "inputs" in tdiff:
        ia = {(i["key"], i["sha256"]) for i in a["inputs"]}
        ib = {(i["key"], i["sha256"]) for i in b["inputs"]}
        print("  inputs: A=%d B=%d only_in_A=%s only_in_B=%s" % (
            len(ia), len(ib), sorted((k, h[:12]) for k, h in ia - ib), sorted((k, h[:12]) for k, h in ib - ia)))
    names_new = "fund=idvz/65a5baab3afd06f0.json" in json.dumps(fa.get("fund_form_ref"))
    print("A.fund_form_ref names the new v2 IDVZ object 65a5baab3afd06f0.json: %s" % names_new)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
