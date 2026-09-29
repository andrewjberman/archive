"""AMGT_CORPUS round 15, CRPS-q-2 -- the crosswalk the builder would publish TODAY from the inputs at HEAD, built in
memory exactly as `crosswalk --dry-run` builds it (NO pool write), then read two ways. Read-only; the issuer's file.

  1. the backlog census through that document (AMGT_CROSSWALK_PATH pointed at a scratch copy):
     -> 'q2 folders N resolved R unresolved U ambiguous A hitachi <security_key|UNRESOLVED>'
  2. the record diff against the pool's latest crosswalk/v1 object, keyed by security_key:
     -> 'q2 diff_vs_pool <pool key> added K removed R changed C added_keys [...] other_jp_moved M'
"""
import datetime
import json
import os
import tempfile

from lib.research.identity import crosswalk as cw
from lib.research.corpus import backlog, library

HITACHI = "Hitachi 6501 JP"

pool_doc, _idx, _amb = cw.load_crosswalk(refresh=True)
pool_key = cw.loaded_from()

as_of = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
universe, universe_source = cw.load_identity_universe(None)
research_folders, research_root = cw._research_folders_for_disclosure()
document = cw.build_crosswalk(
    as_of, identity_universe=universe, identity_source=universe_source,
    research_folders=research_folders, research_root=research_root,
)
payload = cw.serialise(document)

scratch = tempfile.mkdtemp(prefix="q2_crosswalk_")
path = os.path.join(scratch, "crosswalk.json")
with open(path, "wb") as fh:
    fh.write(payload)
os.environ[cw.ENV_CROSSWALK] = path
cw.load_crosswalk(refresh=True)

root = library.library_root()
census = backlog.build(root)
hit = [r for r in census["records"] if r["folder"] == HITACHI]
hitachi = (hit[0]["security_key"] or "UNRESOLVED") if hit else "NO-FOLDER"
print("q2 folders %d resolved %d unresolved %d ambiguous %d hitachi %s" % (
    census["folders_read"], census["resolved"], census["unresolved"], census["ambiguous"], hitachi))


def by_key(doc):
    out = {}
    for r in doc["records"]:
        k = r.get("security_key") or ("UNRESOLVED:" + str(r.get("raw_identifier")))
        out[k] = json.dumps(r, sort_keys=True)
    return out


old, new = by_key(pool_doc), by_key(document)
added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))
changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
jp_old = {k for k in old if k.endswith("_JP_Equity")}
jp_moved = sum(1 for k in jp_old if k not in new or old[k] != new[k])
print("q2 diff_vs_pool %s added %d removed %d changed %d added_keys %s other_jp_moved %d of %d" % (
    pool_key, len(added), len(removed), len(changed), added, jp_moved, len(jp_old)))
if changed:
    print("q2 changed_keys %s" % changed[:20])

os.remove(path)
os.rmdir(scratch)
