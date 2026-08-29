"""ACCOUNT-GRAIN membership delta -- the grain 3.0.0_SA_CVO 79882 will re-derive, and
the one that is IMMUNE to the spine's producer change.

WHY THIS EXISTS. 79882 states the verifying seat will re-derive the computed branch as
"new/lost from two membership books at ACCOUNT grain (850 gained / 75 lost)". The
floor-aligned evidence leaf's Relationships tile reports 2,527 new / 478 lost, because
that tile counts RELATIONSHIPS. Those two numbers are not in conflict and neither is
wrong -- they are DIFFERENT GRAINS, and comparing them directly is the subject/check
mismatch this whole round has been made of. This arm prints both beside each other so
the comparison is never made by accident.

AND THE GRAIN IS NOT A DETAIL HERE -- IT DECIDES WHETHER THE NUMBER IS CONFOUNDED.
2,527 new relationships arising from 850 gained accounts is not possible as client
movement; the excess is the dim_relationship producer change. The window-start spine is
schema_version 1.0 and the as-of spine is 2.0, and a re-keyed account's new
relationship_id presents as a NEW RELATIONSHIP. The ACCOUNT grain reads account_ids out
of jd2 dim_advisor_fee_role and never touches a spine relationship_id, so it cannot see
that reassignment at all. Measured 2026-08-28: re-key across the version boundary is
21.6% over 34 days against 2.0% within 2.0 over 147 days.

>> THE PRACTICAL CONSEQUENCE: at ACCOUNT grain the floor-aligned window is a SOUND
   membership measurement despite the degraded start vintage. At RELATIONSHIP grain it
   is not, and the leaf says so on its face in basis_version_change. <<
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/runners_49f"))
import perfrp_emit_core as C                                    # noqa: E402
from perfrp_book import book_membership                         # noqa: E402

START, END = "2026-07-14", "2026-08-27"
FAILS = []


def check(name, cond, detail=""):
    print("  %-58s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


s_df, s_pin = C._read_jd2_at(START)
e_df, e_pin = C._read_jd2_at(END)
check("both membership books resolve (the computable branch's precondition)",
      s_pin["available"] and e_pin["available"],
      "start partition %s, end partition %s" % (s_pin.get("partition_date"),
                                                e_pin.get("partition_date")))
bs = book_membership(s_df.to_dict("records"))
be = book_membership(e_df.to_dict("records"))

advisors = sorted(set(bs) | set(be))
gained = lost = 0
both = 0
per = {}
for a in advisors:
    S = {str(x) for x in bs.get(a, ())}
    E = {str(x) for x in be.get(a, ())}
    g, ll = E - S, S - E
    gained += len(g)
    lost += len(ll)
    both += len(g & ll)
    per[a] = (len(g), len(ll), len(S & E))

print()
print("=" * 78)
print("ACCOUNT GRAIN -- two membership books, %s -> %s" % (START, END))
print("=" * 78)
print("  advisors: start %d, end %d, union %d" % (len(bs), len(be), len(advisors)))
print("  accounts GAINED : %d" % gained)
print("  accounts LOST   : %d" % lost)
check("no account is in BOTH the gained and lost sets (79840's named arm)",
      both == 0, "%d of %d advisors" % (both, len(advisors)))
# NEGATIVE CONTROL: the same predicate over a fabricated overlap MUST trip.
_g, _l = {"ACCT-X"}, {"ACCT-X"}
check("NEGATIVE CONTROL: an injected account in both sets is caught",
      len(_g & _l) != 0, "control fires")

print()
print("=" * 78)
print("THE TWO GRAINS, SIDE BY SIDE (never compare these directly)")
print("=" * 78)
leaf = json.load(open(ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables"
                      / "emissions/perfrp_book_advisor_floor_aligned.json",
                      encoding="utf-8"))
rel_new = sum(e["tiles"]["relationships"]["new"]["value"] for e in leaf["entries"])
rel_lost = sum(e["tiles"]["relationships"]["lost"]["value"] for e in leaf["entries"])
print("  ACCOUNT grain (jd2 account_ids)        gained %5d   lost %4d" % (gained, lost))
print("  RELATIONSHIP grain (spine rel_ ids)    new    %5d   lost %4d" % (rel_new,
                                                                          rel_lost))
print("  ratio new/gained: %.2fx -- an account cannot join more than one book, so a"
      % (rel_new / max(gained, 1)))
print("  ratio above 1 is relationship_id REASSIGNMENT, not client movement.")
bv = leaf["window"]["basis_version_change"]
# REPOINTED 2026-08-29 -- 2.0.0_SA_COO 81723 as amended by 81738, 1.0.0_SA_CTO 81730,
# form from 3.0.0_SA_CVO 81733. The old form asserted `versions_differ is True and
# bool(warning)`: a WORLD-STATE that inverted the moment the campaign corrected the
# spine, so the arm FAILED on a healthy artifact. What this arm exists to check is that
# a reader can tell client MOVEMENT from relationship_id REASSIGNMENT -- and that
# disclosure is now FIELDS, which survive the versions agreeing.
rk = bv.get("rekey_comparison") or {}
_sub = rk.get("subject") or {}
check("the leaf DISCLOSES the re-key basis AS FIELDS, whatever the version state",
      _sub.get("basis") == "derived" and bool(_sub.get("start_partition"))
      and bool(_sub.get("end_partition")),
      "versions_differ=%s  rate=%s of %s" % (bv["versions_differ"],
                                             _sub.get("rekeyed_accounts"),
                                             _sub.get("shared_accounts")))
check("the derived re-key rate is COMPUTED, so the ratio above has a stated basis",
      _sub.get("rate_state") == "COMPUTED" and _sub.get("rate") is not None,
      "rate_state=%s" % _sub.get("rate_state"))
check("the ACCOUNT grain reads NO spine relationship_id (immune by construction)",
      "relationship_id" not in set(s_df.columns) | set(e_df.columns),
      "jd2 columns carry account_id, not rel_ keys")

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d FAILED: %s" % (len(FAILS), FAILS))
else:
    print("RESULT: ALL PASS. Account grain %d gained / %d lost is the CONFOUND-FREE"
          % (gained, lost))
    print("membership measurement for this window; the relationship-grain tile is not,")
    print("and the leaf declares why. The two are different grains, not a disagreement.")
