"""IRPT_BCKEND round 159 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order (CTO msg 6237, row TCKT_VNEXT-D2-S52):
  IB159-1  IB-pr-463  the portal authorizer's source in the tree is ahead of the build input recorded as deployed (a render-token
                      path): what the LIVE function runs, by its bytes; which commits are unreleased; whether anything that is
                      served depends on the unreleased path; and whether a release is owed or the record is behind.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB159-1-AC1  the live package read by its bytes (digest equal to CodeSha256); its source member matched by content to a git
               blob of the file, or to none; every commit on the file after that blob listed with its order and what it adds.
  IB159-1-AC2  the dependents: every sender of a render token and every route the authorizer guards that a render token is
               meant to pass, each with whether it is live and what it gets from the live authorizer today, with a claim; the
               orders that built the unreleased commits with their status and any ledger entry.
  IB159-1-AC3  one verdict from the closed set with its claim; the bounds held; nothing proposed as a release.
"""
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~318/"
OUT, READ = D + "IB159-1_authorizer_render_token_gap.json", D + "IB159-1_AUTHORIZER_RENDER_TOKEN_GAP_READ.md"
B64 = re.compile(r"^[A-Za-z0-9+/]{43}=$")
CLAIMS = ("measured", "inferred", "held", "absent")
VERDICTS = ("RELEASE_OWED_SOMETHING_SERVED_DEPENDS_ON_IT", "UNRELEASED_AND_NOTHING_SERVED_DEPENDS_ON_IT", "RELEASED_THE_RECORD_IS_BEHIND",
            "CANNOT_BE_TOLD")


def at(x):
    return isinstance(x, str) and ":" in x


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB159"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    if cid == "IB159-1-AC1":
        lv = a.get("live") or {}
        if not B64.match(str(lv.get("code_sha256") or "")) or lv.get("downloaded_bytes_hash_equals_code_sha256") is not True \
                or not lv.get("last_modified_utc") or not isinstance(lv.get("members"), list) or not lv["members"]:
            fail("live needs code_sha256, downloaded_bytes_hash_equals_code_sha256 true, last_modified_utc and members")
        m = a.get("live_source_matches") or {}
        if m.get("matched") not in (True, False) or (m["matched"] and not re.match(r"^[0-9a-f]{10,40}$", str(m.get("commit") or ""))) \
                or not isinstance(m.get("revisions_compared"), int) or m.get("has_render_token_path") not in (True, False):
            fail("live_source_matches needs matched, commit (when matched), revisions_compared and has_render_token_path")
        u = a.get("commits_after_the_live_blob")
        if not isinstance(u, list) or any(not x.get("commit") or not x.get("date") or not x.get("order_or_cell") or not x.get("adds_in_words") for x in u):
            fail("commits_after_the_live_blob must list each commit with its date, order and what it adds")
        if not a.get("map_entry") or not isinstance(a["map_entry"], dict) or "last_deployed_commit" not in a["map_entry"]:
            fail("map_entry (the source map's recorded fields for the function) is not stated")
        print("OK: live %s...; source matched: %s; render-token path in the live member: %s; %d commit(s) after it" % (
            lv["code_sha256"][:8], m["matched"], m["has_render_token_path"], len(u)))
    elif cid == "IB159-1-AC2":
        s = a.get("render_token_senders")
        if not isinstance(s, list) or any(not x.get("sender") or not at(x.get("code_line")) or x.get("live") not in (True, False, None)
                                          or not x.get("what_it_gets_from_the_live_authorizer") or x.get("claim") not in CLAIMS for x in s):
            fail("render_token_senders must list each sender with code_line, live, what_it_gets_from_the_live_authorizer and a claim")
        if not s and not a.get("no_sender_found_explained"):
            fail("no sender is listed and no explanation is given")
        r = a.get("routes_a_render_token_is_meant_to_pass")
        if not isinstance(r, list) or any(not x.get("route") or not at(x.get("declared_at")) for x in r):
            fail("routes_a_render_token_is_meant_to_pass must list each route with where it is declared")
        o = a.get("orders_that_built_the_unreleased_commits")
        if not isinstance(o, list) or any(not x.get("order") or not x.get("status") or "ledger_entry" not in x for x in o):
            fail("orders_that_built_the_unreleased_commits must list each order with its status and ledger_entry (a path or null)")
        if not a.get("searched_for") or not isinstance(a.get("not_searched"), list):
            fail("searched_for and not_searched must be stated")
        print("OK: %d render-token sender(s), %d route(s), %d order(s) behind the unreleased commits" % (len(s), len(r), len(o)))
    elif cid == "IB159-1-AC3":
        if a.get("verdict") not in VERDICTS or a.get("claim") not in CLAIMS or not a.get("reason"):
            fail("verdict in %s, with a claim and a reason" % (VERDICTS,))
        if a["verdict"] == "CANNOT_BE_TOLD" and not a.get("what_would_tell"):
            fail("CANNOT_BE_TOLD needs what_would_tell")
        for k in ("functions_invoked", "aws_writes_made", "sign_ins_made", "product_files_edited", "releases_proposed_as_orders"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list) or not (root / READ).is_file():
            fail("not_established and the read file are required")
        print("OK: verdict %s (%s); nothing invoked, written, signed in, edited or proposed" % (a["verdict"], a["claim"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
