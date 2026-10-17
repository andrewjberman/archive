#!/usr/bin/env python
"""OG-ap-35 Phase B step 6 (COO C2 and C7): re-read before the write, READ-ONLY. Hashes, integers and operation names only.
Compares with AG1_BEFORE.json: her profile and grant revisions (4 and 4), her scope hash, the other two principals' grant hashes. Records the hash of her email_deny record
(attribute hash, 10 hex) as email_deny_hash_before. Saves the RESTORE candidate (her live scope, download_filtered included) off-repo, for rollback.
Exit 0 = nothing moved; exit 3 = STOP (something moved).
usage: python ag1_reread.py before|after   (from the repo root of the worktree)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys

import boto3

TABLE = "gateway-access-state-table"
REGION = "us-east-1"
GW = os.path.join("infra", "aws", "ec2", "opal-gateway")
W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~NFRA1")


def h10(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def x_dir():
    d = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "opal", "og-salt", "ag1")
    if os.path.realpath(d).startswith(os.path.realpath(".")):
        raise SystemExit("REFUSED: X resolves inside the worktree")
    return d


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "before"
    X = x_dir()
    sys.path.insert(0, os.path.abspath(GW))
    import app.access_state as acs                      # noqa: E402
    sys.path.insert(0, os.path.abspath(os.path.join(GW, "ops")))
    import schwab_entitlement_admin as sea              # noqa: E402

    ident = json.load(io.open(os.path.join(X, "ag1_identities.json"), encoding="utf-8"))
    before = json.load(io.open(os.path.join(W, "AG1_BEFORE.json"), encoding="utf-8"))["body"]
    sm = boto3.client("secretsmanager", region_name=REGION)
    roster = json.loads(sm.get_secret_value(SecretId="gateway/principals/rosters")["SecretString"])
    pairs = {k: [p.strip() for p in v.split(",") if "/" in p] for k, v in roster.items() if isinstance(v, str) and "/" in v}
    andrew = pairs.get("master_admin", [None])[0]
    bbg = next((p for v in pairs.values() for p in v if p.split("/")[-1].startswith("517aa5ee")), None)
    store = acs.AccessState()

    def state(tid, oid):
        prof, grant = sea.current_state(store, tid, oid)
        raw = sea._scope_to_raw(grant.scope) if grant is not None else None
        return prof, raw

    prof, raw = state(ident["alyssa_tid"], ident["alyssa_oid"])
    out = {"mode": mode, "alyssa": {"profile_revision": prof.revision, "grant_revision": prof.grant_revision, "operations": sorted(raw["operations"]),
                                     "scope_without_operations_hash": h10(canon({k: v for k, v in raw.items() if k != "operations"}))}}
    others = {}
    for role, pair in (("andrew", andrew), ("bbg", bbg)):
        t, o = pair.split("/", 1)
        _p, r = state(t, o)
        others[role] = h10(canon(r))
    out["others_hash"] = others
    deny = store.get(acs.email_deny_key(os.environ.get("AG1_NONE", "") or _stored_email(store, ident)))
    out["email_deny_hash"] = h10(canon(deny)) if deny is not None else None
    out["email_deny_present"] = deny is not None
    ba = before["alyssa"]
    ok = True
    if mode == "before":
        ok = (out["alyssa"]["profile_revision"] == ba["profile_revision"] and out["alyssa"]["grant_revision"] == ba["grant_revision"]
              and out["alyssa"]["operations"] == ba["operations"] and out["alyssa"]["scope_without_operations_hash"] == ba["scope_without_operations_hash"]
              and out["others_hash"] == before["others_hash"] and out["email_deny_present"])
        with io.open(os.path.join(X, "alyssa_restore_candidate.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"tid": ident["alyssa_tid"], "oid": ident["alyssa_oid"], "email": _stored_email(store, ident), "scope": raw}, fh, indent=1)
            fh.write("\n")
    out["nothing_moved_since_phase_a"] = ok if mode == "before" else None
    with io.open(os.path.join(W, "AG1_REREAD_%s.json" % mode), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(json.dumps(out))
    return 0 if ok else 3


def _stored_email(store, ident):
    import app.data_entitlement as de
    praw = store.get(de.profile_key(ident["alyssa_tid"], ident["alyssa_oid"]))
    return praw.get("email") if isinstance(praw, dict) else None


if __name__ == "__main__":
    sys.exit(main())
