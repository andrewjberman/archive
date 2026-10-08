"""AMGT_CORPUS round 40, CRPS-ap-10 (b) -- the S3 addresses the scheduled fire writes, printed from the naming library of the
tree this is run from (1.0.0_SA_CTO~Z ruling msg 31815: printed at the old pin and at the new pin, and shown equal).

Read-only and offline: it CALLS the store's own address builders with fixed arguments and prints what they return. No S3
call, no Bloomberg call, nothing is written.

  python ap10_fire_addresses.py        (PYTHONPATH=. from the root of the tree to read: a pinned checkout, or the shared tree)

The fire's writes, by their builder (integrations/bloomberg/research/model_block_pull.py stage_pull, :854-857, and
lib/research/harvest/bloomberg.py):
  bronze, three requests per name   store.bronze_put("bloomberg", refdata|histdata|bestdata, security_key=<key>, <stamp>.json)
  state, the pull log               store.address_of("amgt", "state", "pull_log", security_key=<key>, <object>)
  silver, the model block rows      store.silver_append("bloomberg", "model_block", ...)  -> its table prefix
  derived, the served block         a TYPED key in model_block_pull.py (derived/model_block/<safe key>/<stamp>/model_block.json):
                                    not built by the naming library, printed here from the module's own constants
Two names are printed: one plain (BA US Equity) and one whose ticker carries a slash (BP/ LN Equity), because the partition
encodes the key. A fixed stamp is used so two runs are comparable line for line.
"""
import datetime
import importlib.util
import os
import sys

from lib.research.harvest import bloomberg as hbloom
from lib.research.harvest import store

STAMP = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)  # the builder takes a datetime
NAMES = ["BA US Equity", "BP/ LN Equity"]


def main():
    research = os.path.join("integrations", "bloomberg", "research")
    sys.path.insert(0, research)
    spec = importlib.util.spec_from_file_location("mbp_addresses", os.path.join(research, "model_block_pull.py"))
    mbp = importlib.util.module_from_spec(spec)
    sys.modules["mbp_addresses"] = mbp
    spec.loader.exec_module(mbp)
    lines = []
    lines.append("bronze requests %s" % sorted(hbloom.BRONZE_REQUESTS))
    for name in NAMES:
        partition = store.entity_partition("security_key", name)
        for request in ("refdata", "histdata", "bestdata"):
            lines.append("bronze  %-14s %-9s %s" % (name, request, store.address_of(
                "bloomberg", "bronze", request, partition, object_name=store.form_a_object(STAMP, "json"))))
        lines.append("state   %-14s pull_log  %s" % (name, store.address_of(
            "amgt", "state", "pull_log", partition, object_name="%s.json" % STAMP.strftime("%Y%m%dT%H%M%SZ"))))
    lines.append("silver  table prefix model_block  %s" % store.table_prefix("bloomberg", "silver", "model_block"))
    lines.append("state   table prefix pull_log     %s" % store.table_prefix("amgt", "state", "pull_log"))
    lines.append("derived (typed) bucket %s engine %s" % (mbp.BUCKET, mbp.ENGINE))
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
