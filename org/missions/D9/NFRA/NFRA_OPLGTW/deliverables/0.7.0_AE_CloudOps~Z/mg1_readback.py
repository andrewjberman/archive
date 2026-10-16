#!/usr/bin/env python
"""OG-mg-1 Phase B step 7: read both written records back from the store (strongly consistent, fully paginated) and grade C5.
Writes W/MG1_READBACK.json: roles, pk hashes, statuses, revisions, scope KEYS, counts and short hashes only -- no tid, oid, email or
scope value. usage: python mg1_readback.py   (from the repo root)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys

from boto3.dynamodb.types import TypeDeserializer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mg1_before as mb  # noqa: E402

ALYSSA_BEFORE_HASH = "b93cd3cbf990"
DES = TypeDeserializer()


def plain(item: dict) -> dict:
    return {k: DES.deserialize(v) for k, v in item.items()}


def canon(o) -> str:
    return json.dumps(o, sort_keys=True, default=str)


def main() -> int:
    X = mb.x_dir()
    ident = json.load(io.open(os.path.join(X, "mg1_identities.json"), encoding="utf-8"))
    items = mb.scan_all()
    pol = [it for it in items if mb.sval(it, "pk").startswith("POLICY#")]
    out = {"read_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "denominator": {"items_scanned_total": len(items), "policy_items": len(pol),
                           "principal_profile": sum(1 for i in pol if mb.sval(i, "record_type") == "principal_profile"),
                           "data_entitlement": sum(1 for i in pol if mb.sval(i, "record_type") == "data_entitlement"),
                           "operator_audit": sum(1 for i in pol if mb.sval(i, "record_type") == "operator_audit"),
                           "email_deny": sum(1 for i in pol if mb.sval(i, "record_type") == "email_deny")},
           "principals": {}}
    scopes = {}
    for role in ("andrew", "bbg", "alyssa"):
        pk = ident["pk"][role]
        mine = [plain(i) for i in pol if mb.sval(i, "pk") == pk]
        prof = [p for p in mine if p.get("record_type") == "principal_profile"]
        grants = [p for p in mine if p.get("record_type") == "data_entitlement"]
        rec = {"pk_hash": mb.h(pk), "items": len(mine), "profiles": len(prof), "grant_revisions_present": sorted(str(g.get("revision")) for g in grants)}
        if prof:
            p = prof[0]
            rec["profile"] = {"status": p.get("status"), "kind": p.get("profile_kind"), "revision": str(p.get("revision")),
                              "grant_revision": str(p.get("grant_revision"))}
            g = next((g for g in grants if str(g.get("revision")) == str(p.get("grant_revision"))), None)
            if g is not None:
                sc = g.get("scope")
                sc = json.loads(sc) if isinstance(sc, str) else sc
                scopes[role] = sc
                rec["grant_in_force"] = {"status": g.get("status"), "revision": str(g.get("revision")), "scope_keys": sorted(sc),
                                         "calendar_months": str((sc.get("dates") or {}).get("calendar_months")),
                                         "operations": sorted(sc.get("operations") or [])}
        out["principals"][role] = rec
    a, b, al = scopes.get("andrew"), scopes.get("bbg"), scopes.get("alyssa")
    out["mirror_r2_equals_r1"] = (a is not None and a == b)
    out["r1_vs_alyssa_changed_top_keys"] = sorted(k for k in set(a or {}) | set(al or {}) if (a or {}).get(k) != (al or {}).get(k))
    a_items = [i for i in pol if mb.sval(i, "pk") == ident["pk"]["alyssa"]]
    out["alyssa_canonical_hash"] = hashlib.sha256(json.dumps(sorted(a_items, key=lambda i: (mb.sval(i, "sk"), json.dumps(i, sort_keys=True))),
                                                             sort_keys=True).encode("utf-8")).hexdigest()[:12]
    out["alyssa_unchanged"] = out["alyssa_canonical_hash"] == ALYSSA_BEFORE_HASH
    W = os.path.dirname(os.path.abspath(__file__))
    with io.open(os.path.join(W, "MG1_READBACK.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
