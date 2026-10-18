"""HVST-ch-5 step 3 (i) and (ii), READ ONLY, run from the pinned worktree (C:/tmp/ch5-build at 2e0dc6af2e). ASCII only.
  python -u ch5_after.py
Prints fund_form.read_latest("DIVZ") (key and fields), the same substrate._pick_stored call as ch5_build.py step (iv), and the
stored count. Writes nothing."""
from __future__ import annotations

import json
import os
import sys

WT = r"C:\tmp\ch5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import fund_form, gold, substrate  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    client = store._default_client()
    doc = fund_form.read_latest("DIVZ", client=client)
    key = "%sfund=divz/%s.json" % (gold.table_prefix(fund_form.TABLE), fund_form._inputs_sha16(doc["inputs"]))
    print("READ_LATEST DIVZ key=%s method_version=%s content_sha256=%s inputs=%s" % (
        key, doc["method_version"], doc["content_sha256"], json.dumps(doc["inputs"])))
    print("READ_LATEST DIVZ fields=%s" % json.dumps(doc["fields"], sort_keys=True))
    for fund in ("IDVZ", "PFOE"):
        d = fund_form.read_latest(fund, client=client)
        print("READ_LATEST %s method_version=%s reports=%d content_sha256=%s" % (fund, d["method_version"], d["fields"]["reports"], d["content_sha256"]))
    wanted = fund_form.current_inputs("DIVZ", client=client)
    d, uri, current = substrate._pick_stored(fund_form.TABLE, "fund=divz", wanted, fund_form.METHOD_VERSION, client)
    print("PICK DIVZ wanted_inputs=%s uri=%s current=%s method_version=%s reports=%s" % (
        json.dumps(wanted), uri, current, d["method_version"], d["fields"]["reports"]))
    print("STORED-COUNT %d" % len(gold.gold_list(fund_form.TABLE, client=client)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
