"""HVST-cf-5 step 3, READ ONLY, run from the pinned worktree (C:/tmp/cf5-build at 04be089e13). ASCII only.

  python -u cf5_after.py forms             (i) read_latest for IDVZ, PFOE (and DIVZ, expected LookupError); the issuer's AMENDMENT 2 reading of (ii):
                                           substrate._pick_stored called directly on research-fund-form for fund=pfoe and fund=idvz;
                                           CPA's and UNH's _fund_form_member
  python -u cf5_after.py dossier UNH_US_Equity | CPA_US_Equity
                                           (iii) an IN-MEMORY dossier.build compared field by field with the stored served dossier;
                                           NOTHING is written (write_one is never called)
"""
from __future__ import annotations

import json
import os
import sys

WT = r"C:\tmp\cf5-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import dossier, fund_form, gold, substrate  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def forms(client):
    print("--- (i) read_latest")
    for fund in ("IDVZ", "PFOE"):
        d = fund_form.read_latest(fund, client=client)
        print("READ_LATEST %s method_version=%s reports=%d inputs=%d content_sha256=%s" % (
            fund, d["method_version"], d["fields"]["reports"], len(d["inputs"]), d["content_sha256"]))
    try:
        fund_form.read_latest("DIVZ", client=client)
        print("READ_LATEST DIVZ returned an object (UNEXPECTED)")
    except LookupError as exc:
        print("READ_LATEST DIVZ raised LookupError (EXPECTED): %s" % exc)
    print("--- (ii) substrate._pick_stored on research-fund-form, directly")
    for fund in ("PFOE", "IDVZ"):
        wanted = fund_form.current_inputs(fund, client=client)
        doc, uri, current = substrate._pick_stored(
            fund_form.TABLE, "fund=%s" % fund_form._slug(fund), wanted, fund_form.METHOD_VERSION, client)
        print("PICK %s uri=%s current=%s method_version=%s inputs=%d content_sha256=%s" % (
            fund, uri, current, doc["method_version"], len(doc["inputs"]), doc["content_sha256"]))
    print("--- (ii) substrate _fund_form_member")
    for sk in ("CPA_US_Equity", "UNH_US_Equity"):
        entry, cdoc = substrate._continuation_member(sk, client)
        member = substrate._fund_form_member(cdoc, client)
        print("MEMBER %s continuation_uri=%s fund_form=%s" % (sk, entry.get("uri"), json.dumps(member, sort_keys=True)))
    return 0


def stored_dossier(client, sk):
    prefix = gold.table_prefix(dossier.TABLE) + store.entity_partition("security_key", sk) + "/"
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        keys.extend(o["Key"] for o in (page.get("Contents", []) or []))
    return sorted(keys)


def compare(sk, client, served_key):
    stored = json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, served_key), client=client).decode("utf-8"))
    built = dossier.build(sk, client=client)
    print("SERVED-DOSSIER %s" % served_key)
    print("BUILT method_version=%s content_sha256=%s | STORED method_version=%s content_sha256=%s" % (
        built.get("method_version"), built.get("content_sha256"), stored.get("method_version"), stored.get("content_sha256")))
    diffs = []
    for top in sorted(set(built) | set(stored)):
        if top == "fields":
            continue
        if built.get(top) != stored.get(top):
            diffs.append("top:" + top)
    bf, sf = built.get("fields", {}), stored.get("fields", {})
    for k in sorted(set(bf) | set(sf)):
        if bf.get(k) != sf.get(k):
            diffs.append("fields." + k)
    print("DIFFERING %s: %s" % (sk, diffs if diffs else "NONE"))
    for d in diffs:
        if d == "fields.fund_form_ref":
            print("  fund_form_ref stored=%s" % json.dumps(sf.get("fund_form_ref"), sort_keys=True))
            print("  fund_form_ref built =%s" % json.dumps(bf.get("fund_form_ref"), sort_keys=True))
        elif d.startswith("fields."):
            k = d.split(".", 1)[1]
            print("  %s stored=%s" % (d, json.dumps(sf.get(k), sort_keys=True)[:300]))
            print("  %s built =%s" % (d, json.dumps(bf.get(k), sort_keys=True)[:300]))
        else:
            print("  %s stored=%s built=%s" % (d, json.dumps(stored.get(d[4:]), sort_keys=True)[:200], json.dumps(built.get(d[4:]), sort_keys=True)[:200]))
    # a finer reading of the two lists that carry the other differences (printed, not graded)
    si = {(i["key"], i["sha256"]) for i in stored.get("inputs", [])}
    bi = {(i["key"], i["sha256"]) for i in built.get("inputs", [])}
    print("INPUTS stored=%d built=%d only_in_stored=%d only_in_built=%d" % (len(si), len(bi), len(si - bi), len(bi - si)))
    for k, h in sorted(si - bi):
        print("  only_in_stored %s %s" % (k, h[:12]))
    for k, h in sorted(bi - si):
        print("  only_in_built  %s %s" % (k, h[:12]))
    sm = {r.get("mnemonic"): r for r in sf.get("model_rows", [])}
    bm = {r.get("mnemonic"): r for r in bf.get("model_rows", [])}
    changed = sorted(m for m in set(sm) | set(bm) if sm.get(m) != bm.get(m))
    print("MODEL_ROWS stored=%d built=%d rows_differing=%d" % (len(sm), len(bm), len(changed)))
    stamps = {}
    for m in changed:
        for tag, row in (("stored", sm.get(m)), ("built", bm.get(m))):
            fig = (row or {}).get("figure", {})
            stamps.setdefault(tag, set()).add(fig.get("stamp") if isinstance(fig, dict) else None)
    print("  stamps among differing rows: stored=%s built=%s" % (sorted(map(str, stamps.get("stored", []))), sorted(map(str, stamps.get("built", [])))))
    other = [m for m in changed if {k: v for k, v in (sm.get(m) or {}).items() if k != "figure"} != {k: v for k, v in (bm.get(m) or {}).items() if k != "figure"}]
    print("  differing rows whose non-figure keys differ: %d" % len(other))
    same_but_stamp = 0
    for m in changed:
        sfig, bfig = (sm.get(m) or {}).get("figure", {}), (bm.get(m) or {}).get("figure", {})
        if isinstance(sfig, dict) and isinstance(bfig, dict) and {k: v for k, v in sfig.items() if k != "stamp"} == {k: v for k, v in bfig.items() if k != "stamp"}:
            same_but_stamp += 1
    print("  differing rows that differ ONLY in figure.stamp: %d of %d" % (same_but_stamp, len(changed)))
    return 0


def main(argv):
    client = store._default_client()
    if argv[1] == "forms":
        return forms(client)
    if argv[1] == "dossier":
        return compare(argv[2], client, argv[3])
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
