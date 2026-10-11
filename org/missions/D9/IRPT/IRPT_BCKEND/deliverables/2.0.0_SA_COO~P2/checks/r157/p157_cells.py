"""IRPT_BCKEND round 157 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one APPLY order under a signed never-widen pair:
  IB157-1  IB-pr-461  irpt-commentary-draft-store-lambda released: the persist answer carries ticket_id (IB-pr-460 merged
                      @294566c734; COO half @39597f02ec; CTO half @7a2a9182a2).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no record).
  IB157-1-AC1  the act: the ledger entry closed; the precheck read the expected live digest; the BUILD_ONLY digest equalled the
               signed one before any upload; the plan named the one function's code and nothing else; and exactly one end
               state: APPLIED (live digest == signed) or ROLLED_BACK (live digest == the before digest) or STOPPED_BEFORE_APPLY.
  IB157-1-AC2  the after-reads, persisting nothing: a refused shape answers the same before and after; get_ref for a request
               that has a draft answers with exactly the key names status and commentary_ref; no ticket_id on either; the member
               on a real first persist recorded UNEXERCISED LIVE in those words.
  IB157-1-AC3  the bounds: who may invoke was read before any invoke and no grant was made; persists made 0; no other function,
               role, policy or environment touched; no value of a ref and no account id in the record.
"""
import json
import re
import sys
from pathlib import Path

OUT = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~IB2/IB157-1_draft_store_release_after_reads.json"
SIGNED = "cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A="
BEFORE = "AsKY+KWLZBW54N73z9VdnR7SIKMPd9RDoYS8x4vRkpw="
ROLLBACK = "ToWX4K7J1NpXcwbkf4imLR6Xu0_0aJGn"
STATES = ("APPLIED", "ROLLED_BACK", "STOPPED_BEFORE_APPLY")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB157"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    text = f.read_text(encoding="utf-8")
    a = json.loads(text)
    st = a.get("end_state")
    if st not in STATES:
        fail("end_state must be one of %s" % (STATES,))
    if cid == "IB157-1-AC1":
        lg = a.get("ledger") or {}
        if lg.get("state") != "closed" or not lg.get("slug") or not lg.get("opened_commit"):
            fail("the ledger entry must be closed, with its slug and the commit that opened it")
        if a.get("live_before") != BEFORE or a.get("rollback_version_reread") != ROLLBACK:
            fail("live_before and rollback_version_reread must equal the pair's values")
        if st != "STOPPED_BEFORE_APPLY":
            if a.get("build_only_digest") != SIGNED or a.get("build_pin_at_or_after_the_revert") is not True:
                fail("the BUILD_ONLY digest must equal the signed digest, built from a pin at or after the reader's revert")
            pl = a.get("plan_lines")
            if not isinstance(pl, list) or not pl or a.get("plan_resources_other_than_the_function") != 0:
                fail("plan_lines must be recorded and plan_resources_other_than_the_function must be 0")
        want = {"APPLIED": SIGNED, "ROLLED_BACK": BEFORE, "STOPPED_BEFORE_APPLY": BEFORE}[st]
        if a.get("live_after") != want:
            fail("end_state %s needs live_after %s..." % (st, want[:8]))
        if st != "APPLIED" and not a.get("why"):
            fail("%s needs why" % st)
        print("OK: end state %s; live after %s...; ledger closed (%s)" % (st, a["live_after"][:8], lg["slug"]))
    elif cid == "IB157-1-AC2":
        r = a.get("after_reads") or {}
        x = r.get("refused_shape") or {}
        if not x.get("before") or x.get("before") != x.get("after") or x["before"].get("status") != "REFUSED" or not x["before"].get("reason"):
            if st == "APPLIED":
                fail("the refused-shape invoke must answer the same REFUSED body before and after")
        g = r.get("get_ref") or {}
        if st == "APPLIED":
            if g.get("made") is True:
                if sorted(g.get("answer_key_names") or []) != ["commentary_ref", "status"] or g.get("request_had_a_draft") not in (True, False):
                    fail("get_ref must record exactly the key names status and commentary_ref, and whether the request had a draft")
            elif not g.get("why_not_made"):
                fail("get_ref not made needs why_not_made")
            if r.get("member_on_a_real_first_persist") != "UNEXERCISED LIVE":
                fail("member_on_a_real_first_persist must read exactly UNEXERCISED LIVE")
        if "ticket_id" in json.dumps(r.get("refused_shape") or {}) or "ticket_id" in json.dumps(g.get("answer_key_names") or []):
            fail("an after-read answer names ticket_id")
        print("OK: refused shape identical before and after; get_ref made: %r; the member on a real persist: %s" % (
            g.get("made"), r.get("member_on_a_real_first_persist")))
    elif cid == "IB157-1-AC3":
        w = a.get("who_may_invoke") or {}
        if not w.get("read_before_any_invoke") or not w.get("how_read") or w.get("grants_made") != 0:
            fail("who_may_invoke needs read_before_any_invoke true, how_read, and grants_made 0")
        for k in ("persists_made", "other_functions_touched", "iam_changes", "environment_changes", "vendor_calls_made"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if re.search(r"ART-[0-9a-f]{16,}", text) or re.search(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", text) or "Bearer " in text:
            fail("the record carries an artifact id, an eight-digit token or a bearer token")
        if not isinstance(a.get("invokes_made"), list):
            fail("invokes_made (each: what, when, status) is not recorded")
        print("OK: who may invoke read first, no grant; %d invoke(s); 0 persists; nothing else touched" % len(a["invokes_made"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
