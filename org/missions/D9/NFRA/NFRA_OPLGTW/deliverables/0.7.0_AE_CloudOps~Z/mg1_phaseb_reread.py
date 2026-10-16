#!/usr/bin/env python
"""OG-mg-1 Phase B step 6 (C2): re-read the live store and the host at the moment of the GO. Writes NOTHING to the store and no
identifier anywhere. Prints the STOP conditions, one per line, and exits 2 on any of them.

  STOP if (a) Andrew's or the Bloomberg principal holds a profile or any grant item, (b) Alyssa's profile is not active/restricted
  at revision 4 / grant revision 4, (c) the host MASTER_ADMIN_EMAILS holds other than exactly one alias, (d) the off-repo candidates no
  longer carry the identities and email hashes Phase A recorded.

It also prints a short hash of Alyssa's complete profile + grant items (all attributes, canonical JSON), so the read-back can prove her
record is byte-for-byte unchanged. usage: python mg1_phaseb_reread.py   (from the repo root)"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mg1_before as mb  # noqa: E402
import mg1_candidates as mc  # noqa: E402

WANT_R1_SHA10 = "7b1bca22c9"
WANT_R2_SHA10 = "f39c9b2025"


def main() -> int:
    X = mb.x_dir()
    ident = json.load(io.open(os.path.join(X, "mg1_identities.json"), encoding="utf-8"))
    items = mb.scan_all()
    pol = [it for it in items if mb.sval(it, "pk").startswith("POLICY#")]
    stops = []

    def held(role: str) -> list[dict]:
        pk = ident["pk"].get(role)
        return [it for it in pol if mb.sval(it, "pk") == pk] if pk else []

    for role in ("andrew", "bbg"):
        n = len(held(role))
        print("  %-7s pk_hash %s : %d POLICY# item(s)" % (role, mb.h(ident["pk"][role]), n))
        if n:
            stops.append("%s holds %d item(s)" % (role, n))
    a_items = held("alyssa")
    prof = next((it for it in a_items if mb.sval(it, "record_type") == "principal_profile"), None)
    if prof is None:
        stops.append("alyssa has no profile")
    else:
        got = (mb.sval(prof, "status"), mb.sval(prof, "profile_kind"), mb.sval(prof, "revision"), mb.sval(prof, "grant_revision"))
        print("  alyssa  pk_hash %s : status/kind/rev/grant_rev = %s" % (mb.h(ident["pk"]["alyssa"]), got))
        if got != ("active", "restricted", "4", "4"):
            stops.append("alyssa profile is %s, not active/restricted/4/4" % (got,))
    snap = hashlib.sha256(json.dumps(sorted(a_items, key=lambda i: (mb.sval(i, "sk"), json.dumps(i, sort_keys=True))),
                                     sort_keys=True).encode("utf-8")).hexdigest()[:12]
    print("  alyssa  items %d, canonical hash %s" % (len(a_items), snap))
    print("  POLICY# total %d of %d scanned" % (len(pol), len(items)))
    # the host alias: mc.master_admin_email() raises SystemExit on != 1
    try:
        a1 = mc.master_admin_email()
        s1 = mc.ehash(a1)
        print("  host MASTER_ADMIN_EMAILS: exactly 1 alias, sha10 %s domain %s" % (s1, a1.split("@")[-1]))
        if s1 != WANT_R1_SHA10:
            stops.append("host alias sha10 %s != Phase A %s" % (s1, WANT_R1_SHA10))
    except SystemExit as exc:
        stops.append(str(exc))
    for name, want in (("r1", WANT_R1_SHA10), ("r2", WANT_R2_SHA10)):
        c = json.load(io.open(os.path.join(X, "%s_candidate.json" % name), encoding="utf-8"))
        s = mc.ehash(c["email"])
        who = "andrew" if name == "r1" else "bbg"
        ok = (s == want) and ("POLICY#%s#%s" % (c["tid"], c["oid"]) == ident["pk"][who])
        print("  %s candidate: email sha10 %s (want %s), pk matches %s identity: %s" % (name, s, want, who, ok))
        if not ok:
            stops.append("%s candidate drifted" % name)
    for s in stops:
        print("STOP: " + s)
    print("RESULT: %s" % ("STOP" if stops else "CLEAR"))
    return 2 if stops else 0


if __name__ == "__main__":
    sys.exit(main())
